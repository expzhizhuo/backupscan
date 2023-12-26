"""
@Project ：backscan 
@File    ：backup_requests.py
@IDE     ：PyCharm 
@Author  ：zhizhuo
@Date    ：2023/12/26 13:15 
"""
import warnings

import requests
from poc_tool.log import log
from poc_tool.tools import tools
from urllib3.exceptions import InsecureRequestWarning

from config.config import Config

# 解决requests的ssl证书warning提示
warnings.filterwarnings('ignore', category=InsecureRequestWarning)


class BackupRequests:
    def __init__(self, url: str, proxy: str = None, timeout: int = 10):
        """
        初始化配置信息
        :param url:url
        :param proxy:代理信息
        :param timeout:请求超时时间
        """
        self.black_type = Config.BACKUP_BLACK_TYPE
        self.url = url
        self.proxy = proxy
        self.timeout = timeout
        self.headers = {
            'Accept': 'application/x-shockwave-flash, image/gif, image/x-xbitmap, image/jpeg, image/pjpeg, '
                      'application/vnd.ms-excel, application/vnd.ms-powerpoint, application/msword, */*',
            'User-agent': tools.get_random_ua(),
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Connection': 'close'
        }

    @staticmethod
    def _get_file_size(content_size):
        """
        根据Content-Length计算文件的大小
        :param content_size:Content-Length结果
        :return:MB
        """
        file_size = content_size / 1024
        log.debug(f"计算文件大小为:{file_size} KB")
        return file_size

    def _requests_scan(self):
        """
        发送备份文件扫描请求
        :return:
        """
        data = None
        try:
            if self.proxy:
                res = requests.get(url=self.url, headers=self.headers, proxies={
                    'http': self.proxy,
                    'https': self.proxy
                }, verify=False, allow_redirects=False, stream=True, timeout=self.timeout)
            else:
                res = requests.get(url=self.url, headers=self.headers, verify=False, allow_redirects=False, stream=True,
                                   timeout=self.timeout)
            if res.status_code == 200 and all(
                    content not in res.headers.get('Content-Type', '') for content in self.black_type):
                tmp_size = self._get_file_size(int(res.headers.get('Content-Length', 0)))
                if tmp_size > 0:
                    data = dict(url=self.url, size=tmp_size)
        except Exception as e:
            log.debug(f"发送备份文件扫描请求出错，错误信息：{e}")
            pass
        return data

    def run(self):
        """
        总入口函数
        :return:
        """
        return self._requests_scan()
