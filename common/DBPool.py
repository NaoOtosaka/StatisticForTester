import pymysql
from dbutils.pooled_db import PooledDB
from tools.log import *
from config import CONF


class DBPool:
    """
    数据库线程池类
    """
    def __init__(self):
        # 实例化日志对象
        self.logger = setLogger('databases')
        # 线程池初始化
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=None,
            mincached=3,
            maxcached=10,
            maxshared=0,
            blocking=True,
            maxusage=None,
            setsession=None,
            ping=0,
            host=CONF.BD_HOST,
            port=CONF.DB_PORT,
            user=CONF.DB_USER,
            password=CONF.DB_PASSWORD,
            database=CONF.DB_NAME,
            charset='utf8mb4'
        )
