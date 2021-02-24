import pymysql
from config import CONF
from tools.log import *


class StatisticMysql:
    """
    Mysql数据库类
    """
    def __init__(self):
        # 实例化日志对象
        self.logger = setLogger('databases')
        # 数据库链接状态(0关闭/1打开)
        self.status = 0
        # 数据库挂载
        self.conn = self.connect()

    def connect(self):
        if not self.status:
            # 数据库挂载
            try:
                conn = pymysql.connect(
                    host=CONF.BD_HOST,
                    port=CONF.DB_PORT,
                    user=CONF.DB_USER,
                    password=CONF.DB_PASSWORD,
                    database=CONF.DB_NAME
                )
                self.logger.info(conn)
                self.status = 1
                return conn
            except pymysql.DatabaseError:
                self.logger.error(pymysql.DatabaseError)
                return 0

    def query(self, sql):
        """
        查询操作类
        :return:
        """
        if self.status:
            sql = sql.strip()
            # 创建游标
            cursor = self.conn.cursor()

            if sql.lstrip().upper().startswith("SELECT"):
                result = self.select(cursor, sql)
                cursor.close()
                return result
            elif sql.lstrip().upper().startswith("INSERT"):
                result = self.insert(cursor, sql)
                cursor.close()
                return result
            elif sql.lstrip().upper().startswith("UPDATE"):
                result = self.update(cursor, sql)
                cursor.close()
                return result
            elif sql.lstrip().upper().startswith("DELETE"):
                result = self.delete(cursor, sql)
                cursor.close()
                return result
            else:
                return 0
        else:
            return 0

    def select(self, cursor, sql):
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

        self.logger.info(result)

        return result

    def insert(self, cursor, sql):
        """
        INSERT语句
        :param cursor:
        :param sql:
        :return:
        """
        # 执行SQL
        try:
            cursor.execute(sql)
            self.conn.commit()
            result = 1
        except pymysql.DatabaseError:
            result = 0
            self.logger.error(pymysql.DatabaseError)
            # print(pymysql.DatabaseError)
        except pymysql.Error:
            result = 0
            self.logger.error(pymysql.Error)
            # print(pymysql.Error)

        return result

    def update(self, cursor, sql):
        """
        UPDATE语句
        :param cursor:
        :param sql:
        :return:
        """
        # 执行SQL
        try:
            cursor.execute(sql)
            self.conn.commit()
            result = 1
        except pymysql.DatabaseError:
            result = 0
            self.logger.error(pymysql.DatabaseError)
            # print(pymysql.DatabaseError)
        except pymysql.Error:
            result = 0
            self.logger.error(pymysql.Error)
            # print(pymysql.Error)

        return result

    def delete(self, cursor, sql):
        """
        DELETE语句
        :param cursor:
        :param sql:
        :return:
        """
        # 执行SQL
        try:
            cursor.execute(sql)
            self.conn.commit()
            result = 1
        except pymysql.DatabaseError:
            result = 0
            self.logger.error(pymysql.DatabaseError)
            # print(pymysql.DatabaseError)
        except pymysql.Error:
            result = 0
            self.logger.error(pymysql.Error)
            # print(pymysql.Error)

        return result

    def close_db(self):
        """
        关闭数据库挂载
        :return:
        """
        if self.status:
            self.conn.close()
            self.status = 0


if __name__ == '__main__':
    con = StatisticMysql()
