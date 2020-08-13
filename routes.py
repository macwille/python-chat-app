from app import app
from os import getenv
from flask import Flask, url_for, flash, redirect, render_template, request, session
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
            flash("User name or password incorrect", "message")
            return redirect("/")
        else:
            hash_value = res[0]

            if check_password_hash(hash_value, password):
                session["username"] = username
                session["id"] = res[1]
                print("session username", res[0])
                print("session id:", res[1])
                flash("Welcome back!", "message")
                return redirect("/")
            else:
                print("wrong password")
                flash("User name or password incorrect", "message")
                return redirect("/")


@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("id", None)
    flash("You've been logged out", "message")
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
        flash("Username already taken", "error")
        return redirect(url_for("register"))
    else:
        sql = "SELECT id FROM users where username=:username"
        result = db.session.execute(sql, {"username": username})
        id = result.fetchone()[0]
        print(id)
        session["username"] = username
        session["id"] = id
        flash("Registration successful", "message")

        return redirect("/")


@app.route("/subjects")
def subjects():
    try:
        sql = "SELECT id, subject_name, require_permission FROM subjects"
        result = db.session.execute(sql)
        subjects = result.fetchall()
    except:
        print("Error getting subjects from DB")
        return render_template("subjects.html")
    else:
        print("subjects.html with subjects from DB")
        return render_template("subjects.html", subjects=subjects)


@app.route("/room/id=<int:id>")
def room(id):
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


@app.route("/subject/id=<int:id>")
def subject(id):
    try:
        sql = "SELECT * FROM subjects WHERE id=:id"
        result = db.session.execute(sql, {"id": id})
        subject = result.fetchone()
        subject_id = subject[0]
        subject_name = subject[1]
        secret = subject[2]
        content = subject[3]

    except:
        print("error getting data from DB")
        return redirect(url_for("subjects"))
    else:
        sql1 = "SELECT id, room_name FROM rooms WHERE subject_id=:id"
        result = db.session.execute(sql1, {"id": id})
        rooms = result.fetchall()
        return render_template("subject.html", subject_name=subject_name, rooms=rooms, id=subject_id, content=content)


@app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    room_id = request.form["room_id"]
    user_id = session["id"]
    try:
        sql = "INSERT INTO messages (user_id, room_id, content, created_at, visible) VALUES (:user_id, :room_id, :content, NOW(), 1)"
        db.session.execute(
            sql, {"user_id": user_id, "room_id": room_id, "content": content.strip()})
        db.session.commit()
    except:
        print: "error inserting message to db"
        return redirect("subjects")
    else:
        return redirect(url_for("room", id=room_id))


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/result", methods=["GET"])
def result():
    try:
        query = request.args["query"]
        sql = "SELECT username, room_name, content FROM messages LEFT JOIN users ON user_id = users.id LEFT JOIN rooms on room_id = rooms.id WHERE content LIKE :query"
        sql_query = db.session.execute(sql, {"query": "%"+query+"%"})
        results = sql_query.fetchall()
    except:
        return redirect(url_for("search"))
    else:
        if not results:
            flash("No results", "message")
            return redirect(url_for("search"))
        else:
            print(results)
            return render_template("search.html", results=results, query=query)
