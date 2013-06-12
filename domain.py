#coding=utf-8

USER_OPEN_ID_TYPE_WX = 1

USER_STATUS_OK = 1
USER_STATUS_CANCEL = 2

MOVIE_SUB_OK = 1
MOVIE_SUB_CANCEL = 2


class BaseDO(object):
  """docstring for BaseDO"""

  create_time = None
  modified_time = None

  def __init__(self, json=None):
    if not json:
      return
    self.__dict__.update(json)

  def to_json(self):
  	return self.__dict__
  def __str__(self):
    return str(self.__dict__)
    

class User(BaseDO):
  """docstring for User"""

  id = None
  open_id = None
  open_id_type = None
  wx_fakeid = None
  status = None


class Movie(BaseDO):
  """docstring for Movie"""

  code = None
  name = None
  e_name = None
  season = None
  summary = None
  pic_url = None
  all_sets = None
  now_set = None
  is_finished = None
  begin_time = None
  update_time = None
  douban_url = None
  youku_url = None


class MovieSet(BaseDO):
  movie_code = None
  set_num = None
  update_time = None
  movie_url = None
  youku_url = None
  wx_msg_id = None


class MovieSub(BaseDO):
  """docstring for MovieSub"""

  user_id = None
  movie_code = None
  status = None


class MovieSubNotify(BaseDO):
  """docstring for MovieSubNotify"""

  user_id = None
  movie_code = None
  notify_time = None
  notify_set = None
  notify_his = None


if __name__=="__main__":

  userJson = {'open_id':'1234556', 'open_id_type':1}
  user = User(userJson)
  print user.to_string()

  


    
    
