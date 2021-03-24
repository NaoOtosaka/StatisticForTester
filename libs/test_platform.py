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
    id
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
    test_platform.desc,
    test_platform.start_time,
    test_platform.end_time,
    test_platform.pass_rate
    FROM
    test_platform
    INNER JOIN project_phases ON test_platform.id = project_phases.phase_id
    WHERE
    project_phases.phase_id = %i
    """ % phase_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result
    else:
        return []


def add_platform(phase_id, pass_rate, desc):
    """
    创建测试阶段细分记录
    :param phase_id:
    :param pass_rate:
    :param desc:
    :return:
    """
    sql = """
    INSERT INTO `test_platform`(test_platform.phase_id, test_platform.pass_rate, test_platform.desc)
    VALUES
        ( %i, %.2f, '%s');
    """ % (phase_id, pass_rate, desc)

    status = db(sql)
    if status:
        return 1
    else:
        return 0


def edit_platform(platform_id, phase_id, pass_rate, desc, start_time=None, end_time=None):
    """
    编辑测试阶段细分记录
    :param end_time:
    :param start_time:
    :param platform_id:
    :param phase_id:
    :param pass_rate:
    :param desc:
    :return:
    """
    sql = """
        UPDATE test_platform 
        SET"""

    if start_time:
        sql += " start_time=%r," % start_time
    if end_time:
        sql += " end_time=%r," % end_time

    sql += """
        phase_id=%i, 
        pass_rate=%.2f,
        desc='%s'
        WHERE 
        id=%i;
        """ % (phase_id, pass_rate, desc, platform_id)

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