from tools.timeDeal import *

import logging
import config



def setLogger(log_name):
    """
    实例化日志对象
    :param log_name:
    :return:
    """
    # 初始化log实例
    logger = logging.getLogger(log_name)

    # 设定输出等级
    logger.setLevel(config.CONF.LOG_LEVEL)

    # 设置输出日志格式
    formatter = logging.Formatter(
        fmt="%(asctime)s %(name)s %(filename)s %(message)s",
        datefmt="%Y/%m/%d %X"
    )

    # 设定输出文件名
    timestamp = get_today_timestamp()
    log_file_name = str(timestamp) + '.log'

    # 创建handler
    fh = logging.FileHandler(config.CONF.LOG_PATH + log_file_name, encoding="utf-8")
    ch = logging.StreamHandler()

    # 为handler指定输出格式
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    # 添加handler处理器
    logger.addHandler(fh)
    logger.addHandler(ch)

    return logger


if __name__ == '__main__':
    logger = setLogger('test')
    logger.info('测试信息')