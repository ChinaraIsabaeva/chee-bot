# -*- coding: utf-8 -*-

import os
import json
import requests

from flask import Flask, request, redirect, url_for

WEBHOOK_URL_PATH = "/getUpdates/%s/" % (os.environ['TOKEN'])
PORT = int(os.environ['PORT'])

app = Flask(__name__)

@app.route('/')
def home():
    print ("Syasha ne prav")
    return 'Hello chee-bot'

@app.route('/updates/')
def last_updated(data):
    return data

@app.route(WEBHOOK_URL_PATH, methods=['POST'])
def webhook():
    if request.method == 'POST':
        updates = request.get_json()
        print (updates['message']['text'] == 'price')
        if updates['message']['text'] == 'price':
            chat_id = updates['message']['text']
            message_id = updates['message']['message_id']
            message = {'chat_id': chat_id, 'text': 'code succed'}
            requests.post("https://api.telegram.org/bot120560818:AAHKRbbHYEM9l7PIxuW1-3alAGQ1PV0NeUE/sendMessage", json=message)
            print (requests.post("https://api.telegram.org/bot120560818:AAHKRbbHYEM9l7PIxuW1-3alAGQ1PV0NeUE/sendMessage", json=message).json())

    
        
if __name__ == '__main__':
    app.run(debug=True, port=PORT)
