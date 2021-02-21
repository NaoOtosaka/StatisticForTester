from tools.database import db
from tools.log import *

# 实例化日志对象
logger = setLogger('project')


def get_project_list():
    """
    返回项目列表信息
    :return: {
        'projectId': int,
        'projectName': string,
        'planner': string,
        'category': string
    }
    """
    sql = """
        SELECT
        project.project_id,
        project.project_name,
        planner.name,
        project_category.category_name as category
        FROM
        project
        INNER JOIN planner ON project.planner_id = planner.planner_id
        INNER JOIN project_category ON project.category = project_category.category_id
        """
    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(
                {
                    'projectId': result[i][0],
                    'projectName': result[i][1],
                    'planner': result[i][2],
                    'category': result[i][3]
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
        project.planner_id
        FROM
        project
        WHERE
        project.project_id = "%i";
    """ % project_id

    # 获取项目基础信息
    result = db(sql)
    if result:
        logger.debug(result)
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
        logger.debug(result)

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
        logger.debug(result)

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
        project_phases.end_time,
        Count(bug.bug_id) as count
        FROM
        project
        INNER JOIN project_phases ON project_phases.project_id = project.project_id
        INNER JOIN test_plan ON project_phases.plan_id = test_plan.plan_id
        INNER JOIN bug ON bug.phase_id = project_phases.phase_id
        WHERE
        project.project_id = "%i"
        GROUP BY
        project_phases.phase_id,
        test_plan.plan_name,
        project_phases.start_time,
        project_phases.end_time
        ORDER BY
        test_plan.plan_id ASC
    """ % project_id

    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(
                {
                    'phaseId': result[i][0],
                    'name': result[i][1],
                    'startTime': result[i][2],
                    'endTime': result[i][3],
                    'count': result[i][4]
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
        logger.debug(result)

        for i in range(len(result)):
            temp.append(result[i][0])

        return temp
    else:
        return []


def check_project_with_name(project_name):
    """
    根据项目名检查数据是否存在,若存在则返回id
    :return:
    """
    sql = """
    SELECT
    project.project_id
    FROM
    project
    WHERE
    project.project_name = '%s'
    """ % project_name

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def add_project(planner_id, project_name):
    """
    新建项目
    :param planner_id:
    :param project_name:
    :return:
    """
    sql = """
    INSERT INTO "project"("planner_id", "project_name") 
    VALUES ('%i', '%s')
    """ % (planner_id, project_name)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def get_project_insert_id():
    """
    获取新增后id
    :return:
    """
    sql = """
    SELECT project_id 
    FROM project 
    ORDER BY project_id 
    DESC LIMIT 1
    """

    result = db(sql)

    if result:
        return result[0][0]
    else:
        return False


def get_bug_type_count_with_project(project_id):
    """
    获取每个项目对应异常类型统计
    :return:
    """
    sql = """
    SELECT
    bug_type.type_name as type,
    Count(1) as count
    FROM
    project ,
    bug
    INNER JOIN project_phases ON project_phases.project_id = project.project_id 
    AND bug.phase_id = project_phases.phase_id
    INNER JOIN bug_type ON bug.bug_type = bug_type.type_id
    WHERE
    project.project_id = %i
    GROUP BY
    bug_type.type_name
    """ % project_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result
    else:
        return False


def get_bug_category_count_with_project(project_id):
    """
    获取测试人员跟进BUG分类
    :return:
    """
    sql = """
    SELECT
    Count(bug.bug_id) as count,
    bug_category.category_name as category
    FROM
    bug_category
    INNER JOIN bug ON bug.category = bug_category.category_id ,
    project
    INNER JOIN project_phases ON project_phases.project_id = project.project_id AND bug.phase_id = project_phases.phase_id
    WHERE
    project.project_id = %i
    GROUP BY
    bug_category.category_name
    """ % project_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result
    else:
        return False


def get_bug_developer_count_with_project(project_id):
    """
    根据项目获取开发人员跟进BUG占比
    :return: 
    """
    sql = """
    SELECT
    Count(bug.bug_id) AS count,
    developer.name AS developer
    FROM
    developer
    INNER JOIN bug ON bug.developer_id = developer.developer_id
    INNER JOIN project_phases ON bug.phase_id = project_phases.phase_id
    INNER JOIN project ON project_phases.project_id = project.project_id
    WHERE
    project.project_id = %i
    GROUP BY
    developer.name
    """ % project_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result
    else:
        return False
