#coding=utf-8

from xml.etree import ElementTree

MY_WEIXIN_ID = "chirking@outlook.com"

class WxEchostr(object):
	"""docstring for WxEchostr"""

	signature = None # 微信加密签名
	timestamp = None # 时间戳
	nonce = None # 随机数
	echostr = None # 随机字符串

	def __init__(self, signature, timestamp, nonce, echostr):
		self.signature = signature
		self.timestamp = timestamp
		self.nonce = nonce
		self.echostr = echostr

	def check_and_get_echostr(self):
		return self.echostr


class BaseWxMsg(object):
	"""docstring for BaseWxMsg"""

	ToUserName = None # 开发者微信号
	FromUserName = None # 发送方帐号（一个OpenID）
	CreateTime = None # 消息创建时间 （整型）
	MsgType = None # text

	def __str__(self):
		return str(self.__dict__)

	def receive(self):
		pass


class BaseWxContentMsg(BaseWxMsg):
	"""docstring for BaseWxTextMsg"""
	
	MsgId = None # 消息id，64位整型


class BaseWxEventMsg(BaseWxMsg):
	"""docstring for BaseWxEvent"""

	Event = None # 事件类型，subscribe(订阅)、unsubscribe(取消订阅)、CLICK(自定义菜单点击事件)
	EventKey = None # 事件KEY值，与自定义菜单接口中KEY值对应
		

class TextWxMsg(BaseWxContentMsg):
	"""docstring for TextWxMsg"""

	Content = None # 文本消息内容

	def receive(self):
		pass


class ImageWxMsg(BaseWxContentMsg):
	"""docstring for TextWxMsg"""

	PicUrl = None # 图片链接

	def receive(self):
		pass


class LocationWxMsg(BaseWxContentMsg):
	"""docstring for TextWxMsg"""

	Location_X = None # 地理位置纬度
	Location_Y = None # 地理位置经度
	Scale = None # 地图缩放大小
	Label = None # 地理位置信息

	def receive(self):
		pass


class LinkWxMsg(BaseWxContentMsg):
	"""docstring for TextWxMsg"""

	Title = None # 消息标题
	Description = None # 消息描述
	Url = None # 消息链接

	def receive(self):
		pass

		
class SubscribeWxEventMsg(BaseWxEventMsg):
	"""docstring for EventWxMsg"""

	def receive(self):
		pass


class UnSubscribeWxEventMsg(BaseWxEventMsg):
	"""docstring for UnSubscribeWxEventMsg"""

	def receive(self):
		pass


class ClickWxEventMsg(BaseWxEventMsg):
	"""docstring for ClickWxEventMsg"""

	def receive(self):
		pass


def get_WxMsg(xml):
	if None==xml or ''==xml:
		return None
	root = ElementTree.fromstring(xml).getiterator("xml")
	if None==root or 0==len(root):
		return None;
	root = root[0]

	MsgType = get_text_from_Node("MsgType", root)

	wxMsg = None

	if 'text'==MsgType:
		wxMsg = TextWxMsg()
		wxMsg.Content = get_text_from_Node("Content", root)
	elif 'image'==MsgType:
		wxMsg = ImageWxMsg()
		wxMsg.PicUrl = get_text_from_Node("PicUrl", root)
	elif 'location'==MsgType:
		wxMsg = LocationWxMsg()
		wxMsg.Location_X = get_text_from_Node("Location_X", root)
		wxMsg.Location_Y = get_text_from_Node("Location_Y", root)
		wxMsg.Scale = get_text_from_Node("Scale", root)
		wxMsg.Label = get_text_from_Node("Label", root)
	elif 'link'==MsgType:
		wxMsg = LinkWxMsg()
		wxMsg.Title = get_text_from_Node("Title", root)
		wxMsg.Description = get_text_from_Node("Description", root)
		wxMsg.Url = get_text_from_Node("Url", root)
	elif 'event'==MsgType:
		Event = get_text_from_Node("Event", root)
		if 'subscribe'==Event:
			wxMsg = SubscribeWxEventMsg()
		elif 'unsubscribe'==Event:
			wxMsg = UnSubscribeWxEventMsg()
		elif 'CLICK'==Event:
			wxMsg = ClickWxEventMsg()
		else:
			return None
		wxMsg.Event = Event
		wxMsg.EventKey = get_text_from_Node("EventKey", root)
	else:
		return None

	wxMsg.ToUserName = get_text_from_Node("ToUserName", root)
	wxMsg.FromUserName = get_text_from_Node("FromUserName", root)
	wxMsg.CreateTime = get_text_from_Node("CreateTime", root)
	wxMsg.MsgType = get_text_from_Node("MsgType", root)

	return wxMsg


def get_text_from_Node(name, node):
	nodes = node.getiterator(name)
	if None==nodes or 0==len(nodes):
		return None;
	return nodes[0].text


def get_xml(wxMsg):
	pass


if __name__=="__main__":
	xml='''
		<xml>
		 <ToUserName><![CDATA[toUser]]></ToUserName>
		 <FromUserName><![CDATA[fromUser]]></FromUserName> 
		 <CreateTime>1348831860</CreateTime>
		 <MsgType><![CDATA[text]]></MsgType>
		 <Content><![CDATA[this is a test]]></Content>
		 <MsgId>1234567890123456</MsgId>
		</xml>
	'''

	print get_WxMsg(xml)

	pass

		