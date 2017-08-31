# -*- coding: utf-8 -*-
import hashlib
import web
import lxml
import time
import os
import urllib2,json
from lxml import etree
import re
import random
from urllib import urlencode
import json
import pylibmc
import function
import model
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class WeixinInterface:

    def __init__(self):
        self.app_root = os.path.dirname(__file__)
        self.templates_root = os.path.join(self.app_root, 'templates')
        self.render = web.template.render(self.templates_root)

    def GET(self):
        try:
            #获取输入参数
            data = web.input()
            signature=data.signature
            timestamp=data.timestamp
            nonce=data.nonce
            echostr=data.echostr
            #自己的token
            token="sagewang" #这里改写你在微信公众平台里输入的token
            #字典序排序
            list=[token,timestamp,nonce]
            list.sort()
            sha1=hashlib.sha1()
            map(sha1.update,list)
            hashcode=sha1.hexdigest()
            print "handle/GET func: hashcode, signature: ", hashcode, signature
            #sha1加密算法

            #如果是来自微信的请求，则回复echostr
            if hashcode == signature:
                return echostr
            else:
                return "no weixin"
        except Exception, Argument:
            return "Exception: " + Argument

    def POST(self):
        str_xml = web.data()  # 获得post来的数据
        xml = etree.fromstring(str_xml)  # 进行XML解析
        msgType = xml.find("MsgType").text
        fromUser = xml.find("FromUserName").text
        toUser = xml.find("ToUserName").text
        mc = pylibmc.Client()  # 初始化一个memcache实例用来保存用户的操作
        # count = 0 # 记录聊天次数

        if msgType == "event":
            mscontent = xml.find("Event").text
            if mscontent == "subscribe":
                replayText = u'''欢迎关注本微信，这个微信是本人业余爱好所建立，也是想一边学习Python一边玩的东西,现在还没有太多功能，只有一些小玩意。你们有什么好的文章也欢迎反馈给我,我会不定期的分享给大家，输入'help'查看操作指令'''
                return self.render.reply_text(fromUser, toUser, int(time.time()), replayText)
            if mscontent == "unsubscribe":
                replayText = u'我现在功能还很简单，知道满足不了您的需求，但是我会慢慢改进，欢迎您以后再来！'
                return self.render.reply_text(fromUser, toUser, int(time.time()), replayText)
        elif msgType == 'text':
            content = xml.find("Content").text
            if content.startswith('fk'):
                fktime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
                model.addfk(fromUser, fktime, content[3:].encode('utf-8'))
                return self.render.reply_text(fromUser, toUser, int(time.time()), u'感谢您的反馈')
            if content.lower() == 'bye':
                byeTime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
                model.addChat(fromUser, byeTime, u'bye')
                mc.delete(fromUser + '_ali')
                return self.render.reply_text(fromUser, toUser, int(time.time()), u'您已经跳出了和小阿狸的交谈中，输入help来显示操作指令')
            if content.lower() == 'ali':
                startTime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
                model.addChat(fromUser, startTime, u'start')
                mc.set(fromUser + '_ali', 'ali')
                return self.render.reply_text(fromUser, toUser, int(time.time()),
                                              u'您已经进入与小阿狸的交谈中，请尽情的蹂躏它吧！输入bye跳出与小阿狸的交谈')
            # 读取memcache中的缓存数据
            mcxhj = mc.get(fromUser + '_ali')
            if mcxhj == 'ali':
                beginTime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
                model.addChat(fromUser, str(beginTime), content.encode('utf-8'))
                reply_text = function.chat(content,fromUser)
                endTime = time.strftime('%Y-%m-%d %H:%M', time.localtime())
                model.addChat("ali", endTime, reply_text.encode('utf-8'))
                # fromUser = oO45c0iUoiaD0ApARWHTaWZomKas
                if u'微信' in reply_text:
                    reply_text = u"小阿狸脑袋出问题了，请换个问题吧~"
                return self.render.reply_text(fromUser, toUser, int(time.time()), reply_text)

            # elif content == 'm': # 听音乐
            #     musicdata = []
            #     # musicdata = function.music()
            #     musicList = [
            #         [r'http://mp3.flash127.com/music/23472.mp3', u'消愁-毛不易', u'人生苦短何必念念不忘'],
            #         [r'http://mp3.flash127.com/music/13533.mp3', u'演员-薛之谦', u'该配合你演出的我尽力在表演，像情感节目里的嘉宾任人挑选'],
            #         [r'http://mp3.flash127.com/music/20972.mp3', u'暧昧-薛之谦', u'反正现在的感情 都暧昧'],
            #         [r'http://mp3.flash127.com/music/7419.mp3', u'后来的我们-五月天', u'后来的我们 我期待着 泪水中能看到 你真的 自由了']
            #     ]
            #     musicdata = random.choice(musicList)
            #     musicurl = musicdata[0]
            #     musictitle = musicdata[1]
            #     musicdes = musicdata[2]
            #     return self.render.reply_music(fromUser, toUser, int(time.time()), musictitle, musicdes, musicurl)
            if content == u"段子":
                output = function.joke()
                return self.render.reply_text(fromUser, toUser, int(time.time()), output)
            if u"天气" in content:  # 天气功能判断，实现汉字查询天气,上海天气
                # content = "上海天气"
                output = function.weather(content)
                return self.render.reply_text(fromUser, toUser, int(time.time()), output)
            if content == u"你是谁":
                return self.render.reply_text(fromUser, toUser, int(time.time()), "我是主人的小女友！\n 输入'help'看看如何正确的调戏我?")
            if content == 'help':
                output =function.help()
                return self.render.reply_text(fromUser, toUser, int(time.time()), output)
            if content[0:2] == 'fy':
                content = content.encode('UTF-8')
                Nword = function.youdao(content)
                return self.render.reply_text(fromUser, toUser, int(time.time()), Nword)
            else:
                return self.render.reply_text(fromUser, toUser, int(time.time()), "哎呀出错了 输入个help看看如何正确的调戏我？")

