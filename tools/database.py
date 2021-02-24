from config import CONF
from common.StatisticMysql import StatisticMysqlPool


def db(sql=None):
    """
    数据库操作
    :param sql:
    :return:
    """
    # 传入查询时
    if sql:
        # # 挂载链接
        # connect = StatisticMysqlPool.connect()
        # 执行SQL
        result = StatisticMysqlPool.query(sql)
        return result