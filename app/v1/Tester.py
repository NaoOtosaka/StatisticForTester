from flask import Blueprint
from flask import request
import json

from libs.tester import *
from tools.log import *

# 实例化日志对象
logger = setLogger('tester_api')


# 实例化蓝图
tester_api = Blueprint('tester', __name__, url_prefix='/tester')


@tester_api.route('/list', methods=['GET'])
def tester_list():
    """
    返回测试人员列表
    :return:
    """
    return show_tester_list()


@tester_api.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def tester():
    if request.method == 'GET':
        return show_tester_info()
    elif request.method == 'POST':
        return add_tester_api()
    elif request.method == 'PUT':
        return edit_tester_api()
    elif request.method == 'DELETE':
        return delete_tester_api()


def show_tester_list():
    """
    获取测试人员列表
    :return:{
        'msg': string,
        'data': {
            'testerId': int,
            'testerName': string,
            'testerEmail': string
        },
        'status': 1
        }
    """
    result = get_tester_list()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无测试人员信息', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


def show_tester_info():
    """
    展示测试人员详细信息
    :return: {
        'msg': string,
        'data': {
            'testerId': int,
            'testerName': string,
            'testerEmail': string,
            'project': project_info_list
        },
        'status': 1
    }
    """
    tester_id = int(request.values.get('testerId'))

    if tester_id:
        base_info = get_tester_base_info(tester_id)
        if base_info:
            project_info = get_project_info_with_tester(tester_id)

            res = {
                'msg': "成功",
                'data': {
                    'testerId': base_info['testerId'],
                    'testerName': base_info['testerName'],
                    'testerEmail': base_info['testerEmail'],
                    'project': project_info
                },
                'status': 1
            }
        else:
            res = {'msg': '测试人员不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


def add_tester_api():
    """
    新增测试人员
    :return:{
        ‘msg’: string,
        'status': int
    }
    """
    # 接受入参
    tester_name = request.json.get('testerName')
    tester_email = request.json.get('testerEmail')
    logger.debug(tester_name)
    logger.debug(tester_email)

    if tester_name and tester_email:
        if check_tester_with_email(tester_email):
            res = {'msg': '该测试人员已存在', 'status': 2001}
        else:
            status = add_tester(tester_name, tester_email)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def edit_tester_api():
    """
    编辑测试人员
    :return:{
        ‘msg’: string,
        'status': int
    }
    """
    # 接受入参
    tester_id = int(request.json.get('testerId'))
    tester_name = request.json.get('testerName')
    tester_email = request.json.get('testerEmail')
    logger.debug(tester_id)
    logger.debug(tester_name)
    logger.debug(tester_email)

    if tester_name and tester_email and tester_id:
        if check_tester_with_id(tester_id):
            status = edit_tester(tester_id, tester_name, tester_email)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
        else:
            res = {'msg': '该测试人员不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def delete_tester_api():
    """
    删除测试人员
    :return:{
        ‘msg’: string,
        'status': int
    }
    """
    tester_id = int(request.json.get('testerId'))

    if tester_id:
        if check_tester_with_id(tester_id):
            status = delete_tester(tester_id)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
        else:
            res = {'msg': '该测试人员不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


@tester_api.route('/bug_count', methods=['get'])
def bug_count_data():
    """
    人员BUG计数统计
    :return:
    """
    result = get_bug_count_with_tester()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无相关统计信息', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


@tester_api.route('/bug_type', methods=['get'])
def bug_type_data():
    """
    根据测试人员或许BUG类型
    :return:
    """
    tester_id = int(request.values.get('testerId'))

    result = get_bug_type_count_with_tester(tester_id)

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无相关统计信息', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


@tester_api.route('/bug_category', methods=['get'])
def bug_category_data():
    """
    根据测试人员或许BUG类型
    :return:
    """
    tester_id = int(request.values.get('testerId'))

    result = get_bug_category_count_with_tester(tester_id)

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无相关统计信息', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)