from tools.database import db
from tools.log import *

# 实例化日志对象
logger = setLogger('bug')


def get_bug_list():
    """
    获取BUG列表
    :return: bug_list
    [
        {
            'bugId': int,
            'kbId': int,
            'bugTitle': string,
            'bugModel': string,
            'projectName': string,
            'testerName': string,
            'developerName': string,
            'is_finish': boolean,
            'is_close': boolean,
        }
    ]
    """
    sql = """
    SELECT
    bug.bug_id,
    bug.kb_id,
    bug.title,
    bug.model,
    project.project_name,
    tester.name,
    developer.name,
    bug.is_closed,
    bug.is_finished,
    bug_category.category_name,
    bug_type.type_name
    FROM
    bug
    INNER JOIN project_phases ON bug.phase_id = project_phases.phase_id
    INNER JOIN project ON project_phases.project_id = project.project_id
    INNER JOIN tester ON bug.tester_id = tester.tester_id
    INNER JOIN developer ON bug.developer_id = developer.developer_id
    INNER JOIN bug_category ON bug.category = bug_category.category_id
    INNER JOIN bug_type ON bug.bug_type = bug_type.type_id


    """

    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(
                {
                    'bugId': result[i][0],
                    'kbId': result[i][1],
                    'bugTitle': result[i][2],
                    'bugModel': result[i][3],
                    'bugType': result[i][10],
                    'bugCategory': result[i][9],
                    'projectName': result[i][4],
                    'testerName': result[i][5],
                    'developerName': result[i][6],
                    'is_finish': result[i][7],
                    'is_close': result[i][8],
                }
            )

    return temp


def get_bug_base_info(bug_id):
    """
    获取BUG基础信息
    :return:{
        'bugId': int,
        'kbId': int,
        'bugTitle': string,
        'bugModel': string,
        'bugCategory': int,
        'bugType': int,
        'phaseId': int,
        'isClose': boolean,
        'inOnline': boolean,
        'isFinish': boolean,
        'createTime': timestamp,
        'closeTime': timestamp,
        'developerId': int,
        'testerId': int,
    }
    """
    sql = """
        SELECT
        bug.bug_id,
        bug.kb_id,
        bug.title,
        bug.model,
        bug.category,
        bug.bug_type,
        bug.phase_id,
        bug.is_closed,
        bug.is_online,
        bug.is_finished,
        bug.create_time,
        bug.close_time,
        bug.developer_id,
        bug.tester_id
        FROM
        bug
        WHERE 
        bug.bug_id = "%i";
    """ % bug_id

    result = db(sql)
    if result:
        logger.debug(result)
        temp = {
            'bugId': result[0][0],
            'kbId': result[0][1],
            'bugTitle': result[0][2],
            'bugModel': result[0][3],
            'bugCategory': result[0][4],
            'bugType': result[0][5],
            'phaseId': result[0][6],
            'isClose': result[0][7],
            'inOnline': result[0][8],
            'isFinish': result[0][9],
            'createTime': result[0][10],
            'closeTime': result[0][11],
            'developerId': result[0][12],
            'testerId': result[0][13],
        }
        return temp
    else:
        return []


def get_tester_info_with_bug(bug_id):
    """
    根据BUG ID获取与之关联的测试人员信息
    :param bug_id:
    :return:
    """
    sql = """
        SELECT
        tester.tester_id,
        tester.name,
        tester.email
        FROM
        bug
        INNER JOIN tester ON bug.tester_id = tester.tester_id
        WHERE
        bug.bug_id = "%i"
    """ % bug_id

    result = db(sql)
    if result:
        logger.debug(result)
        temp = {
            'testerId': result[0][0],
            'testerName': result[0][1],
            'testerEmail': result[0][2]
        }
        return temp
    else:
        return []


def get_developer_with_bug(bug_id):
    pass


def get_project_with_bug(bug_id):
    pass


def get_bug_type_with_bug(bug_id):
    pass


def get_category_with_bug(bug_id):
    pass


def check_bug_with_kb_id(kb_id):
    """
    根据看板id检查数据是否存在,若存在则返回id
    :param kb_id:
    :return: 对应人员id
    """
    sql = """
    SELECT
    bug_id
    FROM
    bug
    WHERE
    bug.kb_id = %i
    LIMIT 1
    """ % kb_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def check_bug_with_id(bug_id):
    """
    根据BUG ID检查数据是否存在, 若存在则返回id
    :param bug_id:
    :return:
    """
    sql = """
    SELECT 
    bug_id
    FROM
    bug
    WHERE
    bug.bug_id = %i
    LIMIT 1
    """ % bug_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def add_bug(tester_id, developer_id, phase_id, bug_type, category, kb_id, title, model, create_time, close_time,
            is_finished, is_closed, is_online):
    """
    新增Bug
    :param tester_id:
    :param developer_id:
    :param phase_id:
    :param bug_type:
    :param category:
    :param kb_id:
    :param title:
    :param model:
    :param create_time:
    :param close_time:
    :param is_finished:
    :param is_closed:
    :param is_online:
    :return:
    """
    sql = """
    INSERT INTO "bug" ("tester_id", "developer_id", "phase_id", "bug_type", "category", "kb_id", "title", "model", 
    "create_time", "close_time", "is_finished", "is_closed", "is_online")
    VALUES
    (%i, %i, %i, %i, %i, %i, '%s', '%s', '%i', %r, '%s', '%s', '%s')
    """ % (tester_id, developer_id, phase_id, bug_type, category, kb_id, title, model, create_time, close_time,
           is_finished, is_closed, is_online)
    logger.debug(sql)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def edit_bug(tester_id, developer_id, phase_id, bug_type, category, kb_id, title, model, create_time, close_time,
             is_finished, is_closed, is_online):
    """
    编辑Bug
    :param tester_id:
    :param developer_id:
    :param phase_id:
    :param bug_type:
    :param category:
    :param kb_id:
    :param title:
    :param model:
    :param create_time:
    :param close_time:
    :param is_finished:
    :param is_closed:
    :param is_online:
    :return:
    """
    sql = """
    UPDATE bug SET tester_id=%i, developer_id=%i, phase_id=%i, bug_type=%i, category=%i, title='%s', 
    model='%s', create_time=%i, close_time=%i, is_finished='%s', is_closed='%s', is_online='%s' WHERE kb_id=%i;
    """ % (tester_id, developer_id, phase_id, bug_type, category, title, model, create_time, close_time, is_finished,
           is_closed, is_online, kb_id)

    logger.debug(sql)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def delete_bug_with_id(bug_id):
    """
    通过BUG ID删除BUG
    :param bug_id:
    :return:
    """
    sql = """
    DELETE FROM bug WHERE bug_id='%i';
    """ % bug_id

    logger.debug(sql)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def delete_bug_with_kb_id(kb_id):
    """
    通过KB ID删除BUG
    :param kb_id:
    :return:
    """
    sql = """
    DELETE FROM bug WHERE kb_id='%i';
    """ % kb_id

    logger.debug(sql)
    status = db(sql)
    if status:
        return 1
    else:
        return 0


def get_bug_type_count():
    """
    BUG类型统计
    :return:
    """
    sql = """
    SELECT
    bug_type.type_name,
    COUNT(1) as count
    FROM
    tester
    INNER JOIN bug ON bug.tester_id = tester.tester_id
    INNER JOIN bug_type ON bug.bug_type = bug_type.type_id
    GROUP BY
    bug.bug_type
    """

    result = db(sql)
    if result:
        logger.debug(result)
        return result
    else:
        return False


def get_bug_category_count():
    """
    BUG分类统计
    :return:
    """
    sql = """
    SELECT
    Count(1) AS count,
    bug_category.category_name
    FROM
    tester
    INNER JOIN bug ON bug.tester_id = tester.tester_id
    INNER JOIN bug_category ON bug.category = bug_category.category_id
    GROUP BY
    bug.category
    """

    result = db(sql)
    if result:
        logger.debug(result)
        return result
    else:
        return False


def get_bug_trend():
    """
    BUG趋势统计
    :return:
    """
    sql = """
    SELECT
        date,
        COUNT( COUNT ) 
    FROM
        (
    SELECT
        date( bug.create_time, 'unixepoch' ) AS date,
        Count( bug.bug_id ) AS count 
    FROM
        tester
        INNER JOIN bug ON bug.tester_id = tester.tester_id 
    GROUP BY
        bug.create_time 
    ORDER BY
        bug.create_time ASC 
        ) 
    GROUP BY
        date 
    ORDER BY
        date ASC
    """

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


def get_bug_count_by_env():
    """
    获取BUG环境分类
    :return:
    """
    sql = """
    SELECT
    bug.is_online AS env,
    Count(bug.bug_id) AS count
    FROM
    tester
    INNER JOIN bug ON bug.tester_id = tester.tester_id
    GROUP BY
    bug.is_online
    """

    result = db(sql)

    if result:
        logger.debug(result)
        temp = []
        for item in result:
            if item[0] == 'False':
                temp.append(('开发异常', item[1]))
            else:
                temp.append(('线上异常', item[1]))
        return temp
    else:
        return False