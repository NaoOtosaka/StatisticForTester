from tools.database import db
from tools.log import *

# 实例化日志对象
logger = setLogger('bug_type')


def get_bug_type(type_id):
    """
    根据类型id获取BUG类型
    :param type_id:
    :return:
    """
    sql = """
        SELECT
        bug_type.type_name
        FROM
        bug_type
        WHERE
        bug_type.type_id = '%i'
    """ % type_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def check_type_with_name(type_name):
    """
    根据类型名检查数据是否存在,若存在则返回id
    :param type_name:
    :return:
    """
    sql = """
        SELECT
        bug_type.type_id
        FROM
        bug_type
        WHERE
        bug_type.type_id = '%i'
    """ % type_name

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return None
