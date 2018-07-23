# -*- coding: utf-8 -*-
"""
Created on Fri Jul 20 07:32:17 2018

@author: WCH
"""
# import global_var
import json
import datetime

# 直接包装string到json
def pack_string(str_input, state):
    back_msg = {'msg':str_input,
                'state':state}
    return json.dumps(back_msg, ensure_ascii=False)


# 包装orders订单信息
def pack_order_info(order_msg, state):      
    string_out = "****查到如下信息****\n\r"
    for item in order_msg['data']:
        print('aaaaaaaaaaaa:', item)
        my_time = datetime.datetime.strptime(item['watching_time'],"%Y%m%d%H%M")
        my_time = my_time.strftime("%Y-%m-%d %H:%M")
        string_out = string_out  + "\n\r"  \
                    + "影院：" + item['cinema_name'] + "\n\r" \
                    + "电影：" + item['movie_name'] + "\n\r" \
                    + "时间：" + my_time + "\n\r"
    string_out = string_out + "\n\r订单查询完毕 ^.^"
    back_msg = {'msg':string_out,
                'state':state}
    return json.dumps(back_msg, ensure_ascii=False)