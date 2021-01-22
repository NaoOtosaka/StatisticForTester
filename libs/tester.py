from libs.project import *
from tools.log import *

# 实例化日志对象
logger = setLogger('tester')


def get_tester_base_info(tester_id):
    """
    根据测试人员id获取测试人员基础信息
    :param tester_id:   测试人员ID
    :return: tester_info_list
    {
        'testerId': int,
        'testerName': string,
        'testerEmail':string
    }
    """
    sql = """
        SELECT
        tester.tester_id,
        tester.name,
        tester.email
        FROM
        tester
        WHERE
        tester.tester_id = '%i'
    """ % tester_id

    # 获取测试基础信息
    result = db(sql)
    if result:
        logger.debug(result)
        temp = {
            'testerId': result[0][0],
            'testerName': result[0][1],
            'testerEmail': result[0][2]
        }
        return temp
    else:
        return []


def get_tester_list():
    """
    获取测试人员列表
    :return:
    [
        {
            'testerId': int,
            'testerName': string,
            'testerEmail': string
        }
    ]
    """
    sql = """
        SELECT
        tester.tester_id,
        tester.name,
        tester.email
        FROM
        tester;
        """
    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(
                {
                    'testerId': result[i][0],
                    'testerName': result[i][1],
                    'testerEmail': result[i][2]
                }
            )
        return temp
    else:
        return []


def get_project_info_with_tester(tester_id):
    """
    根据测试人员获取其负责的项目列表及项目下bug数量（总数，测试人员负责数）
    :param tester_id:   测试人员ID
    :return: project_info_list
    [
        {
            'projectId': int,
            'projectName': string,
            'total': int,
            'testerCount': int
        }
    ]
    """
    temp = []

    project_list = get_project_list_with_tester(tester_id)
    if project_list:
        for i in project_list:
            # 获取项目对应bug总数
            project_id = i['projectId']
            project_name = i['projectName']

            total = len(get_bug_list_with_project(project_id))
            tester_count = len(get_bug_with_tester_and_project(tester_id, project_id))
            temp.append(
                {
                    'projectId': project_id,
                    'projectName': project_name,
                    'total': total,
                    'testerCount': tester_count
                }
            )

        return temp
    else:
        return []


def get_project_list_with_tester(tester_id):
    """
    根据测试人员获取其负责的项目列表
    :return: project_info_list
    [
        {
            'projectId': int,
            'projectName': string
        }
    ]
    """
    sql = """
        SELECT
        project.project_id,
        project.project_name
        FROM
        tester
        INNER JOIN test ON test.tester_id = tester.tester_id
        INNER JOIN project ON test.project_id = project.project_id
        WHERE
        test.tester_id = '%i'
    """ % tester_id

    temp = []

    # 获取项目id列表
    result = db(sql)

    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(
                {
                    'projectId': result[i][0],
                    'projectName': result[i][1]
                }
            )
        return temp
    else:
        return []


def get_bug_with_tester_and_project(tester_id, project_id):
    """
    根据项目人员负责的项目获取项目中该测试人员负责的Bug
    :type tester_id int
    :type project_id int
    :return: bug_id_list
    [int]
    """
    sql = """
        SELECT
        bug.bug_id
        FROM
        bug
        INNER JOIN project_phases ON bug.phase_id = project_phases.phase_id
        INNER JOIN project ON project_phases.project_id = project.project_id
        INNER JOIN tester ON bug.tester_id = tester.tester_id
        WHERE
        tester.tester_id = '%i' AND
        project.project_id = '%i'
    """ % (tester_id, project_id)

    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(result[i][0])

        return temp
    else:
        return []


def check_tester_with_id(tester_id):
    """
    根据测试人员id检查数据是否存在,若存在则返回True
    :param tester_id:
    :return: 对应人员id
    """
    sql = """
    SELECT
    1
    FROM
    tester
    WHERE
    tester.tester_id = '%i'
    LIMIT 1
    """ % tester_id

    result = db(sql)
    if result:
        logger.debug(result)
        return True
    else:
        return False


def check_tester_with_name(tester_name):
    """
    根据测试人员姓名检查数据是否存在,若存在则返回id
    :param tester_name:
    :return: 对应人员id
    """
    sql = """
    SELECT
    tester.tester_id
    FROM
    tester
    WHERE
    tester.name = '%s'
    LIMIT 1
    """ % tester_name

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def check_tester_with_email(tester_email):
    """
    根据测试邮箱姓名检查数据是否存在,若存在则返回id
    :param tester_email:
    :return: 对应人员id
    """
    sql = """
    SELECT
    tester.tester_id
    FROM
    tester
    WHERE
    tester.email = '%s'
    LIMIT 1
    """ % tester_email

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def add_tester(tester_name, tester_email):
    """
    新建测试人员
    :param tester_name:
    :param tester_email:
    :return: 成功返回1， 失败返回0
    """
    sql = """
    INSERT INTO "tester" ("name", "email")
    VALUES
        ('%s', '%s')
    """ % (tester_name, tester_email)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def edit_tester(tester_id, tester_name, tester_email):
    """
    编辑测试人员信息
    :param tester_id:
    :param tester_name:
    :param tester_email:
    :return: 成功返回1， 失败返回0
    """
    sql = """
    UPDATE tester 
    SET name='%s', email='%s'
    WHERE tester_id='%i'
    """ % (tester_name, tester_email, tester_id)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def delete_tester(tester_id):
    """
    根据id删除测试人员
    :param tester_id:
    :return:
    """
    sql = """
    DELETE FROM tester 
    WHERE tester_id='%i';
    """ % tester_id
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def get_tester_insert_id():
    """
    获取新增后id
    :return:
    """
    sql = """
    SELECT tester_id 
    FROM tester 
    ORDER BY tester_id 
    DESC LIMIT 1
    """

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return False
