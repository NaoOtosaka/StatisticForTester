from flask import Flask
from flask_cors import CORS

from config import CONF
from app.manager import api_v1


def setup(flask_server):
    """
    设置启动
    :param flask_server:
    :return:
    """
    # 跨域处理
    CORS(server, supports_credentials=True)

    # 注册API蓝图
    server.register_blueprint(api_v1)

    # 启动参数
    flask_server.run(port=CONF.API_PORT, debug=CONF.DEBUG, host=CONF.API_HOST)


if __name__ == '__main__':
    server = Flask(__name__)

    setup(server)
