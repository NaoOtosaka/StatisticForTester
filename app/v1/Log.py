from flask import Blueprint
from flask import request
import json

from tools.log import setLogger
from libs.log import get_update_log_list

# 实例化日志对象
logger = setLogger('log_api')

# 实例化蓝图
log_api = Blueprint('log', __name__, url_prefix='/log')


@log_api.route('/', methods=['GET'])
def log():
    return show_log()


def show_log():
    """
    展示更新日志信息
    :return:
    """
    result = get_update_log_list()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无更新信息', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)