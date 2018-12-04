from flask import Flask
app = Flask(__name__)

from views import *


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True, host='0.0.0.0')
