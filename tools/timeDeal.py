import time


def get_today_timestamp():
    """
    获取当日时间戳
    :return:
    """
    now_time = int(time.time())
    day_timestamp = now_time - now_time % 86400 + time.timezone
    return day_timestamp


if __name__ == '__main__':
    get_today_timestamp()