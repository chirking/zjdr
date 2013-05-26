#coding=utf-8

from zjdr import app
from flask import request
import logging

# create logger
logger = logging.getLogger('zjdr.wx_zjdr')

from wx_msg import *

@app.route('/wx_zjdr', methods=['POST', 'GET'])
def wx_zjdr():
	try:
		if('echostr' in request.args):
			wxEchostr = WxEchostr(
				request.args.get('signature'),
				request.args.get('timestamp'),
				request.args.get('nonce'),
				request.args.get('echostr'))
			return wxEchostr.check_and_get_echostr()
		
		logger.warn("request: "+request.data)
		wx_msg = get_ReqMsg(request.data)

		if None==wx_msg:
			return 'success'
		resp_msg = wx_msg.receive()
		resp_xml = get_xml(resp_msg)

		logger.warn("response: "+resp_xml)
		return resp_xml
	except Exception, e:
		logger.warn("/wx_zjdr error:"+str(e))
		return '未知异常'
