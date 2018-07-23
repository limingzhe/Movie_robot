#!/usr/bin/python3

import pymongo

from crawler.cinema import crawl_cinemas
from crawler.movie import crawl_movies

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['AIMovie']
db.drop_collection('cinema')
db.drop_collection('movie')
db.drop_collection('order')

# 影院
collection = db['cinema']
documents = crawl_cinemas()
collection.insert_many(documents)

# 电影
collection = db['movie']
documents = crawl_movies()
collection.insert_many(documents)

# 订单（手动插入）
collection = db['order']
order = [
    {
        'user_id': '1',
        'cinema_name': '保利国际影城(宝龙广场店)',
        'movie_name': '我不是药神',
        'watching_time': '201807170500'
    },
    {
        'user_id': '1',
        'cinema_name': '保利国际影城(宝龙广场店)',
        'movie_name': '邪不压正',
        'watching_time': '201807180625'
    },
    {
        'user_id': '1',
        'cinema_name': '保利国际影城(宝龙广场店)',
        'movie_name': '动物世界',
        'watching_time': '201807222325'
    },
    {
        'user_id': '1',
        'cinema_name': '保利国际影城(宝龙广场店)',
        'movie_name': '摩天营救',
        'watching_time': '201807240820'
    },
    {
        'user_id': '1',
        'cinema_name': '保利国际影城(宝龙广场店)',
        'movie_name': '邪不压正',
        'watching_time': '201807251630'
    }
]

collection.insert_many(order)