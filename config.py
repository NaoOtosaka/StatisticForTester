import sys


class Config(object):
    # 工作区初始化
    workPath = sys.path[1]

    # 数据库路径配置
    DB_HOST = workPath + '/database/data.db'
    # 是否启动外键约束
    USE_FOREIGN = True

    API_VERSION = 'v1'


class DevelopmentConfig(Config):
    DEBUG = True

    API_HOST = '0.0.0.0'
    API_PORT = 9222


class ProjectionConfig(Config):
    DEBUG = False


# 开发配置
CONF = DevelopmentConfig

# 生产配置
# CONF = ProjectionConfig
