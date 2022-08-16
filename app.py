import json
from typing import Dict
from flask import Flask
from flask import request
from flask import Response
from dotenv import load_dotenv
load_dotenv()
import os, re

app = Flask(__name__)
application = app

def write_json(data, filename='response.json'):
    """Creates and writes the json data into the file with filename."""
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

def parse_data(message:Dict):
    """Parses the message dictionary from telegram."""
    chat_id = message['message']['chat']['id']
    txt = message['message']['text']

    pattern = '^/(\w)*'
    ticker = re.search(pattern, txt)

    symbol = ''
    if ticker:
        symbol = ticker[0][1:].upper()

    return chat_id, symbol

def send_message(chat_id, text=''):
    """Sends message to the user."""
    url = os.getenv('SEND_MESSAGE_URL')
    payload = {'chat_id':chat_id, 'text':text}

    response = request.post(url, json=payload)
    return response

@app.route("/", methods=['POST', 'GET'])
def index():
    """Main route function. Receives the message from telegram."""
    if request.method == 'POST':
        msg = request.get_json()
        chat_id, symbol = parse_data(msg)

        if not symbol:
            send_message(chat_id, 'Wrong data')
            return Response('OK', status=200)

        write_json(msg, 'telegram_request.json')
        send_message(chat_id, 'Good command')
        return Response('OK, it is POST', status=200)
    else:
        return os.getenv('TELEGRAM_WEBHOOK_PATH')
 
if __name__ == "__main__":
    """Runner of the application."""
    app.run()