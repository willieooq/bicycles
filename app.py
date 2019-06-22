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
line_bot_api = LineBotApi("0HeKZptErpSs8xltB0YpD86qXJOMWPx/d6D0+G5g9uefBXuL/Iz36WlozauV+02cj0Vc44QJ0EQxgmUd0P5oDc/m6zWD4HBdofi6EfhMcA0l0gY8ODpvc8Unei5JivvxQJMPfkQ2qSRkCwwnwd+nxQdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler('a54a6f99bc65ee5271965bab352c644e')
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
