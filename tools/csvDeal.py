from tools.dealString import *
import pandas


def open_csv():
    with open('../file/export.csv')as f:
        f_csv = pandas.read_csv(f, encoding='utf-8', header=0, index_col=0)
        # print(f_csv['#', '跟踪标签', '主题', '状态', '作者', '指派给', '创建于', '跟进QA'])
        print(type(f_csv))
        deal_data(f_csv)


def deal_data(csv_object):
    """
    基础数据提取
    :return:
    """
    # 数据遍历
    for index, data in csv_object.iterrows():
        bug_id = index
        title_info = deal_title(data['主题'])
        project = title_info[0]
        plan = title_info[2]
        if len(title_info) == 5:
            model = title_info[1] + '-' + title_info[3]
            title = title_info[4]
        else:
            model = title_info[1]
            title = title_info[3]

        tester = reserve_chinese(data['跟进QA'])
        developer = reserve_chinese(data['指派给'])
        bug_type = data['跟踪标签']
        category = model
        create_time = data['创建于']
        if pandas.isnull(data['关闭日期']):
            is_close = False
        else:
            is_close = True
        if data['% 完成'] == 100:
            is_finish = True
        else:
            is_finish = False

        print(get_bug_info(bug_id, tester, developer, False, bug_type, category, title, create_time, is_finish, is_close, False))


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


def deal_title(title):
    """
    :type title str
    :param title:
    :return:
    """
    title_info = title.split('-')
    return title_info


if __name__ == '__main__':
    open_csv()