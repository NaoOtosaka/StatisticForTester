from flask import Blueprint
from flask import request
import json

from libs.project import *
from libs.bug import *
from tools.log import *

# 实例化日志对象
logger = setLogger('project_api')

# 实例化蓝图
project_api = Blueprint('project', __name__, url_prefix='/project')


@project_api.route('/list', methods=['GET'])
def project_list():
    return show_project_list()


@project_api.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'])
def project():
    if request.method == 'GET':
        # 获取项目基础信息
        return show_project_info()
    elif request.method == 'POST':
        # 创建项目
        return add_project_api()
    elif request.method == 'PUT':
        # 编辑项目
        return edit_project_api()
    elif request.method == 'DELETE':
        # 删除项目
        return delete_project_api()


def show_project_info():
    """
    展示项目详细信息
    :return:{
        'msg': string,
        'data': {
            'projectId': int,
            'projectName': string,
            'planner': string,
            'developer': Developer_info_list,
            'tester': Tester_info_list,
            'projectPhase': Phase_info_list
        },
        'status': 1
        }
    """
    project_id = int(request.values.get('projectId'))

    logger.info(project_id)

    if project_id:
        base_info = get_project_base_info(project_id)
        # 项目信息是否存在
        if base_info:
            # 获取开发人员信息
            developer_info = get_developer_with_project(project_id)

            # 获取测试人员信息
            tester_info = get_tester_with_project(project_id)

            # 获取项目进度信息
            phase_info = get_phase_info_with_project(project_id)

            res = {
                'msg': "成功",
                'data': {
                    'projectId': base_info['projectId'],
                    'projectName': base_info['projectName'],
                    'planner': base_info['planner'],
                    'developer': developer_info,
                    'tester': tester_info,
                    'projectPhase': phase_info
                },
                'status': 1
            }
        else:
            res = {'msg': '项目不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def show_project_list():
    """
    展示项目列表
    :return:{
        'msg': string,
        'data': {
            'projectId': int,
            'projectName': string,
            'planner': string,
        },
        'status': 1
        }
    """
    result = get_project_list()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无项目', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


def add_project_api():
    """
    新建项目
    :return:
    """
    # 接收入参
    planner_id = int(request.json.get('plannerId'))
    project_name = request.json.get('projectName')

    logger.info(planner_id)
    logger.info(project_name)

    if project_name and planner_id:
        if check_project_with_name(project_name):
            res = {'msg': '项目已存在', 'status': 2001}
        else:
            status = add_project(planner_id, project_name)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def edit_project_api():
    """
    编辑项目
    :return:
    """
    # 接收入参
    project_id = int(request.json.get('projectId'))
    planner_id = int(request.json.get('plannerId'))
    project_name = request.json.get('projectName')

    if project_id and planner_id and project_name:
        sql = "SELECT * FROM project WHERE project_id = '%i';" % project_id
        if db(sql):
            update_sql = "UPDATE project SET planner_id='%i', project_name='%s' WHERE project_id='%i';"\
                         % (planner_id, project_name, project_id)
            status = db(update_sql)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
        else:
            res = {'msg': '项目不存在', 'status': 2001}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def delete_project_api():
    """
    删除项目
    :return:
    """
    # 接收入参
    project_id = int(request.json.get('projectId'))

    if project_id:
        sql = "SELECT * FROM project WHERE project_id = '%i';" % project_id
        if db(sql):
            delete_sql = "DELETE FROM project WHERE project_id='%i';" % project_id
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


@project_api.route('/bug_type', methods=['get'])
def bug_type():
    """
    根据测试人员或许BUG类型
    传入空时统计全部类型数据
    :return:
    """
    project_id = request.values.get('projectId')

    if project_id:
        result = get_bug_type_count_with_project(int(project_id))
    else:
        result = get_bug_type_count()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无相关统计信息', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)