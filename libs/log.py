from tools.log import setLogger
from tools.database import db
from tools.timeDeal import get_format_str

# 实例化日志对象
logger = setLogger('log')


def get_update_log_list():
    """
    获取更新日志
    :return:
    """
    sql = """
        SELECT
        log.log_id,
        log.content,
        log.commit_time
        FROM
        log
        ORDER BY
        log.commit_time DESC
    """

    temp = []

    # 获取更新日志信息
    result = db(sql)
    if result:
        logger.debug(result)
        for i in range(len(result)):
            temp.append(
                {
                    'logId': result[i][0],
                    'content': result[i][1],
                    'commitTime': get_format_str(result[i][2]),
                }
            )
        return temp
    else:
        return []