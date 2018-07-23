"""
Flask app 初始化操作
"""
from flask import Flask
import logging
import os
import sys
from app import gbdt_eval

# 将工程根目录插入到sys.path中
project_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_path not in sys.path:
    sys.path.insert(0, project_path)

def create_app():
    """
    创建Flask app，并根据环境加载配置
    :return: Flask对象app
    """
    app = Flask(__name__)

    if not hasattr(app, 'production'):
        app.production = not app.debug and not app.testing

    if app.debug or app.testing:
        app.logger.addHandler(logging.StreamHandler())
        app.logger.setLevel(logging.ERROR)

    # 注册蓝图
    register_blueprint(app)

    return app

def register_blueprint(app):
    """
    注册蓝图到给定app上
    :param app: Flask对象
    :return: None
    """
    url_prefix = "/AIMovieIntentionRe"
    app.register_blueprint(gbdt_eval.intention, url_prefix=url_prefix)

    return None


