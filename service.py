#coding=utf-8

from domain import User, Movie, MovieSub
from mongo_dao import userDAO, movieDAO, movieSubDAO

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


def get_movies():

	movies = movieDAO.get_movies()
	return movies


def get_movie_by_code(code):

	movies = movieDAO.get_movie_by_code(code)
	return movies


def add_movie(code, movie):

	movieDAO.create_if_absent(code, movie)


def update_movie(code, movie):

	movieDAO.update_movie_by_code(code, movie)


def search_movies(word):

	movies = []

	movies_1 = movieDAO.find_movie_by_name(word)

	movies_2 = movieDAO.find_movie_by_alias(word)

	if None != movies_1:
		movies = movies + movies_1
	if None != movies_2:
		movies = movies + movies_2

	return movies



if __name__=="__main__":
	# user = userDAO.get_user_by_open_id('1234556', domain.USER_OPEN_ID_TYPE_WX)

	# print user

	# print update_wx_user_info('1234556', 'wx_fakeid_2', 'nick_name_1')

	# user = userDAO.get_user_by_open_id('1234556', domain.USER_OPEN_ID_TYPE_WX)

	# print user

	print get_movies()[0].to_json()

	print '权力的游戏'
	print search_movies('权力的游戏')[0].to_json()
	print '冰与火之歌'
	print search_movies('冰与火之歌')[0].to_json()


