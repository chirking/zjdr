#coding=utf-8

import urllib2
import logging
import re

from wx_send import login, username, pwd

logger = logging.getLogger('zjdr.wx_fakeid')

friend_list_url = 'https://mp.weixin.qq.com/cgi-bin/contactmanagepage?t=wxm-friend&lang=zh_CN&type=0&groupid=0'

def get_friend_list(token, page_id, pagesize=10):
  url = friend_list_url+'&token='+token+'&pagesize='+str(pagesize)+'&pageidx='+str(page_id)

  result = urllib2.urlopen(url)
  html = result.read()
  # print html

  m = re.search('<script\ id=\"json-friendList\"\ type=\"json/text\">\s*([\s\S]+?)\s*</script>', html)
  # print m
  if None==m:
  	return None
  s = m.group(1)
  # print s
  # print s.endswith(']')
  if None==s or ''==s:
  	return None

  friend_list = eval(s)
  return friend_list


def get_


if __name__=="__main__":
  token = login(username, pwd)
  print token

  friend_list = get_friend_list(token, 0)
  print friend_list