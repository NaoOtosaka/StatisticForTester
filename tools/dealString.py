def is_chinese(uchar):
    if '\u4e00' <= uchar <= '\u9fa5':
        return True
    else:
        return False


def reserve_chinese(content):
    content_str = ''
    for i in content:
        if is_chinese(i):
            content_str += i
    return content_str