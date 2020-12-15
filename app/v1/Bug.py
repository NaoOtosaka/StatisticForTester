from flask import Blueprint
from flask import request
import json

from libs.bug import *


# 实例化蓝图
bug_api = Blueprint('bug', __name__, url_prefix='/bug')


@bug_api.route('/list', methods=['GET'])
def bug_list():
    return show_bug_list()


@bug_api.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def bug():
    if request.method == 'GET':
        return show_bug_info()
    elif request.method == 'POST':
        return add_bug()
    elif request.method == 'PUT':
        return edit_bug()
    elif request.method == 'DELETE':
        return delete_bug()


def show_bug_list():
    """
    展示BUG列表
    :return:
    {
        'msg': string,
        'data': bug_list,
        'status': 1
        }
    """
    result = get_bug_list()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '暂无缺陷', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


def show_bug_info():
    """
    展示BUG详细信息
    :return:
    """


def add_bug():
    pass


def edit_bug():
    pass


def delete_bug():
    pass