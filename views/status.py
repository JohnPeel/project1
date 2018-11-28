
from flask import render_template
from app import app
import flask
import db
import cx_Oracle


@app.route('/status')
def status():
    return render_template('status.html', flask=flask, oracle=cx_Oracle, db=db)
