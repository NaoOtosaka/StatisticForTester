from tools.database import db
from tools.log import *

# 实例化日志对象
logger = setLogger('phase')


def get_project_info_with_phase(phase_id):
    """
    根据项目阶段id获取与之对应的项目信息
    :param phase_id:
    :return:project_info_list
    {
        'projectId': int,
        'projectName': string
    }
    """
    sql = """
    SELECT
    project.project_id,
    project.project_name
    FROM
    project_phases
    INNER JOIN project ON project_phases.project_id = project.project_id
    WHERE
    project_phases.phase_id = '%i'
    """ % phase_id

    result = db(sql)
    if result:
        logger.debug(result)
        temp = {
            'projectId': result[0][0],
            'projectName': result[0][1]
        }
        return temp
    else:
        return []


def get_plan_info_with_phase(phase_id):
    """
    根据项目阶段id获取预置对应的测试计划
    :param phase_id:
    :return:plan_info_list
    {
        'planId': int,
        'planName': string
    }
    """
    sql = """
    SELECT
    test_plan.plan_id,
    test_plan.plan_name
    FROM
    project_phases
    INNER JOIN test_plan ON project_phases.plan_id = test_plan.plan_id
    WHERE
    project_phases.phase_id = '%i'
    """ % phase_id

    result = db(sql)
    if result:
        logger.debug(result)
        temp = {
            'planId': result[0][0],
            'planName': result[0][1]
        }
        return temp
    else:
        return []


def get_plan_with_project_id(project_id):
    """
    根据项目id获取项目有关进度
    :return:
    """
    sql = """
    SELECT
    project_phases.phase_id,
    project_phases.plan_id
    FROM
    project_phases
    WHERE
    project_phases.project_id = '%s'
    """ % project_id

    temp = []

    result = db(sql)

    if result:
        logger.debug(result)
        for i in range(len(result)):
            temp.append(
                {
                    'phaseId': result[i][0],
                    'planId': result[i][1],
                }
            )
        return temp
    else:
        return []


def get_plan_with_project_and_plan(project_id, plan_id):
    """
    根据项目id与计划id获取项目有关进度
    :return:
    """
    sql = """
    SELECT
    project_phases.phase_id
    FROM
    project_phases
    WHERE
    project_phases.project_id = '%i' AND
    project_phases.plan_id = '%i'
    """ % (project_id, plan_id)

    temp = []

    result = db(sql)

    if result:
        logger.debug(result)
        for i in range(len(result)):
            temp.append(result[i][0])
        return temp
    else:
        return []


def add_phase(project_id, plan_id):
    """
    新建项目阶段
    :param project_id:
    :param plan_id:
    :return:
    """
    sql = """
    INSERT INTO "project_phases" ("project_id", "plan_id")
    VALUES
    ('%i', '%i')
    """ % (project_id, plan_id)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def get_phase_insert_id():
    """
    获取新增后id
    :return:
    """
    sql = """
    SELECT project_phases.phase_id
    FROM project_phases 
    ORDER BY phase_id 
    DESC LIMIT 1
    """

    result = db(sql)

    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return False
