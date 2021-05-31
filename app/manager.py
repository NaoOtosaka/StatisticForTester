from common.NestableBlueprint import NestableBlueprint
from app.v1 import Project, Tester, Developer, Bug, Files, Planner, Tools, Log


def resign_blueprint(flask_server):
    """
    注册子功能蓝图
    :param flask_server:
    :return:
    """
    flask_server.register_blueprint(Project.project_api)
    flask_server.register_blueprint(Tester.tester_api)
    flask_server.register_blueprint(Developer.developer_api)
    flask_server.register_blueprint(Bug.bug_api)
    flask_server.register_blueprint(Files.files_api)
    flask_server.register_blueprint(Planner.planner_api)
    flask_server.register_blueprint(Tools.tools_api)
    flask_server.register_blueprint(Log.log_api)


# 实例化API二级蓝图
api_v1 = NestableBlueprint('api_v1', __name__, url_prefix='/api/v1')

resign_blueprint(api_v1)
