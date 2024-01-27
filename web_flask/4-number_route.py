#!/usr/bin/python3
''' scripts that starts a flask web application that
displays “Hello HBNB!” on rout / and “HBNB” on rout /hbnb
and C followed by varaible if on rout /c/<text>
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


@app.route("/c/<text>", strict_slashes=False)
def c(text):
    '''
    returns C followed by variable
    and replaces _ with a space
    '''
    return "C {}".format(text.replace('_', ' ') if '_' in text else text)


@app.route("/python/", defaults={'text': 'is cool'}, strict_slashes=False)
@app.route("/python/<text>", strict_slashes=False)
def python(text):
    '''
    returns python followed by variable
    and replaces _ with a space
    '''
    return "Python {}".format(text.replace('_', ' ') if '_' in text else text)


@app.route("/number/<int:n>", strict_slashes=False)
def number(n):
    ''' displays “n is a number” only if n is an integer '''
    try:
        n = int(n)
        return "{} is a number".format(n)
    except Exception as e:
        pass


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
