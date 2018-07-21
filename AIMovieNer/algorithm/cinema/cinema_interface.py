"""
    抽取影院的接口文件
"""


def extract_cinema(input_sentence):
    cinemas = ['保利国际影城']
    for cinema in cinemas:
        if cinema in input_sentence:
            return cinema
    return ''
