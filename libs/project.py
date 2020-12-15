from tools.database import db


def get_project_list():
    """
    返回项目列表信息
    :return: {
        'projectId': int,
        'projectName': string,
        'planner': string,
    }
    """
    sql = """
        SELECT
        project.project_id,
        project.project_name,
        planner.name
        FROM
        project
        INNER JOIN planner ON project.planner_id = planner.planner_id
        """
    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(
                {
                    'projectId': result[i][0],
                    'projectName': result[i][0],
                    'planner': result[i][0]
                }
            )
        return temp
    else:
        return []


def get_project_base_info(project_id):
    """
    根据项目ID获取项目基础信息
    :param project_id:  项目ID
    :return:
    {
        'projectId': int,
        'projectName': string,
        'planner': string,
    }
    """
    sql = """
        SELECT
        project.project_id,
        project.project_name,
        planner.name
        FROM
        project
        INNER JOIN planner ON project.planner_id = planner.planner_id
        WHERE
        project.project_id = "%i";
    """ % project_id

    # 获取项目基础信息
    result = db(sql)
    if result:
        print(result)
        temp = {
                'projectId': result[0][0],
                'projectName': result[0][1],
                'planner': result[0][2],
            }
        return temp
    else:
        return []


def get_developer_with_project(project_id):
    """
    根据项目ID获取与之关联的开发人员列表
    :param project_id:  项目ID
    :return: developer_list
    {
        'developerId': int,
        'name': string,
        'developType': string
    }
    """
    sql = """
        SELECT
        developer.developer_id,
        developer.name,
        develop_type.type_name
        FROM
        developer
        INNER JOIN develop_type ON developer.type_id = develop_type.type_id
        INNER JOIN develop ON develop.developer_id = developer.developer_id
        WHERE
        develop.project_id = "%i";
    """ % project_id

    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(
                {
                    'developerId': result[i][0],
                    'name': result[i][1],
                    'developType': result[i][2]
                }
            )
        return temp
    else:
        return []


def get_tester_with_project(project_id):
    """
    根据项目ID获取与之关联的测试人员列表
    :param project_id:  项目ID
    :return: developer_list
    {
        'testerId': int,
        'name': string
    }
    """
    sql = """
        SELECT
        tester.tester_id,
        tester.name
        FROM
        test
        INNER JOIN tester ON test.tester_id = tester.tester_id
        WHERE
        test.project_id = "%i";
    """ % project_id

    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(
                {
                    'testerId': result[i][0],
                    'name': result[i][1],
                }
            )
        return temp
    else:
        return []


def get_phase_info_with_project(project_id):
    """
    根据项目ID获取对应项目进度
    :param project_id:  项目ID
    :return: developer_list
    {
        'phaseId': int,
        'name': string,
        'startTime' timestamp,
        'endTime' timestamp
    }
    """
    sql = """
        SELECT
        project_phases.phase_id,
        test_plan.plan_name,
        project_phases.start_time,
        project_phases.end_time
        FROM
        project
        INNER JOIN project_phases ON project_phases.project_id = project.project_id
        INNER JOIN test_plan ON project_phases.plan_id = test_plan.plan_id
        WHERE
        project.project_id = "%i";
    """ % project_id

    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(
                {
                    'phaseId': result[i][0],
                    'name': result[i][1],
                    'startTime': result[i][2],
                    'endTime': result[i][3]
                }
            )
        return temp
    else:
        return []


def get_bug_list_with_project(project_id):
    """
    根据项目id获取项目对应bug
    :param project_id:
    :return:bug_id_list
    [int]
    """
    sql = """
        SELECT
        bug.bug_id
        FROM
        project_phases
        INNER JOIN project ON project_phases.project_id = project.project_id
        INNER JOIN bug ON bug.phase_id = project_phases.phase_id
        WHERE
        project.project_id = "%i"
    """ % project_id

    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(result[i][0])

        return temp
    else:
        return []