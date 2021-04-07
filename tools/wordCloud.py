from wordcloud import WordCloud
import base64
import io

from config import CONF
from tools.database import db


def get_model_data(project_id=None):
    """
    获取异常分类模块数据
    :return:
    """
    sql = """
    SELECT
    bug.model
    FROM
    bug
    INNER JOIN project_phases ON bug.phase_id = project_phases.phase_id
    INNER JOIN project ON project_phases.project_id = project.project_id
    """

    if project_id:
        sql += "WHERE project.project_id = %i" % project_id

    temp = []

    result = db(sql)
    if result:
        for value in result:
            if "-" in value[0]:
                list_temp = value[0].split('-')
                temp.append(list_temp[1:])

    return temp


def trans_CN(text):
    temp = ""
    for item in text:
        temp += item[0] + " "

    return temp


def get_wordcloud_with_project(project_id=None):
    """
    获取词云
    :return:
    """
    font = CONF.TTF_PATH + 'msyh.ttc'
    # pil_img = WordCloud(width=500, height=500, font_path=font).generate(text=text).to_image()

    str_list = get_model_data(project_id)

    text = trans_CN(str_list)

    pil_img = WordCloud(
        font_path=font,
        width=800,
        height=300,
        background_color="white",
        prefer_horizontal=0.6).generate(text=text).to_image()
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()
    # print(img_base64)
    return img_base64


if __name__ == '__main__':
    get_wordcloud_with_project(2)

