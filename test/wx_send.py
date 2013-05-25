# -*- coding: utf-8 -*- 

import time,urllib2,urllib
import md5

def login_wx():
    try:
        #设置 cookie
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies)
        urllib2.install_opener(opener)

        pwd0 = md5.new("iamChirk")
        pwd0.digest()
        pwd = pwd0.hexdigest()
        #print pwd

        url = "https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN"

        headers = {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset' : 'GBK,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding' : 'gzip,deflate,sdch',
            'Accept-Language' : 'zh-CN,zh;q=0.8',
            'Connection' : 'keep-alive',
            'Host' : 'mp.weixin.qq.com',
            'Referer' : 'https://mp.weixin.qq.com/cgi-bin/loginpage?t=wxm2-login&lang=zh_CN',
            'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31'
        }

        parms = {"username":"chirking@outlook.com",
			"pwd":pwd,
			"imgcode:":"",
			"f":"json"}

        req  = urllib2.Request(
           url = url,
           data = urllib.urlencode(parms),
           headers = headers
        )
        #print req
        result = urllib2.urlopen(req)
        
        #print result
        print(unicode(result.read(),"utf8"))

        #显示配置页面
        #avatar = urllib2.urlopen("https://mp.weixin.qq.com/cgi-bin/userinfopage?t=wxm-setting&token=2093896881&lang=zh_CN")
        #print(avatar.read().decode("utf8"))
    except Exception,e:
        print(e)
    pass


def send_wx():
    try:

        url = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?sub=preview&t=ajax-appmsg-preview'

        headers = {'Accept':'*/*',
            'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding':'gzip,deflate,sdch',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Connection':'keep-alive',
            # 'Content-Length':'237',
            'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
            'Host':'mp.weixin.qq.com',
            'Origin':'https://mp.weixin.qq.com',
            # 'Referer':'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?token=674088017&lang=zh_CN&sub=edit&t=wxm-appmsgs-edit-new&type=10&subtype=3&ismul=1',
            'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31',
            'X-Requested-With':'XMLHttpRequest'
        }

        parms = {'error':'false',
            'count':'2',
            'AppMsgId':'',
            'title0':'python test 123',
            'digest0':'aaa 000',
            'content0':'<p>aaa</p>',
            'fileid0':'10000005',
            'title1':'python test 456',
            'digest1':'bbb',
            'content1':'<p><img src="http://mmsns.qpic.cn/mmsns/vD2tCj81DvDBEsC9aAchDm6uJ0sOIIsTyLO7b2BnCTQbCNCdLickrcA/0"></p>',
            'fileid1':'10000004',
            'preusername':'junfusu',
            'token':'674088017',
            'ajax':'1'
        }

        req  = urllib2.Request(
           url = url,
           data = urllib.urlencode(parms),
           headers = headers
        )
        #print req
        result = urllib2.urlopen(req)

        print(unicode(result.read(),"utf8"))

    except Exception,e:
        print(e)
    pass	

if __name__=="__main__":
	login_wx()
	send_wx()
