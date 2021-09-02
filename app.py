from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
from UserData import UserDataHandle
import pandas as pd

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('ahG3SbCDu1RG4P+qxRHQXLYnqFjAXjSn3zE1q+6OkSwgHt/6OoylT60gzjWHnsiVcT+o1k0fJltFvJ9sNwlo4DryCpTdFE6WCvUNrum/e7x4gJU5VcxFkibs421KBI+IRVxT8q1JBCDHKk0PR6XoEQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('9645c319f34c541b3389fe2e1c27821a')
# Worldwide Setting
checkword_bad = ["白目","壞","笨","幹","低能","王八蛋","討厭"]
checkword_good = ["小龍好帥",]
timeconvert = {"早":"153 08:00～14:00","晚":"153 21:30～2:00"}
#印出填單者資料
def show(mes):
    lines = ""
    for i in list(mes):
        lines+= timeconvert[i]+"\n"
        print(timeconvert[i])
        for j in range(1,3):
            lines+=str(j)+"團\n\n"
            print(j,"團\n\n")
            for n,x in enumerate(mes[i][j]):
                lines+=str(n+1)+"."+x+"\n"
                print(n+1,".",x)
                if n ==len(mes[i][j])-1:
                    lines+="★－:+:－:+:－:+:－:+:－★\n"
                    print("★－:+:－:+:－:+:－:+:－★")
    return lines

button_template_message =ButtonsTemplate(
                            thumbnail_image_url="https://i.imgur.com/i8tEmlY.jpg",
                            title='哼！', 
                            text='選擇動作',
                            ratio="1.51:1",
                            image_size="cover",
                            actions=[
#                                PostbackTemplateAction 點擊選項後，
#                                 除了文字會顯示在聊天室中，
#                                 還回傳data中的資料，可
#                                 此類透過 Postback event 處理。
                                PostbackTemplateAction(
                                    label='填單', 
                                    text='填單',
                                    data='action=buy&itemid=1'
                                ),
                                # MessageTemplateAction(
                                #     label='填單', text='填單'
                                # ),
                                URITemplateAction(
                                    label='巴哈楓之谷m', uri='https://forum.gamer.com.tw/B.php?bsn=29461'
                                ),
                                URITemplateAction(
                                    label='楓之谷m官方臉書粉絲團', uri='https://www.facebook.com/TW.PlayMapleM/?epa=SEARCH_BOX'
                                )
                            ]
                        )


# 監聽所有來自 /callback 的 Post Request
@app.route("/callback/", methods=['POST'])
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
    # form = UserDataHandle()
    if event.message.text == "功能":
        line_bot_api.reply_message(event.reply_token, TemplateSendMessage(alt_text="Template Example", template=button_template_message))
    elif event.message.text == "填單":
        datadict = {"早":{1:[],2:[]},"晚":{1:[],2:[]}}
        dataDF = pd.DataFrame(datadict)
        dataDF.to_json("datadict.json")
        dfjson = pd.read_json("datadict.json")
        lines = show(dfjson)
        # form.createemptyform()
        # lines = form.readData()
        message_init = TextSendMessage(text=lines)
        line_bot_api.reply_message(event.reply_token,message_init)
    
    elif any(ext in event.message.text for ext in checkword_bad):
        message = TextSendMessage(text="阿紹才是{}".format(event.message.text))
        line_bot_api.reply_message(event.reply_token, message)
    elif any(ext in event.message.text for ext in checkword_good):
        texts = "紅茶超可愛~~~~"
        tex1 = ""
        for i in range(3):
            if i!=2:
                tex1 += texts+"\n"
            else:
                tex1 += texts
        message = TextSendMessage(text=tex1)
        line_bot_api.reply_message(event.reply_token, message)

    elif len(event.message.text.split(" ")) == 3:
        one = event.message.text.split(" ")
        dfjson = pd.read_json("datadict.json")
        dfjson[one[0]][int(one[1])].append(one[2])
        dfjson.to_json("datadict.json")
        lines = show(dfjson)
        # lines = form.addmessage(event.message.text)
        message_init = TextSendMessage(text=lines)
        line_bot_api.reply_message(event.reply_token, message_init)

    
    
import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)