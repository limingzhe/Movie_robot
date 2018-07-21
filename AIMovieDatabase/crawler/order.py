import pymongo

client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['AIMovie']

collection = db['order']
order = [
    {
        'user_id': '1',
        'cinema_name': '保利国际影城(宝龙广场店)',
        'movie_name': '我不是药神',
        'watching_time': '2017.07.14 15:00'
    },
    {
        'user_id': '1',
        'cinema_name': '保利国际影城(宝龙广场店)',
        'movie_name': '邪不压正',
        'watching_time': '2017.07.18 23:45'
    }
]

collection.insert_many(order)