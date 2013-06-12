#coding=utf-8

import urllib2
import logging
import re

from wx_send import login, username, pwd, http_post, user_agent

from image_add_info import read_info
import service

logger = logging.getLogger('zjdr.wx_fakeid')

friend_list_url = 'https://mp.weixin.qq.com/cgi-bin/contactmanagepage?t=wxm-friend&lang=zh_CN&type=0&groupid=0'

def get_friend_list(token, page_id, pagesize=10):
  resp = ''
  try:
    url = friend_list_url+'&token='+token+'&pagesize='+str(pagesize)+'&pageidx='+str(page_id)

    result = urllib2.urlopen(url)
    html = result.read()
    resp = html
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

  except Exception, e:
      print 'get_friend_list error resp='+str(resp), e
      logger.error('get_friend_list error resp='+str(resp), e) 


def get_open_id_info(token, fromfakeid):
  resp = ''
  try:
    user_msg_url = 'https://mp.weixin.qq.com/cgi-bin/singlemsgpage?t=wxm-singlechat&lang=zh_CN'

    url = user_msg_url+'&token='+token+'&fromfakeid='+fromfakeid+'&count=100'

    result = urllib2.urlopen(url)
    html = result.read()
    # print html

    m = re.search('<script\ id=\"json-msgList\"\ type=\"json\">\s*([\s\S]+?)\s*</script>', html)
    # print m
    if None==m:
      return None
    s = m.group(1)
    # print s
    # print s.endswith(']')
    if None==s or ''==s:
      return None
    resp = s

    msg_list = eval(s)

    # 图片消息在管理页面上看不到，草！

    # image_id = None

    # for msg in msg_list:
    #   if 'title' in msg and '你好，我是追剧达人'==msg['title']:
    #     image_id = msg['id']
    #     break

    # if None==image_id:
    #   return

    # image_base_url = 'https://mp.weixin.qq.com/cgi-bin/getimgdata?mode=large&source=biz&fileId=0'

    # image_url = image_base_url+'&token='+token+'&msgid='+image_id

    # image_result = urllib2.urlopen(image_url)

    # open_id_info = read_info(image)

    open_id_info = None
    for msg in msg_list:
      if 'content' in msg and msg['content'].startswith('你好，我是追剧达人.&nbsp;:)&nbsp;'):
        open_id_info = msg['content'][len('你好，我是追剧达人.&nbsp;:)&nbsp;'):].strip()
        break

    return open_id_info
    

  except Exception, e:
      print 'get_open_id_info error resp='+str(resp), e
      logger.error('get_open_id_info error resp='+str(resp), e) 



def mv_user_fakeid_group(token, tofakeid, groupid):
    resp = None
    try:
        url = 'https://mp.weixin.qq.com/cgi-bin/modifycontacts?action=modifycontacts&t=ajax-putinto-group'

        parms = {'contacttype':groupid,
            'tofakeidlist':tofakeid,
            'token':token,
            'ajax':1
        }

        headers = {'Accept':'*/*',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Origin':'https://mp.weixin.qq.com',
            'Referer':'https://mp.weixin.qq.com/cgi-bin/contactmanagepage',
            'User-Agent':user_agent,
            'X-Requested-With':'XMLHttpRequest'
        }

        resp = http_post(url, parms, headers)

        # print resp

        if None==resp or 'ret' not in resp:
            raise Exception('no ret')
        if '0'==resp['ret']:
            return 0
        if '-20000'==resp['ret']:
            return -1

        raise Exception('unknow ret')
    except Exception, e:
        print 'mv_user_fakeid_group error resp='+str(resp), e
        logger.error('mv_user_fakeid_group error resp='+str(resp), e) 
    pass


def update_wx_user_info():
  token = login(username, pwd)

  fake_id_group = 100
  error_group = 101

  while True:
    friend_list = get_friend_list(token, 0)
    if None==friend_list or 0==len(friend_list):
      break

    for friend in friend_list:
      try:
        fake_id = friend['fakeId']
        open_id = get_open_id_info(token, fake_id) 
        print open_id
        if None == open_id:
          mv_user_fakeid_group(token, fake_id, error_group)
          continue

        user = service.get_wx_user_by_fakeid(fake_id)
        print user
        if None != user:
          mv_user_fakeid_group(token, fake_id, fake_id_group)
          continue

        user = service.get_wx_user_by_open_id(open_id)
        print user
        if None == user:
          mv_user_fakeid_group(token, fake_id, error_group)
          continue

        try:
          service.update_wx_user_info(open_id, fake_id, friend['nickName'])  
        except Exception, e:
          print 'update_wx_user_info error open_id='+str(open_id), e
          logger.error('update_wx_user_info error open_id='+str(open_id), e)

          mv_user_fakeid_group(token, fake_id, error_group)
          continue

        mv_user_fakeid_group(token, fake_id, fake_id_group)

      except Exception, e:
        print 'update_wx_user_info error friend='+str(friend), e
        logger.error('update_wx_user_info error friend='+str(friend), e)





if __name__=="__main__":
  # token = login(username, pwd)
  # print token

  # friend_list = get_friend_list(token, 0)
  # print friend_list

  # # print mv_user_fakeid_group(token, '3957225', 100)

  # print get_open_id_info(token, '3957225')

  update_wx_user_info()

  pass
