from flask import Flask, render_template
import flask

import db
import cx_Oracle

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello Jazy!'


@app.route('/status')
def status():
    return render_template('status.html', flask=flask, oracle=cx_Oracle, db=db.get_conn())


if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')