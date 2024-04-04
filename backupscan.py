"""
@Project ：backscan
@File    ：backupscan.py
@IDE     ：PyCharm
@Author  ：zhizhuo
@Date    ：2023/12/26 12:25
"""
import time
from urllib.parse import urljoin
import asyncio
from poc_tool.tools import tools
from termcolor import cprint
import colorama
from alive_progress import alive_bar
from poc_tool.log import log, LOGGER, LoggingLevel
from core.backup_requests import BackupRequests
from core.output import Output
from core.get_backup_filename import GetBackupFilename
from pyfiglet import Figlet
import argparse

# 解决cmd样式问题
colorama.init(autoreset=True)
# 多线程操作
max_threads = 100
# 默认结果输出文件
outfile = 'result.txt'
# 代理信息
proxy = None
# 请求超时时间
timeout = 10


async def producer(queue: asyncio.Queue, url_list: list):
    for scan_url in url_list:
        log.debug(f"正在扫描：{scan_url}")
        await queue.put(scan_url)
    for _ in range(max_threads):
        await queue.put(None)  # 用于标记队列结束的值


async def consumer(queue: asyncio.Queue, semaphore: asyncio.Semaphore, bar):
    while True:
        scan_url = await queue.get()
        if scan_url is None:
            queue.task_done()
            break
        async with semaphore:  # 使用信号量限制并发
            try:
                res = await asyncio.wait_for(BackupRequests(url=scan_url, proxy=proxy).run(), timeout)
                if res:
                    cprint(
                        f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] SUCCESS 成功扫描到备份文件，备份文件地址:{res.get("url")}，备份文件大小:{res.get("size")}',
                        'green')
                    data = f"地址：{res.get('url')}\t文件大小：{res.get('size')}"
                    Output(outfile).write_to_file(data)
            except asyncio.TimeoutError:
                log.debug(f"任务超时: {scan_url}")
            finally:
                bar()  # 更新进度
                queue.task_done()


async def scan(url_list: list):
    """
    扫描函数
    :param url_list:url
    :return:
    """
    # 使用 Semaphore 控制并发
    semaphore = asyncio.Semaphore(max_threads)
    queue = asyncio.Queue(maxsize=max_threads)
    with alive_bar(len(url_list)) as bar:
        # 启动生产者和消费者任务
        producer_task = asyncio.create_task(producer(queue, url_list))
        consumer_tasks = [asyncio.create_task(consumer(queue, semaphore, bar)) for _ in range(max_threads)]
        # 等待生产者任务完成
        await producer_task
        # 等待队列中的所有项目被处理
        await queue.join()
        # 取消消费者任务
        # for task in consumer_tasks:
        #     if not task.done():
        #         task.cancel()
        # 等待所有消费者任务取消完成
        await asyncio.gather(*consumer_tasks, return_exceptions=True)


def get_backup_dict(url: str):
    """
    获取备份文件字典
    :param url:url
    :return:dict
    """
    return GetBackupFilename(url).run()


def main(url, file):
    """
    主运行函数
    :param url:url
    :param file:文件
    :return:
    """
    url_list = []
    Output(outfile).clear_to_file()
    if url is None:
        urlfile = Output.open_file(file_path=file)
    else:
        urlfile = ['{}'.format(url)]
    log.info(f"需要扫描{len(urlfile)}个资产")
    log.info(f"正在生成扫描字典")
    with alive_bar(len(urlfile)) as bar:
        for url in urlfile:
            url = tools.get_url_format(url)
            backup_dict = GetBackupFilename(url).run()
            for b in backup_dict:
                scan_url = urljoin(url, b)
                url_list.append(scan_url)
            bar()
    log.info(f"扫描资产生成完成")
    log.info(f"产生任务{len(url_list)}个")
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(scan(url_list=url_list))
    return result


def cmd_output():
    time_start = time.time()
    global max_threads, outfile, timeout
    f = Figlet(font="slant", width=300)
    cprint(f.renderText('''Backup Scan
        by zhizhuo'''), "green")
    parser = argparse.ArgumentParser(
        description='''
        Backup Scan
        by zhizhuo
        ''')
    parser.add_argument('-u', '-url', dest="url", type=str,
                        help='单个url检测，输入样例http://www.baidu.com', required=False)
    parser.add_argument('-f', '-file', dest="url_file", nargs='?', type=str,
                        help='多个url检测，以txt文件形式存储,文件中的url格式为http://www.baidu.com或者www.baidu.com',
                        required=False)
    parser.add_argument('-t', '-T', dest="threads", type=int,
                        help='线程数量，默认是100线程', required=False)
    parser.add_argument('-o', '-output', dest="output", nargs='?', type=str,
                        help='结果输出文件', required=False)
    parser.add_argument('-tm', '-timeout', dest="timeout", nargs='?', type=str,
                        help='设置请求超时时间，默认是10s', required=False)
    parser.add_argument('-d', '-debug', dest="debug", default="debug", nargs='?', type=str,
                        help='开启debug模式', required=False)
    url_arg = parser.parse_args().url
    file_arg = parser.parse_args().url_file
    threads_arg = parser.parse_args().threads
    outfile_arg = parser.parse_args().output
    timeout_arg = parser.parse_args().timeout
    debug_arg = parser.parse_args().debug
    if debug_arg != "debug":
        LOGGER.setLevel(LoggingLevel.DEBUG)
    if outfile_arg:
        outfile = outfile_arg
    if timeout_arg:
        timeout = int(timeout_arg)
    if threads_arg is not None:
        max_threads = int(threads_arg)
    if file_arg is not None or url_arg is not None:
        main(url_arg, file_arg)
    else:
        print("参数错误，请使用命令-h查看命令使用帮助 --by zhizhuo")
    print(f'扫描完成，总共用时{round(time.time() - time_start, 2)}S')


if __name__ == '__main__':
    cmd_output()
