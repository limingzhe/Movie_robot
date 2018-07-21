"""
    将中文转化为阿拉伯数字
"""
import re

# constants for chinese_to_arabic
CN_NUM = {
    '一': 1, '二': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9, '零': 0, '两': 2,
}

CN_UNIT = {
    '十': 10,
    '百': 100,
    '千': 1000,
    '万': 10000,
    '亿': 100000000,
}


def chinese2digits(cn: str) -> int:
    unit = 0  # current
    ldig = []  # digest
    for cndig in reversed(cn):
        if cndig in CN_UNIT:
            unit = CN_UNIT.get(cndig)
            if unit == 10000 or unit == 100000000:
                ldig.append(unit)
                unit = 1
        else:
            dig = CN_NUM.get(cndig)
            if unit:
                dig *= unit
                unit = 0
            ldig.append(dig)
    if unit == 10:
        ldig.append(10)
    val, tmp = 0, 0
    for x in reversed(ldig):
        if x == 10000 or x == 100000000:
            val += tmp * x
            tmp = 0
        else:
            tmp += x
    val += tmp
    return val


num_str_start_symbol = ['一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十']
more_num_str_symbol = ['零', '一', '二', '两', '三', '四', '五', '六', '七', '八', '九', '十', '百', '千', '万', '亿']


def change_chinese_num_to_arab(origin_string):
    # 先将阿拉伯数字转换为中文
    arab_list = re.findall('[0-9]+', origin_string)
    if arab_list:
        for val in arab_list:
            after_change = change_arab_to_num(val)
            origin_string = origin_string.replace(val, after_change)

    len_str = len(origin_string)
    a_pro_str = ''
    if len_str == 0:
        return a_pro_str

    has_num_start = False
    number_str = ''
    for idx in range(len_str):
        if origin_string[idx] in num_str_start_symbol:
            if not has_num_start:
                has_num_start = True

            number_str += origin_string[idx]
        else:
            if has_num_start:
                if origin_string[idx] in more_num_str_symbol:
                    number_str += origin_string[idx]
                    continue
                else:
                    num_result = str(chinese2digits(completion(number_str)))
                    number_str = ''
                    has_num_start = False
                    a_pro_str += num_result

            a_pro_str += origin_string[idx]
            pass

    if len(number_str) > 0:
        result_num = chinese2digits(completion(number_str))
        a_pro_str += str(result_num)

    return a_pro_str


def completion(number_str):
    """
    补全，如“二百五”补全为“二百五十”
    :param number_str:
    :return:
    """
    units_digits = ['一', '二', '三', '四', '五', '六', '七', '八', '九']
    if len(number_str) < 3 or number_str[-1] not in units_digits:
        return number_str
    completion_dict = {'百': '十', '千': '百', '万': '千'}
    for key in completion_dict:
        if key == number_str[-2]:
            number_str += completion_dict[key]
    return number_str


unitArab = (2, 3, 4, 5, 9)
unitStr = '十百千万亿'
# 单位字典unitDic,例如(2,'十')表示给定的字符是两位数,那么返回的结果里面定会包含'十'.3,4,5,9以此类推.
unitDic = dict(zip(unitArab, unitStr))

numArab = '0123456789'
numStr = '零一二三四五六七八九'
# 数值字典numDic,和阿拉伯数字是简单的一一对应关系
numDic = dict(zip(numArab, numStr))


def change_arab_to_num(s):
    def wrapper(v):
        """
        针对多位连续0的简写规则设计的函数
        例如"壹佰零零"会变为"壹佰","壹仟零零壹"会变为"壹仟零壹"
        """
        if '零零' in v:
            return wrapper(v.replace('零零', '零'))
        return v[:-1] if v[-1] == '零' else v

    def recur(s, bit):
        """
        :param s: 纯数字字符串
        :param bit: 字符串的长度,相当于位数
        :return:
        """
        # 如果是一位数,则直接按numDic返回对应汉字
        if bit == 1:
            return numDic[s]
        # 否则,且第一个字符是0,那么省略"单位"字符,返回"零"和剩余字符的递归字符串
        if s[0] == '0':
            return wrapper('%s%s' % ('零', recur(s[1:], bit - 1)))
        # 否则,如果是2,3,4,5,9位数,那么返回最高位数的字符串"数值"+"单位"+"剩余字符的递归字符串"
        if bit < 6 or bit == 9:
            return wrapper('%s%s%s' % (numDic[s[0]], unitDic[bit], recur(s[1:], bit - 1)))
        # 否则,如果是6,7,8位数,那么用"万"将字符串从万位数划分为2个部分.
        # 例如123456就变成:12+"万"+3456,再对两个部分进行递归.
        if bit < 9:
            return '%s%s%s' % (recur(s[:-4], bit - 4), "万", recur(s[-4:], 4))
        # 否则(即10位数及以上),用"亿"仿照上面的做法进行划分.
        if bit > 9:
            return '%s%s%s' % (recur(s[:-8], bit - 8), "亿", recur(s[-8:], 8))

    return recur(s, len(s))


def pretreatment(input_sentence):
    # 将中文转换为阿拉伯字母
    return change_chinese_num_to_arab(input_sentence)


if __name__ == '__main__':
    print(pretreatment('上周五上午五点30'))
