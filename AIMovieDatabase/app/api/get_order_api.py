"""
分期算法服务api
"""
import datetime
import json

from flask import Blueprint, request, make_response

from manager import db

get_order = Blueprint('get_order', __name__)


@get_order.route('/getUserExistence.json', methods=['POST'])
def get_user_existence():
    """
    判断order表中是否存在user_id的订单信息
    :return:
    """
    if not request.json.get('user_id'):
        return make_response(json.dumps({"respCode": "9501", "respMsg": "参数错误"}, ensure_ascii=False))
    # noinspection PyBroadException
    try:
        user_id = request.json.get('user_id')
        collection = db['order']
        results = list(collection.find({'user_id': user_id}))
        json_str = {'state': '1'} if results else {'state': '0'}
        return make_response(json.dumps({'respCode': '1000', 'respMsg': '成功', 'data': json_str},
                                        ensure_ascii=False))
    except BaseException:
        return make_response(json.dumps({"respCode": "1001", "respMsg": "系统异常"}, ensure_ascii=False))


@get_order.route('/getOrderByEntity.json', methods=['POST'])
def get_order_by_entity():
    """
    get{"user_id":userId, "timeRange":timeRange}
    :return: order
    """
    user_id = request.json.get('user_id')
    cinema = request.json.get('cinema')
    time = request.json.get('timeRange')
    if user_id is None or cinema is None or time is None:
        return make_response(json.dumps({"respCode": "9501", "respMsg": "参数错误"}, ensure_ascii=False))
    # noinspection PyBroadException
    try:
        begin_date = time.split('-')[0]
        end_date = time.split('-')[1]

        if cinema != "" and begin_date != "" and end_date != "":
            my_query = {"user_id": user_id, "cinema_name": cinema,
                        "watching_time": {"$lt": end_date, "$gt": begin_date}}
        elif cinema != "":
            my_query = {"user_id": user_id, "cinema_name": cinema}
        else:
            my_query = {"user_id": user_id, "watching_time": {"$lt": end_date, "$gt": begin_date}}

        collection = db['order']
        result = list(collection.find(my_query))
        result = [
            {
                'cinema_name': result['cinema_name'],
                'movie_name': result['movie_name'],
                'watching_time': result['watching_time']
            }
            for result in result
        ]
        return make_response(json.dumps({'respCode': '1000', 'respMsg': '成功', 'data': result},
                                        ensure_ascii=False))
    except BaseException:
        return make_response(json.dumps({"respCode": "1001", "respMsg": "系统异常"}, ensure_ascii=False))


@get_order.route('/getOrderAfter.json', methods=['POST'])
def get_order_after():
    """
    get{"userId":userId}
    :return:
    """
    user_id = request.json.get('user_id')
    if not user_id:
        return make_response(json.dumps({"respCode": "9501", "respMsg": "参数错误"}, ensure_ascii=False))

    # noinspection PyBroadException
    try:
        time_now = str(datetime.datetime.now())
        time = time_now[0:4] + time_now[5:7] + time_now[8:10] + time_now[11:13] + time_now[14:16]

        collection = db['order']
        # 查询条件未电影播放时间在当前时间之后的
        my_query = {"user_id": user_id, "watching_time": {"$gt": time}}
        result = list(collection.find(my_query))
        result = [
            {
                'cinema_name': result['cinema_name'],
                'movie_name': result['movie_name'],
                'watching_time': result['watching_time']
            }
            for result in result
        ]
        return make_response(json.dumps({'respCode': '1000', 'respMsg': '成功', 'data': result},
                                        ensure_ascii=False))

    except BaseException:
        return make_response(json.dumps({"respCode": "1001", "respMsg": "系统异常"}, ensure_ascii=False))


@get_order.route('/getOrderBefore.json', methods=['POST'])
def get_order_before():
    """
    get{"userId":userId}
    :return:
    """
    user_id = request.json.get('user_id')
    if not user_id:
        return make_response(json.dumps({"respCode": "9501", "respMsg": "参数错误"}, ensure_ascii=False))

    # noinspection PyBroadException
    try:
        time_now = str(datetime.datetime.now())
        time = time_now[0:4] + time_now[5:7] + time_now[8:10] + time_now[11:13] + time_now[14:16]

        collection = db['order']
        # 查询条件未电影播放时间在当前时间之前的
        my_query = {"user_id": user_id, "watching_time": {"$lt": time}}
        result = list(collection.find(my_query))
        result = [
            {
                'cinema_name': result['cinema_name'],
                'movie_name': result['movie_name'],
                'watching_time': result['watching_time']
            }
            for result in result
        ]
        return make_response(json.dumps({'respCode': '1000', 'respMsg': '成功', 'data': result},
                                        ensure_ascii=False))

    except BaseException:
        return make_response(json.dumps({"respCode": "1001", "respMsg": "系统异常"}, ensure_ascii=False))