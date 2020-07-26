
from flask import Flask
from flask import render_template


app = Flask(__name__)

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')

import routes