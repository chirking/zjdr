#coding=utf-8

from domain import User, Movie, MovieSub, MovieSubNotify
from mongo_dao import userDAO, movieDAO, movieSubDAO, movieSubNotifyDAO

import domain


def wx_subscribe(open_id):
	user = User()

	user = userDAO.create_if_absent(open_id, domain.USER_OPEN_ID_TYPE_WX, user)



def get_wx_user_by_fakeid(wx_fakeid):

	user = userDAO.get_user_by_wx_fakeid(wx_fakeid)
	return user


def get_wx_user_by_open_id(open_id):

	user = userDAO.get_user_by_open_id(open_id, domain.USER_OPEN_ID_TYPE_WX)
	return user


def update_wx_user_info(open_id, wx_fakeid, nick_name):

	user = userDAO.get_user_by_open_id(open_id, domain.USER_OPEN_ID_TYPE_WX)

	if None == user:
		raise Exception('微信user is None. open_id='+open_id)

	user.wx_fakeid = wx_fakeid
	user.nick_name = nick_name

	success = userDAO.update_user_info_by_id(user.id, user)

	# if None==success:
	# 	raise Exception('更新微信user失败, open_id='+open_id)
	return success




if __name__=="__main__":
	user = userDAO.get_user_by_open_id('1234556', domain.USER_OPEN_ID_TYPE_WX)

	print user

	print update_wx_user_info('1234556', 'wx_fakeid_2', 'nick_name_1')

	user = userDAO.get_user_by_open_id('1234556', domain.USER_OPEN_ID_TYPE_WX)

	print user