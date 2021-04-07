from flask import Blueprint
from flask import request
import json

from tools.log import setLogger
from tools.wordCloud import get_wordcloud_with_project

# 实例化日志对象
logger = setLogger('tools_api')

# 实例化蓝图
tools_api = Blueprint('tools', __name__, url_prefix='/tools')


@tools_api.route('/wordcloud', methods=['GET'])
def wordcloud():
    project_id = int(request.values.get('projectId'))

    return get_wordcloud_with_project(project_id)