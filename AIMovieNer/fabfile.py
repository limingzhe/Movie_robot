from fabric.api import *

env.user = 'root'
env.hosts = ['120.78.133.20']
env.password = 'Limingzhe@123'


def go():
    # run('su admin')
    with cd('/home/admin'):  # with的作用是让后面的表达式语句继承当前状态，实现：cd /var/logs  && ls -l的效果
        run('sudo rm -rf AIMovieNer')
        put('C://Users//erdai//Desktop//AIMovieNer.rar', './')
        run('rar x AIMovieNer.rar')
        run('sudo rm -rf AIMovieNer.rar')
