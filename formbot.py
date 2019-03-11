from flask import Flask, request
import os
import requests
import json

app = Flask(__name__)

# accept data from manychat
@app.route('/formbot', methods=['POST'])
def handle_message():
    print("incoming message handling started")
    data = request.json

    print("---printing the data we get from manychat in a POST---")
    print(data)
    print("---------------------------------")

    data = {'recipient': {'id': '1718968874810833'}, 
                'message': {'attachment': 
                {'type': 'image', 
                'payload': {'url': "test_url" }}}}
    
    msg = {
    "type": "text",
    "text": "test message from my pc",
    }

    return "ok", 200

# reply with data
@app.route('/formbot', methods=['GET'])
def do_stuff():
    query = request.args
    print("---printing the data we get from manychat in a GET---")
    print(request)
    print(query)
    print(request.headers)
    print(list(query.items()))
    print("---------------------------------")

    school = request.headers.get('class', "Class_Name")
    name = request.headers.get("name", 'Fake Name')
    print(f"School: {school} Name: {name}")

    msg = {
        "version": "v2",
        "content": {
            "messages": [
                {
                "type": "text",
                "text": f"hello {name} from the server! I've found {school} near you!"    
                }
            ]
            }
    }
    
    return json.dumps(msg)
    #r = requests.post(url=None, json=msg)
    return "ok", 200



def reply(user_id, msg="No message specified", image_url=None):
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
    app.run()
    #app.run(host="0.0.0.0", port="5000")