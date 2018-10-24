from flask import Flask

try:
    import cx_Oracle
    cx_Oracle_test = 'SUCCESS'
except ImportError:
    cx_Oracle_test = 'FAILED'

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello Jazy! ' + cx_Oracle_test

if __name__ == '__main__':
    app.run(debug=False, host='0.0.0.0')
