from tools.database import db
from libs.project import *


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
        tester.name
        FROM
        tester
        WHERE
        tester.tester_id = "%i"
    """ % tester_id

    # 获取测试基础信息
    result = db(sql)
    if result:
        print(result)
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
        tester
        """
    temp = []

    result = db(sql)
    if result:
        print(result)

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
        test.tester_id = "%i"
    """ % tester_id

    temp = []

    # 获取项目id列表
    result = db(sql)

    if result:
        print(result)

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
        tester.tester_id = "%i" AND
        project.project_id = "%i"
    """ % (tester_id, project_id)

    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(result[i][0])

        return temp
    else:
        return []
