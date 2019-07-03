from flask import Flask, request, abort
from flask_sqlalchemy import SQLAlchemy
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import psycopg2
import datetime
import os
from dbmodle import *
app = Flask(__name__)
#conncect to the db

# con = psycopg2.connect(
#             host = 'ec2-54-83-192-245.compute-1.amazonaws.com',
#             database = 'df3vg11r7cab9s',
#             user = 'ouwlmxtvewdibl',
#             password ='05f09b74d57c0cf93c2594966a1e03e06c7ba3605d56b46d8ecce6f61da50131',
#             port = '5432')
# cur = con.cursor()
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ouwlmxtvewdibl:05f09b74d57c0cf93c2594966a1e03e06c7ba3605d56b46d8ecce6f61da50131@ec2-54-83-192-245.compute-1.amazonaws.com:5432/df3vg11r7cab9s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)

manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Channel Access Token
line_bot_api = LineBotApi("Z89KlbPxoc+N16dQw2gIOBUj1nht+r3FZLqjnHdGHX/WUZ8WpdvueISiYf+0J71JNll4ZJBw+D3QEHDjI8AwqxMMcS8dISHLl5YKn+FEyEnWp3Yt7pqE+Pl7hJ/5bgBSYOeyniI/pBKiD89LfE6+dwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler('bd799d810b0b87531264f40763235c56')
to = "Ue7aa1b3d42ca4e7df1dc143cbc97d13c"
#變數、類別
levelname = ["新生", "國小低年級", "國小中年級", "國小高年級", "國中一年級", "國中二年級", "國中三年級", "高中一年級", "高中二年級", "高中三年級", "大學一年級", "大學二年級", "大學三年級", "大學四年級", "碩士", "博士", "博士後研究", "助理教授", "副教授", "教授", "校長"]
item = {'UserId' : 'UserId',
        'Name' : '未填',
        'Num' : '未填',
        'Time' : 'Time',
        'Address' : 'Address',
        'Photo' : 'Photo',
        'City' : 'City',
        'Detail' : 'Detail',
        'Handler' : 'Handler',
        'Status' : 'Status',
        'Score' : 'Score',
        'Updatedate' : 'Updatedate'}

#選單
#大廳
title_btn =ButtonsTemplate(
                            thumbnail_image_url="https://scontent.ftpe12-1.fna.fbcdn.net/v/t1.0-9/60502088_868260083527412_4497744968470757376_n.png?_nc_cat=103&_nc_ht=scontent.ftpe12-1.fna&oh=33c77713dcab51e5e26f307cf3eae86e&oe=5D54CF9A",
                            title='您好，這是【廢棄腳踏車~重生!】活動大廳，小智機器人在此為您服務', 
                            text='Please select',
                            actions=[
                            MessageTemplateAction(
                            label="開始舉報廢棄腳踏車", 
                            text="開始舉報廢棄腳踏車"),
                            MessageTemplateAction(
                            label='活動說明',
                            text='活動說明'),
                            MessageTemplateAction(
                            label="我的成績與設定",
                            text="我的成績與設定")]
						    )
#開始舉報廢棄腳踏車
str_btn =ButtonsTemplate(
                            title='請選擇',
                            text='Please select',
                            actions=[
                            MessageTemplateAction(
                            label="上傳圖片",
                            text="上傳圖片"),
                            MessageTemplateAction(
                            label="變更稱呼",
                            text="變更稱呼"),
                            MessageTemplateAction(
                            label="變更電話",
                            text="變更電話"),
                            MessageTemplateAction(
                            label="點我回到大廳",
                            text="回到大廳")]
                            )
#活動說明
act_btn=ButtonsTemplate(
                            title='請選擇',
                            text='Please select',
                            actions=[
                            MessageTemplateAction(
                            label="怎麼判斷是廢棄的腳踏車",
                            text="怎麼判斷是廢棄的腳踏車",),
                            MessageTemplateAction(
                            label="廢棄腳踏車處理流程",
                            text="廢棄腳踏車處理流程",),
                            MessageTemplateAction(
                            label="建議與回饋",
                            text="建議與回饋")]
			    )
#怎麼判斷是廢棄的腳踏車
broken_btn=ButtonsTemplate(
                            thumbnail_image_url="https://scontent.ftpe11-1.fna.fbcdn.net/v/t1.0-9/16806647_402936603393098_4996495945397619203_n.jpg?_nc_cat=102&_nc_ht=scontent.ftpe11-1.fna&oh=54f2057f010f3672d14683897c455681&oe=5D3486C0",
                            title="廢棄腳踏車的標準如下：嚴重生鏽，重要零組件缺漏等等明顯已經不能騎乘",
                            text='Please select',
                            actions=[
                            MessageTemplateAction(
                            label="怎麼判斷是廢棄的腳踏車", 
                            text="怎麼判斷是廢棄的腳踏車",),
                            MessageTemplateAction(
                            label="廢棄腳踏車處理流程",
                            text="廢棄腳踏車處理流程",),
                            MessageTemplateAction(
                            label="建議與回饋",
                            text="建議與回饋")]
			    )
process_btn=ButtonsTemplate(
                            title='請選擇',
                            text='Please select',
                            actions=[
                            MessageTemplateAction(
                            label="怎麼判斷是廢棄的腳踏車", 
                            text="怎麼判斷是廢棄的腳踏車",),
                            MessageTemplateAction(
                            label="廢棄腳踏車處理流程",
                            text="廢棄腳踏車處理流程",),
                            MessageTemplateAction(
                            label="建議與回饋",
                            text="建議與回饋")]
                            )
name_check = ButtonsTemplate(
                            title='確定要變更嗎?',
                            text='Please select',
                            actions=[
                            MessageTemplateAction(
                            label="繼續舉報", 
                            text="繼續舉報",),
                            MessageTemplateAction(
                            label="變更稱呼",
                            text="變更稱呼",)]
                            )
num_check = ButtonsTemplate(
                            title='確定要變更嗎?',
                            text='Please select',
                            actions=[
                            MessageTemplateAction(
                            label="繼續舉報", 
                            text="繼續舉報",),
                            MessageTemplateAction(
                            label="變更電話",
                            text="變更電話",)]
                            )
# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'
#加入歡迎
@handler.add(JoinEvent)
def handle_join(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text='Joined this ' + event.source.type))
# 處理訊息
#line_bot_api.push_message(to, TextSendMessage(text="您好，這是【廢棄腳踏車~重生!】活動大廳，小智機器人在此為您服務"))
line_bot_api.push_message(to, TemplateSendMessage(alt_text="這是【廢棄腳踏車~重生!】活動大廳", template=title_btn))

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    UserMsg =event.message.text
    Token =event.reply_token
    UserJpg = event.message.picture
    item['UserId'] = event.source.user_id
    #ID check
    filter_UserId = db.session.query(bicycles).filter(bicycles.UserId==item['UserId']).first()            
    if filter_UserId == None:
        insert_UserId = bicycles(UserId=item['UserId'])
        db.session.add(insert_UserId)
        db.session.commit()
    else:
        # filter_UserId  = db.session.query(bicycles).filter(bicycles.UserId==item['UserId']).first()
        item["Name"]=filter_UserId.Name
        item["Num"]=filter_UserId.Num
    if UserMsg == '回到大廳':
        line_bot_api.reply_message(Token ,[TextSendMessage(text="您好，這是【廢棄腳踏車~重生!】活動大廳，小智機器人在此為您服務"),
                                          TemplateSendMessage(alt_text="這是【廢棄腳踏車~重生!】活動大廳", template=title_btn)])
    elif UserMsg == "繼續舉報":
        line_bot_api.reply_message(Token, [TextSendMessage(text="請拍攝想要舉報的報廢腳踏車照片上傳給我，謝謝。\n\n舉報聯絡人:"+item['Name']+"\n聯絡電話:"+str(item['Num'])),
                                        TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
    elif (UserMsg == "開始舉報廢棄腳踏車"):
        if item['Name'] or item['Num'] == "未填":
            line_bot_api.reply_message(Token, [TextSendMessage(text="您尚未填寫聯絡資料，依照規定，請您提供聯絡人稱呼以及聯絡電話。您只需填寫一次，小智會記住，以後就可以直接舉報囉!\n\n舉報聯絡人:"+item['Name']+"\n聯絡電話:"+str(item['Num'])),
                                            TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
        else:
            line_bot_api.reply_message(Token, [TextSendMessage(text="請拍攝想要舉報的報廢腳踏車照片上傳給我，謝謝。\n\n舉報聯絡人:"+item['Name']+"\n聯絡電話:"+str(item['Num'])),
                                        TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])

    elif (UserMsg == "變更稱呼"):
        if item["Name"]=="未填":
            line_bot_api.reply_message(Token , TextSendMessage(text="請輸入稱呼:"+item["Name"]))
        else:
            line_bot_api.reply_message(Token , [TextSendMessage(text='您現在的名字為"'+item['Name']+'"'),
                                            TemplateSendMessage(alt_text="變更稱呼", template=name_check)])
            # line_bot_api.reply_message(Token, TemplateSendMessage(alt_text="變更稱呼", template=name_check))
    elif (UserMsg == "變更電話"):
        if item["Num"]=="未填":
            line_bot_api.reply_message(Token , TextSendMessage(text='請輸入電話"'+str(item['Num'])+'"'))
        else:
            line_bot_api.reply_message(Token , [TextSendMessage(text='您現在的電話為"'+str(item['Num'])+'"'),
                                            TemplateSendMessage(alt_text="變更電話", template=num_check)])
    elif UserMsg == '活動說明':
        line_bot_api.reply_message(Token , [ImageSendMessage(original_content_url=
                                                            'https://scontent.ftpe12-1.fna.fbcdn.net/v/t1.0-9/61247413_874283832925037_2067012891634040832_o.jpg?_nc_cat=103&_nc_eui2=AeEJ5rT9dEt2-tY27RRJKwOtrfVDPM0F3a5ATB6dc7R3Hdu-qiAlDxx9vxcC153BUS5O8FzCrbdgqr_ZR1HS8Yp9Jeb55QqzPfO3hRpghZRM6A&_nc_ht=scontent.ftpe12-1.fna&oh=f5baf242e3c57b15afb458713347fbd4&oe=5D5142AD',
                                                            preview_image_url="https://scontent.ftpe12-1.fna.fbcdn.net/v/t1.0-9/61247413_874283832925037_2067012891634040832_o.jpg?_nc_cat=103&_nc_eui2=AeEJ5rT9dEt2-tY27RRJKwOtrfVDPM0F3a5ATB6dc7R3Hdu-qiAlDxx9vxcC153BUS5O8FzCrbdgqr_ZR1HS8Yp9Jeb55QqzPfO3hRpghZRM6A&_nc_ht=scontent.ftpe12-1.fna&oh=f5baf242e3c57b15afb458713347fbd4&oe=5D5142AD"),
                                            TextSendMessage(text="【廢棄腳踏車~重生!】是由一群小學生在2016年發起的公益活動，目的是要發動大家幫忙舉報路邊的廢棄腳踏車，讓清潔隊員可以回收再利用.\n這個活動先後獲得【國語日報】、【大愛電視】、【漢聲廣播電台】等媒體專題報導，並曾經獲得【捷安特】、【日立】、【伊藤園茶飲】、【巨匠電腦】、【佛蒙特咖哩】...等企業贊助。\n更榮獲2017年信義房屋社區一家楷模獎肯定，是最適合親子一起做的公益活動，可以讓孩子透過自己的作為改變社區環境，不但社區變美變安全、還能幫助資源回收、清理出更多空間，最重要的是讓孩子和父母一起體驗: 改變世界就由我開始! "),
                                            TemplateSendMessage(alt_text="活動說明", template=act_btn)])
    elif UserMsg == "廢棄腳踏車處理流程":
        line_bot_api.reply_message(Token ,[ImageSendMessage(original_content_url="https://i.imgur.com/6OyTIyr.gif",
                                                           preview_image_url="https://i.imgur.com/6OyTIyr.gif"),
                                                           TextSendMessage(text= "為您說明整個處理流程:清潔隊收到舉報後，會在三個工作天左右到現場勘查，如果確實符合標準，就會在腳踏車上張貼告示，再過七天清潔隊員會回來確認，如果告示仍在，就會把腳踏車回收到處置場並上網公告一個月，若都沒有車主來認領，就會進行拆解資源回收"),
                                            TemplateSendMessage(alt_text="廢棄腳踏車處理流程",template=process_btn)])
    elif UserMsg == "怎麼判斷是廢棄的腳踏車":
        line_bot_api.reply_message(Token ,TemplateSendMessage(alt_text="怎麼判斷是廢棄的腳踏車",template=broken_btn))
    else:
        #insert Name
        if item["Name"]=="未填":
            item['Name']=UserMsg
            insert_Name = db.session.query(bicycles).filter(bicycles.UserId==item['UserId'])
            insert_Name.update({'Name':item['Name']})
            db.session.commit()
        elif item["Num"]=="未填":
            item['Num']=UserMsg 
            insert_Name = db.session.query(bicycles).filter(bicycles.UserId==item['UserId'])
            insert_Name.update({'Num':item['Num']})
            db.session.commit()
        else:
            line_bot_api.reply_message(Token , TextSendMessage(text=UserMsg))

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    manager.run()

