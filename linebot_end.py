from flask import Flask, request
from linebot import LineBotApi, WebhookHandler
from linebot.models import TextSendMessage   # 載入 TextSendMessage 模組
import json
import os
import openai

openai_api_key = os.getenv("OPENAI_API_KEY")
app = Flask(__name__)

def openai_a(msg):
    completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "你是一名聊天機器人."},
        {"role": "user", "content": msg}
    ]
    )

    return completion.choices[0].message.content

CHANNEL_SECRET = "CHANNEL_SECRET"
CHANNEL_ACCESS_TOKEN = "CHANNEL_ACCESS_TOKEN"

@app.route("/", methods=['GET'])
def home():
    return "Hi"

@app.route("/", methods=['POST'])
def linebot():
    body = request.get_data(as_text=True)
    json_data = json.loads(body)
    print(json_data)
    try:
        line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
        handler = WebhookHandler(CHANNEL_SECRET)
        signature = request.headers['X-Line-Signature']
        handler.handle(body, signature)
        tk = json_data['events'][0]['replyToken']         # 取得 reply token
        msg = json_data['events'][0]['message']['text']   # 取得使用者發送的訊息
        re = openai_a(msg)
        text_message = TextSendMessage(text = re) # gpt回覆
        
        line_bot_api.reply_message(tk,text_message)       # 回傳訊息至客戶端
    except Exception as e:
        print('error: ' + str(e))
    return 'OK'
print("OpenAI API Key:", openai_api_key)
app.run(port="5000")
