from flask import Blueprint
from flask import request
import json
import os

from tools.csvDeal import *

# 实例化蓝图
files_api = Blueprint('files', __name__, url_prefix='/files')


@files_api.route('/upload', methods=['POST'])
def upload_csv():
    """
    上传易协作导出csv
    :return:
    """
    file_obj = request.files['csvFile']
    print(file_obj)
    if file_obj:
        timestamp = int(round(time.time() * 1000))
        file_name = 'yxz-' + str(timestamp) + '.csv'
        print(file_obj)
        path = os.path.join(config.CONF.FILES_PATH, file_name)
        print(type(path))
        file_obj.save(path)
        try:
            api_main(path)
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