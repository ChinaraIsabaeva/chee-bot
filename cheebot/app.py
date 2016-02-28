# -*- coding: utf-8 -*-

import os
import requests

from flask import Flask, request



WEBHOOK_URL_PATH = "/getUpdates/{token}/".format(token=os.environ['TOKEN'])
PORT = int(os.environ['PORT'])

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello chee-bot'

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.method == 'POST':
        updates = request.get_json()
        chat_id = updates['message']['chat']['id']
        text = ''
        keyboard = [['A', 'B'], ['C',]]
        message = dict(chat_id=updates['chat_id'], text=text, reply_markup=dict(keyboard=keyboard, resize_keyboard=True))
        print (updates)
        if updates['message']['text'] == 'price':
            message['text'] = 'You could receive prices soon'
        elif updates['message']['text'] in ['привет', 'Привет', 'hi', 'Hi', 'HI', 'hello', 'Hello']:
            print ('hello')
            message['text'] = 'Привет\nЯ хорошо'
        else:
            message['text'] = 'Я не знаю, что на это сказать'
        requests.post('https://api.telegram.org/bot120560818:AAHKRbbHYEM9l7PIxuW1-3alAGQ1PV0NeUE/sendMessage', json=message)
        return 'OK'

    
        
if __name__ == '__main__':
    app.run(debug=True, port=PORT)
