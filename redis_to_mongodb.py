# coding=utf-8
from pymongo import MongoClient
import redis,json

# 链接数据库
redis_cli = redis.Redis(host='127.0.0.1',port=6379,db=0)

# 链接mongodb
mongo_cli = MongoClient("127.0.0.1",27017)
db = mongo_cli['Zhiyou']
col = db['zhiyouji']
while True:

    # 读取数据
    source, data = redis_cli.blpop(['zhiyouji:items'])
    print(source)
    # 转换数据
    str_data = data.decode()
    dict_data = json.loads(str_data)
    print(dict_data)

    # 写入数据库
    col.insert(dict_data)