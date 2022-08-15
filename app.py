import json
from flask import Flask
from flask import request
from flask import Response

app = Flask(__name__)
application = app # our hosting requires application in passenger_wsgi

telegram_request_path = "https://api.telegram.org/"
token = "5485671544:AAHTTwQpqxXEXJarcgN98rq7d8U5Qn_YZzw"
application_url = "https://access.process.kz/bot/"
telegram_webhook_path = telegram_request_path + "bot" + token + "/setWebhook?url=" + application_url

def write_json(data, filename='response.json'):
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4, ensure_ascii=False)

@app.route("/", methods=['POST', 'GET'])
def hello():
    if request.method == 'POST':
        msg = request.get_json()
        write_json(msg, 'telegram_request.json')
        return Response('OK, it is POST', status=200)
    else:
        return telegram_webhook_path
 
if __name__ == "__main__":
    app.run()