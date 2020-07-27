from app import app
from flask import render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://postgres:postgres@localhost:5432/messages"
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login/")
def login():
    return render_template("login.html")


@app.route("/room/")
def room():
    
    return render_template("room.html")


@app.route("/send", methods=["POST"])
def send():
    return redirect("/")
