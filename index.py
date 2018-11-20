#from http.server import BaseHTTPRequestHandler
from cowpy import cow
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    message = cow.Cowacter().milk('Hello from Python on Now Lambda!1111111')
    return 'Hello, World!' + message

if __name__ == '__main__':
    #app.run()
    app.run(debug=True, port=5000)
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
