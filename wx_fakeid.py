#coding=utf-8

import urllib2
import logging
import re

from wx_send import login, username, pwd, http_post, user_agent

from image_add_info import read_info

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
    print url

    result = urllib2.urlopen(url)
    html = result.read()
    resp = html
    # print html

    m = re.search('<script\ id=\"json-msgList\"\ type=\"json\">\s*([\s\S]+?)\s*</script>', html)
    print m
    if None==m:
      return None
    s = m.group(1)
    print s
    # print s.endswith(']')
    if None==s or ''==s:
      return None

    image_id = None

    msg_list = eval(s)
    for msg in msg_list:
      if '你好，我是追剧达人'==msg['title']:
        image_id = msg['id']
        break

    if None==image_id:
      return

    image_base_url = 'https://mp.weixin.qq.com/cgi-bin/getimgdata?mode=large&source=biz&fileId=0'

    image_url = image_base_url+'&token='+token+'&msgid='+image_id

    image_result = urllib2.urlopen(image_url)

    open_id_info = read_info(image)

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

        print resp

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


if __name__=="__main__":
  token = login(username, pwd)
  print token

  # friend_list = get_friend_list(token, 0)
  # print friend_list

  # print mv_user_fakeid_group(token, '3957225', 100)

  print get_open_id_info(token, '3957225')


