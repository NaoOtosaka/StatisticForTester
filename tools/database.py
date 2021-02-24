from common.StatisticMysql import StatisticMysql


def db(sql=None):
    """
    数据库操作
    :param sql:
    :return:
    """
    # 挂载链接
    connect = StatisticMysql()
    # 传入查询时
    if sql:
        # 执行SQL
        result = connect.query(sql)
        connect.close_db()
        return result
    # 关闭链接
    connect.close_db()