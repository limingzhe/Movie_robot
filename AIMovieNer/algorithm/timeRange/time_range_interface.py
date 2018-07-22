"""
    抽取时间范围的接口文件
"""
import re
from datetime import datetime, timedelta
from algorithm.utils.utils import pretreatment
import calendar
now = datetime.now()


def extract_year(input_sentence):
    """
    抽取年份，返回4位数字或空
    :param input_sentence:
    :return:
    """
    year = re.search('\d{2}年', input_sentence)
    if year:
        num = year.group(0)[0:2]
        return '20' + num
    if re.search('前年', input_sentence):
        return str(now.year - 2)
    if re.search('去年', input_sentence):
        return str(now.year - 1)
    if re.search('今年', input_sentence):
        return str(now.year)
    return ''


def extract_month(input_sentence):
    """
    抽取年份，返回2位数字或空
    :param input_sentence:
    :return:
    """
    month = re.search('\d{1,2}月', input_sentence)
    if month:
        num = month.group(0)[:-1]
        return '0' + num if int(num) < 10 else num
    if re.search('上上个月', input_sentence):
        num = str(now.month - 2)
        return '0' + num if int(num) < 10 else num
    if re.search('上个月|上月', input_sentence):
        num = str(now.month - 1)
        return '0' + num if int(num) < 10 else num
    if re.search('这个月|这月|本月', input_sentence):
        num = str(now.month)
        return '0' + num if int(num) < 10 else num
    if re.search('下个月|下月', input_sentence):
        num = str(now.month + 1)
        return '0' + num if int(num) < 10 else num
    return ''


def extract_day(input_sentence):
    """
    抽取日期，返回2位数字或空
    :param input_sentence:
    :return:
    """
    day = re.search('\d{1,2}(日|号)', input_sentence)
    if day:
        num = day.group(0)[:-1]
        return '0' + num if int(num) < 10 else num
    if re.search('大前天', input_sentence):
        num = str(now.day - 3)
        return '0' + num if int(num) < 10 else num
    if re.search('前天', input_sentence):
        num = str(now.day - 2)
        return '0' + num if int(num) < 10 else num
    if re.search('昨天', input_sentence):
        num = str(now.day - 1)
        return '0' + num if int(num) < 10 else num
    if re.search('今天', input_sentence):
        num = str(now.day)
        return '0' + num if int(num) < 10 else num
    if re.search('明天', input_sentence):
        num = str(now.day + 1)
        return '0' + num if int(num) < 10 else num
    if re.search('后天', input_sentence):
        num = str(now.day + 2)
        return '0' + num if int(num) < 10 else num
    return ''


def extract_week(input_sentence):
    """
    抽取周
    :param input_sentence:
    :return:
    """
    if re.search('上周', input_sentence):
        start = str(now - timedelta(days=now.weekday()+7))
        end = str(now - timedelta(days=now.weekday()+1))
        return start[0:4] + start[5:7] + start[8:10] + '0000' + '-' + end[0:4] + end[5:7] + end[8:10] + '2359'
    if re.search('本周|这周', input_sentence):
        # 本周第一天和最后一天
        start = str(now - timedelta(days=now.weekday()))
        end = str(now + timedelta(days=6 - now.weekday()))
        return start[0:4] + start[5:7] + start[8:10] + '0000' + '-' + end[0:4] + end[5:7] + end[8:10] + '2359'
    if re.search('下周', input_sentence):
        start = str(now - timedelta(days=now.weekday() - 7))
        end = str(now + timedelta(days=now.weekday() + 1))
        return start[0:4] + start[5:7] + start[8:10] + '0000' + '-' + end[0:4] + end[5:7] + end[8:10] + '2359'
    return ''


def extract_time_range(input_sentence):
    input_sentence = pretreatment(input_sentence)
    if extract_week(input_sentence):
        return extract_week(input_sentence)

    if re.search('未观看|没看|未看', input_sentence):
        time_now = str(now)
        return time_now[0:4] + time_now[5:7] + time_now[8:10] + time_now[11:13] + time_now[14:16] + '-201809010000'

    year = extract_year(input_sentence)
    month = extract_month(input_sentence)
    day = extract_day(input_sentence)
    if year:
        if month:
            if day:
                return year + month + day + '0000' + '-' + year + month + day + '2359'
            else:
                month_range = calendar.monthrange(int(year), int(month))
                return year + month + "010000" + '-' + year + month + str(month_range[1]) + '2359'
        else:
            return year + "01010000" + '-' + year + '12312359'
    else:
        if month:
            if day:
                return str(now.year) + month + day + '0000' + '-' + str(now.year) + month + day + '2359'
            else:
                month_range = calendar.monthrange(now.year, int(month))
                return str(now.year) + month + '010000' + '-' + str(now.year) + month + str(month_range[1]) + '2359'
        else:
            if day:
                month = '0' + str(now.month) if now.month < 10 else now.month
                return str(now.year) + month + day + '0000' + '-' + str(now.year) + month + day + '2359'

    if re.search('之前|以前|已看|已观看', input_sentence):
        time_now = str(now)
        return '201801010000-' + time_now[0:4] + time_now[5:7] + time_now[8:10] + time_now[11:13] + time_now[14:16]

    return ''


if __name__ == '__main__':
    print(extract_time_range('以前'))
