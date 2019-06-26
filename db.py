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
line_bot_api = LineBotApi("Z89KlbPxoc+N16dQw2gIOBUj1nht+r3FZLqjnHdGHX/WUZ8WpdvueISiYf+0J71JNll4ZJBw+D3QEHDjI8AwqxMMcS8dISHLl5YKn+FEyEnWp3Yt7pqE+Pl7hJ/5bgBSYOeyniI/pBKiD89LfE6+dwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler('bd799d810b0b87531264f40763235c56')
to = "Ue7aa1b3d42ca4e7df1dc143cbc97d13c"
con = psycopg2.connect(
            host = 'ec2-54-83-192-245.compute-1.amazonaws.com',
            database = 'df3vg11r7cab9s',
            user = 'ouwlmxtvewdibl',
            password ='05f09b74d57c0cf93c2594966a1e03e06c7ba3605d56b46d8ecce6f61da50131',
            port = '5432')

#cursor
cur = con.cursor()
x= input('please input x= ')
def insert(a):
    
 #   cur.execute("insert into bicycles (userid) values (%s)",(str(a)))
    line_bot_api.push_message(to, TextSendMessage(text="Success"))
    cur.executemany("insert into bicycles (userid) values (%(Userid)s)",item)
#    print('Success')
#cur.execute("select city, date from weather")
#insert(x)
#rows = cur.fetchall()
if x=='yes':
    cur.executemany("insert into bicycles (userid) values (%(Userid)s)",item)
elif x== 'no':
    cur.executemany("insert into bicycles (userid) values (%(Name)s)",item)
#commit the transcation
con.commit()

#close the cur 
cur.close()

#close the connection
con.close()
