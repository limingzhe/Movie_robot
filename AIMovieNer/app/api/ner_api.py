"""
分期算法服务api
"""
import json

from flask import Blueprint, request, make_response

from app.service import ner_service

robot_bp = Blueprint('robot', __name__)


@robot_bp.route('/getEntity.json', methods=['POST'])
def extract_entities():
    """
    实体抽取
    :return:
    |respCode|String|必填|返回码|
    |respMsg|String|必填|返回信息|
    |data|List|必填|实体列表|
    """
    if not request.json.get('text'):
        return make_response(json.dumps({"respCode": "9501", "respMsg": "参数错误"}, ensure_ascii=False))
    # noinspection PyBroadException
    try:
        text = request.json.get('text')
        entity_type = request.json.get("type")
        if not entity_type:
            entities = ner_service.extract_all(text)
        elif entity_type == "timeRange":
            entities = ner_service.extract_time_range(text)
        elif entity_type == "cinema":
            entities = ner_service.extract_cinema(text)
        result = {"respCode": "1000", "respMsg": "success", "data": entities}
        return make_response(json.dumps(result, ensure_ascii=False))
    except BaseException:
        return make_response(json.dumps({"respCode": "1001", "respMsg": "系统异常"}, ensure_ascii=False))
