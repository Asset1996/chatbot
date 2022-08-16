import os
import json
import telebot
from handler import Handler
from typing import Dict
from flask import Flask
from flask import request
from flask import Response
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
application = app

bot = telebot.TeleBot(os.getenv('TOKEN'))
handle = Handler(bot)

def write_json(data, filename='response.json'):
    """Creates and writes the json data into the file with filename."""
    with open(filename, 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

@app.route("/", methods=['POST', 'GET'])
def index():
    """Main route function. Receives the message from telegram."""
    if os.getenv("DEBUG") == 'true':
        handle.start(request)
        return Response('OK, it is DEBUG MODE', status=200)
    else:
        if request.method == 'POST':
            handle.start(request)
            return Response('OK, it is POST', status=200)
        else:
            return os.getenv('SET_WEBHOOK_PATH')
        
 
if __name__ == "__main__":
    """Runner of the application."""
    app.run(debug=True)