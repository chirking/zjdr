#coding=utf-8

class BaseWxMsg(object):
	"""docstring for BaseWxMsg"""
	def __init__(self, arg):
		super(BaseWxMsg, self).__init__()
		self.arg = arg

class TextWxMsg(BaseWxMsg):
	"""docstring for TextWxMsg"""
	def __init__(self, arg):
		super(TextWxMsg, self).__init__()
		self.arg = arg
		
class EventWxMsg(BaseWxMsg):
	"""docstring for EventWxMsg"""
	def __init__(self, arg):
		super(EventWxMsg, self).__init__()
		self.arg = arg
		

def getWxMsg():
	pass