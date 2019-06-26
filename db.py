import psycopg2
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
#from app import *
#conncect to the db
item =[{'Userid':'2','Name':'name'}]
con = psycopg2.connect(
            host = 'ec2-54-83-192-245.compute-1.amazonaws.com',
            database = 'df3vg11r7cab9s',
            user = 'ouwlmxtvewdibl',
            password ='05f09b74d57c0cf93c2594966a1e03e06c7ba3605d56b46d8ecce6f61da50131',
            port = '5432')

#cursor
cur = con.cursor()
#x= input('please input x= ')
#cur.execute("insert into weather (city,date) values ('tapei','2014-11-29' )",)


def insert(a):
    #cur.executemany("insert into bicycles (userid) values (%(Userid)s)",item)
 #   cur.execute("insert into bicycles (userid) values (%s)",(str(a)))
    line_bot_api.push_message(to, TextSendMessage(text="Success"))
#    print('Success')
#cur.execute("select city, date from weather")
#insert(x)
#rows = cur.fetchall()

#commit the transcation
con.commit()

#close the cur 
cur.close()

#close the connection
con.close()
