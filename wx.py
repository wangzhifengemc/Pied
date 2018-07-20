#coding=utf8
import requests
import itchat 
from itchat.content import *
import paho.mqtt.client as mqtt
import time

import sys
reload(sys)
sys.setdefaultencoding( "utf8" )
c = mqtt.Mosquitto()
c.connect("test.mosquitto.org")

def get_response(msg):
    if msg == 'STATUS':
        r=requests.get('https://wzf001.cfapps.io/getstatus.html')
        return 'Get Status:'+r.text

    apiUrl = 'https://wzf001.cfapps.io/suthankyou.html'
    data = {
        'LambSwitch'   : msg,
    }
    try:
        print 'Begin getstatus, Time:',time.asctime(time.localtime(time.time()))
        r = requests.post(apiUrl, data=data)
#        r = requests.post(apiUrl, data=data).json()
        print 'Status:', r.text, 'Time:',time.asctime(time.localtime(time.time()))
        c.publish("wzf01","SET")
        print 'publish'
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
#        print r.text
        return 'Set Status:'+msg
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return 'Internal Error'
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    global c
    if msg['FromUserName'] == myid:
        print 'From me'
        return
    if msg['Text'] not in ['ON', 'OFF', 'AUTO', 'STATUS']:
#        print msg['Text']
        return 'Please input ON/OFF/AUTO/STATUS!'
#    print 'msg:', msg['Text']
#	if msg['Text'] in ['ON', 'OFF', 'AUTO']:
    reply = get_response(msg['Text'])
    return reply 


itchat.auto_login(hotReload=True)
myid = itchat.get_friends(update=True)[0]["UserName"]
itchat.run()
