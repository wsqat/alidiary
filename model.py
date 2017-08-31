# _*_ coding:utf-8 _*_
import web
import web.db
import sae.const

chatTab = 'chat'
fkTab = 'fk'

db = web.database(
    dbn='mysql',
    host=sae.const.MYSQL_HOST, # 主数据库域名（读写）
    # host=sae.const.MYSQL_HOST_S,  从数据库域名（只读）
    port=int(sae.const.MYSQL_PORT),
    user=sae.const.MYSQL_USER,
    passwd=sae.const.MYSQL_PASS,
    db=sae.const.MYSQL_DB
)

def addChat(username, chatTime, chatContent):
    return db.insert(chatTab, userId=username, time=chatTime, content=chatContent)

def get_chat_content():
    return db.select(chatTab, order='id')


def addfk(username, fktime, fkcontent):
    return db.insert(fkTab, user=username, time=fktime, fk_content=fkcontent)


def get_fkcontent():
    return db.select(fkTab, order='id')