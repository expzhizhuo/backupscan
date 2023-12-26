"""
@Project ：backscan 
@File    ：output.py
@IDE     ：PyCharm 
@Author  ：zhizhuo
@Date    ：2023/12/26 13:56 
"""


class Output:
    def __init__(self, outfile: str = "result.txt"):
        """
        初始化配置信息
        """
        self.outfile = outfile

    def write_to_file(self, data):
        """
        结果写入到文件中
        :param data:写入信息
        :return:True or False
        """
        with open(self.outfile, 'a+') as f:
            f.write(data + '\n')
            f.close()

    def clear_to_file(self):
        """
        清空文件内容
        :return:
        """
        with open(self.outfile, 'a+') as f:
            f.truncate(0)
            f.close()

    @staticmethod
    def open_file(file_path):
        """
        读取指定文件内容
        :param file_path:文件路径
        :return:
        """
        return open('{}'.format(file_path), encoding='utf8').read().splitlines()
