from app import app
from os import getenv
from flask import Flask, url_for
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
    username = request.form["username"]
    password = request.form["password"]
    print("search for:", username)
    try:
        sql = "SELECT password, id FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username": username})
        res = result.fetchone()
    except:
        return redirect("/")
    else:

        if res == None:
            print("no user found")
            return redirect("/")
        else:
            hash_value = res[0]

            if check_password_hash(hash_value, password):
                print("correct password")
                session["username"] = username
                session["id"] = res[1]
                print("session id:", res[1])
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
        sql = "INSERT INTO users (username,password, role) VALUES (:username,:password, 1)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        print("Username already taken")
        return redirect(url_for("register"))
    else:
        session["username"] = username
        return redirect(url_for("register"))


@app.route("/subjects")
def subjects():
    return render_template("subjects.html")


@app.route("/room/id=<int:id>")
def room(id):
    error = "Room not found"
    try:

        sql = "SELECT rooms.id AS room_id, room_name, username FROM rooms LEFT JOIN users ON user_id = users.id WHERE rooms.id=:id AND rooms.visible=1"
        result = db.session.execute(sql, {"id": id})
        room = result.fetchone()
        print(room)
        room_id = room[0]
        name = room[1]
        username = room[2]

    except:
        return redirect(url_for("subjects"))
    else:
        print("search for messages")
        sql1 = "SELECT content, username, messages.created_at AS datetime  FROM messages LEFT JOIN users ON user_id = users.id LEFT JOIN rooms ON room_id = rooms.id WHERE rooms.id=:id ORDER BY messages.created_at"
        result = db.session.execute(sql1, {"id": id})
        messages = result.fetchall()
        if not messages:
            print("no messages found")
            return render_template("room.html", id=room_id, name=name,  owner=username)
        else:
            print("messages found")
            return render_template("room.html", id=room_id, name=name,  owner=username, messages=messages)


@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    room_id = request.form["room_id"]
    user_id = session["id"]
    try:
        sql = "INSERT INTO messages (user_id, room_id, content, visible) VALUES (:user_id, :room_id, :content, 1)"
        db.session.execute(
            sql, {"user_id": user_id, "room_id": room_id, "content": content})
        db.session.commit()
    except:
        print: "error inserting message to db"
        return redirect("subjects")
    else:
        return redirect(url_for("subjects"))


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/result", methods=["GET"])
def result():
    query = request.args["query"]
    return render_template("search.html", result=query)
