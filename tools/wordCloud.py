from wordcloud import WordCloud
import base64
import io

from config import CONF
from libs.bug import get_model_data_with_project


def count_model(str_list):
    str_set = set(str_list)

    count_data = {}

    for item in str_set:
        count_data[item] = str_list.count(item)
    temp = sorted(count_data.items(), key=lambda kv: (kv[1], kv[0]), reverse=True)
    print(temp)


def get_wordcloud_with_project(project_id=None):
    """
    获取词云
    :return:
    """
    # 字体文件路径
    font = CONF.TTF_PATH + 'msyh.ttc'

    # 源数据处理(模块名称)
    str_list = get_model_data_with_project(project_id)

    # 分词
    text = ""
    for item in str_list:
        text += item + " "

    # 生成词云
    pil_img = WordCloud(
        font_path=font,
        width=800,
        height=300,
        background_color="white",
        prefer_horizontal=0.6,
        collocations=False).generate(text=text).to_image()

    # base64输出
    img = io.BytesIO()
    pil_img.save(img, "PNG")
    img.seek(0)
    img_base64 = base64.b64encode(img.getvalue()).decode()

    return img_base64


if __name__ == '__main__':
    get_wordcloud_with_project(2)

