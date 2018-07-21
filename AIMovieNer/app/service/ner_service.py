from algorithm.cinema import cinema_interface
from algorithm.timeRange import time_range_interface


# 抽取时间段
def extract_time_range(text):
    entities = time_range_interface.extract_time_range(text)
    if entities:
        return [{'slotType': 'timeRange', 'slotValue': entities}]
    else:
        return []


# 抽取影院
def extract_cinema(text):
    entities = cinema_interface.extract_cinema(text)
    if entities:
        return [{'slotType': 'cinema', 'slotValue': entities}]
    else:
        return []


# 抽取全部实体
def extract_all(text):
    entities = []

    currency_type = time_range_interface.extract_time_range(text)
    if currency_type:
        entities.append({'slotType': 'timeRange', 'slotValue': currency_type})

    currency_type = cinema_interface.extract_cinema(text)
    if currency_type:
        entities.append({'slotType': 'cinema', 'slotValue': currency_type})

    return entities
