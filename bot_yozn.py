import json
import requests
from slackbot import bot

from slackbot.bot import Bot
from slackbot.bot import listen_to
to='xoxb-240483497840-YvKJLTvTyakjCTmeh3JkVmGC'
to1='xoxp-240900795988-240193395344-241099344882-c6f9b9b526ddd3f2bb1c27a1a97e86d9'
bot.settings.API_TOKEN  = to1
import threading, time

class MyClass (threading.Thread): # 繼承 Thread 類別
       def run(self):
           bot = Bot()
           print('bot is running...')
           bot.run()

@listen_to("hero:" + ' (.*)')
def receive_question(message, question_string):
    pos='receive from hero:'+question_string
    message.send(pos)
    t='yozn: '+question_string
    message.send(t)

MyClass().start() # 啟動執行緒

def send2slack(text):
    bb="yozn: "+text
    s_url = 'https://hooks.slack.com/services/T72SGPDV2/B745DN7B9/t1YkLh4LMoUkmXXxX2XZ4gln'

    dict_headers = {'Content-type': 'application/json'}

    dict_payload = {
        "text": bb}
    json_payload = json.dumps(dict_payload)

    rtn = requests.post(s_url, data=json_payload, headers=dict_headers)

def main():
    while True:
        ss=input()
        send2slack(ss)







if __name__ == '__main__':
    main()



