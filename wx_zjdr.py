from zjdr import app
from flask import request

from wx_msg import *

@app.route('/wx_zjdr')
def wx_zjdr():
	if('echostr' in request.args):
		wxEchostr = WxEchostr(
			request.args.get('signature'),
			request.args.get('timestamp'),
			request.args.get('nonce'),
			request.args.get('echostr'))
		return wxEchostr.check_and_get_echostr()
	
	print request.form
	wx_msg = get_WxMsg(request.form['aa'])

	if None==wx_msg:
		return None
	return_msg = wx_msg.receive()
	return get_xml(return_msg)
