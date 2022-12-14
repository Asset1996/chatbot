import os
import json
import telebot
import requests

from flask import Flask
from flask import request
from flask import Response

from flask_mysqldb import MySQL
from handler import Handler

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.config.from_object('config.Config')
if os.getenv('DEBUG') == 'true':
    app.config.from_object('config.DevConfig')
else: 
    app.config.from_object('config.ProdConfig')
application = app

app.config["MYSQL_USER"] = os.getenv('DB_USER')
app.config["MYSQL_PASSWORD"] = os.getenv('DB_PASS')
app.config["MYSQL_HOST"] = os.getenv('DB_HOST')
app.config["MYSQL_DB"] = os.getenv('DB_NAME')
app.config["MYSQL_CURSORCLASS"] = "DictCursor"
mysql = MySQL(app)

bot = telebot.TeleBot(os.getenv('TOKEN'))

def write_json(data, filename='response.json'):
    """Creates and writes the json data into the file with filename."""
    with open(filename, 'a') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


@app.route("/", methods=['POST', 'GET'])
def index():
    """Main route function. Receives the message from telegram."""
    if os.getenv('DEBUG') == 'true':
        bot.remove_webhook()

        @bot.message_handler()
        def admin_of_group(message):
            bot.send_message(message.chat.id, ('DEV mode! Your message {} is saved in the DB.').format(message.text))

        bot.infinity_polling()
    else:
        webhook_info = requests.get(url=os.getenv('GET_WEBHOOK_INFO_PATH'))
        wh_info = webhook_info.json()
        if not wh_info['result']['url']:
            bot.set_webhook(url=os.getenv('SET_WEBHOOK_PATH'))
        
        if request.method == 'POST':
            message = request.get_json()
            chat_id, text = (
                message['message']['chat']['id'],
                message['message']['text'],
            )

            write_json(message, 't_message.json')
            handler = Handler(message, mysql)
            handler.make()

            bot.send_message(chat_id, 'Your message "{}" is saved in the DB'.format(text))
            return Response('OK, it is POST', status=200)
        else:
            return os.getenv('SET_WEBHOOK_PATH')

@app.route("/test", methods=['POST', 'GET'])
def test():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT name, email FROM support_user WHERE id=1""")
    rv = cur.fetchall()
    print(rv)
    return Response('OK, it is TEST page for db' + rv[0]['name'], status=200)

if __name__ == "__main__":
    """Runner of the application."""
    app.run()