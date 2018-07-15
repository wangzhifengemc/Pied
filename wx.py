#coding=utf8
import requests
import itchat 
from itchat.content import *

import sys
reload(sys)
sys.setdefaultencoding( "utf8" )


def get_response(msg):
    apiUrl = 'http://127.0.0.1:5000/suthankyou.html'
    data = {
        'LambSwitch'   : msg,
    }
    try:
        r = requests.post(apiUrl, data=data)
#        r = requests.post(apiUrl, data=data).json()
        # 字典的get方法在字典没有'text'值的时候会返回None而不会抛出异常
#        print r.text
        return r.text
    # 为了防止服务器没有正常响应导致程序异常退出，这里用try-except捕获了异常
    # 如果服务器没能正常交互（返回非json或无法连接），那么就会进入下面的return
    except:
        # 将会返回一个None
        return
@itchat.msg_register(itchat.content.TEXT)
def tuling_reply(msg):
    if msg['FromUserName'] == myid:
        print 'From me'
        return
    if msg['Text'] not in ['ON', 'OFF', 'AUTO']:
#        print msg['Text']
        return 'Please input ON/OFF/AUTO!'
#    print 'msg:', msg['Text']
    reply = get_response(msg['Text'])
    s='Status:'+msg['Text']
    return s 


itchat.auto_login(hotReload=True)
myid = itchat.get_friends(update=True)[0]["UserName"]
itchat.run()
