#coding=utf-8

import pymongo

con = pymongo.Connection('mongodb://admin:admin@localhost:27017/zjdr')
db_zjdr = con.zjdr

user1 = {'openId':'123',
        'openIdType':1,
        'name':'测试测试',
        'status':-1}

# try:
#     db_zjdr.user.insert(user1)
# except Exception,e:
#     print(e)

# print db_zjdr.user.find_one()

#db_zjdr.users.remove()

