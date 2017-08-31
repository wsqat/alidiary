# -*- coding: utf-8 -*-
import json
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
import urllib, urllib2, sys
# from urllib2 import quote
from urllib import urlencode
import random
import hashlib
import re
import pylibmc

# help
def help():
    output = "1、看段子，输入指令，如:'段子'，看搞笑段子。\n2、天气查询，输入城市+天气，如:'上海天气'，查询上海天气。" \
             "\n3、英汉互译，输入fy+要翻译的内容，如：'fy+hello'，翻译'hello'。" \
             "\n4、调戏小阿狸，输入'ali'即可进入聊天模式，输入'bye'退出聊天模式。" \
             "\n5、反馈功能，输入fk+要反馈的内容，如：'fk+小阿狸真可爱！'。" \
             "\n更多功能，敬请期待……"
    return output

# 找段子
def joke():
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
    output = p.sub("", text)
    return output

# 天气查询
def weather(content):
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
        return output
    else:
        return u"主人，我还还查到，请再按照如下格式重新输入（如'上海天气'）！"

# 有道翻译
def youdao(word):
    # API:http://ai.youdao.com/docs/api.s
    salt = random.randint(10, 20)
    # print salt
    # query = "good";
    query = word.split("+")[1]
    # query = word
    # from = "EN";
    # to = "zh-CHS";
    # 应用ID
    appKey ="3fd00b4d30f39b06";
    # 应用密钥
    key = "B8o9gJ7Z2oMEJozEZxrSNL3oUxffSC2m"
    # sign = md5(appKey + query + salt+ key);
    # md5
    m2 = hashlib.md5()
    m2.update(appKey + query + str(salt) + key)
    sign = m2.hexdigest()
    # print sign
    data = {
        'q': query,
        # 'from': 'EN',
        # 'to': 'zh_CHS',
        'from': 'auto',
        'to': 'auto',
        'appKey': appKey,
        'salt': salt,
        'sign': sign
    }

    querys = urlencode(data)
    # print querys
    url = "http://openapi.youdao.com/api?" + querys
    resp = urllib2.urlopen(url)
    fanyi = json.loads(resp.read())
    # print fanyi['errorCode']
    # print fanyi['translation']
    # print fanyi['basic']['phonetic']
    if fanyi["errorCode"]:
        print fanyi['translation']
        if 'basic' in fanyi.keys():
            trans = u'%s:\n%s\n%s\n网络释义：\n%s' % (
            fanyi['query'], ''.join(fanyi['translation']), ' '.join(fanyi['basic']['explains']),
            '，'.join(fanyi['web'][0]['value']))
            return trans
        else:
            trans = u'%s:\n基本翻译:%s\n' % (fanyi['query'], ''.join(fanyi['translation']))
            return trans
    else:
        return u"主人，我还还查到，请再按照如下格式重新输入（如'fy+hello'）！"


# 听音乐
# def music():
#     musicList = [
#         [r'http://mp3.flash127.com/music/23472.mp3',u'消愁-毛不易', u'人生苦短何必念念不忘'],
#         [r'http://mp3.flash127.com/music/13533.mp3',u'演员-薛之谦',u'该配合你演出的我尽力在表演，像情感节目里的嘉宾任人挑选'],
#         [r'http://mp3.flash127.com/music/20972.mp3', u'暧昧-薛之谦', u'反正现在的感情 都暧昧'],
#         [r'http://mp3.flash127.com/music/7419.mp3', u'后来的我们-五月天', u'后来的我们 我期待着 泪水中能看到 你真的 自由了']
#     ]
#     musicData =  random.choice(musicList)
#     return musicData

# 聊天
# def xiaohuangji(ask):
#     # http: // sandbox.api.simsimi.com / request.p?key = your_trial_key & lc = en & ft = 1.0 & text = hi
#     ask = ask.encode('UTF-8')
#     key = '41250a68-3cb5-43c8-9aa2-d7b3caf519b1'
#     data = {
#         'key':key,
#         'lc':'en',
#         'ft':'1.0',
#         'text':ask
#     }
#     query = urllib2.quote(data)
#
#     url = r'http://api.simsimi.com/request.p?'+ query
#     # url = baseurl + enask + '&lc=ch&ft=0.0'
#     resp = urllib2.urlopen(url)
#     reson = json.loads(resp.read)
#     return reson

# tuling123  图灵机器人,userId场景对话
def chat(ask,userid):
    ask = ask.encode('UTF-8')
    key = '5fe392e70ffc42b693833f695e5389f3'
    # userid = '1111'
    data = {
        'key': key,
        'info': ask,
        'userid': userid
    }

    textmod = json.dumps(data)

    header_dict = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Trident/7.0; rv:11.0) like Gecko',
                   "Content-Type": "application/json"}
    url = 'http://www.tuling123.com/openapi/api'
    req = urllib2.Request(url=url, data=textmod, headers=header_dict)
    resp = urllib2.urlopen(req)
    res = resp.read()
    reson = json.loads(res)
    if reson['code']:
        return reson['text']
    else:
        return u"主人，我的小脑子出问题了，请换个问题吧~"