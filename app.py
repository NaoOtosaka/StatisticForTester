from flask import Flask
from flask_cors import CORS

from app.v1 import Project, Tester


def resign_blueprint(flask_server):
    """
    注册蓝图
    :param flask_server:
    :return:
    """
    flask_server.register_blueprint(Project.project_api)
    flask_server.register_blueprint(Tester.tester_api)


def setup(flask_server):
    """
    设置启动参数
    :param flask_server:
    :return:
    """
    flask_server.run(port=9222, debug=True, host="0.0.0.0")


if __name__ == '__main__':
    server = Flask(__name__)
    CORS(server, supports_credentials=True)

    resign_blueprint(server)

    setup(server)