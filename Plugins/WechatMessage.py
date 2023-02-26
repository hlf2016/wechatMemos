import time
import xml.etree.ElementTree as ET

"""
解析微信XML消息
"""

def parse_xml(xml_data):
    xml_data = ET.fromstring(xml_data)
    msg_type = xml_data.find('MsgType').text
    if msg_type == 'text':
        return TextMsg(xml_data)
    elif msg_type == 'event':
        return EventMsg(xml_data)
    elif msg_type == 'voice':
        return VoiceMsg(xml_data)
    else:
        return Msg(xml_data)

class Msg(object):
    def __init__(self, xml_data):
        self.ToUserName = xml_data.find('ToUserName').text
        self.FromUserName = xml_data.find('FromUserName').text
        self.CreateTime = xml_data.find('CreateTime').text
        self.MsgType = xml_data.find('MsgType').text

class TextMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.Content = xml_data.find('Content').text

class EventMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.EventKey = xml_data.find('EventKey').text
        self.Event = xml_data.find('Event').text

class VoiceMsg(Msg):
    def __init__(self, xml_data):
        Msg.__init__(self, xml_data)
        self.Recognition = xml_data.find('Recognition').text

class Message:
    def __init__(self, ToUserName, FromUserName, Content):
        self.ToUserName = ToUserName
        self.FromUserName = FromUserName
        self.Content = Content

    def send(self):
        message = f"""
                    <xml>
                    <ToUserName><![CDATA[{self.ToUserName}]]></ToUserName>
                    <FromUserName><![CDATA[{self.FromUserName}]]></FromUserName>
                    <CreateTime>{int(time.time())}</CreateTime>
                    <MsgType><![CDATA[text]]></MsgType>
                    <Content><![CDATA[{self.Content}]]></Content>
                    </xml>
                    """
        return message


