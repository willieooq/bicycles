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
from imgurpython  import ImgurClient
import datetime,requests,ast,tempfile,os
from dbmodle import *
import email_reply.email_reply as email_reply
from vision import *
from config import client_id, client_secret, album_id, access_token, refresh_token, line_channel_access_token, \
    line_channel_secret
#db key
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://ouwlmxtvewdibl:05f09b74d57c0cf93c2594966a1e03e06c7ba3605d56b46d8ecce6f61da50131@ec2-54-83-192-245.compute-1.amazonaws.com:5432/df3vg11r7cab9s'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

# Channel Access Token
line_bot_api = LineBotApi(line_channel_access_token)
handler = WebhookHandler(line_channel_secret)
to = "Ue7aa1b3d42ca4e7df1dc143cbc97d13c"
static_tmp_path = os.path.join(os.path.dirname(__file__), 'static', 'tmp')

#image url
img_great = "https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.0-9/67301384_913440575676029_1834425191191543808_n.jpg?_nc_cat=105&_nc_oc=AQkwa9UTmxgHH1Wxj5Sgdk649PIOhYQ2M3rc1m-QfF-dPJh2xLKS0oLJQlzT0y4pE98&_nc_ht=scontent.fkhh1-1.fna&oh=71ea7aee51a0eb4da8a00cf2d9e949b8&oe=5DB5B61F"
img_sorry = "https://scontent.fkhh1-2.fna.fbcdn.net/v/t1.0-9/67190049_913440499009370_1757733799887634432_n.jpg?_nc_cat=109&_nc_oc=AQlUW4PllPhv2KqBH-bbu5m4aGPf7XpNGdp4sEGJdXR-d973MmgLpQB6v-QucsuTPOo&_nc_ht=scontent.fkhh1-2.fna&oh=52fdd0400382fe0da67039af91adb66d&oe=5DAAD665"
img_cry = "https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.0-9/67154157_913440442342709_5496511270666371072_n.jpg?_nc_cat=106&_nc_oc=AQkiX_rd_iHbutWLM3PWMgLeG_UBL2Ua7CoT2YVlTFg0HrKMAIt60kZn0taGKKPMJII&_nc_ht=scontent.fkhh1-1.fna&oh=2ff900deedb3c14e110f3ee0100b4534&oe=5DA6F958"
img_heihei = "https://scontent.fkhh1-2.fna.fbcdn.net/v/t1.0-9/67364028_913440522342701_3341716561831395328_n.jpg?_nc_cat=108&_nc_oc=AQkyupRc_LPEQAeOPfwGZ0uZi79HfupAfc-Z2JXXmi_St4C3VSge1eWLto8RWeCCxYQ&_nc_ht=scontent.fkhh1-2.fna&oh=db94f83af65c1019602cb57626660a7d&oe=5DE2F4C3"
img_letsgo = "https://scontent.fkhh1-2.fna.fbcdn.net/v/t1.0-9/67224808_913440449009375_2573876344605638656_n.jpg?_nc_cat=109&_nc_oc=AQmYxsoBCFa67E6509tiL0Aaw22muw97Qq4WJBectr0D1M2CvnC1mnKQNLvRxH7BLPs&_nc_ht=scontent.fkhh1-2.fna&oh=f9627d9b82b20223d2c95d8f37b14bf6&oe=5DA92467"
img_heart = "https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.0-9/67402433_913440535676033_1568705241149341696_n.jpg?_nc_cat=101&_nc_oc=AQnj4QtcVcCEocFgz7w8v8ESMkHgUA8bIhJinEO5jV82KKEevNsaWKkgA2WpupCmMz4&_nc_ht=scontent.fkhh1-1.fna&oh=a6159795c70cc3d03bce450da8f1d68f&oe=5DA235D3"
img_stop = "https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.0-9/67181106_913440482342705_8168422051984441344_n.jpg?_nc_cat=102&_nc_oc=AQkpI19WlOumQP-81m8x7lPNz3s3E82ZiwMgZ6X3NLp0hBQR1ICzswmo3cDMW0y__-8&_nc_ht=scontent.fkhh1-1.fna&oh=dc50cc3fa652d65e2ef644a83c02cf90&oe=5DED2CF5"
img_ok = "https://scontent.fkhh1-1.fna.fbcdn.net/v/t1.0-9/67301384_913440575676029_1834425191191543808_n.jpg?_nc_cat=105&_nc_oc=AQkwa9UTmxgHH1Wxj5Sgdk649PIOhYQ2M3rc1m-QfF-dPJh2xLKS0oLJQlzT0y4pE98&_nc_ht=scontent.fkhh1-1.fna&oh=71ea7aee51a0eb4da8a00cf2d9e949b8&oe=5DB5B61F"
img_smile = "https://scontent.fkhh1-2.fna.fbcdn.net/v/t1.0-9/67412582_913440569009363_1431190674778095616_n.jpg?_nc_cat=111&_nc_oc=AQk8HNJTMJzTc6Pxleayqz3nVp1Aqhhz4Okio2XjOu1kBIIu-BkjpUxh5Q94Cm0rMYU&_nc_ht=scontent.fkhh1-2.fna&oh=a1cabd565ac5e946ee33e755aae87cc7&oe=5DEEA611"
img_doorplate = "https://scontent.ftpe12-2.fna.fbcdn.net/v/t1.0-9/61078857_875267386160015_4437566467994550272_n.jpg?_nc_cat=110&_nc_eui2=AeGcYmXCQge4PFlRf7H0MOUxf1pMxIHCJXPuLC6zsdYHArI3OvX1Cj7RbqRXyf1OzM0My-iebhNKWSwnZKsC1m_6GhyOVGZYq5XbsAUi9ck77A&_nc_ht=scontent.ftpe12-2.fna&oh=223c83920133792c4e4efff794795d81&oe=5D9E7DC1"

levelname = ["新生", "國小低年級", "國小中年級", "國小高年級", "國中一年級", "國中二年級", "國中三年級", "高中一年級", "高中二年級", "高中三年級", "大學一年級", "大學二年級", "大學三年級", "大學四年級", "碩士", "博士", "博士後研究", "助理教授", "副教授", "教授", "校長"]
#template
#begin title
title_btn =ButtonsTemplate(
                            title='您好，這是【廢棄腳踏車~重生!】活動大廳，小智機器人在此為您服務', 
                            thumbnail_image_url=img_smile,
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
                            text="我的成績與設定"),
                            MessageTemplateAction(
                            label="建議與回饋",
                            text="建議與回饋")]
						    )
#start report
str_btn =ButtonsTemplate(
                            title='請選擇',
                            text='Please select',
                            actions=[
                            MessageTemplateAction(
                            label="上傳照片",
                            text="上傳照片"),
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
#Event Description
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
#how to decide
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
#recycle process            
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
#name check
name_check = ButtonsTemplate(
                            title='請寫下讓清潔隊聯絡您的電話',
                            text= "如果不想變更請按『繼續舉報』按鈕。",
                            actions=[
                            MessageTemplateAction(
                            label="繼續舉報", 
                            text="繼續舉報")]
                            )
#phone number check
num_check = ButtonsTemplate(
                            title='請寫下讓清潔隊聯絡您的電話',
                            text= "如果不想變更請按『繼續舉報』按鈕。",
                            actions=[
                            MessageTemplateAction(
                            label="繼續舉報", 
                            text="繼續舉報")]
                            )
#address check
address_check = ButtonsTemplate(
                            text="如果您確定地址正確，請按下按鈕傳給我。\
                                \n再次提醒您一定要確認地址是對的喔! 不然清潔隊員會白跑一趟，也會影響您的積分!!\
                                \n如果擔心清潔隊員找不到，也可以再添加註解。",
                            actions=[
                            MessageTemplateAction(
                            label="地址正確", 
                            text="地址正確"),
                            MessageTemplateAction(
                            label="添加註解",
                            text="添加註解")]
                            )

#change option func
def commit_user_msg(user_id,option):
    insert_user_msg_query = db.session.query(UserMsg).filter(UserMsg.user_id==user_id)
    insert_user_msg_query.update({'user_msg':option})
    db.session.commit()
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
#greet message
@handler.add(FollowEvent)
def handle_follow(event):
    #insert follower ID 
    item = {'user_id' : 'user_id'}
    item['user_id'] = event.source.user_id
    try:
        insert_user_id = Bicycles(user_id=item['user_id'])
        db.session.add(insert_user_id)
        db.session.commit()
        print(event.source.user_id)
    except:
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text='已加入好友，可開始使用'))

    line_bot_api.push_message(item['user_id'], TemplateSendMessage(alt_text="這是【廢棄腳踏車~重生!】活動大廳", template=title_btn))
# deployer test message
line_bot_api.push_message(to, TemplateSendMessage(alt_text="這是【廢棄腳踏車~重生!】活動大廳", template=title_btn))

# handle message
@handler.add(MessageEvent, message=(ImageMessage, TextMessage, LocationMessage))
def handle_message(event):
    #dict
    item = {'user_id' : 'user_id',
        'name' : '未填',
        'num' : '未填',
        'time' : 'time',
        'address' : 'address',
        'photo' : 'photo',
        'city' : 'city',
        'detail' : 'detail',
        'handler' : 'handler',
        'status' : 'status',
        'score' : 'score',
        'total' : 'total',
        'updatedate' : 'updatedate'}
    #get user id from db
    item['user_id'] = event.source.user_id
    insert_user_msg = db.session.query(UserMsg).filter(UserMsg.user_id==item['user_id']).first()
    insert_user_msg_query = db.session.query(UserMsg).filter(UserMsg.user_id==item['user_id'])
    insert_user_status = db.session.query(Bicycles).filter(Bicycles.user_id==item['user_id']).first()
    insert_user_status_query = db.session.query(Bicycles).filter(Bicycles.user_id==item['user_id'])
    # get reply token
    token = event.reply_token
    # 
    image_path = os.path.join(
        os.path.dirname(__file__),
        'images',
        item['user_id']+'.jpg'
    )
    # user check
    if insert_user_status == None:
        line_bot_api.reply_message(token , TextSendMessage(text="未知用戶，請重新加入好友"))
    else:
        #load data from db
        item["name"]=insert_user_status.name
        item["num"]=insert_user_status.num
        item['address']=insert_user_status.address
        item['detail']=insert_user_status.detail
        item['photo']=insert_user_status.photo
        item['score']=insert_user_status.score
        item['total']=insert_user_status.total
        item['level']=insert_user_status.level
    # determine where the process
    try:
        option=insert_user_msg.user_msg
    except:
        option='no'
    print('try:'+option)
    # when user push ImageMessage
    if isinstance(event.message, ImageMessage):
        if option == '上傳照片':
            ext = 'jpg'
            message_content = line_bot_api.get_message_content(event.message.id)
            # try:
            line_bot_api.reply_message(token,TextSendMessage(text='上傳中請稍候...'))
            # upload image to imgur
            # file_path = '{}.{}'.format('temp', ext)
            print('image_path:', image_path)
            with open(image_path, 'wb') as fd:
                for chunk in message_content.iter_content():
                    fd.write(chunk)
            with open(image_path, "rb") as fs:
                binary_data = fs.read()
            url = 'https://api.imgur.com/3/image'
            payload = {'image': binary_data}
            files = {}
            headers = {'Authorization': 'Client-ID ' + client_id}
            response = requests.request('POST', url, headers = headers, data = payload, files = files, allow_redirects = False, timeout = 10000)
            image_url = response.json()['data']['link']

            #test message
            print(image_url)
            insert_user_status_query.update({'photo':image_url})#upload message
            option = "添加地址"# jump to add address
            insert_user_msg_query.update({'user_msg':option})
            db.session.commit()

            image_labels = detect_labels(image_path)
            scores = get_bike_scores(image_labels)
            print('final score:', scores)

            line_bot_api.push_message(item['user_id'],[ImageSendMessage(original_content_url=img_ok,preview_image_url=img_ok),
                                        TextSendMessage(text='上傳成功'),
                                        TextSendMessage(text="請告訴我廢棄腳踏車的所在地。\
                                        \n\n提醒您，地址一定要精確，因為清潔隊員會依據您提供的地址到現場來勘驗，如果地址錯誤會讓辛苦忙碌的清潔隊員白白跑一趟喔!! \
                                        \n\n您可以選擇用地圖定位，也可以直接用文字輸入地址給我喔!")])
            # except:
            #     line_bot_api.push_message(
            #         item['user_id'],
            #         TextSendMessage(text='上傳失敗,請再試一次'))
            # print(response.json()['data']['link'])
            return 0
    # when user push LocationMessage
    elif isinstance(event.message, LocationMessage):
        if option == "添加地址":
            # set the latitude and longitude from user message
            latitude = event.message.latitude
            longitude = event.message.longitude
            # put it on google geocoding 
            url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(latitude)+','+str(longitude)+'&key=AIzaSyBao1oEqKtiUwjQOrWtmRlwrhonfbpbtUY&language=zh-TW'
            response = requests.request('GET', url)
            # change type from str to dict
            location = ast.literal_eval(response.text)
            item['address'] = location["results"][0]['formatted_address']
            # insert_user_status_query.update({'address':location["results"][0]['formatted_address']})
            # db.session.commit()
            line_bot_api.push_message
            insert_user_status_query.update({'address':item['address']})
            db.session.commit()
            line_bot_api.push_message(item['user_id'],[TextSendMessage(text = item['address']),
                                            TemplateSendMessage(alt_text ='address check',template = address_check)])
             
    # when user push TextMessage
    elif isinstance(event.message, TextMessage):
        user_msg =event.message.text
        if user_msg == '回到大廳':
            line_bot_api.reply_message(token ,TemplateSendMessage(alt_text="這是【廢棄腳踏車~重生!】活動大廳", template=title_btn))
        elif user_msg == "繼續舉報":
            line_bot_api.reply_message(token, [TextSendMessage(text="請拍攝想要舉報的報廢腳踏車照片上傳給我，謝謝。\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                            TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
        elif (user_msg == "開始舉報廢棄腳踏車"):
            if item['name'] and item['num'] == "未填":
                line_bot_api.reply_message(token, [TextSendMessage(text="您尚未填寫聯絡資料，依照規定，請您提供聯絡人稱呼以及聯絡電話。您只需填寫一次，小智會記住，以後就可以直接舉報囉!\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                                TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
            else:
                line_bot_api.reply_message(token, [TextSendMessage(text="請拍攝想要舉報的報廢腳踏車照片上傳給我，謝謝。\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                            TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
        elif (user_msg == "變更稱呼"):
            #change option to add name
            option = "變更稱呼"
            commit_user_msg(item['user_id'],option)
            # name check
            line_bot_api.reply_message(token , [TextSendMessage(text='您現在的稱呼為"'+str(item['name'])+'"'),
                                                TemplateSendMessage(alt_text='change name',template=name_check)])
            print(option)
        elif (user_msg == "變更電話"):
            #change option to add phone number
            option = "變更電話"
            commit_user_msg(item['user_id'],option)
            # phone check
            line_bot_api.reply_message(token , [TextSendMessage(text='您現在的電話為"'+str(item['num'])+'"'),
                                                TemplateSendMessage(alt_text="變更電話", template=num_check)])
        # jump to upload image
        elif user_msg == '上傳照片':
            option = '上傳照片'
            insert_user_msg_query.update({'user_msg':option})
            db.session.commit()
            line_bot_api.reply_message(token ,TextSendMessage(text="請上傳一張照片喔！"))
        # Event Description
        elif user_msg == '活動說明':
            line_bot_api.reply_message(token , [ImageSendMessage(original_content_url=
                                                                'https://scontent.ftpe12-1.fna.fbcdn.net/v/t1.0-9/61247413_874283832925037_2067012891634040832_o.jpg?_nc_cat=103&_nc_eui2=AeEJ5rT9dEt2-tY27RRJKwOtrfVDPM0F3a5ATB6dc7R3Hdu-qiAlDxx9vxcC153BUS5O8FzCrbdgqr_ZR1HS8Yp9Jeb55QqzPfO3hRpghZRM6A&_nc_ht=scontent.ftpe12-1.fna&oh=f5baf242e3c57b15afb458713347fbd4&oe=5D5142AD',
                                                                preview_image_url="https://scontent.ftpe12-1.fna.fbcdn.net/v/t1.0-9/61247413_874283832925037_2067012891634040832_o.jpg?_nc_cat=103&_nc_eui2=AeEJ5rT9dEt2-tY27RRJKwOtrfVDPM0F3a5ATB6dc7R3Hdu-qiAlDxx9vxcC153BUS5O8FzCrbdgqr_ZR1HS8Yp9Jeb55QqzPfO3hRpghZRM6A&_nc_ht=scontent.ftpe12-1.fna&oh=f5baf242e3c57b15afb458713347fbd4&oe=5D5142AD"),
                                                TextSendMessage(text="【廢棄腳踏車~重生!】是由一群小學生在2016年發起的公益活動，目的是要發動大家幫忙舉報路邊的廢棄腳踏車，讓清潔隊員可以回收再利用.\n這個活動先後獲得【國語日報】、【大愛電視】、【漢聲廣播電台】等媒體專題報導，並曾經獲得【捷安特】、【日立】、【伊藤園茶飲】、【巨匠電腦】、【佛蒙特咖哩】...等企業贊助。\n更榮獲2017年信義房屋社區一家楷模獎肯定，是最適合親子一起做的公益活動，可以讓孩子透過自己的作為改變社區環境，不但社區變美變安全、還能幫助資源回收、清理出更多空間，最重要的是讓孩子和父母一起體驗: 改變世界就由我開始! "),
                                                TemplateSendMessage(alt_text="活動說明", template=act_btn)])
        #recycle process
        elif user_msg == "廢棄腳踏車處理流程":
            line_bot_api.reply_message(token ,[ImageSendMessage(original_content_url="https://i.imgur.com/6OyTIyr.gif",
                                                            preview_image_url="https://i.imgur.com/6OyTIyr.gif"),
                                                            TextSendMessage(text= "為您說明整個處理流程:清潔隊收到舉報後，會在三個工作天左右到現場勘查，如果確實符合標準，就會在腳踏車上張貼告示，再過七天清潔隊員會回來確認，如果告示仍在，就會把腳踏車回收到處置場並上網公告一個月，若都沒有車主來認領，就會進行拆解資源回收"),
                                                TemplateSendMessage(alt_text="廢棄腳踏車處理流程",template=process_btn)])
        #how to decide
        elif user_msg == "怎麼判斷是廢棄的腳踏車":
            line_bot_api.reply_message(token ,TemplateSendMessage(alt_text="怎麼判斷是廢棄的腳踏車",template=broken_btn))
        elif user_msg == "我的成績與設定":
            print(type(str(insert_user_status.level)))
            line_bot_api.reply_message(token,TextSendMessage(text="舉報聯絡人:"+item['name']+"\n聯絡電話:"+item['num']+" \
                                                            \n成就分數："+str(round(float(item['score'])) )+"\n等級是["+levelname[int(str(item['level']))]+"] \
                                                            \n總共舉報了"+str(item['total'])+"筆\n已經幫助清潔隊回收了0輛\n未結案案件筆數:"+str(item['total'])+" \
                                                            \n我幫您列出您的舉報案件喔!"))
        elif user_msg == "地址正確": 
            line_bot_api.reply_message(token,TextSendMessage(text="謝謝！小智用AI幫你審查整個案子，請稍候...")) 
            #add judge

            line_bot_api.push_message(item['user_id'],[ImageSendMessage(original_content_url=img_great,preview_image_url=img_great),
                                                        TextSendMessage(text="太棒了，你這次舉報獲得"+str(item['score'])+"分！"),
                                                        TextSendMessage(text="以下是這次舉報的內容\n舉報聯絡人："+str(item['name'])+"\n聯絡電話："+str(item['num'])+"\n位置:"+str(item['address'])+"(註:"+str(item['detail'])+")"),
                                                        TemplateSendMessage(alt_text='address corect',template=ButtonsTemplate(text='請再次確認舉報內容是否正確，確定請點選『確認送出舉報內容』，或按下『放棄舉報』',actions=[MessageTemplateAction(label="確認送出舉報內容",text="確認送出舉報內容"),MessageTemplateAction(label="放棄舉報，回到大廳",text="回到大廳")]))])
        elif user_msg == "添加註解" or user_msg == "重新註解":
            print(user_msg)
            print('1')
            option = "添加註解"
            commit_user_msg(item['user_id'],option)
            line_bot_api.reply_message(token,TemplateSendMessage(alt_text='add ps',
                                    template= ButtonsTemplate(
                                    title = '地址:'+str(item['address']),
                                    text="請直接輸入您要提供的註解。\n如果地址不用說明，可以直接按【地址正確】按鈕確認地址。",
                                    actions=[MessageTemplateAction(label="地址正確",text="地址正確")])))
        elif user_msg == "確認送出舉報內容":
            email_reply.send_email("brokenbikeline@gmail.com","【廢棄腳踏車~重生!】民眾舉報案件", "敬啟者，您好\n\n這是來自報廢腳踏車~重生!活動的民眾舉報案件，這已經過我們人工智慧篩選過，應該是正確的舉報，敬請安排清潔隊員前往勘查並處理，以下是舉報的資訊 \
                                     \n\n舉報人稱呼： "+item['name']+"\n聯絡電話： "+item['num']+"\n舉報地址: "+item['address']+"(註:"+str(item['detail'])+")\n現場照片： "+item['photo']+"\n\n本案件的人工智慧評價分數為 "+str(item['score'])+" 分(滿分為10分)，請參考。 \
                                     \n\n感謝您及貴單位和清潔隊員對台灣環境的貢獻。\n\n廢棄腳踏車~重生! 活動全體志工 敬上") #send email
            print(item['detail'])
            print(item['score'])
        else:
            #insert Name
            if option == "變更稱呼":
                item['name']=user_msg
                insert_user_status_query.update({'name':item['name']})
                db.session.commit()
                if item['name'] == "未填" or item['num'] == "未填":
                    line_bot_api.reply_message(token, [TextSendMessage(text="您尚未填寫聯絡資料，依照規定，請您提供聯絡人稱呼以及聯絡電話。您只需填寫一次，小智會記住，以後就可以直接舉報囉!\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                                    TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
                else:
                    line_bot_api.reply_message(token, [TextSendMessage(text="請拍攝想要舉報的報廢腳踏車照片上傳給我，謝謝。\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                                TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
                option = 'no' #reset option
                commit_user_msg(item['user_id'],option)
            #insert Name
            elif option == "變更電話":
                item['num']=user_msg 
                try:
                    int(item['num'])
                except:
                    line_bot_api.reply_message(token, TextSendMessage(text='請輸入正確格式的電話號碼'))
                if len(item['num']) != 10 or item['num'][0] != '0' or item['num'][1] != '9':
                    line_bot_api.reply_message(token, TextSendMessage(text='請輸入正確格式的電話號碼'))
                else:
                    insert_user_status_query.update({'num':item['num']})
                    db.session.commit()
                    if item['name'] == "未填" or item['num'] == "未填":
                        print('name: '+item['name'])
                        print('num: '+item['num'])
                        line_bot_api.reply_message(token, [TextSendMessage(text="您尚未填寫聯絡資料，依照規定，請您提供聯絡人稱呼以及聯絡電話。您只需填寫一次，小智會記住，以後就可以直接舉報囉!\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                                        TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
                    else:
                        line_bot_api.reply_message(token, [TextSendMessage(text="請拍攝想要舉報的報廢腳踏車照片上傳給我，謝謝。\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                                    TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
                    option = 'no' #reset option
                    commit_user_msg(item['user_id'],option)
            elif option == "添加地址": #add address by user message
                option = 'no' #reset option
                commit_user_msg(item['user_id'],option)
                insert_user_status_query.update({'address':user_msg})
                db.session.commit()
                line_bot_api.reply_message(token,[TextSendMessage(text = user_msg),
                                            TemplateSendMessage(alt_text ='address check',template = address_check)])
            elif option == "添加註解":
                print('2')
                option = 'no' #reset option
                commit_user_msg(item['user_id'],option)
                item['detail'] = user_msg
                insert_user_status_query.update({'detail':user_msg})
                db.session.commit()
                line_bot_api.reply_message(token,[ImageSendMessage(original_content_url=img_ok,preview_image_url=img_ok),
                                                    TemplateSendMessage(alt_text='註解已添加',template=ButtonsTemplate(title='地址:'+str(item['address'])+'(註:'+str(item['detail'])+')',text='註解已添加！',
                                                                                                                    actions=[MessageTemplateAction(label="地址正確",text="地址正確"),MessageTemplateAction(label="重新註解",text="重新註解")]))])
            #unknown message
            else:
                line_bot_api.reply_message(token , [ImageSendMessage(original_content_url=img_sorry,preview_image_url=img_sorry),
                                                    TextSendMessage(text='抱歉，您傳了一個我看不懂的指令'),
                                                    TemplateSendMessage(alt_text='sorry',template=title_btn)])
                print(option)
            


        
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    manager.run()