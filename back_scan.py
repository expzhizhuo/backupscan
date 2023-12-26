"""
@Project ：backscan
@File    ：back_scan.py
@IDE     ：PyCharm
@Author  ：zhizhuo
@Date    ：2023/12/26 12:25
"""
import time
from urllib.parse import urljoin

from poc_tool.tools import tools
from termcolor import cprint
import colorama
from alive_progress import alive_bar
from poc_tool.log import log, LOGGER, LoggingLevel
from core.backup_requests import BackupRequests
from core.output import Output
from core.get_backup_filename import GetBackupFilename
from concurrent.futures import ThreadPoolExecutor, as_completed
from pyfiglet import Figlet
import argparse

# 解决cmd样式问题
colorama.init(autoreset=True)
# 多线程操作
max_threads = 50
# 默认结果输出文件
outfile = 'result.txt'
# 代理信息
proxy = None
# 请求超时时间
timeout = 10


def scan(url_list: list):
    """
    扫描函数
    :param url_list:url
    :return:
    """
    with alive_bar(len(url_list)) as bar:
        with ThreadPoolExecutor(max_workers=max_threads) as executor:
            futures = []
            for scan_url in url_list:
                log.debug(f"正在扫描：{scan_url}")
                futures.append(executor.submit(BackupRequests(url=scan_url, proxy=proxy).run))
            for future in as_completed(futures):
                res = future.result()
                bar()  # 更新进度
                # log.debug(f'结果 {res}')
                if res:
                    #     # log.success(f"成功扫描到备份文件，备份文件大小:{res.get('size')} KB")
                    cprint(
                        f'[{time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())}] SUCCESS 成功扫描到备份文件，备份文件大小:{res.get("size")}KB',
                        'green')
                    data = f"地址：{res.get('url')}\t文件大小：{res.get('size')} KB"
                    Output(outfile).write_to_file(data)


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
    for url in urlfile:
        url = tools.get_url_format(url)
        backup_dict = GetBackupFilename(url).run()
        for b in backup_dict:
            scan_url = urljoin(url, b)
            url_list.append(scan_url)
    log.info(f"产生任务{len(url_list)}个")
    return scan(url_list=url_list)


def cmd_output():
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
                        help='线程数量，默认是50线程', required=False)
    parser.add_argument('-o', '-output', dest="output", nargs='?', type=str,
                        help='结果输出文件', required=False)
    parser.add_argument('-tm', '-timeout', dest="timeout", nargs='?', type=str,
                        help='结果输出文件', required=False)
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


if __name__ == '__main__':
    cmd_output()
