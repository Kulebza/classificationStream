import os
from flask import Flask

app = Flask(__name__, static_folder=None)



@app.route('/')
def hello_world():
    return 'Hello World!'