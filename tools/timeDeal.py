import time


def get_today_timestamp():
    """
    获取当日时间戳
    :return:
    """
    now_time = int(time.time())
    day_timestamp = now_time - now_time % 86400 + time.timezone
    return day_timestamp


def get_format_str(timestamp):
    """
    获取指定格式时间字符串
    :param timestamp:
    :return:
    """
    timeArray = time.localtime(timestamp)
    otherStyleTime = time.strftime("%Y-%m-%d", timeArray)

    return otherStyleTime


if __name__ == '__main__':
    get_today_timestamp()