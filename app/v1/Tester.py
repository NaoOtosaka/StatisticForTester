from flask import Blueprint
from flask import request
import json

from libs.tester import *

# 实例化蓝图
tester_api = Blueprint('tester', __name__, url_prefix='/tester')


@tester_api.route('/list', methods=['GET'])
def tester_list():
    """
    返回测试人员列表
    :return:
    """
    return json.dumps(show_tester_list(), ensure_ascii=False)


@tester_api.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def tester():
    if request.method == 'GET':
        return show_tester_info()
    elif request.method == 'POST':
        return add_tester()
    elif request.method == 'PUT':
        return edit_tester()
    elif request.method == 'DELETE':
        return delete_tester()


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
    tester_id = request.values.get('testerId')

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


def add_tester():
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
    print(tester_name)
    print(tester_email)

    if tester_name and tester_email:
        sql = 'SELECT * FROM tester WHERE tester.email = "%s";' % tester_email
        if db(sql):
            res = {'msg': '该测试人员已存在', 'status': 2001}
        else:
            insert_sql = 'INSERT INTO "tester" ("name", "email") VALUES ("%s", "%s");' \
                         % (tester_name, tester_email)
            status = db(insert_sql)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def edit_tester():
    """
    编辑测试人员
    :return:{
        ‘msg’: string,
        'status': int
    }
    """
    # 接受入参
    tester_id = request.json.get('testerId')
    tester_name = request.json.get('testerName')
    tester_email = request.json.get('testerEmail')
    print(tester_id)
    print(tester_name)
    print(tester_email)

    if tester_name and tester_email and tester_id:
        sql = 'SELECT * FROM tester WHERE tester.tester_id = "%i";' % tester_id
        if db(sql):
            sql = 'SELECT * FROM tester WHERE tester.email = "%s";' % tester_email
            if db(sql):
                update_sql = 'UPDATE tester SET name="%s", email="%s" WHERE tester_id="%i"' \
                             % (tester_name, tester_email, tester_id)
                status = db(update_sql)
                if status:
                    res = {'msg': '成功', 'status': 1}
                else:
                    res = {'msg': '系统错误', 'status': 500}
            else:
                res = {'msg': '邮箱不可重复', 'status': 2001}
        else:
            res = {'msg': '该测试人员不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def delete_tester():
    """
    删除测试人员
    :return:{
        ‘msg’: string,
        'status': int
    }
    """
    tester_id = request.json.get('testerId')

    if tester_id:
        sql = 'SELECT * FROM tester WHERE tester_id = "%i";' % tester_id
        if db(sql):
            delete_sql = 'DELETE FROM tester WHERE tester_id="%i";' % tester_id
            status = db(delete_sql)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
        else:
            res = {'msg': '项目不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)