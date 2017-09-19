import os
import sys

from argparse import ArgumentParser
import requests
import json
from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)
def send2yozn(text):
    a = json.dumps({"text": text})
    r = requests.post("http://140.134.26.28:2914/callback", data=a)
    return r.text
def send2slack(text):
    aa="hero: "+text
    s_url = 'https://hooks.slack.com/services/T72SGPDV2/B745DN7B9/t1YkLh4LMoUkmXXxX2XZ4gln'

    dict_headers = {'Content-type': 'application/json'}

    dict_payload = {
        "text": aa}
    json_payload = json.dumps(dict_payload)

    rtn = requests.post(s_url, data=json_payload, headers=dict_headers)
app = Flask(__name__)

# get channel_secret and channel_access_token from your environment variable
channel_secret = os.getenv('LINE_CHANNEL_SECRET', None)
channel_access_token = os.getenv('LINE_CHANNEL_ACCESS_TOKEN', None)
if channel_secret is None:
    print('Specify LINE_CHANNEL_SECRET as environment variable.')
    sys.exit(1)
if channel_access_token is None:
    print('Specify LINE_CHANNEL_ACCESS_TOKEN as environment variable.')
    sys.exit(1)

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    tok = eval(body)['events'][0]['replyToken']
    textt = eval(body)['events'][0]['message']['text']
    # toslack.slack_send(textt)
    print(textt)
    ans=send2yozn(textt)
    # send2slack(textt)
    # handle webhook body
    try:
        handler.handle(body, signature)

        
        line_bot_api.reply_message(
            tok,
            TextSendMessage(text=ans)
        )
    except InvalidSignatureError:
        abort(400)

    return 'OK'


# @handler.add(MessageEvent, message=TextMessage)
# def message_text(event):
#     line_bot_api.reply_message(
#         event.reply_token,
#         TextSendMessage(text=event.message.text)
#     )


if __name__ == "__main__":
    arg_parser = ArgumentParser(
        usage='Usage: python ' + __file__ + ' [--port <port>] [--help]'
    )
    arg_parser.add_argument('-p', '--port', default=8000, help='port')
    arg_parser.add_argument('-d', '--debug', default=False, help='debug')
    options = arg_parser.parse_args()

    app.run(debug=options.debug, port=options.port)