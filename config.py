import sys


class Config(object):
    # 工作区初始化
    workPath = sys.path[1]

    # 数据库路径配置
    DB_HOST = workPath + '/database/data.db'

    # 是否启动外键约束
    USE_FOREIGN = True

    # 数据库缓存分页大小
    CACHE_SIZE = 8000

    # API版本
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
            "线上异常": 12,
        }
        bug_type = {
            "前端BUG": 1,
            "服务端BUG": 2,
            "Android BUG": 3,
            "iOS BUG": 4,
            "前端开发": 5,
            "服务端开发": 6,
            "Android开发": 7,
            "iOS开发": 8
        }
        bug_category = {
            "未选定": 1,
            "需求缺失": 2,
            "功能缺失": 3,
            "功能阻塞": 4,
            "环境异常": 5,
            "用例缺失": 6,
            "兼容性异常": 7,
            "部署异常": 8,
            "功能异常": 9
        }
        develop_project = [
            '游戏学院-开发',
            'KM-平台开发'
        ]
        prod_project = [
            '游戏学院-缺陷',
            'KM-缺陷跟踪'
        ]


class DevelopmentConfig(Config):
    # API调试模式
    DEBUG = True

    # 日志路径配置
    LOG_PATH = Config.workPath + '\\log\\'

    # 日志输出等级
    LOG_LEVEL = 'DEBUG'

    # 主机配置
    API_HOST = '0.0.0.0'
    API_PORT = 9222

    # 文件解析编码配置
    ENCODING = 'utf-8'

    # 文件路径配置
    FILES_PATH = Config.workPath + '\\file\\'


class ProjectionConfig(Config):
    # API调试模式
    DEBUG = False

    # 工作区配置
    workPath = '/Users/pijingwen/PycharmProjects/qa-dbstatistics'

    # 日志输出等级
    LOG_LEVEL = 'WARNING'

    # 日志路径配置
    LOG_PATH = workPath + '/log/'

    # 数据库路径配置
    DB_HOST = workPath + '/database/data.db'

    # 主机配置
    API_HOST = '0.0.0.0'
    API_PORT = 9222

    # 文件解析编码配置
    ENCODING = 'gbk'

    # 文件路径配置
    FILES_PATH = workPath + '/file/'


# 开发配置
CONF = DevelopmentConfig

# 生产配置
# CONF = ProjectionConfig
