import sqlite3

from config import CONF


def db(sql=None):
    """
    数据库操作
    :param sql:
    :return:
    """
    # 挂载链接
    connect = connect_database()
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
    :return: sqlite3.Connection
    """
    # 挂载链接
    connect = sqlite3.connect(CONF.DB_HOST)

    # 强制启动外键约束
    if CONF.USE_FOREIGN:
        connect.execute("PRAGMA foreign_keys=1;")

    return connect


def do_query(connect, sql):
    """
    执行SQL
    :type connect: sqlite3.Connection
    :type sql: string
    """
    sql = sql.strip()

    if sql.lstrip().upper().startswith("SELECT"):
        # 创建游标
        cursor = connect.cursor()
        # 查询
        result = select(cursor, sql)
        # 关闭游标
        cursor.close()
        return result
    elif sql.lstrip().upper().startswith("INSERT"):
        result = insert(connect, sql)
        return result
    elif sql.lstrip().upper().startswith("UPDATE"):
        result = update(connect, sql)
        return result
    elif sql.lstrip().upper().startswith("DELETE"):
        result = delete(connect, sql)
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
        print(sqlite3.DatabaseError)
    except sqlite3.Error:
        result = 0
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
        print(sqlite3.DatabaseError)
    except sqlite3.Error:
        result = 0
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
        print(sqlite3.DatabaseError)
    except sqlite3.Error:
        result = 0
        print(sqlite3.Error)

    return result


if __name__ == '__main__':
    print(connect_database())