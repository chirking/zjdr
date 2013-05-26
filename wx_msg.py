#coding=utf-8

from xml.etree import ElementTree

MY_WEIXIN_ID = "chirking@outlook.com"
SYS_ENCODING = "UTF-8"

class Echostr(object):
	"""docstring for Echostr"""

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


class BaseMsg(object):
	"""docstring for BaseMsg"""

	ToUserName = None # 开发者微信号
	FromUserName = None # 发送方帐号（一个OpenID）
	CreateTime = None # 消息创建时间 （整型）
	MsgType = None # text

	def __str__(self):
		return str(self.__dict__)

	def receive(self):
		pass


class BaseReqMsg(BaseMsg):
		"""docstring for BaseReqMsg"""


class BaseRespMsg(BaseMsg):
	"""docstring for BaseResp"""

	def __init__(self, ToUserName, CreateTime=None):
		self.FromUserName = MY_WEIXIN_ID
		self.ToUserName = ToUserName
		self.CreateTime = CreateTime


class BaseContentMsg(BaseReqMsg):
	"""docstring for BaseTextMsg"""
	
	MsgId = None # 消息id，64位整型


class BaseEventMsg(BaseReqMsg):
	"""docstring for BaseEvent"""

	MsgType = 'event'
	Event = None # 事件类型，subscribe(订阅)、unsubscribe(取消订阅)、CLICK(自定义菜单点击事件)
	EventKey = None # 事件KEY值，与自定义菜单接口中KEY值对应
		

class TextMsg(BaseContentMsg):
	"""docstring for TextMsg"""

	MsgType = 'text'
	Content = None # 文本消息内容

	def receive(self):
		Msg = RespTextMsg(self.FromUserName, int(self.CreateTime)+1)

		Msg.Content = '呵呵'

		return Msg


class ImageMsg(BaseContentMsg):
	"""docstring for TextMsg"""

	MsgType = 'image'
	PicUrl = None # 图片链接

	def receive(self):
		pass


class LocationMsg(BaseContentMsg):
	"""docstring for TextMsg"""

	MsgType = 'location'
	Location_X = None # 地理位置纬度
	Location_Y = None # 地理位置经度
	Scale = None # 地图缩放大小
	Label = None # 地理位置信息

	def receive(self):
		pass


class LinkMsg(BaseContentMsg):
	"""docstring for TextMsg"""

	MsgType = 'like'
	Title = None # 消息标题
	Description = None # 消息描述
	Url = None # 消息链接

	def receive(self):
		pass

		
class SubscribeEventMsg(BaseEventMsg):
	"""docstring for EventMsg"""

	Event = 'subscribe'

	def receive(self):
		pass


class UnSubscribeEventMsg(BaseEventMsg):
	"""docstring for UnSubscribeEventMsg"""

	Event = 'unsubscribe'

	def receive(self):
		pass


class ClickEventMsg(BaseEventMsg):
	"""docstring for ClickEventMsg"""

	Event = 'CLICK'

	def receive(self):
		pass


class BaseRespContentMsg(BaseRespMsg):
	"""docstring for BaseRespContentMsg"""

	FuncFlag = 1 # 位0x0001被标志时，星标刚收到的消息。
	

class RespTextMsg(BaseRespContentMsg):
	"""docstring for RespTextMsg"""
		
	MsgType = 'text'
	Content = None # 回复的消息内容,长度不超过2048字节
				

class RespMusicMsg(BaseRespContentMsg):
	"""docstring for RespMusicMsg"""
	
	MsgType = 'music'
	MusicUrl = None # 音乐链接
	HQMusicUrl = None # 高质量音乐链接，WIFI环境优先使用该链接播放音乐


class RespNewsMsg(BaseRespContentMsg):
	"""docstring for RespNewsMsg"""
		
	MsgType = 'news'
	ArticleCount = None # 图文消息个数，限制为10条以内
	Articles = None # 多条图文消息信息，默认第一个item为大图
	Title = None # 图文消息标题
	Description = None # 图文消息描述
	PicUrl = None # 图片链接，支持JPG、PNG格式，较好的效果为大图640*320，小图80*80。
	Url = None # 点击图文消息跳转链接



def get_ReqMsg(xml):
	if None==xml or ''==xml:
		return None
	root = ElementTree.fromstring(xml).getiterator("xml")
	if None==root or 0==len(root):
		return None;
	root = root[0]

	MsgType = get_text_from_Node("MsgType", root)

	msg = None

	if 'text'==MsgType:
		msg = TextMsg()
		msg.Content = get_text_from_Node("Content", root)
	elif 'image'==MsgType:
		msg = ImageMsg()
		msg.PicUrl = get_text_from_Node("PicUrl", root)
	elif 'location'==MsgType:
		msg = LocationMsg()
		msg.Location_X = get_text_from_Node("Location_X", root)
		msg.Location_Y = get_text_from_Node("Location_Y", root)
		msg.Scale = get_text_from_Node("Scale", root)
		msg.Label = get_text_from_Node("Label", root)
	elif 'link'==MsgType:
		msg = LinkMsg()
		msg.Title = get_text_from_Node("Title", root)
		msg.Description = get_text_from_Node("Description", root)
		msg.Url = get_text_from_Node("Url", root)
	elif 'event'==MsgType:
		Event = get_text_from_Node("Event", root)
		if 'subscribe'==Event:
			msg = SubscribeEventMsg()
		elif 'unsubscribe'==Event:
			msg = UnSubscribeEventMsg()
		elif 'CLICK'==Event:
			msg = ClickEventMsg()
		else:
			return None
		msg.Event = Event
		msg.EventKey = get_text_from_Node("EventKey", root)
	else:
		return None

	msg.ToUserName = get_text_from_Node("ToUserName", root)
	msg.FromUserName = get_text_from_Node("FromUserName", root)
	msg.CreateTime = get_text_from_Node("CreateTime", root)

	return msg


def get_text_from_Node(name, node):
	nodes = node.getiterator(name)
	if None==nodes or 0==len(nodes):
		return None;
	return nodes[0].text


def get_xml(respMsg):
	if None==respMsg:
		return None

	root = ElementTree.Element('xml')

	ElementTree.SubElement(root, "ToUserName").text = getElementText(respMsg.ToUserName)
	ElementTree.SubElement(root, "FromUserName").text = getElementText(respMsg.FromUserName)
	ElementTree.SubElement(root, "CreateTime").text = getElementText(respMsg.CreateTime)
	ElementTree.SubElement(root, "MsgType").text = getElementText(respMsg.MsgType)

	ElementTree.SubElement(root, "FuncFlag").text = getElementText(respMsg.FuncFlag)

	MsgType = respMsg.MsgType
	if 'text'==MsgType:
		ElementTree.SubElement(root, "Content").text = getElementText(respMsg.Content)
	elif 'music'==MsgType:
		ElementTree.SubElement(root, "MusicUrl").text = getElementText(respMsg.MusicUrl)
		ElementTree.SubElement(root, "HQMusicUrl").text = getElementText(respMsg.HQMusicUrl)
	elif 'news'==MsgType:
		pass
		# TODO
	else:
		pass

	return ElementTree.tostring(root)

def getElementText(text):
	if None==text:
		return None

	return str(text).decode(SYS_ENCODING)
	#return '<![CDATA['+str(text).decode(SYS_ENCODING)+']]>'


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

	msg = get_ReqMsg(xml)
	print msg

	resp_msg = Msg.receive() 
	print resp_msg

	print get_xml(resp_msg)

	pass

		