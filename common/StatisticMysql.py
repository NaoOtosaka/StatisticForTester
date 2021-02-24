import pymysql
from config import CONF
from tools.log import *
from dbutils.pooled_db import PooledDB


class StatisticMysql:
    """
    Mysql操作
    """
    def __init__(self):
        # 实例化日志对象
        self.logger = setLogger('databases')
        # 线程池初始化
        self.pool = PooledDB(
            creator=pymysql,
            maxconnections=None,
            mincached=5,
            maxcached=50,
            maxshared=0,
            blocking=False,
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

    def connect(self):
        try:
            # 线程池中链接线程
            conn = self.pool.connection()
            cursor = conn.cursor()
            return conn, cursor
        except pymysql.DatabaseError:
            self.logger.error(pymysql.DatabaseError)
            return 0

    def query(self, sql):
        """
        查询操作类
        :return:
        """
        # 获取链接对象，游标
        conn, cursor = self.connect()

        # sql解析
        sql = sql.strip()

        # 查询处理
        if sql.lstrip().upper().startswith("SELECT"):
            result = self.select(cursor, sql)
        elif sql.lstrip().upper().startswith("INSERT"):
            result = self.insert(conn, cursor, sql)
        elif sql.lstrip().upper().startswith("UPDATE"):
            result = self.update(conn, cursor, sql)
        elif sql.lstrip().upper().startswith("DELETE"):
            result = self.delete(conn, cursor, sql)
        else:
            result = 0

        # 释放游标
        cursor.close()
        # 释放链接
        conn.close()

        return result

    @staticmethod
    def select(cursor, sql):
        """
        SELECT语句
        :param sql:
        :param cursor:
        :return:
        """
        # 执行SQL
        cursor.execute(sql)
        # 获取结果
        result = cursor.fetchall()

        # self.logger.info(result)

        return result

    @staticmethod
    def insert(conn, cursor, sql):
        """
        INSERT语句
        :param conn:
        :param cursor:
        :param sql:
        :return:
        """
        # 执行SQL
        try:
            cursor.execute(sql)
            conn.commit()
            result = 1
        except pymysql.DatabaseError:
            result = 0
            print(sql)
            # self.logger.error(pymysql.DatabaseError)
            # print(pymysql.DatabaseError)
        except pymysql.Error:
            result = 0
            print(sql)
            # self.logger.error(pymysql.Error)
            # print(pymysql.Error)

        return result

    @staticmethod
    def update(conn, cursor, sql):
        """
        UPDATE语句
        :param conn:
        :param cursor:
        :param sql:
        :return:
        """
        # 执行SQL
        try:
            cursor.execute(sql)
            conn.commit()
            result = 1
        except pymysql.DatabaseError:
            result = 0
            # self.logger.error(pymysql.DatabaseError)
            # print(pymysql.DatabaseError)
        except pymysql.Error:
            result = 0
            # self.logger.error(pymysql.Error)
            # print(pymysql.Error)

        return result

    @staticmethod
    def delete(conn, cursor, sql):
        """
        DELETE语句
        :param conn:
        :param cursor:
        :param sql:
        :return:
        """
        # 执行SQL
        try:
            cursor.execute(sql)
            conn.commit()
            result = 1
        except pymysql.DatabaseError:
            result = 0
            # self.logger.error(pymysql.DatabaseError)
            # print(pymysql.DatabaseError)
        except pymysql.Error:
            result = 0
            # self.logger.error(pymysql.Error)
            # print(pymysql.Error)

        return result


# 单例模式
StatisticMysqlPool = StatisticMysql()
