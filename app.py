from flask import Flask
from flask_cors import CORS

from config import CONF
from app.manager import api_v1
from gevent import pywsgi


def setup(flask_server, debug):
    """
    设置启动
    :param debug:
    :param flask_server:
    :return:
    """
    # 跨域处理
    CORS(flask_server, supports_credentials=True)

    # 注册API蓝图
    flask_server.register_blueprint(api_v1)

    if debug:
        # 启动参数
        flask_server.run(port=CONF.API_PORT, debug=CONF.DEBUG, host=CONF.API_HOST)
    else:
        server = pywsgi.WSGIServer((CONF.API_HOST, CONF.API_PORT), flask_server)
        server.serve_forever()


if __name__ == '__main__':
    app = Flask(__name__)

    setup(app, CONF.DEBUG)