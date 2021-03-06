from flask import Blueprint
from flask import request
import threading
import random
import string
import json
import os

from tools.csvDeal import *
from tools.log import *

# 实例化日志对象
logger = setLogger('files_api')


# 实例化蓝图
files_api = Blueprint('files', __name__, url_prefix='/files')

# 初始化锁
project_lock = threading.Lock()


@files_api.route('/upload', methods=['POST'])
def upload_csv():
    """
    上传易协作导出csv
    :return:
    """
    file_obj = request.files['csvFile']
    logger.debug(file_obj)
    if file_obj:
        timestamp = int(round(time.time() * 1000))
        ran_str = ''.join(random.sample(string.ascii_letters + string.digits, 5))
        file_name = 'yxz-' + str(timestamp) + ran_str + '.csv'
        logger.debug(file_obj)
        path = os.path.join(CONF.FILES_PATH, file_name)
        logger.debug(type(path))
        file_obj.save(path)
        try:
            api_main(path, project_lock)
            res = {
                'msg': "成功",
                'status': 1
            }
        except:
            res = {
                'msg': "文件异常",
                'status': 4001
            }
    else:
        res = {
            'msg': "系统错误",
            'status': 4001
        }

    return json.dumps(res, ensure_ascii=False)