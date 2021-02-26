from tools.database import db
from tools.log import *

# 实例化日志对象
logger = setLogger('test')


def add_test_record_with_tester_and_project(tester_id, project_id):
    """
    添加测试人员与项目之间的跟进关系
    :return:
    """
    sql = """
    INSERT INTO test(tester_id, project_id)
    VALUES
        ('%i', '%i')
    """ % (tester_id, project_id)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def check_test_record_with_tester_and_project(tester_id, project_id):
    """
    检查测试人员与项目之间的跟进关系
    :return:
    """
    sql = """
    SELECT
    test.tester_id
    FROM
    test
    WHERE
    test.tester_id = %i AND
    test.project_id = %i
    """ % (tester_id, project_id)
    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def delete_test_record_with_tester_and_project():
    """
    删除测试跟进记录
    :return:
    """
    pass