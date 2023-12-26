"""
@Project ：backscan 
@File    ：config.py
@IDE     ：PyCharm 
@Author  ：zhizhuo
@Date    ：2023/12/26 12:27 
"""


class Config(object):
    def __init__(self):
        """
        初始化配置信息
        """

    BACKUP_FILENAME_SUFFIX = ['.zip', '.rar', '.tar.gz', '.tgz', '.tar.bz2', '.tar', '.jar', '.war', '.7z', '.bak',
                              '.sql', '.gz', '.sql.gz', '.tar.tgz', '.backup']
    DEFAULT_INFO_DICT = ['1', '2', '11', '12', '123', '127.0.0.1', '2010', '2011', '2012', '2013', '2014', '2015',
                         '2016', '2017', '2018', '2019', '2020', '2021', '2022', '2023', '2024', '2025', 'admin',
                         'archive', 'asp', 'aspx', 'auth', 'back', 'backup', 'backups', 'bak', 'bbs', 'bin', 'clients',
                         'code', 'com', 'customers', 'dat', 'data', 'database', 'db', 'dump', 'engine', 'error_log',
                         'faisunzip', 'files', 'forum', 'home', 'html', 'index', 'joomla', 'js', 'jsp', 'local',
                         'localhost', 'master', 'media', 'members', 'my', 'mysql', 'new', 'old', 'orders', 'php',
                         'sales', 'site', 'sql', 'store', 'tar', 'test', 'user', 'users', 'vb', 'web', 'website',
                         'wordpress', 'wp', 'www', 'wwwroot', 'root', 'log']
    BACKUP_BLACK_TYPE = ['html', 'image', 'xml', 'text', 'json', 'javascript']
