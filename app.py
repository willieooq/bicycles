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
app = Flask(__name__)


# Channel Access Token
line_bot_api = LineBotApi("Z89KlbPxoc+N16dQw2gIOBUj1nht+r3FZLqjnHdGHX/WUZ8WpdvueISiYf+0J71JNll4ZJBw+D3QEHDjI8AwqxMMcS8dISHLl5YKn+FEyEnWp3Yt7pqE+Pl7hJ/5bgBSYOeyniI/pBKiD89LfE6+dwdB04t89/1O/w1cDnyilFU=")
handler = WebhookHandler('bd799d810b0b87531264f40763235c56')
to = "Ue7aa1b3d42ca4e7df1dc143cbc97d13c"
#選單
#大廳

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


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    message_content = line_bot_api.get_message_content('<message_id>')
    with open(file_path, 'wb') as fd:
        for chunk in message_content.iter_content():
            fd.write(chunk)
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

