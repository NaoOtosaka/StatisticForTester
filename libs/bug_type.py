from tools.database import db


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
        bug_type.type_id = "%i"
    """ % type_id

    result = db(sql)
    if result:
        print(result)
        return result[0][0]
    else:
        return None

