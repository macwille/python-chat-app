from flask import Flask

app = Flask(__name__)

# Checks for template changes when reloading web page.
app.config['TEMPLATES_AUTO_RELOAD'] = True


import routes
