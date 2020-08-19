from app import app
from os import getenv
from flask import Flask, url_for, flash, redirect, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
import usersService
import roomsService
import subjectsService


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
    if usersService.login(username, password, db):
        flash("Welcome back", "message")
        return redirect("/")
    else:
        flash("Error logging in", "error")
        return redirect("/")


@app.route("/logout")
def logout():
    usersService.logout()
    flash("You've been logged out", "message")
    return redirect("/")


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/registerNew", methods=["POST", "GET"])
def registerNew():
    username = request.form["username"]
    password = request.form["password"]
    if usersService.register(username, password, db):
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

    if roomsService.createRoom(user_id, room_name, subject_id, db):
        flash("Room created", "message")
        return redirect(url_for("subject", id=subject_id))

    else:
        flash("Problem creating room", "error")
        return redirect(url_for("subject", id=subject_id))


@app.route("/deleteRoom/id=<int:id>")
def deleteRoom(id):
    if roomsService.deleteRoom(id, db):
        flash("Room deleted", "message")
        return redirect(url_for("subjects"))
    else:
        flash("Error deleting room", "error")
        return redirect(url_for("subjects"))


@app.route("/createSubject", methods=["POST", "GET"])
def createSubject():
    user_id = session["id"]
    subject_name = request.form["subject_name"]
    password = request.form["password"]
    content = request.form["content"]
    require = request.form["require"]

    if subjectsService.createSubject(user_id, subject_name, password, content, require, db):
        flash("Subject created", "message")
        return redirect(url_for("subjects"))
    else:
        flash("Error creating subject", "error")
        return redirect(url_for("subjects"))


@app.route("/subjects")
def subjects():
    subjectsData = subjectsService.getSubjects(db)
    if subjectsData is not None:
        return render_template("subjects.html", subjects=subjectsData)
    else:
        return render_template("subjects.html")


@app.route("/room/id=<int:id>")
def room(id):
    roomData = roomsService.getRoom(id, db)
    if roomData is not None:
        room_id = roomData[0]
        name = roomData[1]
        username = roomData[2]
        messages = roomsService.getMessages(room_id, db)
        if messages is not None:
            return render_template("room.html", id=room_id, name=name,  owner=username, messages=messages)
        else:
            return render_template("room.html", id=room_id, name=name,  owner=username)
    else:
        flash("Room not found", "error")
        return redirect(url_for("subjects"))


@app.route("/subject/id=<int:id>")
def subject(id):
    subjectData = subjectsService.getSubject(id, db)
    if subjectData is not None:
        subject_id = subjectData[0]
        subject_name = subjectData[1]
        secret = subjectData[2]
        content = subjectData[3]
        require = subjectData[4]
        roomsData = subjectsService.getRooms(subject_id, db)
        hasRight = subjectsService.hasRights(session["id"], subject_id, db)

        if roomsData is not None:
            return render_template("subject.html", subject_name=subject_name, rooms=roomsData, id=subject_id, content=content, require=require, hasRight=hasRight)
        else:
            return render_template("subject.html", subject_name=subject_name, id=subject_id, content=content, require=require, hasRight=hasRight)
    else:
        return redirect(url_for("subjects"))


@app.route("/subjectLogin", methods=["POST"])
def subjectLogin():
    subject_id = request.form["id"]
    password = request.form["password"]

    if subjectsService.checkPassword(subject_id, password, db):
        subjectsService.setRightsById(session["id"], subject_id, db)
        flash("Access granted", "message")
        return redirect(url_for("subject", id=subject_id))
    else:
        flash("Access denied", "error")
        return redirect(url_for("subject", id=subject_id))


@ app.route("/send", methods=["POST"])
def send():
    content = request.form["content"]
    room_id = request.form["room_id"]
    user_id = session["id"]

    lengths = [len(x) for x in content.split()]
    if any(l > 30 for l in lengths):
        flash("Don't spam", "message")
        return redirect(url_for("room", id=room_id))

    else:
        try:
            sql = "INSERT INTO messages (user_id, room_id, content, created_at, visible) VALUES (:user_id, :room_id, :content, NOW(), 1)"
            db.session.execute(
                sql, {"user_id": user_id, "room_id": room_id, "content": content.strip()})
            db.session.commit()
        except:
            return redirect("subjects")
        else:
            return redirect(url_for("room", id=room_id))


@ app.route("/search")
def search():
    return render_template("search.html")


@ app.route("/setVisible/id=<int:id>", methods=["GET"])
def setVisible(id):
    user_id = session["id"]
    try:
        if session["admin"]:
            sql = "UPDATE messages SET visible = 0 WHERE id = :id"
            db.session.execute(sql, {"id": id})
            db.session.commit()
        else:
            sql = "UPDATE messages SET visible = 0 WHERE id = :id AND user_id = :user_id"
            db.session.execute(sql, {"id": id, "user_id": user_id})
            db.session.commit()
    except:
        flash("Error deleteting message", "error")
        return redirect(url_for("subjects"))
    else:
        flash("Message deleted", "message")
        return redirect(url_for("subjects"))


@ app.route("/result", methods=["GET"])
def result():
    try:
        query = request.args["query"]
        sql = "SELECT username, room_name, content, messages.id AS messages_id FROM messages LEFT JOIN users ON user_id = users.id LEFT JOIN rooms on room_id = rooms.id WHERE content LIKE :query AND messages.visible = 1"
        sql_query = db.session.execute(sql, {"query": "%"+query+"%"})
        results = sql_query.fetchall()
    except:
        return redirect(url_for("search"))
    else:
        if not results:
            flash("No results", "message")
            return redirect(url_for("search"))
        else:
            return render_template("search.html", results=results, query=query)
