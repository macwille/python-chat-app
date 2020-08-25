from app import app
from os import getenv
from flask import Flask, url_for, flash, redirect, render_template, request, session, abort
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash
from services import user_service, room_service, subject_service


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
    if user_service.login(username, password, db):
        flash("Welcome back", "message")
        return redirect(url_for("index"))
    else:
        flash("Error logging in", "error")
        return redirect(url_for("index"))


@app.route("/logout")
def logout():
    user_service.logout()
    flash("Logged out", "message")
    return redirect(url_for("index"))


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/new_user", methods=["POST", "GET"])
def new_user():
    username = request.form["username"]
    password = request.form["password"]
    if user_service.register(username, password, db):
        flash("Registration Successful", "message")
        return redirect(url_for("index"))
    else:
        flash("Registration Failed", "message")
        return redirect(url_for("register"))


@app.route("/create/id=<int:id>")
def create(id):
    return render_template("create.html", id=id)


@app.route("/create_room", methods=["POST", "GET"])
def create_room():
    check_token()
    user_id = session["id"]
    room_name = request.form["room_name"]
    subject_id = request.form["subject_id"]

    if subject_service.has_right(user_id, subject_id, db):

        if room_service.create_room(user_id, room_name, subject_id, db):
            flash("Room created", "message")
            return redirect(url_for("subject", id=subject_id))

        else:
            flash("Problem creating room", "error")
            return redirect(url_for("subject", id=subject_id))
    else:
        flash("Problem creating room", "error")
        return redirect(url_for("subject", id=subject_id))


@app.route("/delete_room", methods=["GET", "POST"])
def delete_room():
    check_token()
    user_id = session["id"]
    room_id = request.form["room_id"]
    print(room_id)
    if room_service.is_owner(user_id, room_id, db):
        if room_service.delete_room(room_id, db):
            flash("Room deleted", "message")
            return redirect(url_for("subjects"))
        else:
            flash("Error deleting room", "error")
            return redirect(url_for("subjects"))
    else:
        flash("Error deleting room", "error")
        return redirect(url_for("subjects"))


@app.route("/create_subject", methods=["POST", "GET"])
def create_subject():
    check_token()
    page = request.referrer
    user_id = session["id"]
    subject_name = request.form["subject_name"]
    password = request.form["password"]
    content = request.form["content"]
    require = request.form["require"]

    if word_too_long(content):
        flash("Description had a word that was too long", "error")
        return redirect(page)

    if require == 1 and not password.strip():
        flash("Enter a password", "error")
        return redirect(page)

    if subject_service.create_subject(user_id, subject_name, password, content, require, db):
        flash("Subject created", "message")
        return redirect(url_for("subjects"))

    else:
        flash("Error creating subject", "error")
        return redirect(page)


@app.route("/subjects")
def subjects():
    subjects_data = subject_service.get_subjects(db)
    if subjects_data:
        return render_template("subjects.html", subjects=subjects_data)
    else:
        return render_template("subjects.html")


@app.route("/room/id=<int:id>")
def room(id):
    user_id = session["id"]
    subject_id = room_service.get_subject(id, db)

    if subject_service.has_right(user_id, subject_id, db):

        roomData = room_service.get_room(id, db)
        if roomData:
            room_id = roomData[0]
            name = roomData[1]
            username = roomData[2]
            messages = room_service.get_messages(room_id, db)
            if messages:
                return render_template("room.html", id=room_id, name=name,  owner=username, messages=messages)
            else:
                return render_template("room.html", id=room_id, name=name,  owner=username)
        else:
            flash("Room not found", "error")
            return redirect(url_for("subjects"))
    else:
        return redirect(url_for("subject", id=subject_id))


@app.route("/subject/id=<int:id>")
def subject(id):
    subject_data = subject_service.get_subject(id, db)
    if subject_data:
        subject_id = subject_data[0]
        subject_name = subject_data[1]
        secret = subject_data[2]
        content = subject_data[3]
        require = subject_data[4]
        rooms = subject_service.get_rooms(subject_id, db)
        hasRight = subject_service.has_right(session["id"], subject_id, db)

        if rooms:
            return render_template("subject.html", subject_name=subject_name, rooms=rooms, id=subject_id, content=content, require=require, hasRight=hasRight)
        else:
            return render_template("subject.html", subject_name=subject_name, id=subject_id, content=content, require=require, hasRight=hasRight)
    else:
        return redirect(url_for("subjects"))


@app.route("/subject_login", methods=["POST"])
def subject_login():
    check_token()
    subject_id = request.form["id"]
    password = request.form["password"]

    if subject_service.check_password(subject_id, password, db):
        subject_service.add_rights_id(session["id"], subject_id, db)
        flash("Access granted", "message")
        return redirect(url_for("subject", id=subject_id))
    else:
        flash("Access denied", "error")
        return redirect(url_for("subject", id=subject_id))


@app.route("/send", methods=["POST"])
def send():
    check_token()
    content = request.form["content"]
    room_id = request.form["room_id"]
    user_id = session["id"]
    subect_id = room_service.get_subject(room_id, db)

    if word_too_long(content):
        flash("Message had a word that was too long", "message")
        return redirect(url_for("room", id=room_id))

    elif subject_service.has_right(user_id, subect_id, db):
        try:
            sql = """INSERT INTO messages (user_id, room_id, content, created_at, visible)
            VALUES (:user_id, :room_id, :content, NOW(), 1)"""
            db.session.execute(
                sql, {"user_id": user_id, "room_id": room_id, "content": content.strip()})
            db.session.commit()
        except:
            return redirect("subjects")
        else:
            return redirect(url_for("room", id=room_id))
    else:
        return redirect(url_for("subjects"))


@app.route("/search")
def search():
    return render_template("search.html")


@app.route("/delete_message", methods=["GET", "POST"])
def delete_message():
    check_token()
    user_id = session["id"]
    message_id = request.form["message_id"]
    page = request.referrer
    try:
        if session["admin"]:
            sql = "UPDATE messages SET visible = 0 WHERE id = :id"
            db.session.execute(sql, {"id": message_id})
            db.session.commit()
        else:
            sql = "UPDATE messages SET visible = 0 WHERE id = :id AND user_id = :user_id"
            db.session.execute(sql, {"id": message_id, "user_id": user_id})
            db.session.commit()
    except:
        flash("Error deleteting message", "error")
        return redirect(url_for("subjects"))
    else:
        flash("Message deleted", "message")
        return redirect(page)


@app.route("/result", methods=["GET"])
def result():
    if not session["username"]:
        return redirect(url_for(search))

    username = session["username"]
    query = request.args["query"]

    sql = """SELECT username, room_name, content, messages.id AS messages_id FROM messages
        LEFT JOIN users ON user_id = users.id LEFT JOIN rooms on room_id = rooms.id
        WHERE content LIKE :query AND messages.visible = 1"""

    sql_not_admin = " AND username = :username"

    if session["admin"]:
        sql_query = db.session.execute(
            sql, {"query": "%"+query+"%"})
    else:
        sql2 = sql + sql_not_admin
        sql_query = db.session.execute(
            sql2, {"query": "%"+query+"%", "username": username})

    results = sql_query.fetchall()

    if not results:
        flash("No results", "message")
        return redirect(url_for("search"))
    else:
        return render_template("search.html", results=results, query=query)


def check_token():
    token = session["csrf_token"]
    form_token = request.form["csrf_token"]
    if token != form_token:
        print("Failed token")
        abort(403)
    else:
        print("Token checked")


def word_too_long(string):
    lengths = [len(x) for x in string.split()]
    if any(l > 30 for l in lengths):
        return True
    else:
        return False


@app.errorhandler(403)
def resource_not_found(e):
    flash("Forbidden 403", "error")
    return render_template("index.html")


@app.errorhandler(500)
def server_error(e):
    flash("Server encountered an internal error", "error")
    return render_template("index.html")


@app.errorhandler(Exception)
def error_dump(error):
    logout()
    flash("Unexpected Error", "error")
    return render_template("index.html")
