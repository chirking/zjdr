from zjdr import app
from flask import request

from mongo import db_zjdr

@app.route('/wx_zjdr')
def wx_zjdr():
    if('echostr' in request.args):
    	return request.args.get('echostr')
    print request.form
    return 'hehe'
