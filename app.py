
from flask import Flask
from waitress import serve


app = Flask(__name__)
serve(app, host='0.0.0.0', port=8080, url_scheme='https')

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True


import routes