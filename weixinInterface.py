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
        if msgType == 'text':
            content = xml.find("Content").text
            if content == 'help':
                return self.render.reply_text(fromUser, toUser, int(time.time()), "1、输入指令，如:段子，看搞笑段子。\n2输入城市+天气，如:上海天气，查询天气。\n3、更多功能，敬请期待……")
            elif content == u"段子":
                url_8 = "http://www.qiushibaike.com/"
                url_24 = "http://www.qiushibaike.com/hot/"
                headers = {
                    'Connection': 'Keep-Alive',
                    'Accept': 'text/html, application/xhtml+xml, */*',
                    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'}
                req_8 = urllib2.Request(url_8, headers=headers)
                req_24 = urllib2.Request(url_24, headers=headers)
                opener_8 = urllib2.urlopen(req_8)
                opener_24 = urllib2.urlopen(req_24)
                html_8 = opener_8.read()
                html_24 = opener_24.read()
                rex = r'(?<=div class="content">).*?(?=<!--)'
                m_8 = re.findall(rex, html_8, re.S)
                m_24 = re.findall(rex, html_24, re.S)
                m_8.extend(m_24)
                random.shuffle(m_8)
                text = m_8[0].replace('<br/>', '').replace('\n', '')
                # print text 清洗<>标签
                p = re.compile('<[^>]+>')
                # print p.sub("", text)
                return self.render.reply_text(fromUser, toUser, int(time.time()), p.sub("", text))
            elif u"天气" in content:  # 天气功能判断，实现汉字查询天气,上海天气
                # content = "上海天气"
                cityname = content.split("天气")[0]
                host = 'http://jisutqybmf.market.alicloudapi.com'
                path = '/weather/query'
                method = 'GET'
                appcode = '7f21d6917d4245fab6c38172d04ef6c0'
                # querys = 'city=%E5%AE%89%E9%A1%BA&citycode=citycode&cityid=cityid&ip=ip&location=location'
                data = {'city': cityname}
                querys = urlencode(data)
                print querys
                # querys = cityName+'&citycode=citycode&cityid=cityid&ip=ip&location=location'
                # querys = cityName
                bodys = {}
                url = host + path + '?' + querys
                request = urllib2.Request(url)
                request.add_header('Authorization', 'APPCODE ' + appcode)
                response = urllib2.urlopen(request)
                content = response.read()

                if content:
                    data = json.loads(content)  # 使用json库将字符转化为字典
                    res = data["result"]
                    sport = res["index"][1]['detail']  #运动指数
                    air = res["index"][5]['detail']  #空气指数
                    clothes = res["index"][6]['detail']  #穿衣指数
                    str_temp = ("%s，最低气温%s，最高气温%s。") % (res["weather"], res["templow"], res["temphigh"])  # 格式化字符
                    output = u"主人，"+res["city"]+"的天气是：" + str_temp + "\n1、"+ sport+"\n2、"+air+"\n3、"+clothes  # 输出天气信息

                return self.render.reply_text(fromUser, toUser, int(time.time()), output)
            elif content == u"你是谁":
                return self.render.reply_text(fromUser, toUser, int(time.time()), "我是主人的小女友！")
            else:
                return self.render.reply_text(fromUser, toUser, int(time.time()), "哎呀出错了 输入个help看看如何正确的调戏我？")