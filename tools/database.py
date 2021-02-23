import pymysql

from config import CONF
from tools.log import *

# 实例化日志对象
logger = setLogger('databases')


def db(sql=None):
    """
    数据库操作
    :param sql:
    :return:
    """
    # 挂载链接
    connect = connect_database()
    logger.info(connect)
    # 传入查询时
    if sql:
        # 执行SQL
        result = do_query(connect, sql)
        connect.close()
        return result
    # 关闭链接
    connect.close()


def connect_database():
    """
    挂载数据库
    :return: mysql.Connection
    """
    connect = pymysql.connect(
        host=CONF.BD_HOST,
        port=CONF.DB_PORT,
        user=CONF.DB_USER,
        passwd=CONF.DB_PASSWORD,
        db=CONF.DB_NAME)

    return connect


def do_query(connect, sql):
    """
    执行SQL
    :type connect: sqlite3.Connection
    :type sql: string
    """
    sql = sql.strip()
    # 创建游标
    cursor = connect.cursor()

    if sql.lstrip().upper().startswith("SELECT"):
        # 查询
        result = select(cursor, sql)
        # 关闭游标
        cursor.close()
        return result
    elif sql.lstrip().upper().startswith("INSERT"):
        result = insert(cursor, sql)
        return result
    elif sql.lstrip().upper().startswith("UPDATE"):
        result = update(cursor, sql)
        return result
    elif sql.lstrip().upper().startswith("DELETE"):
        result = delete(cursor, sql)
        return result
    else:
        return 0


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

    return result


def insert(connect, sql):
    """
    INSERT语句
    :param sql:
    :param connect:
    :type connect: sqlite3.Connection
    :return:
    """
    # 执行SQL
    try:
        connect.execute(sql)
        connect.commit()
        result = 1
    except sqlite3.DatabaseError:
        result = 0
        logger.error(sqlite3.DatabaseError)
        print(sqlite3.DatabaseError)
    except sqlite3.Error:
        result = 0
        logger.error(sqlite3.Error)
        print(sqlite3.Error)

    return result


def update(connect, sql):
    """
    UPDATE语句
    :param connect:
    :param sql:
    :type connect: sqlite3.Connection
    :return:
    """
    # 执行SQL
    try:
        connect.execute(sql)
        connect.commit()
        result = 1
    except sqlite3.DatabaseError:
        result = 0
        logger.error(sqlite3.DatabaseError)
        print(sqlite3.DatabaseError)
    except sqlite3.Error:
        result = 0
        logger.error(sqlite3.Error)
        print(sqlite3.Error)

    return result


def delete(connect, sql):
    """
    DELETE语句
    :param connect:
    :param sql:
    :type connect: sqlite3.Connection
    :return:
    """
    # 执行SQL
    try:
        connect.execute(sql)
        connect.commit()
        result = 1
    except sqlite3.DatabaseError:
        result = 0
        logger.error(sqlite3.DatabaseError)
        print(sqlite3.DatabaseError)
    except sqlite3.Error:
        result = 0
        logger.error(sqlite3.Error)
        print(sqlite3.Error)

    return result

# if __name__ == '__main__':
#     # pass
#     sql = """
#     UPDATE bug SET tester_id=1, developer_id=1, phase_id=1, bug_type=1, category=8, title='作品展示页翻页后点击进入作品详情页后，点击退回上个页面保持页面筛选状态，即维持在进入此作品详情页的作品类表页数',
#     model='前端-作品展示区', create_time=1611147000, close_time=0, is_finished='False', is_closed='False', is_online='False' WHERE kb_id=71892;
#     """
#     db(sql)
