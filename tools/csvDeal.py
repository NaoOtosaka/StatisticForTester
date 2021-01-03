from tools.dealString import *
from libs.tester import *
from libs.developer import *
from libs.project import *
from libs.phase import *
from libs.bug import *
import pandas
import config
import time


def open_csv():
    with open('../file/export.csv')as f:
        f_csv = pandas.read_csv(f, encoding='utf-8', header=0, index_col=0)
        # print(f_csv['#', '跟踪标签', '主题', '状态', '作者', '指派给', '创建于', '跟进QA'])
        print(type(f_csv))
        return f_csv


def process_data(csv_object):
    """
    基础数据提取
    :return:
    """
    bug_data = []
    # 数据遍历
    for index, data in csv_object.iterrows():
        # 看板id
        kb_id = index

        # 标题源数据处理
        title_info = process_title(data['主题'])

        # BUG标题
        title = title_info[len(title_info) - 1]

        # BUG模块
        if len(title_info) == 5:
            model = title_info[1] + '-' + title_info[3]
        else:
            model = title_info[1]

        # 项目阶段处理
        phase_id = get_phase_info(title_info[0], title_info[2])

        # 测试人员
        tester = reserve_chinese(data['跟进QA'])
        tester_id = process_tester(tester)

        # 开发人员
        developer = reserve_chinese(data['指派给'])
        developer_id = process_developer(developer)

        # BUG标签
        bug_type = process_bug_type(data['跟踪标签'])

        # BUG类型
        category = 'NULL'

        # 创建时间
        create_time = process_time(data['创建于'])

        # 关闭时间
        if pandas.isnull(data['关闭日期']):
            is_close = False
            close_time = ''
        else:
            is_close = True
            close_time = process_time(data['完成日期'])

        # 完成判定
        if data['% 完成'] == 100:
            is_finish = True
        else:
            is_finish = False

        bug_data.append(get_bug_info(tester_id, developer_id, phase_id, bug_type, category, kb_id, title, model,
                                     create_time, close_time, is_finish, is_close, False))

    return bug_data


def process_title(title):
    """
    标题信息处理
    :type title str
    :param title:
    :return:
    """
    title_info = title.split('-')
    return title_info


def process_bug_type(bug_type):
    """
    BUG类型操作
    :param bug_type:
    :return:
    """
    if bug_type in config.Config.BaseData.bug_type:
        type_id = config.Config.BaseData.bug_type[bug_type]
        return type_id
    else:
        print('字段异常')


def get_phase_info(project, plan):
    """
    根据项目名与计划获取对应项目阶段id
    :param project:
    :param plan:
    :return:
    """
    project_id = int(process_project(project))
    plan_id = int(process_plan(plan))

    temp = get_plan_with_project_and_plan(project_id, plan_id)
    if temp:
        return temp[0]
    else:
        if add_phase(project_id, plan_id):
            return get_phase_insert_id()
        else:
            return False


def process_project(project):
    """
    项目名称操作
    :param project:
    :return:
    """
    # 测试用默认参数
    planner = 1

    print(project)

    project_id = check_project_with_name(project)
    # 项目不存在则创建
    if not project_id:
        add_project(planner, project)
        project_id = get_project_insert_id()
    return project_id


def process_plan(plan):
    """
    测试计划操作
    :param plan:
    :return:
    """
    if plan in config.Config.BaseData.plan:
        plan_id = config.Config.BaseData.plan[plan]
        return plan_id
    else:
        print('字段异常')


def process_tester(tester):
    """
    测试人员处理
    :param tester:
    :return:
    """
    # 测试用置空
    tester_email = ''

    tester_id = check_tester_with_name(tester)
    if not tester_id:
        add_tester(tester, tester_email)
        tester_id = get_tester_insert_id()
    return tester_id


def process_developer(developer):
    """
    开发人员处理
    :param developer:
    :return:
    """
    # 测试用置空
    developer_email = ''

    developer_id = check_developer_with_name(developer)
    if not developer_id:
        add_developer(developer, developer_email)
        developer_id = get_developer_insert_id()
    return developer_id


def process_time(time_str):
    """
    csv时间字符串转时间戳
    :param time_str:
    :return:
    """
    time_array = time.strptime(time_str, "%Y/%m/%d %H:%M")
    timestamp = int(time.mktime(time_array))
    print(timestamp)
    return timestamp


def get_bug_info(tester_id, developer_id, phase_id, bug_type, category, kb_id, title, model, create_time, close_time,
                 is_finish, is_close, is_online):
    """
    数据整合
    :return:
    """
    temp = [
        tester_id,
        developer_id,
        phase_id,
        bug_type,
        category,
        kb_id,
        title,
        model,
        create_time,
        close_time,
        is_finish,
        is_close,
        is_online,
    ]
    return temp


def insert_bug_info(bug_info):
    """
    添加Bug
    :param bug_info:
    :return:
    """
    if not check_bug_with_kb_id(bug_info[5]):
        add_bug(
            bug_info[0],
            bug_info[1],
            bug_info[2],
            bug_info[3],
            bug_info[4],
            bug_info[5],
            bug_info[6],
            bug_info[7],
            bug_info[8],
            bug_info[9],
            bug_info[10],
            bug_info[11],
            bug_info[12]
        )
    else:
        print("BUG已存在")


def main():
    csv_object = open_csv()
    bug_data = process_data(csv_object)
    for data in bug_data:
        print(data)
        insert_bug_info(data)


if __name__ == '__main__':
    main()