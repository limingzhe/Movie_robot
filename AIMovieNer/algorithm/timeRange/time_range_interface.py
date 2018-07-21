"""
    抽取时间范围的接口文件
"""
import re

from algorithm.utils.utils import pretreatment


def extract_time_range(input_sentence):
    input_sentence = pretreatment(input_sentence)
    if re.search('年|月|日|天|时|分|周', input_sentence):
        return '201807140000-201807302359'
    return ''


if __name__ == '__main__':
    print(extract_time_range('我要查询昨天'))
