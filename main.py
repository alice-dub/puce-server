from flask import Flask 

app = Flask(__ name __)


@app.route('/')
def hello_world():
    return 'Hello, World!'

