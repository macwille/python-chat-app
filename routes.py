from app import app
from os import getenv
from flask import Flask
from flask import redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash


app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
db = SQLAlchemy(app)


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    name = request.form["username"]
    password = request.form["password"]
    print("search for:", name)
    error = "Error"

    try:
        sql = "SELECT password FROM users WHERE name=:name"
        result = db.session.execute(sql, {"name": name})
        res = result.fetchone()

    except:
        return redirect("/")

    else:

        if res == None:
            print("no user found")
            flash(error)
            return redirect("/")

        else:
            hash_value = res[0]

            if check_password_hash(hash_value, password):
                print("correct password")
                session["username"] = name
                return redirect("/")
            else:
                print("wrong password")
                return redirect("/")


@app.route("/logout")
def logout():
    try:
        del session["username"]
    except:
        return redirect("/")
    else:
        return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/registerNew", methods=["POST", "GET"])
def registerNew():
    username = request.form["username"]
    password = request.form["password"]
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (name,password, role) VALUES (:name,:password, 1)"
        db.session.execute(sql, {"name": username, "password": hash_value})
        db.session.commit()
    except:
        print("Username already taken")
        return redirect("/register")
    else:
        session["username"] = username
        return redirect("/register")


@app.route("/subject")
def subjects():
    return render_template("subject.html")


@app.route("/room/id=<int:id>")
def room(id):
    try:
        sql = "SELECT * FROM rooms WHERE id=:id"
        result = db.session.execute(sql, {"id": id})
        name = result.fetchone()[1]

    except:
        print("Not found")
        return render_template("room.html", name="ROOM NOT FOUND")
    else:
        return render_template("room.html", name=name)


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
