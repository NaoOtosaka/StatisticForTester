from flask import Blueprint
from flask import request
import json

from libs.developer import *
from libs.develop_type import *
from tools.log import *

# 实例化日志对象
logger = setLogger('developer_api')


# 实例化蓝图
developer_api = Blueprint('developer', __name__, url_prefix='/developer')


@developer_api.route('/list', methods=['GET'])
def developer_list():
    """
    返回开发者列表
    :return:
    """
    result = get_developer_list()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无人员', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


@developer_api.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def developer():
    if request.method == 'GET':
        return show_developer_info()
    elif request.method == 'POST':
        return add_developer_api()
    elif request.method == 'PUT':
        return edit_developer_api()
    elif request.method == 'DELETE':
        return delete_developer_api()


def show_developer_info():
    """
    展示开发人员详细信息
    :return:{
        'msg': "成功",
        'data': {
            'developerId': int,
            'developerName': string,
            'developerType': string,
            'developerEmail': string,
            'project': project_info_list
        },
        'status': 1
    }
    """
    developer_id = int(request.values.get('developerId'))

    if developer_id:
        base_info = get_developer_base_info(developer_id)
        if base_info:
            develop_type = get_develop_type_with_type_id(base_info['typeId'])
            project_info = get_project_info_with_developer(developer_id)

            res = {
                'msg': "成功",
                'data': {
                    'developerId': base_info['developerId'],
                    'developerName': base_info['developerName'],
                    'developerType': develop_type,
                    'developerEmail': base_info['developerEmail'],
                    'project': project_info
                },
                'status': 1
            }
        else:
            res = {'msg': '开发人员不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


def add_developer_api():
    """
    新增开发人员
    :return:
    """
    # 接受入参
    developer_name = request.json.get('developerName')
    developer_email = request.json.get('developerEmail')
    develop_type = int(request.json.get('developType'))

    if developer_name and developer_email:
        if check_developer_with_email(developer_email):
            res = {'msg': '该开发人员已存在', 'status': 2001}
        else:
            if select_develop_type_exist(develop_type):
                status = add_developer(developer_name, developer_email, develop_type)
                if status:
                    res = {'msg': '成功', 'status': 1}
                else:
                    res = {'msg': '系统错误', 'status': 500}
            else:
                res = {'msg': '开发类型不存在', 'status': 4001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def edit_developer_api():
    """
    编辑开发人员
    :return:{
        ‘msg’: string,
        'status': int
    }
    """
    # 接受入参
    developer_id = request.json.get('developerId')
    developer_name = request.json.get('developerName')
    developer_email = request.json.get('developerEmail')
    develop_type = request.json.get('developType')
    logger.debug(developer_id)
    logger.debug(developer_name)
    logger.debug(developer_email)

    if developer_name and developer_email and developer_id:
        sql = 'SELECT * FROM developer WHERE developer.developer_id = "%s";' % developer_id
        if db(sql):
            res = {'msg': '该开发人员已存在', 'status': 2001}
        else:
            if select_develop_type_exist(develop_type):
                update_sql = 'UPDATE developer SET type_id = "%i", name="%s", email="%s" WHERE developer_id="%i"' \
                             % (develop_type, developer_name, developer_email, developer_id)
                status = db(update_sql)
                if status:
                    res = {'msg': '成功', 'status': 1}
                else:
                    res = {'msg': '系统错误', 'status': 500}
            else:
                res = {'msg': '开发类型不存在', 'status': 4001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def delete_developer_api():
    """
    删除开发人员
    :return:
    """
    developer_id = request.json.get('developerId')

    if developer_id:
        sql = 'SELECT * FROM developer WHERE developer_id = "%i";' % developer_id
        if db(sql):
            delete_sql = 'DELETE FROM developer WHERE developer_id="%i";' % developer_id
            status = db(delete_sql)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
        else:
            res = {'msg': '人员不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)
