#from http.server import BaseHTTPRequestHandler
from flask import Flask
import os

app = Flask(__name__)

PAGE_ACCESS_TOKEN = os.getenv("PAGE_ACCESS_TOKEN")
FB_CLIENT_TOKEN = os.getenv("FB_CLIENT_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN")
TEST_SECRET_KEY = os.getenv("TEST_SECRET_KEY")


@app.route('/')
def hello_world():
    message = "<h1>This is a test</h1> <p>And this is a paragragh.</p>"
    
    if type(PAGE_ACCESS_TOKEN) == str:
        message += "<p>Page access token loaded<p>"

    return message + f"<p>Test Secret key is: {TEST_SECRET_KEY}</p> "