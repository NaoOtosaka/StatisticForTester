from tools.database import db
from tools.log import *

# 实例化日志对象
logger = setLogger('project')


def get_project_list(category_id=None):
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
        project.planner_id,
        project_category.category_name as category,
        project.doc_url,
        project.test_time,
        project.publish_time
        FROM
        project
        INNER JOIN project_category ON project.category = project_category.category_id
        """

    if category_id:
        sql += "WHERE project.category = %i" % int(category_id)

    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            tester = get_tester_with_project(result[i][0])

            tester_list = []
            for item in tester:
                tester_list.append(item['testerId'])

            temp.append(
                {
                    'projectId': result[i][0],
                    'projectName': result[i][1],
                    'planner': result[i][2],
                    'category': result[i][3],
                    'docUrl': result[i][4],
                    'testTime': result[i][5],
                    'publishTime': result[i][6],
                    'tester': tester_list
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
        project.planner_id,
        project.doc_url,
        project.test_time,
        project.publish_time
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
                'planner': result[0][2]
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


def check_project_with_id(project_id):
    """
    根据BUG ID检查数据是否存在, 若存在则返回id
    :param project_id:
    :return:
    """
    sql = """
    SELECT 
    project_id
    FROM
    project
    WHERE
    project_id = %i
    LIMIT 1
    """ % project_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def add_project(planner_id, project_name, category=None):
    """
    新建项目
    :param category:
    :param planner_id:
    :param project_name:
    :return:
    """
    if category:
        sql = """
        INSERT INTO project(planner_id, project_name, category) 
        VALUES ('%i', '%s', '%i')
        """ % (planner_id, project_name, category)
    else:
        sql = """
        INSERT INTO project(planner_id, project_name) 
        VALUES ('%i', '%s')
        """ % (planner_id, project_name)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def edit_project(project_id, planner_id, project_name, doc_url, test_time, publish_time):
    """
    编辑项目信息
    :param project_id:
    :param planner_id:
    :param project_name:
    :param doc_url:
    :param test_time:
    :param publish_time:
    :return:
    """
    sql = """
    UPDATE project 
    SET"""

    if test_time:
        sql += " test_time=%r," % test_time
    if publish_time:
        sql += " publish_time=%r," % publish_time

    sql += """
    planner_id=%i, 
    project_name='%s',
    doc_url='%s'
    WHERE 
    project_id=%i;
    """ % (planner_id, project_name, doc_url, project_id)

    print(sql)

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
        Count( bug.bug_id ) AS count,
        bug_type.type_name AS type 
    FROM
        bug
        INNER JOIN bug_type ON bug.bug_type = bug_type.type_id
        INNER JOIN project_phases ON bug.phase_id = project_phases.phase_id
        INNER JOIN project ON project_phases.project_id = project.project_id 
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


def get_bug_type_count_with_project_phase(project_id):
    """
    根据项目id获取每个项目阶段BUG类型数
    :param project_id:
    :return:
    """
    sql = """
    SELECT
    bug_type.type_name,
    test_plan.plan_name,
    Count(1)
    FROM
    bug
    INNER JOIN bug_type ON bug.bug_type = bug_type.type_id
    INNER JOIN project_phases ON bug.phase_id = project_phases.phase_id
    INNER JOIN test_plan ON project_phases.plan_id = test_plan.plan_id
    WHERE
    project_phases.project_id = %i
    GROUP BY
    bug_type.type_name,
    test_plan.plan_id
    ORDER BY
    bug_type.type_name ASC,
    test_plan.plan_id ASC
    """ % project_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result
    else:
        return False


def get_bug_category_count_with_project(project_id):
    """
    获取项目BUG分类
    :return:
    """
    sql = """
    SELECT
        Count( bug.bug_id ) AS count,
        bug_category.category_name AS category 
    FROM
        bug
        INNER JOIN bug_category ON bug.category = bug_category.category_id
        INNER JOIN project_phases ON bug.phase_id = project_phases.phase_id
        INNER JOIN project ON project_phases.project_id = project.project_id 
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


def get_bug_trend_with_project(project_id):
    """
    BUG趋势统计
    :return:
    """
    date = '%Y-%m-%d'
    sql = """
    SELECT
        date,
        COUNT( COUNT ) 
    FROM
        (
    SELECT
        FROM_UNIXTIME( bug.create_time, '%s' ) AS date,
        Count( bug.bug_id ) AS count 
    FROM
        project
        INNER JOIN project_phases ON project.project_id = project_phases.project_id
        INNER JOIN bug ON project_phases.phase_id = bug.phase_id 
    WHERE
        project.project_id = %i
    GROUP BY
        bug.create_time 
    ORDER BY
        bug.create_time ASC 
        ) AS data
    GROUP BY
        date 
    ORDER BY
        date ASC
    """ % (date, project_id)

    result = db(sql)

    if result:
        logger.debug(result)
        temp = {
            'startDate': result[0][0],
            'endDate': result[-1][0],
            'data': {}
        }
        for item in result:
            temp['data'][item[0]] = item[1]
        return temp
    else:
        return False


if __name__ == '__main__':
    pass