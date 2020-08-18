from app import app
from os import getenv
from flask import Flask, url_for, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import users


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
    if users.login(username, password, db):
        flash("Welcome back", "message")
        return redirect("/")
    else:
        flash("Error logging in", "error")
        return redirect("/")


@app.route("/logout")
def logout():
    users.logout()
    flash("You've been logged out", "message")
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/registerNew", methods=["POST", "GET"])
def registerNew():
    username = request.form["username"]
    password = request.form["password"]
    if users.register(username, password, db):
        flash("Registration Successful", "message")
        return redirect("/")
    else:
        flash("Registration Failed", "message")
        return redirect(url_for("register"))


@app.route("/create/id=<int:id>")
def create(id):
    return render_template("create.html", id=id)


@app.route("/createRoom", methods=["POST", "GET"])
def createRoom():
    user_id = session["id"]
    room_name = request.form["room_name"]
    subject_id = request.form["subject_id"]

    # TODO check user rights to subject

    try:
        sql = "INSERT INTO rooms (room_name, user_id, subject_id, visible) values(:room_name, :user_id, :subject_id, 1)"
        db.session.execute(
            sql, {"room_name": room_name, "user_id": user_id, "subject_id": subject_id})
        db.session.commit()
    except:
        print("Error adding room")
        flash("Problem creating room", "error")
        return redirect(url_for("subject", id=subject_id))
    else:
        flash("Room created", "message")
        return redirect(url_for("subject", id=subject_id))


@app.route("/createSubject", methods=["POST", "GET"])
def createSubject():
    user_id = session["id"]
    subject_name = request.form["subject_name"]
    password = request.form["password"]
    content = request.form["content"]
    require = request.form["require"]
    hash_value = generate_password_hash(password)
    print(require)

    try:
        sql = "INSERT INTO subjects (subject_name, password, content, require_permission) values (:subject_name, :password, :content, :require_permission)"
        db.session.execute(
            sql, {"subject_name": subject_name, "password": hash_value, "content": content, "require_permission": require})
        db.session.commit()
        # TODO add rights to subject
    except:
        flash("Error creating subject", "error")
        return redirect(url_for("subjects"))
    else:
        flash("Subject created", "message")
        return redirect(url_for("subjects"))


@app.route("/subjects")
def subjects():
    try:
        sql = "SELECT id, subject_name, require_permission FROM subjects"
        result = db.session.execute(sql)
        subjects = result.fetchall()
    except:
        print("Error getting subjects from DB")
        flash("Error getting subjects from database", "error")
        return render_template("subjects.html")
    else:
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
        flash("Problem loading the room", "error")
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
