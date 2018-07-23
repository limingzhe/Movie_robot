
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 19 03:50:22 2018

@author: WCH
"""

import global_var
import search_mod
import nlg

from flask import Flask, request
import requests
# from flask import render_template, redirect, session
import json

app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'
# app.secret_key = 'u2jksidjflsduwerjl'
# app.debug = True


@app.route('/', methods=['POST'])
def index():
    # 获取openid, context, state
    info = request.values.get('inform')
    info = json.loads(info)
    openid = info['id']
    context = info['text']
    state = info['state']
    info['id'] = '1'
    print('openid:', openid)
    print('context:', type(context), context)
    print('state:', state)
    
    out = deal_info(info)
    return out
# =============================================================================
#     return json.dumps({'msg':'我好\n\rhappy', 'state':1},ensure_ascii=False)
# =============================================================================
    

    

def deal_info(info):
    state = info['state']
    context = info['text']
    print('context',type(context), context)
    # state1: 识别意图
    if state == global_var.STATE_TO_INTENT:
        # 调用意图识别接口
        intent_id = get_intent(context)
        # 不同意图处理
        if intent_id == global_var.INTENT_SEARCH:
            # search_mod里的接口
            print('search')
            return search_mod.Search(info).search_main()
# =============================================================================
#             return json.dumps({'msg':'查询功能', 'state':global_var.STATE_TO_INTENT},ensure_ascii=False)
# =============================================================================
            
        elif intent_id == global_var.INTENT_BOOK:
            # book_mod里的接口
            print('book')
            return json.dumps({'msg':'订票功能开发中', 'state':global_var.STATE_TO_INTENT},ensure_ascii=False)
            
        elif intent_id == global_var.INTENT_RECOMMEND:
            # recommend_mod里的接口
            print('recommend')
            return json.dumps({'msg':'推荐功能开发中', 'state':global_var.STATE_TO_INTENT},ensure_ascii=False)
        elif intent_id == global_var.INTENT_NO:
            # 返回没有识别到意图
            print('no 意图')
            return json.dumps({'msg':'不清楚您的意图 ^.^', 'state':global_var.STATE_TO_INTENT},ensure_ascii=False)
        else:
            print('意图识别服务器异常')
            return nlg.pack_string(global_var.NLG_SYSTEM_ERROR, global_var.STATE_TO_INTENT)
            # 意图服务器连接异常
    # state2：追问
    elif state == global_var.STATE_SEARCH_TIME:
        print('STATE_SEARCH_TIME')
        return json.dumps({'msg':'STATE_SEARCH_TIME', 'state':global_var.STATE_TO_INTENT},ensure_ascii=False)
        
    else:
        print('else')
        return json.dumps({'msg':'else', 'state':global_var.STATE_TO_INTENT},ensure_ascii=False)
        
    

# 意图识别
def get_intent(text):
    try:
        intention_url = global_var.IP_GET_INTENT
        print('intent:',type(text), text)
    
        json_data = json.dumps({'text': text})
        print('jsdate:',type(json_data), json_data)
        response = requests.post(intention_url, data=json_data, headers={'Content-Type': 'application/json'}).text
        print(response)
        print(type(response))
        return json.loads(response)['intention']
    except Exception as e:
        print(e)
        return 'error'
  
      
if __name__ == '__main__':
    app.run()
