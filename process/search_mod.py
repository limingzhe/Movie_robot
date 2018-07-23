# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 09:02:42 2018

@author: WCH
"""

import global_var
import json
import datetime
import nlg
import requests

# from flask import request

class Search(object):
    def __init__(self, info):
        self.openid = info['id']
        self.text = info['text']
        self.state = info['state']
        
        
    # 订单记录是否存在的查询
    def get_orders(self):
        url = global_var.IP_GET_ORDER
        json_data = json.dumps({'user_id': self.openid},ensure_ascii=False)
        response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}).text
        orders = json.loads(response)    
        print(orders)
        # orders 3情况
        if orders['respCode']==global_var.SEVER_FAILED:
            return -1
        elif orders['data']['state'] == '0':
            return 0
        else:
            return 1
    
    # 实体识别
    def recognize_entity(self, r_type):
        url = global_var.IP_RECOGNIZE_ENTITY
        json_data = json.dumps({'text': self.text, 'type': r_type})
        response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}).text
        entity_msg = json.loads(response)
        return entity_msg
    
    # 查询时间及影院实体对应订单
    def search_by_entity(self, entity_msg):
        # 打包entity信息
        info_search = {'user_id': self.openid,
                       'cinema':"",
                       'timeRange':""}
        for item in entity_msg['data']:
            if item['slotType']=='cinema':
                info_search['cinema'] = item['slotValue']
            if item['slotType']=='timeRange':
                info_search['timeRange'] = item['slotValue']
        # 查询
        print('baoli',info_search)
        url = global_var.IP_BY_ENTITY
        json_data = json.dumps(info_search)
        response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}).text
        order_msg = json.loads(response)
        return order_msg
    
    # 废弃---查询时间实体对应订单
    def search_by_date(self, entity_msg):
        url = global_var.IP_BY_DATE
        
        # 获取实体里的时间（2种情况，data有2个实体及一个的情况）
        my_date = ""
        for item in entity_msg['data']:
            if item['slotType']=='timeRange':
                my_date = item['slotValue']
        date_start, date_end = my_date.split("-")
        date_start = datetime.datetime.strptime(date_start,"%Y%m%d%H%M").date()
        date_end = datetime.datetime.strptime(date_end,"%Y%m%d%H%M").date()
        
        # 与接口交互
        json_data = json.dumps({'user_id': self.openid,
                                'beginDate':date_start,
                                'endDate':date_end},
                                ensure_ascii=False)
        response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}).text
        order_msg = json.loads(response)
        
        return order_msg
    
    # 废弃---查询影院实体对应订单
    def search_by_cinema(self, entity_msg):
        url = global_var.IP_BY_CINEMA
        
        # 获取实体里的地点(2种情况，data有2个以及一个的情况)
        my_cinema = ""
        for item in entity_msg['data']:
            if item['slotType']=='cinema':
                my_cinema = item['slotValue']
        
        # 与接口交互
        json_data = json.dumps({'user_id': self.openid,
                                'cinema_name': my_cinema},ensure_ascii=False)
        response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}).text
        order_msg = json.loads(response)      
        return order_msg
    
    # 查询当前时间之后的订单
    def search_after_date(self):
        url = global_var.IP_AFTER_DATE
        
        # 与接口交互
        json_data = json.dumps({'user_id': self.openid},ensure_ascii=False)
        response = requests.post(url, data=json_data, headers={'Content-Type': 'application/json'}).text
        order_msg = json.loads(response)      
        return order_msg
    
    # 查询当前时间之前的订单
    def search_before_date(self):
        url = global_var.IP_BEFORE_DATE
        
        # 与接口交互
        json_data = json.dumps({'user_id': self.openid},ensure_ascii=False)
        response = requests.post(url, data=json_data,headers={'Content-Type': 'application/json'}).text
        order_msg = json.loads(response)      
        return order_msg
    
 
    # 废弃
    @staticmethod
    def get_overlap(order_by_date, order_by_cinema):
        my_cinema = order_by_cinema[0]['cinema_name']
        new_order = []
        for item in order_by_date:
            if item['cinema_name']==my_cinema:
                new_order.append(item)
        return new_order
            
    
    # 查询主流程
    def search_main(self):
        try:
            # 如果没有查到订单信息
            if self.get_orders()==0:
                return nlg.pack_string(global_var.NLG_NO_ORDER, global_var.STATE_TO_INTENT)
            elif self.get_orders()<0:
                print('id订单查询服务器error')
                return nlg.pack_string(global_var.NLG_SYSTEM_ERROR, global_var.STATE_TO_INTENT)
            # 如果查到订单信息
            else:
                # -->识别2个实体
                entity_msg = self.recognize_entity("")
                # 1. 系统没有报错
                if entity_msg["respCode"]==global_var.SEVER_SUCCESS:
                    # 1.1 如果两个都识别到
                    if len(entity_msg['data']) > 0:
                        # 用实体查询
                        order_by_entity = self.search_by_entity(entity_msg)
                        print('order_by_entity:',order_by_entity)
                        # 1.1.1 订单结果为空
                        if len(order_by_entity['data']) == 0:
                            return nlg.pack_string(global_var.NLG_NO_MATCH, global_var.STATE_TO_INTENT)
                        # 1.1.2 有订单
                        else:
                            return nlg.pack_order_info(order_by_entity, global_var.STATE_TO_INTENT)
                    # 1.2 如果没有识别到
                    else:
                        order_msg = self.search_after_date() 
                        print("after date:", order_msg)                       
                        if len(order_msg['data']) == 0:
                            # 如果order_msg为空，返回之前的订单
                            order_msg = self.search_before_date()
                        return nlg.pack_order_info(order_msg, global_var.STATE_TO_INTENT)
                # 2. --> 系统报错
                else:
                    print('实体识别查询服务器error')
                    return nlg.pack_string(global_var.NLG_SYSTEM_ERROR, global_var.STATE_TO_INTENT)
        except Exception as e:
            print(e)
            return nlg.pack_string(global_var.NLG_SYSTEM_ERROR, global_var.STATE_TO_INTENT)

                            
    
if __name__ == '__main__':
    print('here is: search_mod.py')
    my_time = datetime.datetime.strptime("201809101111","%Y%m%d%H%M")
    my_time = my_time.strftime("%Y-%m-%d %H:%M")
    print(type(my_time), my_time)
