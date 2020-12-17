

from libs.project import *


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
        developer.developer_id = "%i";
    """ % developer_id

    # 获取测试基础信息

    result = db(sql)
    if result:
        print(result)
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
        print(result)

        for i in range(len(result)):
            temp.append(
                {
                    'developerId': result[i][0],
                    'typeId': result[i][1],
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
        developer.developer_id = "%s"
    """ % developer_id

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
        developer.developer_id = "%i" AND
        project.project_id = "%i"
    """ % (developer_id, project_id)

    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(result[i][0])

        return temp
    else:
        return []