from flask import Blueprint
from flask import request
import json

from tools.log import *
from libs.planner import *

# 实例化日志对象
logger = setLogger('planner_api')

# 实例化蓝图
planner_api = Blueprint('planner', __name__, url_prefix='/planner')


@planner_api.route('/list', methods=['GET'])
def planner_list():
    """
    返回策划人员列表
    :return:
    """
    return show_planner_list()


def show_planner_list():
    """
    获取策划列表
    :return:{
        'msg': string,
        'data': {
            'plannerId': int,
            'plannerName': string,
            'plannerEmail': string
        },
        'status': 1
        }
    """
    result = get_planner_list()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无策划人员信息', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)
