#coding=utf-8

import pymongo

con = pymongo.Connection('mongodb://admin:admin@localhost:27017/zjdr')
db_zjdr = con.zjdr