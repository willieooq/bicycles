from linebot.models import *
#image url
img_good_job = "https://i.imgur.com/b3Xwfmf.jpg"
img_sorry = "https://i.imgur.com/D9g53cr.jpg"
img_cry = "https://i.imgur.com/L1ZDNX8.jpg"
img_omg = "https://i.imgur.com/usF3WLY.jpg"
img_wow = "https://i.imgur.com/cRqW2CA.jpg"
img_lol = "https://i.imgur.com/4HZXPic.jpg"
img_what = "https://i.imgur.com/Kk6VfQQ.jpg"
img_greet = "https://i.imgur.com/9t73ixX.jpg"

#template
#begin title
title_btn = ButtonsTemplate(
                            title='您好，這是【廢棄腳踏車~重生!】活動大廳，小智機器人在此為您服務', 
                            thumbnail_image_url=img_greet,
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
str_btn = ButtonsTemplate(
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
                            #start report
str_btn_no = ButtonsTemplate(
                            title='請選擇',
                            text='Please select',
                            actions=[
                            MessageTemplateAction(
                            label="變更稱呼",
                            text="變更稱呼"),
                            MessageTemplateAction(
                            label="變更電話",
                            text="變更電話"),
                            MessageTemplateAction(
                            label="回到大廳",
                            text="回到大廳")]
                            )
#how to decide
broken_btn=ButtonsTemplate(
                            thumbnail_image_url="https://i.imgur.com/hdwQlWk.jpg",
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
                            text="建議與回饋"),
                            MessageTemplateAction(
                            label="回到大廳",
                            text="回到大廳")]
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
                            text="建議與回饋"),
                            MessageTemplateAction(
                            label="回到大廳",
                            text="回到大廳")]
                            )
#name check
name_check = ButtonsTemplate(
                            title='請寫下您讓清潔隊聯絡您的稱呼(姓名)',
                            text= "如果不想變更請按下『繼續舉報』。",
                            actions=[
                            MessageTemplateAction(
                            label="繼續舉報", 
                            text="繼續舉報")]
                            )
#phone number check
num_check = ButtonsTemplate(
                            title='請寫下讓清潔隊聯絡您的電話',
                            text= "如果不想變更請按『繼續舉報』。",
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
#photo check
photo_check = ButtonsTemplate(
    text="如果您確認照片中含有廢棄腳踏車的話，請按『確認送出』，此案件將會交由人工審查或是選擇『上傳圖片』再重新上傳",
    actions=[
        MessageTemplateAction(
        label="確認送出", 
        text="確認送出"),
        MessageTemplateAction(
        label="上傳照片",
        text="上傳照片")
    ]
    )