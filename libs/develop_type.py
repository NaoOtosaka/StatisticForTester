from tools.database import db


def get_develop_type_with_type_id(type_id):
    """
    根据开发类型id获取对应类型名称
    :param type_id:
    :return: string
    """
    sql = """
        SELECT
        develop_type.type_name
        FROM
        develop_type
        WHERE
        develop_type.type_id = '%i'
    """ % type_id

    result = db(sql)
    print(result)
    if result:
        return result[0][0]
    else:
        return []


def select_develop_type_exist(type_id):
    """
    查询开发类型是否存在
    :return:  boolean
    """
    sql = """
            SELECT
            *
            FROM
            develop_type
            WHERE
            develop_type.type_id =  '%i'
        """ % type_id

    result = db(sql)
    print(result)
    if result:
        return True
    else:
        return False
