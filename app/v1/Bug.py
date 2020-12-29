from flask import Blueprint
from flask import request
import json
import random

from libs.bug import *
from libs.tester import *
from libs.developer import *
from libs.bug_category import *
from libs.bug_type import *
from libs.phase import *


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
    {
        'bugId': int,
        'bugTitle': string,
        'bugCategory': string,
        'bugType': string,
        'createTime': timestamp,
        'closeTime': timestamp,
        'isClose': boolean,
        'inOnline': boolean,
        'isFinish': boolean,
        'projectInfo': project_info_list,
        'planInfo': plan_info_list,
        'developerInfo': developer_info_list,
        'testerInfo': tester_info_list,
    }
    """
    bug_id = int(request.values.get('bugId'))

    if bug_id:
        base_info = get_bug_base_info(bug_id)
        print(base_info)
        if base_info:
            developer_info = get_tester_base_info(base_info['testerId'])
            tester_info = get_developer_base_info(base_info['developerId'])
            category = get_bug_category(base_info['bugCategory'])
            bug_type = get_bug_type(base_info['bugType'])
            project_info = get_project_info_with_phase(base_info['phaseId'])
            plan_info = get_plan_info_with_phase(base_info['phaseId'])

            res = {
                'bugId': base_info['bugId'],
                'bugTitle': base_info['bugTitle'],
                'bugCategory': category,
                'bugType': bug_type,
                'createTime': base_info['createTime'],
                'closeTime': base_info['closeTime'],
                'isClose': base_info['isClose'],
                'inOnline': base_info['inOnline'],
                'isFinish': base_info['isFinish'],
                'projectInfo': project_info,
                'planInfo': plan_info,
                'developerInfo': developer_info,
                'testerInfo': tester_info
            }
        else:
            res = {'msg': 'BUG信息不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


def add_bug():
    """
    新增BUG
    :return:
    """
    pass


def edit_bug():
    pass


def delete_bug():
    pass


@bug_api.route('test', methods=['get'])
def jmeter_test():
    data = random.randint(1, 6)
    print(data)
    res = {
        'msg': '成功',
        'data': data,
        'status': 1
    }
    return json.dumps(res, ensure_ascii=False)
