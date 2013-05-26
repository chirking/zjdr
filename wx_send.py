#coding=utf-8 

import time,urllib2,urllib
import md5
import logging
import poster
import re
import tempfile

logger = logging.getLogger('zjdr.wx_send')

headers = {
  'Accept':'*/*',
  'Accept-Charset':'GBK,utf-8;q=0.7,*;q=0.3',
  'Accept-Encoding':'gzip,deflate,sdch',
  'Accept-Language':'zh-CN,zh;q=0.8',
  'Connection':'keep-alive',
  # 'Content-Length':'237',
  'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
  'Host':'mp.weixin.qq.com',
  'Origin':'https://mp.weixin.qq.com',
  'Referer':'https://mp.weixin.qq.com',
  'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_3) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.65 Safari/537.31',
  'X-Requested-With':'XMLHttpRequest'
}

username = "chirking@outlook.com"
pwd = "iamChirk"

cookies = None
token = None

my_test_preusername = 'junfusu'

def http_post(url, parms, headers=headers):
    req  = urllib2.Request(
           url = url,
           data = urllib.urlencode(parms),
           headers = headers
        )
    result = urllib2.urlopen(req)
    
    resp_str = result.read()
    print resp_str
    resp = eval(resp_str)
    return resp


def login(username, pwd):
    resp_str = ''
    try:
        url = "https://mp.weixin.qq.com/cgi-bin/login?lang=zh_CN"

        # 设置 cookie
        global cookies
        cookies = urllib2.HTTPCookieProcessor()
        opener = urllib2.build_opener(cookies)
        urllib2.install_opener(opener)

        # 设置密码
        pwd_0 = md5.new(pwd)
        pwd_0.digest()
        pwd_1 = pwd_0.hexdigest()

        parms = {"username":username,
            "pwd":pwd_1,
            "imgcode:":"",
            "f":"json"
        }

        resp = http_post(url, parms)        

        if "ErrMsg" in resp and None!=resp["ErrMsg"]:
            tokens = [z[1] for z in (y.split('=') for y in resp["ErrMsg"].split('&')) if z[0]=='token' and None!=z and len(z)==2]
            if None==tokens or len(tokens)==0:
                raise Exception('None==tokens')
            return tokens[0]
        
        raise Exception('no ErrMsg')

    except Exception,e:
        print 'login error resp_str='+resp_str, e
        logger.error('login error resp_str='+resp_str, e)


def send(token, appmsgid, tofakeid):
    resp_str = ''
    try:
        url = 'https://mp.weixin.qq.com/cgi-bin/singlesend?t=ajax-response&lang=zh_CN'

        post_headers = {}
        post_headers.update(headers)
        post_headers.update({
            'Referer':'https://mp.weixin.qq.com/cgi-bin/singlemsgpage'
        })
        # print post_headers

        parms = {'type':'10',
            'fid':appmsgid,
            'appmsgid':appmsgid,
            'error':'false',
            'tofakeid':tofakeid,
            'token':token,
            'ajax':'1'
        }

        resp = http_post(url, parms, post_headers)

        if None==resp or 'ret' not in resp:
            raise Exception('no ret')
        if '0'==resp['ret']:
            return 0
        if '-20000'==resp['ret']:
            return 1

        raise Exception('unknow ret')

    except Exception,e:
        logger.error('login error resp_str='+resp_str, e)


def create_msg_0(token):
    resp_str = ''
    try:
        url = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?lang=zh_CN&t=ajax-response&sub=create'

        url = url+'&token='+token

        parms = {'error':'false',
            'count':'1',
            # 'AppMsgId':'',
            'token':'1871176681',
            'ajax':'1',

            'title0':'aaa',
            'digest0':'aaa',
            'content0':'<p>aaa</p>',
            'fileid0':'10000054'
        }

        resp = http_post(url, parms)

        if None==resp or 'ret' not in resp:
            raise Exception('no ret')
        if '0'==resp['ret']:
            return 0
        if '-20000'==resp['ret']:
            return -1

        raise Exception('unknow ret')

    except Exception,e:
        print 'add_msg error resp_str='+resp_str, e
        logger.error('add_msg error resp_str='+resp_str, e)


def create_msg(token):
    resp_str = ''
    try:
        url = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?sub=preview&t=ajax-appmsg-preview'

        url = url+'&token='+token

        parms = {'error':'false',
            'count':'1',
            # 'AppMsgId':'',
            'token':token,
            'ajax':'1',

            'preusername':my_test_preusername,

            'title0':'aaa',
            'digest0':'aaa',
            'content0':'<p>aaa</p>',
            'fileid0':'10000054'
        }

        resp = http_post(url, parms)

        if None==resp or 'ret' not in resp:
            raise Exception('no ret')
        if '0'==resp['ret'] and 'appMsgId' in resp:
            return resp['appMsgId']
        if '-20000'==resp['ret']:
            return -1

        raise Exception('unknow ret')

    except Exception,e:
        print 'create_msg error resp_str='+resp_str, e
        logger.error('create_msg error resp_str='+resp_str, e)


def update_msg(token, appmsgid):
    resp_str = ''
    try:
        url = 'https://mp.weixin.qq.com/cgi-bin/operate_appmsg?sub=preview&t=ajax-appmsg-preview'

        url = url+'&token='+token

        parms = {'error':'false',
            'count':'1',
            'AppMsgId':appmsgid,
            'token':token,
            'ajax':'1',

            'preusername':my_test_preusername,

            'title0':'aaa',
            'digest0':'aaa',
            'content0':'<p>aaa</p>',
            'fileid0':'10000054',

            'title1':'aaa2',
            'digest1':'aaa2',
            'content1':'<p>aaa2</p>',
            'fileid1':'10000054'
        }

        resp = http_post(url, parms)

        if None==resp or 'ret' not in resp:
            raise Exception('no ret')
        if '0'==resp['ret'] and 'appMsgId' in resp:
            return resp['appMsgId']
        if '-20000'==resp['ret']:
            return -1

        raise Exception('unknow ret')

    except Exception,e:
        print 'update_msg error resp_str='+resp_str, e
        logger.error('update_msg error resp_str='+resp_str, e)


def upload_cover_image(token, file, filename):
    resp_str = ''
    try:
        url = 'https://mp.weixin.qq.com/cgi-bin/uploadmaterial?cgi=uploadmaterial&type=2&t=iframe-uploadfile&lang=zh_CN&formId=1'

        url = url+'&token='+token

        parms = {'uploadfile':file,
            'Content-Disposition':'form-data; name="uploadfile"; filename="'+filename+'"',
            'Content-Type':'image/jpeg'
        }

        #注册poster这个handle
        opener = poster.streaminghttp.register_openers()
        opener.add_handler(cookies)

        #编码数据
        datagen, multipart_headers = poster.encode.multipart_encode(parms)

        post_headers = {}
        post_headers.update(headers)
        post_headers.update(multipart_headers)
        # print post_headers

        req  = urllib2.Request(url, datagen, post_headers)

        # 上传文件并获得响应信息
        resp_str = urllib2.urlopen(req).read()
        # print resp_str

        if None==resp_str or ''==resp_str:
            raise Exception("None==resp_str")
        m = re.search(r'formId,\ \'(\d+)\'', resp_str)
        if None==m:
            raise Exception("no formId")
        return m.group(1)

    except Exception,e:
        print 'upload_cover_image error resp_str='+resp_str, e
        logger.error('upload_cover_image error resp_str='+resp_str, e)


def upload_image(token, file, filename):
    resp_str = ''
    try:
        url = 'https://mp.weixin.qq.com/cgi-bin/uploadimg2cdn?t=ajax-editor-upload-img&lang=zh_CN'

        url = url+'&token='+token

        parms = {'upfile':file,
            'Content-Disposition':'form-data; name="upfile"; filename="'+filename+'"',
            'Content-Type':'image/jpeg'
        }

        #注册poster这个handle
        opener = poster.streaminghttp.register_openers()
        opener.add_handler(cookies)

        #编码数据
        datagen, multipart_headers = poster.encode.multipart_encode(parms)

        post_headers = {}
        post_headers.update(headers)
        post_headers.update(multipart_headers)
        # print post_headers

        req  = urllib2.Request(url, datagen, post_headers)

        # 上传文件并获得响应信息
        resp_str = urllib2.urlopen(req).read()
        # print resp_str

        if None==resp_str or ''==resp_str:
            raise Exception("None==resp_str")
        resp = eval(resp_str)
        if None==resp or 'url' not in resp:
            raise Exception("no url")
        return resp['url']

    except Exception,e:
        print 'upload_image error resp_str='+resp_str, e
        logger.error('upload_image error resp_str='+resp_str, e) 


def download_file(url, file_type):
    # temp = tempfile.NamedTemporaryFile()
    temp_path = tempfile.mktemp()
    if None!=file_type and ''!=file_type:
        temp_path = temp_path+'.'+file_type
    temp = open(temp_path, 'wb')
    resp = urllib2.urlopen(url).read()
    temp.write(resp)

    return temp_path


def login_and_send(appmsgid, tofakeid):
    global token, cookies

    if None==token or None==cookies:
        token = login(username, pwd)
    code = send(token, '10000006', '3957225')
    if 0==code:
        return
    if -1==code:
        token = login(username, pwd)
        code = send(token, '10000006', '3957225')
        if 0==code:
            return
    raise Exception("login_and_send error")


if __name__=="__main__":
    token = login(username, pwd)
    print token

    # url = 'http://mmsns.qpic.cn/mmsns/vD2tCj81DvCBma5iaeLwOgfQGPew83Qk9vGTqaIv1mTH375AN3IlsDQ/0'
    # file_name = download_file(url, 'jpg')
    # print file_name

    # pic = '/Users/chirking/workspace/github/zjdr/tmp/xlk.jpg'
    # filename = 'tmpbspWjI'

    # formId = upload_cover_image(token, open(file_name, "rb"), filename)
    # print formId

    # url = upload_image(token, open(file_name, "rb"), filename)
    # print url

    # appmsgid = create_msg(token)
    # print appmsgid

    # update_appmsgid = update_msg(token, appmsgid)
    # print update_appmsgid   

    login_and_send('10000059', '3957225')


