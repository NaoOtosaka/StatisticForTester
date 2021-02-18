from flask import Blueprint
from flask import request
import json

from libs.bug import *
from libs.tester import *
from libs.developer import *
from libs.bug_category import *
from libs.bug_type import *
from libs.phase import *
from tools.log import *

# 实例化日志对象
logger = setLogger('bug_api')


# 实例化蓝图
bug_api = Blueprint('bug', __name__, url_prefix='/bug')


@bug_api.route('/list', methods=['GET'])
def bug_list():
    return show_bug_list()


@bug_api.route('/', methods=['GET', 'POST', 'PUT', 'DELETE'], strict_slashes=False)
def bug():
    if request.method == 'GET':
        return show_bug_info()
    elif request.method == 'POST':
        return add_bug_api()
    elif request.method == 'PUT':
        return edit_bug_api()
    elif request.method == 'DELETE':
        return delete_bug_api()


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
    phase_id = request.values.get('phaseId')

    result = get_bug_list(phase_id=phase_id)

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
        'kbId': int,
        'bugTitle': string,
        'bugModel': string,
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
        logger.debug(base_info)
        if base_info:
            developer_info = get_tester_base_info(base_info['testerId'])
            tester_info = get_developer_base_info(base_info['developerId'])
            if base_info['bugCategory']:
                category = get_bug_category(base_info['bugCategory'])
            else:
                category = ''
            bug_type = get_bug_type(base_info['bugType'])
            project_info = get_project_info_with_phase(base_info['phaseId'])
            plan_info = get_plan_info_with_phase(base_info['phaseId'])

            res = {
                'bugId': base_info['bugId'],
                'kbId': base_info['kbId'],
                'bugTitle': base_info['bugTitle'],
                'bugModel': base_info['bugModel'],
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


def add_bug_api():
    """
    新增BUG
    :return:
    """
    # 接收入参
    kb_id = request.json.get('kbId')
    bug_title = request.json.get('bugTitle')
    bug_model = request.json.get('bugModel')
    bug_category = request.json.get('bugCategory')
    bug_type = request.json.get('bugType')

    create_time = request.json.get('createTime')
    close_time = request.json.get('closeTime')
    is_closed = request.json.get('isClose')
    is_online = request.json.get('inOnline')
    is_finished = request.json.get('isFinish')

    phase_id = request.json.get('phaseId')
    developer_id = request.json.get('developerId')
    tester_id = request.json.get('testerId')

    # 唯一性判断
    if check_bug_with_kb_id(kb_id):
        res = {'msg': '该缺陷已存在', 'status': 2001}
    else:
        status = add_bug(tester_id, developer_id, phase_id, bug_type, bug_category, kb_id, bug_title, bug_model,
                         create_time, close_time, is_finished, is_closed, is_online)
        if status:
            res = {'msg': '成功', 'status': 1}
        else:
            res = {'msg': '系统错误', 'status': 500}

    return json.dumps(res, ensure_ascii=False)


def edit_bug_api():
    """
    编辑BUG
    :return:
    """
    # 接收入参
    kb_id = request.json.get('kbId')
    bug_title = request.json.get('bugTitle')
    bug_model = request.json.get('bugModel')
    bug_category = request.json.get('bugCategory')
    bug_type = request.json.get('bugType')

    create_time = request.json.get('createTime')
    close_time = request.json.get('closeTime')
    is_closed = request.json.get('isClose')
    is_online = request.json.get('inOnline')
    is_finished = request.json.get('isFinish')

    phase_id = request.json.get('phaseId')
    developer_id = request.json.get('developerId')
    tester_id = request.json.get('testerId')

    # 唯一性判断
    if check_bug_with_kb_id(kb_id):
        status = edit_bug(tester_id, developer_id, phase_id, bug_type, bug_category, kb_id, bug_title, bug_model,
                          create_time, close_time, is_finished, is_closed, is_online)
        if status:
            res = {'msg': '成功', 'status': 1}
        else:
            res = {'msg': '系统错误', 'status': 500}
    else:
        res = {'msg': '该缺陷不存在', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)


def delete_bug_api():
    """
    删除BUG
    :return:
    """
    # 接收入参
    bug_id = int(request.values.get('bugId'))

    # 存在性判断
    if check_bug_with_id(bug_id):
        status = delete_bug_with_id(bug_id)
        if status:
            res = {'msg': '成功', 'status': 1}
        else:
            res = {'msg': '系统错误', 'status': 500}
    else:
        res = {'msg': '该缺陷不存在', 'status': 2001}

    return json.dumps(res, ensure_ascii=False)
