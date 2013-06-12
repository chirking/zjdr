#coding=utf-8

from domain import User, Movie, MovieSub, MovieSubNotify
from mongo_dao import userDAO, movieDAO, movieSubDAO, movieSubNotifyDAO

import domain


def wx_subscribe(open_id):
	User user = User()

	user = userDAO.create_if_absent(open_id, domain.USER_OPEN_ID_TYPE_WX, user)


