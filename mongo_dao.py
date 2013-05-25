#coding=utf-8

from domain import User, Movie, MovieSub, MovieSubNotify
from mongo import db_zjdr
from bson.objectid import ObjectId
from pymongo import ASCENDING, DESCENDING

userDAO = None
movieDAO = None
movieSubDAO = None
movieSubNotifyDAO = None

class BaseDAO(object):
	"""docstring for BaseDAO"""
	def create_id(self, json):
		if None!=json and None!=json['_id']:
			json['id'] = str(json['_id'])
			json['_id'] = None
		return json

	def remove_id(self, json):
		if None!=json and None!=json['_id']:
			json['_id'] = None
		return json

	def get_object_id(self, id):
		if None==id:
			return None
		return ObjectId(id)


class UserDAO(BaseDAO):
	"""docstring for UserDAO"""

	db = db_zjdr.user

	def to_User(self, json):
		if None==json:
			return None
		return User(self.create_id(json))	
	
	def insert(self, user):
		if None==user:
			return None
		user.id = None
		user.crate_time = None
		user.modified_time = None
		return self.db.insert(user.to_json())

	def create_if_absent(self, open_id, open_id_type, user):
		user_ = self.get_user_by_open_id(open_id, open_id_type)
		if user_:
			return user_
		user.open_id = open_id
		user.open_id_type = open_id_type
		self.insert(user)
		return self.get_user_by_open_id(open_id, open_id_type)

	def get_user(self, id):
		json = self.db.find_one({'id':id})
		return self.to_User(json)
		

	def get_user_by_open_id(self, open_id, open_id_type):
		json = self.db.find_one({'open_id':open_id, 'open_id_type':open_id_type})
		return self.to_User(json)


class MovieDAO(BaseDAO):
	"""docstring for MovieDAO"""
	
	db = db_zjdr.movie

	def to_Movie(self, json):
		if None==json:
			return None
		return Movie(self.remove_id(json))	

	def to_Movies(self, jsons):
		if None==jsons:
			return None
		return [self.to_movie(json) for json in jsons]	

	def insert(self, movie):
		if None==movie:
			return None
		movie.crate_time = None
		movie.modified_time = None
		self.db.insert(movie.to_json())

	def create_if_absent(self, code, movie):
		movie_ = self.get_movie_by_code(code)
		if movie_:
			return movie_;
		movie.code = code
		self.insert(movie)
		return self.get_movie_by_code(code)

	def get_movie_by_code(self, code): 
		if None==code or ''==code:
			return None
		json = self.db.find_one({'code':code})
		return self.to_Movie(json)

	def find_movie_by_name(self, name):
		if None==name or ''==name:
			return None
		jsons = self.db.find({'name':name}).sort('season', DESCENDING)
		return self.to_Movies(jsons)

	

class MovieSubDAO(BaseDAO):
	"""docstring for MovieSubDAO"""
	
	db = db_zjdr.movie_sub

	def to_MovieSub(self, json):
		if None==json:
			return None
		return MovieSub(self.remove_id(json))

	def insert(self, movie_sub):
		if None==movie_sub:
			return None
		movie_sub.crate_time = None
		movie_sub.modified_time = None
		self.db.insert(movie_sub.to_json())

	def create_if_absent(self, user_id, movie_code, movie_sub):
		movie_sub_ = self.get_movie_sub(user_id, movie_code)
		if movie_sub_:
			return movie_sub_;
		movie_sub_.user_id = user_id
		movie_sub_.movie_code = movie_code
		self.insert(movie_sub_)
		return self.get_movie_sub(user_id, movie_code)

	def get_movie_sub(self, user_id, movie_code):
		json = self.db.find_one({'user_id':user_id, 'movie_code':movie_code})
		return self.to_MovieSub(json)


class MovieSubNotifyDAO(object):
	"""docstring for MovieSubNotifyDAO"""
	
	db = db_zjdr.movie_sub_notify

	def to_MovieSubNotify(self, json):
		if None==json:
			return None
		return MovieSubNotify(self.remove_id(json))

	def insert(self, movie_sub_notify):
		if None==movie_sub_notify:
			return None
		movie_sub_notify.crate_time = None
		movie_sub_notify.modified_time = None
		self.db.insert(movie_sub_notify.to_json())

	def create_if_absent(self, user_id, movie_code, movie_sub_notify):
		movie_sub_notify_ = self.get_movie_sub_notify(user_id, movie_code)
		if movie_sub_notify_:
			return movie_sub_notify_;
		movie_sub_notify_.user_id = user_id
		movie_sub_notify_.movie_code = movie_code
		self.insert(movie_sub_notify_)
		return self.get_movie_sub(user_id, movie_code)

	def get_movie_sub_notify(self, user_id, movie_code):
		json = self.db.find_one({'user_id':user_id, 'movie_code':movie_code})
		return self.to_MovieSub(json)
		

userDAO = UserDAO()
movieDAO = MovieDAO()
movieSubDAO = MovieSubDAO()
movieSubNotifyDAO = MovieSubNotifyDAO()


if __name__=="__main__":

  # db_zjdr.user.remove()	

  # user_json = {'open_id':'1234556', 'open_id_type':1}
  # user = User(user_json)

  # user1 = userDAO.create_if_absent('1234556', 1, user)
  # print user1.to_json()

  # user2 = userDAO.get_user_by_open_id('1234556', 1)
  # print user2

  #db_zjdr.movie.remove()	

  movie = Movie()
  movie.code = 'sherlock 1'
  movie.name = u'夏洛克'
  movie.e_name = 'sherlock'
  movie.season = 1
  print movie 

  movie1 = movieDAO.create_if_absent(movie.code, movie)
  print movie1.name.encode('utf8')

  movies = movieDAO.find_movie_by_name(u'夏洛克')
  print movies[0]


