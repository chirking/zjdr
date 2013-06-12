#coding=utf-8

import pymongo

con = pymongo.Connection('mongodb://admin:admin@106.187.34.97:27017/zjdr')
db_zjdr = con.zjdr