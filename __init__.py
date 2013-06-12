
import logger

from flask import Flask
app = Flask(__name__)

import zjdr.hello_world
import zjdr.wx_zjdr

import zjdr.admin.zjdr_admin
