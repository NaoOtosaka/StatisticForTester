from tools.database import db
from tools.log import *

# 实例化日志对象
logger = setLogger('platform_tag')


def add_platform_tag(project_id, tag_name):
    """
    新增细分标签
    :param project_id:
    :param tag_name:
    :return:
    """
    sql = """
    INSERT INTO `platform_tag` ( platform_tag.project_id, platform_tag.tag_name )
    VALUES
        ( %i, '%s');
    """ % (project_id, tag_name)

    status = db(sql)
    if status:
        return 1
    else:
        return 0

