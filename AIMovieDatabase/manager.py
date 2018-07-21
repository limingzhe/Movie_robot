"""
开发环境调试使用，启动脚本
"""
import pymongo
from flask import render_template

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['AIMovie']

from app import create_app

app = create_app()


@app.route("/AIMovieDatabase/")
def heart_check():
    return render_template("index.html")


def run():
    """使用脚本运行"""
    app.run(host='0.0.0.0', port=6000)


if __name__ == '__main__':
    run()
