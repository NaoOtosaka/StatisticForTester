from tools.dealString import *
from libs.tester import *
from libs.developer import *
from libs.project import *
from libs.phase import *
from libs.bug import *
import pandas
import tkinter
from tkinter import filedialog
from tools.log import *
from config import CONF

# 实例化日志对象
logger = setLogger('csvDeal')


def choose_file():
    """
    选择文件
    :return:
    """
    windows = tkinter.Tk()
    windows.withdraw()
    # 选择文件
    file_path = filedialog.askopenfilename()

    if file_path:
        # 打印文件路径
        logger.info('Filepath:' + file_path)
        return file_path
    else:
        print('未选择目录')
        return False


def open_csv(file_name):
    if file_name:
        with open(file_name)as f:
            f_csv = pandas.read_csv(f, encoding='utf-8', header=0, index_col=0)
            # print(f_csv['#', '跟踪标签', '主题', '状态', '作者', '指派给', '创建于', '跟进QA'])
            return f_csv
    else:
        return False


def process_data(csv_object):
    """
    基础数据提取
    :return:
    """
    bug_data = []
    # 数据遍历
    for index, data in csv_object.iterrows():

        if 'BUG' in data['跟踪标签'] or '开发' in data['跟踪标签']:
            # 看板id
            kb_id = index

            # 标题源数据处理
            title_info = process_title(data['主题'], kb_id)

            if title_info:
                # BUG标题
                title = title_info[-1]

                # BUG模块
                model = process_model(title_info)

                # 项目阶段处理
                phase_id = get_phase_info(title_info[0], title_info[2])

                # 测试人员
                tester_id = process_tester(reserve_chinese(data['跟进QA']))

                # 开发人员
                developer_id = process_developer(reserve_chinese(data['指派给']))

                # BUG标签
                bug_type = process_bug_type(data['跟踪标签'])

                # BUG类型
                bug_category = process_bug_category(data['跟踪标签'])

                # 创建时间
                create_time = process_time(data['创建于'])

                # 关闭时间
                if pandas.isnull(data['关闭日期']) or pandas.isnull(data['完成日期']):
                    is_close = False
                    close_time = 0
                else:
                    is_close = True
                    close_time = process_close_time(data['完成日期'])

                # 完成判定
                if data['% 完成'] == 100:
                    is_finish = True
                else:
                    is_finish = False

                # 是否为线上异常
                if data['项目'] in CONF.BaseData.develop_project:
                    is_online = False
                elif data['项目'] in CONF.BaseData.prod_project:
                    is_online = True
                else:
                    is_online = False

                bug_data.append(get_bug_info(tester_id, developer_id, phase_id, bug_type, bug_category, kb_id, title, model,
                                             create_time, close_time, is_finish, is_close, is_online))
            else:
                continue

        else:
            continue

    return bug_data


def get_phase_info(project, plan):
    """
    根据项目名与计划获取对应项目阶段id
    :param project:
    :param plan:
    :return:
    """
    logger.debug(plan)

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


def process_title(title, kb_id):
    """
    标题信息处理
    :param kb_id:
    :type title str
    :param title:
    :return:
    """
    """
    单名适配规则：
    {项目名}-{细分平台}-{测试阶段}-{BUG所属一级模块[-{BUG所属二级模块}]}-{问题标题}[-{F}]
    -例：
    正常单：MG大赛直播竞猜抽奖-WEB-一轮测试-投票-投票数据异常
    废弃单：MG大赛直播竞猜抽奖-WEB-一轮测试-投票-投票数据异常-F
    """
    if title.startswith("-"):
        title_info = title[1:].split('-')
        title_info[0] = '-' + title_info[0]
    else:
        title_info = title.split('-')

    if not title_info[-1] == 'F':
        logger.info(title_info)
        return title_info
    else:
        # 当存在-F后缀时,检测BUG是否已入库,若已入库则删除对应BUG
        bug_status = check_bug_with_kb_id(kb_id)
        if bug_status:
            delete_bug_with_kb_id(kb_id)

        return False


def process_model(title_info):
    """
    提取头数组中模块信息
    :type title_info list
    :param title_info:
    :return:
    """
    # 细分平台
    model = title_info[1]

    for i in range(3, len(title_info) - 1):
        model += '-' + title_info[i]

    return model


def process_bug_type(bug_type):
    """
    BUG类型操作
    :param bug_type:
    :return:
    """
    if bug_type in CONF.BaseData.bug_type:
        type_id = CONF.BaseData.bug_type[bug_type]
        return type_id
    else:
        logger.error('字段异常')


def process_bug_category(bug_category):
    """
    BUG分类操作
    :param bug_category:
    :return:
    """
    if "开发" in bug_category:
        category = CONF.BaseData.bug_category['需求缺失']
    else:
        category = CONF.BaseData.bug_category['未选定']

    return category


def process_project(project):
    """
    项目名称操作
    :param project:
    :return:
    """
    # 测试用默认参数
    planner = 1

    logger.debug(project)

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
    if plan in CONF.BaseData.plan:
        plan_id = CONF.BaseData.plan[plan]
        return plan_id
    else:
        logger.error('系统异常')


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
    logger.debug(time_str)
    time_array = time.strptime(time_str, "%Y-%m-%d %H:%M")
    timestamp = int(time.mktime(time_array))
    logger.info(timestamp)
    return timestamp


def process_close_time(time_str):
    """
    csv时间字符串转时间戳
    :param time_str:
    :return:
    """
    logger.debug(time_str)
    time_array = time.strptime(time_str, "%Y-%m-%d")
    timestamp = int(time.mktime(time_array))
    logger.info(timestamp)
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
        edit_bug(
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
        logger.warning("BUG已更新")


def local_main():
    """
    本地运行主逻辑
    :return:
    """
    file_name = choose_file()
    if file_name:
        csv_object = open_csv(file_name)
        bug_data = process_data(csv_object)
        for data in bug_data:
            insert_bug_info(data)


def api_main(file_name):
    """
    API主逻辑
    :param file_name 文件路径
    :return:
    """
    csv_object = open_csv(file_name)
    bug_data = process_data(csv_object)
    for data in bug_data:
        insert_bug_info(data)


if __name__ == '__main__':
    local_main()