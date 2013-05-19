from zjdr import app
from flask import request

@app.route('/wx_zjdr')
def wx_zjdr():
    return request.args.get('echostr')
