# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 07:54:18 2018

@author: WCH
"""
# --------------状态管理--------------------
STATE_TO_INTENT = 100      # 意图识别状态

STATE_SEARCH_TIME = 10     # 查询状态1
STATE_BOOK =  11           # 订票状态1
STATE_RECOMMEND = 12       # 推荐状态1

# --------------意图变量--------------------
INTENT_SEARCH = '0'         # 查询
INTENT_BOOK = '1'            # 订票
INTENT_RECOMMEND = '2'       # 推荐
INTENT_NO = 'null'

# --------------目标IP管理------------------
# 意图识别接口IP
IP_GET_INTENT = 'http://47.93.237.174:5000/IntentionRe/request.json'

# openid查询订单是否存在 IP
IP_GET_ORDER = 'http://120.78.133.20:6000/AIMovieDatabase/getOrder/getUserExistence.json'
# 用时间、影院实体查询订单
IP_BY_ENTITY = 'http://120.78.133.20:6000/AIMovieDatabase/getOrder/getOrderByEntity.json'
# 查当前时间之后订单 IP
IP_AFTER_DATE = 'http://120.78.133.20:6000/AIMovieDatabase/getOrder/getOrderAfter.json'
# 查当前时间之前订单 IP
IP_BEFORE_DATE = 'http://120.78.133.20:6000/AIMovieDatabase/getOrder/getOrderBefore.json'

# 实体识别接口 IP
IP_RECOGNIZE_ENTITY = 'http://120.78.133.20:4000/AIMovieNer/getEntity.json'


# --------------服务器是否正常-----------------
SEVER_SUCCESS = "1000"
SEVER_FAILED = "1001"

# --------------NLG输入---------------------
NLG_NO_ORDER = "您还没有订票哦 ^.^"
NLG_SYSTEM_ERROR = '系统繁忙，稍后再试 ^.^'
NLG_NO_MATCH = '未查到相应结果 ^.^'