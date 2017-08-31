# -*- coding: utf-8 -*-
import os
import sae
import web
import model
from weixinInterface import WeixinInterface

urls = (
    '/weixin','WeixinInterface',
    '/chatByoO45c0iUoiaD0ApARWHTaWZomKas','ChatLog',
    '/ck','Feedback'
)

# ????
class ChatLog:
    def GET(self):
        chatCon = model.get_chat_content()
        return render.checkChat(chatCon)

# ????
class Feedback:
    def GET(self):
        fkcon = model.get_fkcontent()
        return render.checkfk(fkcon)

app_root = os.path.dirname(__file__)
templates_root = os.path.join(app_root, 'templates')
render = web.template.render(templates_root)

app = web.application(urls, globals()).wsgifunc()

application = sae.create_wsgi_app(app)