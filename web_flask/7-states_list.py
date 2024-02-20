#!/usr/bin/python3
'''
starts a web server listening on port 5000 at 0.0.0.0
'''

from flask import Flask, render_template
from models import storage

app = Flask(__name__)


@app.route("/states_list", strict_slashes=False)
def states_list():
    '''
    displaysh html page using render_template
    '''
    states = storage.all("State")
    return render_template("7-states_list.html", states=states)


@app.teardown_appcontext
def teardown(exc):
    '''
    closes current sqlalchemy session
    '''
    storage.close()


if __name__ == "__main__":
    app.run(host='0.0.0.0.')
