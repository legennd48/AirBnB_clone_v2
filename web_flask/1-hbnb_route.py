#!/usr/bin/python3
''' scripts that starts a flask web application that
displays “Hello HBNB!” on rout / and “HBNB” on rout /hbnb
'''

from flask import Flask

app = Flask(__name__)


@app.route("/", strict_slashes=False)
def hello():
    ''' reurn the hello greeting'''
    return "Hello HBNB"


@app.route("/hbnb", strict_slashes=False)
def hbnb():
    '''returns hbnb'''
    return "HBNB"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
