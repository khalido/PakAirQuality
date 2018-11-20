from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello, World!' + "<h2>this is the slash route</h2>"

#@app.route('/hello')
#def hello_world():
#    return "<h1>This is the /hello route</h1>" + '<p>Hello, World!</p>' 


if __name__ == '__main__':
    app.run()
    #app.run(host="0.0.0.0", port="5000")