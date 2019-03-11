from flask import Flask, request
import os
import requests

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
FB_CLIENT_TOKEN = os.getenv("FB_CLIENT_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
TEST_SECRET_KEY = os.getenv("TEST_SECRET_KEY")

VERBOSE = True

# keep track of the last msg received to handle duplicate msgs from fB
last_msg_id = "None at the moment"
last_msg_intent = "None"

# handle incoming messages and reply to them
@app.route('/facebook', methods=['POST'])
def handle_incoming_messages():
    print("incoming message handling started")
    data = request.json

    print("---printing the data we get from facebook---")
    print(data)
    print("---------------------------------")
    
    sender_id = data['entry'][0]['messaging'][0]['sender']['id']     
    recipient_id = data['entry'][0]['messaging'][0]['recipient']['id']

    # deal with blank messages
    if "message" not in data['entry'][0]['messaging'][0].keys():
        print("No msg received, sending ok response")    
        return "ok", 200

    msg = data['entry'][0]['messaging'][0]['message']
    
    # hacky way to handle getting repeated messages
    global last_msg_id
    if msg['mid'] == last_msg_id:
        print("this is the same msg as the last one")
        return "ok", 200
    
    last_msg_id = msg['mid']


    # send is_typing msg
    if VERBOSE: 
        print("Sent is_typing msg")
    is_typing(sender_id)

    # check what kind of msg it is
    if 'attachments' in msg.keys(): # deal with file
        if msg['attachments'][0]['type'] == 'file':
            print("----file received----")
            reply(sender_id, "Attachment received, trying to parse it")
            file_url = msg['attachments'][0]['payload']['url']
            file_name = utils.deal_with_file(sender_id, file_url)
            if file_name:
                msg = utils.new_csv(sender_id, file_name, file_url)
                reply(sender_id, msg)
            else:
                reply(sender_id, "couldn't download your file, try again")
        else:
            reply(sender_id, "Attachment received, can't deal with it, the bot can only deal with air quality questions for now.")  
            reply(sender_id, "Try asking a question, like `whats the weather forecast?`")
        # do nothing for now
        return "ok", 200
    else: # assume its text
        message_text = msg['text']   # txt of msg
        nlp_json = msg['nlp']['entities'] # nlp parsed dict
        
        nlp = {} # simplified nlp dict
        for key in nlp_json.keys():
            nlp[key] = nlp_json[key][0]["value"]
            nlp[key+"_confidence"] = nlp_json[key][0]["confidence"]
            if key == "datetime":
                nlp["date_grain"] = nlp_json[key][0]["grain"]
    
    if VERBOSE:
        print("echo msg back for debugging")
        reply(sender_id, "your msg was: " + message_text)
        print("send NLP dict for debugging")
        reply(sender_id, str(nlp))
        print("--"*10)

    
    # main if/else loop to make sense of different kinds of intents
    if 'intent' in nlp.keys():
        intent = nlp['intent']
        if intent == "air":
            #intent_air(sender_id, nlp, data)
            reply(sender_id, "Yay! You want to know about the air? Well WAIT`")
        else:
            reply(sender_id, "Try asking a question, like `hows the air q in Karachi?`")
    else:
        print("no intents found")
        reply(sender_id, "I can only asnwer questions about a few things")    
    return "ok", 200

# handle verification challange from fb to authenticate the app
@app.route('/facebook', methods=['GET'])
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
    app.run(debug=True)
    #app.run(debug=True, port=5000)
    #app.run(host="0.0.0.0", port="80")