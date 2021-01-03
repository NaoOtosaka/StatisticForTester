from tools.database import db


def get_bug_category(category_id):
    """
    根据bug分类id获取分类
    :param category_id:
    :return:
    """
    sql = """
        SELECT
        bug_category.category_name
        FROM
        bug_category
        WHERE
        bug_category.category_id = '%i'
    """ % category_id

    result = db(sql)
    if result:
        print(result)
        return result[0][0]
    else:
        return 0


def check_category_with_name(category_name):
    """
    根据分类名检查数据是否存在,若存在则返回id
    :param category_name:
    :return:
    """
    sql = """
        SELECT
        bug_category.category_id
        FROM
        bug_category
        WHERE
        bug_category.category_name = '%i'
    """ % category_name

    result = db(sql)
    if result:
        print(result)
        return result[0][0]
    else:
        return 0
