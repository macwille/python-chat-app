from app import app
from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    session["username"] = username
    return redirect("/")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/subjects")
def subjects():
    return render_template("subjects.html")


@app.route("/room/<int:id>")
def room(id):
    result = db.session.execute("SELECT content FROM messages")
    messages = result.fetchall()
    return render_template("room.html", messages=messages, id=id)


@app.route("/send", methods=["POST"])
def send():
    return redirect("/")


@app.route("/search")
def search():
    result = "Time to search"
    return render_template("search.html", result=result)


@app.route("/result")
def result():
    query = request.args["query"]
    return render_template("search.html", result=query)


@app.route("/test")
def test():
    result = db.session.execute("SELECT COUNT(*) FROM messages")
    count = result.fetchone()[0]
    result = db.session.execute("SELECT content FROM messages")
    messages = result.fetchall()

    return render_template("test.html", count=count, messages=messages)
