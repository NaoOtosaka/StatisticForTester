from tools.database import db


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
        project_phases.phase_id = "%i"
    """ % phase_id

    result = db(sql)
    if result:
        print(result)
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
        project_phases.phase_id = "%i"
    """ % phase_id

    result = db(sql)
    if result:
        print(result)
        temp = {
            'planId': result[0][0],
            'planName': result[0][1]
        }
        return temp
    else:
        return []
