# -*- coding:utf-8 -*- 
"""
蛋卷斗牛二八轮动 回测
"""
import tushare as ts
import pymongo
from functools import reduce 

#初始现金
cash = 100
#总净值
assets = 100
#持仓
position = {}
#沪深300指数
csi300 = {}
#中证500指数
csi500 = {}
#国债指数
gbi = {}

conn = pymongo.MongoClient('127.0.0.1', 27017)

def order(strategy):
    global cash, position
    cash = 0
    position = {}
    position[strategy] = assets / eval(strategy)[date]

for i in conn.quant.csi300.find().sort("_id", pymongo.ASCENDING):
    csi300[i['_id']] = i['close']
for i in conn.quant.csi500.find().sort("_id", pymongo.ASCENDING):
    csi500[i['_id']] = i['close']
for i in conn.quant.gbi.find().sort("_id", pymongo.ASCENDING):
    gbi[i['_id']] = i['close']

dates = list(csi300.keys())
dates.sort()

for date in dates:
    if date < '2006-01-01':
        continue
    assets = reduce(lambda x, y: position[x] * eval(x)[date] if isinstance(x, str) else x + position[y] * eval(y)[date], position, 0)
    assets += cash
    index = dates.index(date)
    datePrev = dates[index-21]
    yesterday = dates[index-1]
    csi300Incr = csi300[yesterday] / csi300[datePrev] - 1
    csi500Incr = csi500[yesterday] / csi500[datePrev] - 1
    strategy = None
    if csi300Incr < 0 and csi500Incr < 0:
        strategy = 'gbi'
    elif csi300Incr > csi500Incr and csi300Incr > 0:
        strategy = 'csi300'
    elif csi500Incr > csi300Incr and csi500Incr > 0:
        strategy = 'csi500'
    if strategy is not None:
        order(strategy)

print(date, assets, position, strategy, csi300[date], csi500[date], gbi[date])