import sys


class Config(object):
    # 工作区初始化
    workPath = sys.path[1]

    # 数据库路径配置
    DB_HOST = workPath + '/database/data.db'
    # 是否启动外键约束
    USE_FOREIGN = True

    API_VERSION = 'v1'

    class BaseData(object):
        plan = {
            "冒烟测试": 1,
            "冒烟复核": 2,
            "一轮测试": 3,
            "二轮测试": 4,
            "兼容性测试": 5,
            "弱网测试": 6,
            "压力测试": 7,
            "灵敏度测试": 8,
            "性能测试": 9,
            "单元测试": 10,
            "回归测试": 11,
            "线上验收": 12,
        }
        bug_type = {
            "前端BUG": 1,
            "服务端BUG": 2,
            "Android BUG": 3,
            "IOS BUG": 4,
        }


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
