from libs.project import *
from libs.develop_type import *
from tools.log import *

# 实例化日志对象
logger = setLogger('planner')


def get_planner_list():
    """
    获取策划人员列表
    :return:
    [
        {
            'plannerId': int,
            'plannerName': string,
            'plannerEmail': string
        }
    ]
    """
    sql = """
        SELECT
        planner_id, 
        name, 
        email
        FROM
        planner
    """
    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(
                {
                    'plannerId': result[i][0],
                    'plannerName': result[i][1],
                    'plannerEmail': result[i][2],
                }
            )
        return temp
    else:
        return []