#from http.server import BaseHTTPRequestHandler
from cowpy import cow
from flask import Flask
import os

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
FB_CLIENT_TOKEN = os.getenv("FB_CLIENT_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")


# handle incoming messages and reply to them
@app.route('/fbhook', methods=['POST'])
def handle_incoming_messages():
    print("incoming message handling started")
    data = request.json

    print("---printing the data we get from facebook---")
    print(data)
    print("---------------------------------")
    
    msg = data['entry'][0]['messaging'][0]

    message_text = msg['message']['text']   # txt of msg
    nlp_json = msg["message"]["nlp"]['entities'] # nlp parsed dict

    reply(sender_id, "your msg was: " + message_text)
    # send NLP dict for debugging
    reply(sender_id, str(nlp))

# handle verification challange from fb to authenticate the app
@app.route('/fbhook', methods=['GET'])
def handle_verification():
    if (request.args['hub.verify_token'] == VERIFY_TOKEN):
        print("Verified")
        return request.args['hub.challenge']
    else:
        print("Wrong token")
        return "Error, wrong validation token"


def is_typing(user_id):
    """sends a is typing msg to user_id"""
    data = {
        "recipient": {"id": user_id},
        "sender_action": "typing_on"
    }
    post_url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + PAGE_ACCESS_TOKEN
    resp = requests.post(post_url, json=data)


def reply(user_id, msg=None, image_url=None):
    """takes in user_id and a msg and sends it
    takes in either a msg or image_url, not both"""
    if image_url:
        data = {'recipient': {'id': '1718968874810833'}, 
                'message': {'attachment': 
                {'type': 'image', 
                'payload': {'url': image_url }}}}
    else:
        data = {"recipient": {"id": user_id}, 
                "message": {"text": msg}}

    post_url = "https://graph.facebook.com/v2.6/me/messages?access_token=" + PAGE_ACCESS_TOKEN
    resp = requests.post(post_url, json=data)

if __name__ == '__main__':
    app.run(debug=True)
    #app.run(debug=True, port=5000)
    #app.run(host="0.0.0.0", port="80")
    
    
"""
class handler(BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/plain')
        self.end_headers()
        message = cow.Cowacter().milk('Hello from Python on Now Lambda!1111111')
        self.wfile.write(message.encode())
        return
"""
