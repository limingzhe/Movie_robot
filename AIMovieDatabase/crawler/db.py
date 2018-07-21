#!/usr/bin/python3

import pymongo

from crawler.cinema import crawl_cinemas
from crawler.movie import crawl_movies

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['AIMovie']

# 影院
collection = db['cinema']
documents = crawl_cinemas()
collection.insert_many(documents)

# 电影
collection = db['movie']
documents = crawl_movies()
collection.insert_many(documents)

