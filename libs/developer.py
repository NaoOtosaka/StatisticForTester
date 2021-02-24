from libs.project import *
from libs.develop_type import *
from tools.log import *

# 实例化日志对象
logger = setLogger('developer')


def get_developer_base_info(developer_id):
    """
    根据测试人员id获取测试人员基础信息
    :param developer_id:   测试人员ID
    :return: developer_info_list
    {
        'developerId': int,
        'typeId': int,
        'developerName': string,
        'developerEmail': string
    }
    """
    sql = """
        SELECT
        developer.developer_id,
        developer.type_id,
        developer.name,
        developer.email
        FROM
        developer
        WHERE
        developer.developer_id = '%i';
    """ % developer_id

    # 获取测试基础信息

    result = db(sql)
    if result:
        logger.debug(result)
        temp = {
                'developerId': result[0][0],
                'typeId': result[0][1],
                'developerName': result[0][2],
                'developerEmail': result[0][3]
            }
        return temp
    else:
        return []


def get_developer_list():
    """
    获取开发人员列表
    :return:
    [
        {
            'developerId': int,
            'typeId': int,
            'developerName': string,
            'developerEmail': string
        }
    ]
    """
    sql = """
        SELECT
        developer.developer_id,
        developer.type_id,
        developer.name,
        developer.email
        FROM
        developer
    """
    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            type_name = get_develop_type_with_type_id(result[i][1])
            temp.append(
                {
                    'developerId': result[i][0],
                    'typeId': type_name,
                    'developerName': result[i][2],
                    'developerEmail': result[i][3]
                }
            )
        return temp
    else:
        return []


def get_project_info_with_developer(developer_id):
    """
    根据开发人员获取获取其负责的项目列表及项目下bug数量（总数，开发人员负责数）
    :param developer_id:
    :return:project_info_list
    [
        {
            'projectId': int,
            'projectName': string,
            'total': int,
            'developerCount': int
        }
    ]
    """
    temp = []

    project_list = get_project_list_with_developer(developer_id)

    if project_list:
        for i in project_list:
            project_id = i['projectId']
            project_name = i['projectName']

            total = len(get_bug_list_with_project(project_id))
            developer_count = len(get_bug_with_developer_and_project(developer_id, project_id))
            temp.append(
                {
                    'projectId': project_id,
                    'projectName': project_name,
                    'total': total,
                    'testerCount': developer_count
                }

            )
        return temp
    else:
        return []


def get_project_list_with_developer(developer_id):
    """
    根据开发人员获取其负责的项目列表
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
        project
        INNER JOIN develop ON develop.project_id = project.project_id
        INNER JOIN developer ON develop.developer_id = developer.developer_id
        WHERE
        developer.developer_id = '%s'
    """ % developer_id

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


def get_bug_with_developer_and_project(developer_id, project_id):
    """
    根据项目人员负责的项目获取项目中该开发人员负责的Bug
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
        INNER JOIN developer ON bug.developer_id = developer.developer_id
        WHERE
        developer.developer_id = '%i' AND
        project.project_id = '%i'
    """ % (developer_id, project_id)

    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(result[i][0])

        return temp
    else:
        return []


def check_developer_with_id(developer_id):
    """
    根据开发人员id检查数据是否存在,若存在则返回True
    :param developer_id:
    :return: 对应人员id
    """
    sql = """
    SELECT
    1
    FROM
    developer
    WHERE
    developer.developer_id = '%i'
    LIMIT 1
    """ % developer_id

    result = db(sql)
    if result:
        logger.debug(result)
        return True
    else:
        return False


def check_developer_with_name(developer_name):
    """
    根据开发人员姓名检查数据是否存在,若存在则返回id
    :return:
    """
    sql = """
    SELECT
    developer.developer_id
    FROM
    developer
    WHERE
    developer.name = '%s'
    """ % developer_name

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def check_developer_with_email(developer_email):
    """
    根据开发人员邮箱检查数据是否存在,若存在则返回id
    :return:
    """
    sql = """
    SELECT
    developer.developer_id
    FROM
    developer
    WHERE
    developer.email = '%s'
    """ % developer_email

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def add_developer(developer_name, developer_email, develop_type=None):
    if develop_type:
        sql = """
        INSERT INTO developer (type_id, name, email)
        VALUES ('%i', '%s', '%s');
        """ % (develop_type, developer_name, developer_email)
    else:
        sql = """
        INSERT INTO developer (name, email) 
        VALUES ('%s', '%s');
        """ % (developer_name, developer_email)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def get_developer_insert_id():
    """
    获取新增后id
    :return:
    """
    sql = """
    SELECT developer_id 
    FROM developer 
    ORDER BY developer_id 
    DESC LIMIT 1
    """

    result = db(sql)
    if result:
        logger.debug(result)
        return True
    else:
        return False
