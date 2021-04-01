from tools.database import db
from tools.log import *

# 实例化日志对象
logger = setLogger('test_platform')


def check_platform_with_id(platform_id):
    """
    检查细分阶段存在性, 若存在则返回id
    :param platform_id:
    :return:
    """
    sql = """
    SELECT 
    1
    FROM
    test_platform
    WHERE
    id = %i
    LIMIT 1
    """ % platform_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def get_platform_info_with_phase(phase_id):
    """
    获取测试阶段对应细分类别通过率信息
    :return:
    """
    sql = """
    SELECT
    test_platform.id,
    platform_tag.tag_id,
    platform_tag.tag_name,
    test_platform.desc,
    test_platform.start_time,
    test_platform.end_time,
    test_platform.pass_rate
    FROM
    test_platform
    INNER JOIN project_phases ON test_platform.phase_id = project_phases.phase_id
    INNER JOIN platform_tag ON test_platform.tag_id = platform_tag.tag_id
    WHERE
    test_platform.phase_id = %i
    """ % phase_id

    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(
                {
                    'platformId': result[i][0],
                    'tagId': result[i][1],
                    'tagName': result[i][2],
                    'desc': result[i][3],
                    'startTime': result[i][4],
                    'endTime': result[i][5],
                    'passRate': result[i][6]
                }
            )

        return temp
    else:
        return []


def add_platform(phase_id, pass_rate, tag_id):
    """
    创建测试阶段细分记录
    :param phase_id:
    :param pass_rate:
    :param tag_id:
    :return:
    """
    sql = """
    INSERT INTO `test_platform`(test_platform.phase_id, test_platform.pass_rate, test_platform.tag_id)
    VALUES
        ( %i, %.2f, %i);
    """ % (phase_id, pass_rate, tag_id)

    status = db(sql)
    if status:
        return 1
    else:
        return 0


def edit_platform(platform_id, pass_rate, tag_id, start_time=None, end_time=None):
    """
    编辑测试阶段细分记录
    :param end_time:
    :param start_time:
    :param platform_id:
    :param pass_rate:
    :param tag_id:
    :return:
    """
    sql = """
        UPDATE test_platform 
        SET"""

    if start_time:
        sql += " test_platform.start_time=%r," % start_time
    if end_time:
        sql += " test_platform.end_time=%r," % end_time

    sql += """
        test_platform.pass_rate=%.2f,
        test_platform.tag_id=%i
        WHERE 
        id=%i;
        """ % (pass_rate, tag_id, platform_id)

    status = db(sql)
    if status:
        return 1
    else:
        return 0


def delete_platform(platform_id):
    """
    删除测试阶段细分记录
    :param platform_id:
    :return:
    """
    sql = """
    DELETE 
    FROM
        test_platform 
    WHERE
        id = '%i';
    """ % platform_id

    status = db(sql)
    if status:
        return 1
    else:
        return 0


def get_pass_rate_statistic_with_project(project_id):
    """
    获取项目对应的通过率统计信息
    :param project_id:
    :return:
    """
    sql = """
    SELECT
    platform_tag.tag_name,
    test_plan.plan_name,
    test_platform.pass_rate
    FROM
    test_platform
    INNER JOIN platform_tag ON test_platform.tag_id = platform_tag.tag_id
    INNER JOIN project_phases ON test_platform.phase_id = project_phases.phase_id
    INNER JOIN test_plan ON project_phases.plan_id = test_plan.plan_id
    WHERE
    project_phases.project_id = %i
    """ % project_id

    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(
                {
                    'tagName': result[i][0],
                    'planName': result[i][1],
                    'passRate': result[i][2]
                }
            )

        return temp
    else:
        return []
