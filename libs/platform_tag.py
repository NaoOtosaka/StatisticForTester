from tools.database import db
from tools.log import *

# 实例化日志对象
logger = setLogger('platform_tag')


def check_platform_tag_with_id(tag_id):
    """
    根据标签ID检查存在性
    :param tag_id:
    :return:
    """
    sql = """
    SELECT
    1
    FROM
    platform_tag
    WHERE
    tag_id=%i
    LIMIT 1;
    """ % tag_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def get_tag_info_with_id(tag_id):
    """
    根据tag ID获取对应tag信息
    :param tag_id:
    :return:
    """
    sql = """
    SELECT
    platform_tag.tag_name
    FROM
    platform_tag
    WHERE
    platform_tag.tag_id = %i
    """ % tag_id

    result = db(sql)
    if result:
        logger.debug(result)
        return result[0][0]
    else:
        return 0


def get_platform_tag_with_project_id(project_id):
    """
    根据项目id获取对应tag列表
    :param project_id:
    :return:
    """
    sql = """
    SELECT
    platform_tag.tag_id,
    platform_tag.tag_name
    FROM
    platform_tag
    WHERE
    platform_tag.project_id=%i;
    """ % project_id

    temp = []

    result = db(sql)
    if result:
        logger.debug(result)

        for i in range(len(result)):
            temp.append(
                {
                    'tagId': result[i][0],
                    'tagName': result[i][1]
                }
            )

        return temp
    else:
        return []


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


def edit_platform_tag(tag_id, tag_name):
    """
    编辑细分标签内容
    :param tag_id:
    :param tag_name:
    :return:
    """
    sql = """
    UPDATE platform_tag 
    SET
    platform_tag.tag_name='%s'
    WHERE 
    platform_tag.tag_id=%i
    """ % (tag_name, tag_id)

    status = db(sql)
    if status:
        return 1
    else:
        return 0


def delete_platform_tag(tag_id):
    """
    删除测试阶段细分记录
    :param tag_id:
    :return:
    """
    sql = """
    DELETE 
    FROM
        platform_tag 
    WHERE
        tag_id = '%i';
    """ % tag_id

    status = db(sql)
    if status:
        return 1
    else:
        return 0


if __name__ == '__main__':
    print(check_platform_tag_with_id(1))
    print(get_platform_tag_with_project_id(2))