# -*- coding: utf-8 -*-
__version__ = '0.0.1'

from pymongo import *
import pymongo
client = MongoClient('mongodb://112.124.122.233:27017/')
db = client.zsxx
collection_tick = db.tick
collection_kline = db.kline
#cursor = collection.find({"date":"20170828","symbol": "a1711"},{"_id":0})

def printtick(var):
    cursor_t=collection_tick.find(var,{"_id":0})
    for doc in cursor_t:
        print(doc)

def printkline(var):
    cursor_k=collection_kline.find(var,{"_id":0})
    for doc in cursor_k:
        print(doc)

def printdoc2():
    print("zsxx")

