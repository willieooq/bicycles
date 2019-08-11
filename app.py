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
import datetime,requests,ast,tempfile, os, re
from dbmodle import *
import email_reply.email_reply as email_reply
from vision import *
from template import *
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

levelname = ["新生", "國小低年級", "國小中年級", "國小高年級", "國中一年級", "國中二年級", "國中三年級", "高中一年級", "高中二年級", "高中三年級", "大學一年級", "大學二年級", "大學三年級", "大學四年級", "碩士", "博士", "博士後研究", "助理教授", "副教授", "教授", "校長"]

#change option func
def commit_user_msg(user_id,option):
    insert_user_msg_query = db.session.query(UserData).filter(UserData.user_id==user_id)
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
        insert_user_id = UserData(user_id=item['user_id'])
        db.session.add(insert_user_id)
        db.session.commit()
        insert_user_id_bicycles = Bicycles(user_id = item['user_id'])
        db.session.add(insert_user_id_bicycles)
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
    insert_user_data = db.session.query(UserData).filter(UserData.user_id==item['user_id'])
    insert_user_data_query = db.session.query(UserData).filter(UserData.user_id==item['user_id']).first()
    insert_bicycles_status = db.session.query(Bicycles).filter(Bicycles.user_id==item['user_id'])
    insert_bicycles_status_query = db.session.query(Bicycles).filter(Bicycles.user_id==item['user_id']).first()
    # get reply token
    token = event.reply_token
    # 
    image_path = os.path.join(
        os.path.dirname(__file__),
        'images',
        item['user_id']+'.jpg'
    ) 
    # user check
    if insert_user_data_query  == None or insert_bicycles_status_query == None:
        line_bot_api.reply_message(token , TextSendMessage(text="未知用戶，請重新加入好友"))
    else:
        #load data from db
        item["name"]=insert_user_data_query.name
        item["num"]=insert_user_data_query.num
        item['address']=insert_bicycles_status_query.address
        item['detail']=insert_bicycles_status_query.detail
        item['photo']=insert_bicycles_status_query.photo
        item['score']=insert_user_data_query.score
        item['total']=insert_user_data_query.total
        item['level']=insert_user_data_query.level
    # determine where the process
    try:
        option=insert_user_data_query.user_msg
    except:
        option='no'
    print('try:'+option)
    # when user push ImageMessage
    if isinstance(event.message, ImageMessage):
        if option == '上傳照片':
            message_content = line_bot_api.get_message_content(event.message.id)
            try:
                line_bot_api.reply_message(token,TextSendMessage(text="收到照片，小智正在辨認照片, 請稍候..."))
                # upload image to imgur
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
                #insert db
                insert_bicycles_status.update({'photo':image_url})#upload message
                

                #google vision determine
                image_labels = detect_labels(image_path)
                scores = get_bike_scores(image_labels)
                print('final score:', scores)
                #Is the picture have bike?
                ans = scores[0]+scores[1]*2
                if ans > 10:#max score is 10
                    ans = 10
                if scores[0]>3 and scores[1]>1:
                    line_bot_api.push_message(item['user_id'],[ImageSendMessage(original_content_url=img_good_job,preview_image_url=img_good_job),
                                                            TextSendMessage(text="太好了，小智看到腳踏車囉! 它的評分是"+str(int(ans))+"分!"),
                                                            TextSendMessage(text="請告訴我廢棄腳踏車的所在地。\
                                                            \n\n提醒您，地址一定要精確，因為清潔隊員會依據您提供的地址到現場來勘驗，如果地址錯誤會讓辛苦忙碌的清潔隊員白白跑一趟喔!! \
                                                            \n\n您可以選擇用地圖定位，也可以直接用文字輸入地址給我喔!")])                                            
                    option = "添加地址"# jump to add address
                    commit_user_msg(item['user_id'],option)
                else:
                    print(ans)
                    line_bot_api.push_message(item['user_id'],[ImageSendMessage(original_content_url=img_sorry,preview_image_url=img_sorry),
                                                            TextSendMessage(text = "哎呀! ，小智找不到腳踏車呢，請換個角度拍攝看看喔!"),
                                                            TemplateSendMessage(alt_text='photo check',template=photo_check)])
                #upload score
                item['score']=ans
                insert_user_data.update({'score':item['score']})
            except:
                line_bot_api.push_message(
                    item['user_id'],
                    TextSendMessage(text='上傳失敗,請再試一次'))
            print(response.json()['data']['link'])
            return 0
    # when user push LocationMessage
    elif isinstance(event.message, LocationMessage):
        if option == "添加地址":
            line_bot_api.push_message(item['user_id'],TextSendMessage(text = '確認中請稍候...'))
            # set the latitude and longitude from user message
            latitude = event.message.latitude
            longitude = event.message.longitude
            # put it on google geocoding 
            url = 'https://maps.googleapis.com/maps/api/geocode/json?latlng='+str(latitude)+','+str(longitude)+'&key=AIzaSyBao1oEqKtiUwjQOrWtmRlwrhonfbpbtUY&language=zh-TW'
            response = requests.request('GET', url)
            # change type from str to dict
            location = ast.literal_eval(response.text)
            item['address'] = location["results"][0]['formatted_address']
            item['city'] = location["results"][0]["address_components"][2]["long_name"]
            #checking address
            checking = re.compile(r'.*[縣市].*[鄉鎮市區村].*[街路].*號')
            # insert_bicycles_status_query.update({'address':location["results"][0]['formatted_address']})
            if checking.search(item['address']) != None:
                insert_bicycles_status.update({'address':item['address'],'city':item['city']})
                db.session.commit()
                line_bot_api.push_message(item['user_id'],[TextSendMessage(text = item['address']),
                                                TemplateSendMessage(alt_text ='address check',template = address_check)])
            else:
                line_bot_api.push_message(item['user_id'],TextSendMessage(text = '地址格式錯誤，請輸入正確的地址')) 
    # when user push TextMessage
    elif isinstance(event.message, TextMessage):
        user_msg =event.message.text
        if user_msg == '回到大廳':
            line_bot_api.reply_message(token ,TemplateSendMessage(alt_text="這是【廢棄腳踏車~重生!】活動大廳", template=title_btn))
        elif user_msg == "繼續舉報":
            line_bot_api.reply_message(token, [TextSendMessage(text="請拍攝想要舉報的報廢腳踏車照片上傳給我，謝謝。\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                            TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
        elif (user_msg == "開始舉報廢棄腳踏車"):
            if item['name'] == "未填" or item['num'] == "未填":
                line_bot_api.reply_message(token, [TextSendMessage(text="您尚未填寫聯絡資料，依照規定，請您提供聯絡人稱呼以及聯絡電話。您只需填寫一次，小智會記住，以後就可以直接舉報囉!\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                                TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn_no)])
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
            commit_user_msg(item['user_id'],option)
            line_bot_api.reply_message(token ,TextSendMessage(text="請上傳一張照片喔！"))
        #image check
        elif user_msg == '確認送出':
            line_bot_api.reply_message(token,TextSendMessage("請告訴我廢棄腳踏車的所在地。\
                                                            \n\n提醒您，地址一定要精確，因為清潔隊員會依據您提供的地址到現場來勘驗，如果地址錯誤會讓辛苦忙碌的清潔隊員白白跑一趟喔!! \
                                                            \n\n您可以選擇用地圖定位，也可以直接用文字輸入地址給我喔!"))
            option = "添加地址"# jump to add address
            commit_user_msg(item['user_id'],option)
        # Event Description
        elif user_msg == '活動說明':
            line_bot_api.reply_message(token , [ImageSendMessage(original_content_url=
                                                                'https://i.imgur.com/Pe1OqjG.jpg',
                                                                preview_image_url="https://i.imgur.com/Pe1OqjG.jpg"),
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
            line_bot_api.reply_message(token,TextSendMessage(text="舉報聯絡人:"+item['name']+"\n聯絡電話:"+item['num']+" \
                                                            \n成就分數："+str(item['level'])+"\n等級是["+levelname[int(str(item['level']))]+"] \
                                                            \n總共舉報了"+str(item['total'])+"筆\n已經幫助清潔隊回收了0輛\n未結案案件筆數:"+str(item['total'])+" \
                                                            \n我幫您列出您的舉報案件喔!"))
        elif user_msg == '建議與回饋':
            option = "建議與回饋"# jump to advice
            commit_user_msg(item['user_id'],option)
            line_bot_api.reply_message(token,TextSendMessage(text="我們很重視您的建議，請您把建議寫下來給我們。\n\n如果不想寫請按【回到活動大廳】按鈕。")) 
        elif user_msg == "地址正確": 
            line_bot_api.reply_message(token,TextSendMessage(text="謝謝！小智用AI幫你審查整個案子，請稍候...")) 
            #add judge

            line_bot_api.push_message(item['user_id'],[ImageSendMessage(original_content_url=img_good_job,preview_image_url=img_good_job),
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
            line_bot_api.push_message(item['user_id'],TextSendMessage(text = "好的，我會將這個案件交給清潔隊，大約一週內就會有隊員來勘查，如果符合標準就會再以Line通知！現在帶你回活動大廳"))
            email_reply.send_email("brokenbikeline@gmail.com","【廢棄腳踏車~重生!】民眾舉報案件", "敬啟者，您好\n\n這是來自報廢腳踏車~重生!活動的民眾舉報案件，這已經過我們人工智慧篩選過，應該是正確的舉報，敬請安排清潔隊員前往勘查並處理，以下是舉報的資訊 \
                                     \n\n舉報人稱呼： "+item['name']+"\n聯絡電話： "+item['num']+"\n舉報地址: "+item['address']+"(註:"+str(item['detail'])+")\n現場照片： "+item['photo']+"\n\n本案件的人工智慧評價分數為 "+str(item['score'])+" 分(滿分為10分)，請參考。 \
                                     \n\n感謝您及貴單位和清潔隊員對台灣環境的貢獻。\n\n廢棄腳踏車~重生! 活動全體志工 敬上") #send email
            line_bot_api.push_message(item['user_id'],TemplateSendMessage(alt_text = 'back to title ',template = title_btn))
        else:
            #insert Name
            if option == "變更稱呼":
                item['name']=user_msg
                insert_user_data.update({'name':item['name']})
                db.session.commit()
                if item['name'] == "未填" or item['num'] == "未填":
                    line_bot_api.reply_message(token, [TextSendMessage(text="您尚未填寫聯絡資料，依照規定，請您提供聯絡人稱呼以及聯絡電話。您只需填寫一次，小智會記住，以後就可以直接舉報囉!\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                                    TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn_no)])
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
                    insert_user_data.update({'num':item['num']})
                    db.session.commit()
                    if item['name'] == "未填" or item['num'] == "未填":
                        print('name: '+item['name'])
                        print('num: '+item['num'])
                        line_bot_api.reply_message(token, [TextSendMessage(text="您尚未填寫聯絡資料，依照規定，請您提供聯絡人稱呼以及聯絡電話。您只需填寫一次，小智會記住，以後就可以直接舉報囉!\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                                        TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn_no)])
                    else:
                        line_bot_api.reply_message(token, [TextSendMessage(text="請拍攝想要舉報的報廢腳踏車照片上傳給我，謝謝。\n\n舉報聯絡人:"+item['name']+"\n聯絡電話:"+str(item['num'])),
                                                    TemplateSendMessage(alt_text="開始舉報廢棄腳踏車", template=str_btn)])
                    option = 'no' #reset option
                    commit_user_msg(item['user_id'],option)
            elif option == "添加地址": #add address by user message
                option = 'no' #reset option
                commit_user_msg(item['user_id'],option)
                insert_bicycles_status.update({'address':user_msg})
                db.session.commit()
                line_bot_api.reply_message(token,[TextSendMessage(text = user_msg),
                                            TemplateSendMessage(alt_text ='address check',template = address_check)])
            elif option == "建議與回饋":
                option = 'no' #reset option
                commit_user_msg(item['user_id'],option)
                email_reply.send_email("brokenbikeline@gmail.com","【廢棄腳踏車~重生!】民眾建議", "您好，\n這是來自報廢腳踏車~重生!聊天機器人的民眾建議喔!請轉交志工們進行討論並回應。\n\n建議者:"+str(item['name'])+"\n建議者電話:"+str(item['num'])+"\n建議內容:\n-----------\n"+user_msg+"\n-----------\n\n來自小智機器人，請勿回信")
                line_bot_api.push_message(item['user_id'],TextSendMessage(text = "好的，我已經轉交給志工們囉!"))
                line_bot_api.push_message(item['user_id'],TemplateSendMessage(alt_text = 'back to title',template = title_btn))
            elif option == "添加註解":
                print('2')
                option = 'no' #reset option
                commit_user_msg(item['user_id'],option)
                item['detail'] = user_msg
                insert_bicycles_status.update({'detail':user_msg})
                db.session.commit()
                line_bot_api.reply_message(token,[ImageSendMessage(original_content_url=img_good_job,preview_image_url=img_good_job),
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