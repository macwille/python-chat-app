
from flask import Flask


app = Flask(__name__)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True

# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///chat:1234@localhost:5432/chat"
# app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://chatuser:1234@localhost:5432/chat"
# db = SQLAlchemy(app)

import routes