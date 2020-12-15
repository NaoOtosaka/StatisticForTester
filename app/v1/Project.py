from flask import Blueprint
from flask import request
import json

from libs.project import *


# 实例化蓝图
project_api = Blueprint('project', __name__)


@project_api.route('/api/v1/project/list', methods=['GET'])
def project_list():
    return show_project_list()


@project_api.route('/api/v1/project', methods=['GET', 'POST', 'PUT', 'DELETE'])
def project():
    if request.method == 'GET':
        # 获取项目基础信息
        return show_project_info()
    elif request.method == 'POST':
        # 创建项目
        return add_project()
    elif request.method == 'PUT':
        # 编辑项目
        return edit_project()
    elif request.method == 'DELETE':
        # 删除项目
        return delete_project()


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


def add_project():
    """
    新建项目
    :return:
    """
    # 接收入参
    planner_id = request.json.get('plannerId')
    print(planner_id)
    print(type(planner_id))
    project_name = request.json.get('projectName')

    if project_name and planner_id:
        sql = 'SELECT * FROM project WHERE project_name = "%s";' % project_name
        if db(sql):
            res = {'msg': '项目已存在', 'status': 2001}
        else:
            insert_sql = 'INSERT INTO project ("planner_id", "project_name") VALUES (%i, "%s")' \
                         % (planner_id, project_name)
            status = db(insert_sql)
            if status:
                res = {'msg': '成功', 'status': 1}
            else:
                res = {'msg': '系统错误', 'status': 500}
    else:
        res = {'msg': '参数错误', 'status': 4001}

    return json.dumps(res, ensure_ascii=False)


def edit_project():
    """
    编辑项目
    :return:
    """
    # 接收入参
    project_id = request.json.get('projectId')
    planner_id = request.json.get('plannerId')
    project_name = request.json.get('projectName')

    if project_id and planner_id and project_name:
        sql = 'SELECT * FROM project WHERE project_id = "%i";' % project_id
        if db(sql):
            update_sql = 'UPDATE project SET planner_id="%i", project_name="%s" WHERE project_id="%i"'\
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


def delete_project():
    """
    删除项目
    :return:
    """
    # 接收入参
    project_id = request.json.get('projectId')

    if project_id:
        sql = 'SELECT * FROM project WHERE project_id = "%i";' % project_id
        if db(sql):
            delete_sql = 'DELETE FROM project WHERE project_id="%i";' % project_id
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

