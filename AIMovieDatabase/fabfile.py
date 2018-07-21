from fabric.api import *

env.user = 'root'
env.hosts = ['120.78.133.20']
env.password = 'Limingzhe@123'


def go():
    # run('su admin')
    with cd('/home/admin'):  # with的作用是让后面的表达式语句继承当前状态，实现：cd /var/logs  && ls -l的效果
        run('sudo rm -rf AIMovieDatabase')
        put('C://Users//erdai//Desktop//AIMovieDatabase.rar', './')
        run('rar x AIMovieDatabase.rar')
        run('sudo rm -rf AIMovieDatabase.rar')
