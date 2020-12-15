from tools.database import db


def get_bug_list():
    """
    获取BUG列表
    :return: bug_list
    [
        {
            'bugId': int,
            'bugTitle': string,
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
    bug.title,
    project.project_name,
    tester.name,
    developer.name,
    bug.is_closed,
    bug.is_finished
    FROM
    bug
    INNER JOIN project_phases ON bug.phase_id = project_phases.phase_id
    INNER JOIN project ON project_phases.project_id = project.project_id
    INNER JOIN tester ON bug.tester_id = tester.tester_id
    INNER JOIN developer ON bug.developer_id = developer.developer_id

    """

    temp = []

    result = db(sql)
    if result:
        print(result)

        for i in range(len(result)):
            temp.append(
                {
                    'bugId': result[i][0],
                    'bugTitle': result[i][1],
                    'projectName': result[i][2],
                    'testerName': result[i][3],
                    'developerName': result[i][4],
                    'is_finish': result[i][5],
                    'is_close': result[i][6],
                }
            )

    return temp


def get_bug_base_info(bug_id):
    """
    获取BUG基础信息
    :return:
    """
    sql = """
        SELECT
        bug.bug_id,
        bug.title,
        bug.category,
        bug.bug_type,
        bug.phase_id,
        bug.is_closed,
        bug.is_online,
        bug.is_finished,
        bug.close_time,
        bug.create_time,
        bug.developer_id,
        bug.tester_id
        FROM
        bug
        WHERE 
        bug.bug_id = "%i";
    """ % bug_id

    result = db(sql)
    if result:
        print(result)


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
        print(result)
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

