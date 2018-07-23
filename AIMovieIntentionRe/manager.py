"""
开发环境调试使用，启动脚本
"""
from app import create_app

app = create_app()

def run():
    """使用脚本运行"""
    app.run(host='0.0.0.0', port=5000)

if __name__ == '__main__':
    run()