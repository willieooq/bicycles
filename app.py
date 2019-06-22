from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi("Z89KlbPxoc+N16dQw2gIOBUj1nht+r3FZLqjnHdGHX/WUZ8WpdvueISiYf+0J71JNll4ZJBw+D3QEHDjI8AwqxMMcS8dISHLl5YKn+FEyEnWp3Yt7pqE+Pl7hJ/5bgBSYOeyniI/pBKiD89LfE6+dwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler('bd799d810b0b87531264f40763235c56')
to = "Ue7aa1b3d42ca4e7df1dc143cbc97d13c"

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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message = TextSendMessage(text=event.message.text)
    line_bot_api.reply_message(event.reply_token, message)

import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
