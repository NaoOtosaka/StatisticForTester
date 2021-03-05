from flask import Blueprint
from flask import request
import json

from libs.project import *
from libs.bug import *
from libs.test import *
from tools.log import *
from common.DateEncoder import DateEncoder

# 实例化日志对象
logger = setLogger('project_api')

# 实例化蓝图
project_api = Blueprint('project', __name__, url_prefix='/project')


@project_api.route('/list', methods=['GET'])
def project_list():
    return show_project_list()


@project_api.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'], strict_slashes=False)
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

    return json.dumps(res, cls=DateEncoder, ensure_ascii=False)


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
    category_id = request.values.get('categoryId')

    result = get_project_list(category_id=category_id)

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
    project_id = int(request.values.get('projectId'))
    planner_id = int(request.values.get('plannerId'))
    project_name = request.values.get('projectName')
    doc_url = request.values.get('docUrl')
    test_time = int(request.values.get('testTime'))
    publish_time = int(request.values.get('publishTime'))

    # 时间字段完整性判断
    if test_time == 'null':
        test_time = None

    if publish_time == 'null':
        publish_time = None

    if project_id and planner_id and project_name:
        if check_project_with_id(project_id):
            status = edit_project(project_id, planner_id, project_name, doc_url, test_time, publish_time)
            # 状态码判断
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
    根据项目获取BUG类型
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


@project_api.route('/bug_phase_type', methods=['GET'])
def bug_phase_type():
    """
    根据项目获取每个项目阶段BUG类型数
    :return:
    """
    project_id = int(request.values.get('projectId'))

    if project_id:
        result = get_bug_type_count_with_project_phase(project_id)
        if result:
            plan_list = []

            plan_temp = get_phase_info_with_project(project_id)
            for value in plan_temp:
                plan_list.append(value['name'])

            type_list = []
            data_temp = {}
            for value in result:
                if value[0] not in type_list:
                    type_list.append(value[0])
                if value[1] not in plan_list:
                    plan_list.append(value[1])

            for type_value in type_list:
                data_temp[type_value] = {}
                for plan in plan_list:
                    data_temp[type_value][plan] = 0

            for value in result:
                data_temp[value[0]][value[1]] = value[2]

            res_temp = {
                'planList': plan_list,
                'typeList': type_list,
                'data': data_temp
            }

            res = {
                'msg': '成功',
                'data': res_temp,
                'status': 1
            }
        else:
            res = {'msg': '无相关统计信息', 'status': 2001}

        return json.dumps(res, ensure_ascii=False)


@project_api.route('/bug_category', methods=['get'])
def bug_category():
    """
    根据项目获取BUG分类
    传入空时统计全部类型数据
    :return:
    """
    project_id = request.values.get('projectId')

    if project_id:
        result = get_bug_category_count_with_project(int(project_id))
    else:
        result = get_bug_category_count()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无相关统计信息', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


@project_api.route('/developer_count', methods=['get'])
def developer_count():
    """
    根据测试人员或许BUG类型
    传入空时统计全部类型数据
    :return:
    """
    project_id = request.values.get('projectId')

    if project_id:
        result = get_bug_developer_count_with_project(int(project_id))
    else:
        result = get_bug_developer_count()

    if result:
        res = {
            'msg': '成功',
            'data': result,
            'status': 1
        }
    else:
        res = {'msg': '无相关统计信息', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


@project_api.route('/test_record', methods=['PUT'])
def test_record():
    """
    测试人员与项目跟进关系处理
    :return:
    """
    project_id = int(request.values.get('projectId'))
    tester = request.values.get('tester')

    tag = 1

    tester_list = []

    if tester:
        list_temp = []
        # 获取测试人员列表id
        tester_list = tester.split(',')

        # 数据类型转换
        for i in tester_list:
            list_temp.append(int(i))
        tester_list = list_temp

    temp = []

    # 获取项目当前跟进测试人员列表
    for item in get_tester_with_project(project_id):
        temp.append(item['testerId'])

    # 差集运算，取新增人员
    add_list = set(tester_list).difference(set(temp))

    # 新增跟进关系
    for tester_id in add_list:
        tag = add_test_record_with_tester_and_project(tester_id, project_id)

    # 差集运算，取删除人员
    delete_list = set(temp).difference(set(tester_list))

    # 删除跟进关系
    for tester_id in delete_list:
        tag = delete_test_record_with_tester_and_project(tester_id, project_id)

    if tag:
        res = {
            'msg': '成功',
            'status': 1
        }
    else:
        res = {
            'msg': '系统错误',
            'status': 1
        }

    return json.dumps(res, ensure_ascii=False)


