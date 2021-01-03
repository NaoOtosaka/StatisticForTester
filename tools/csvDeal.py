from tools.dealString import *
from libs.tester import *
from libs.developer import *
from libs.project import *
from libs.phase import *
import pandas
import config


def open_csv():
    with open('../file/export.csv')as f:
        f_csv = pandas.read_csv(f, encoding='utf-8', header=0, index_col=0)
        # print(f_csv['#', '跟踪标签', '主题', '状态', '作者', '指派给', '创建于', '跟进QA'])
        print(type(f_csv))
        process_data(f_csv)


def process_data(csv_object):
    """
    基础数据提取
    :return:
    """
    # 数据遍历
    for index, data in csv_object.iterrows():
        # 看板id
        bug_id = index

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

        # 开发人员
        developer = reserve_chinese(data['指派给'])

        # BUG标签
        bug_type = data['跟踪标签']

        # BUG类型
        category = ''

        # 创建时间
        create_time = data['创建于']

        # 关闭时间
        if pandas.isnull(data['关闭日期']):
            is_close = False
        else:
            is_close = True

        # 完成判定
        if data['% 完成'] == 100:
            is_finish = True
        else:
            is_finish = False

        print(get_bug_info(bug_id, phase_id, tester, developer, model, bug_type, category, title, create_time, is_finish, is_close, False))


def process_title(title):
    """
    标题信息处理
    :type title str
    :param title:
    :return:
    """
    title_info = title.split('-')
    return title_info


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


def get_bug_info(bug_id, tester, developer, phase, bug_type, category, title, create_time, is_finish, is_close, is_online):
    """
    数据封装
    :return:
    """
    temp = [
        bug_id,
        tester,
        developer,
        phase,
        bug_type,
        category,
        title,
        create_time,
        is_finish,
        is_close,
        is_online,
    ]
    return temp


def insert_bug_info():
    pass


if __name__ == '__main__':
    open_csv()
    # check_tester_with_name('QA侧测试3')
    # check_developer_with_name('开发侧测试1')
    # project_id = check_project_with_name('测试用项目1')
    # print(get_plan_with_project_id(project_id))