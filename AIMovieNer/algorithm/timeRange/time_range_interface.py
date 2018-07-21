"""
    抽取时间范围的接口文件
"""
import re
from datetime import datetime

from algorithm.utils.utils import pretreatment

local_time = datetime.now()


def extract_year(input_sentence):
    """
    抽取年份，返回4位数字或空
    :param input_sentence:
    :return:
    """
    year = re.search('\d{2}年', input_sentence).group(0)
    if year:
        return '20' + year[0:2]
    if input_sentence.find('前年'):
        return local_time.year - 2
    if input_sentence.find('去年'):
        return local_time.year - 1
    if input_sentence.find('今年'):
        return local_time.year
    return ''


def extract_month(input_sentence):
    """
    抽取年份，返回2位数字或空
    :param input_sentence:
    :return:
    """
    month = re.search('\d{1,2}月', input_sentence)
    if month:
        return month[:-1]
    if input_sentence.find('上上个月'):
        return local_time.month - 2
    if input_sentence.find('上个月') or input_sentence.find('上月'):
        return local_time.month - 1
    if input_sentence.find('这个月') or input_sentence.find('本月'):
        return local_time.month
    if input_sentence.find('下个月') or input_sentence.find('下月'):
        return local_time.month + 1
    return ''


def extract_day(input_sentence):
    """
    抽取日期，返回2位数字或空
    :param input_sentence:
    :return:
    """
    day = re.search('\d{1,2}(日|号)', input_sentence)
    if day:
        return day[:-1]
    if input_sentence.find('大前'):
        return local_time.day - 3
    if input_sentence.find('前'):
        return local_time.day - 2
    if input_sentence.find('昨'):
        return local_time.day - 1
    if input_sentence.find('今'):
        return local_time.day
    if input_sentence.find('明'):
        return local_time.day + 1
    if input_sentence.find('后天'):
        return local_time.day + 2


def extract_time_range(input_sentence):
    input_sentence = pretreatment(input_sentence)
    local_year = local_time.year
    local_month = local_time.month
    local_weekday = local_time.weekday()
    local_day = local_time.day
    local_hour = local_time.hour
    local_minute = local_time.minute

    if re.search('年|月|日|天|时|分|周', input_sentence):
        return '201807140000-201807302359'
    return ''


if __name__ == '__main__':
    print(extract_time_range('我要查询昨天'))
