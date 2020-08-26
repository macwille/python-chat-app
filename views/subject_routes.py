from app import app
from views import routes
from flask import Flask, url_for, flash, redirect, render_template, request, session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from models import subject_service
from db import db


@app.route("/subjects")
def subjects():
    subjects_data = subject_service.get_subjects(db)
    if subjects_data:
        return render_template("subjects.html", subjects=subjects_data)
    else:
        return render_template("subjects.html")


@app.route("/create_subject", methods=["POST", "GET"])
def create_subject():
    routes.check_token()
    page = request.referrer
    user_id = session["id"]
    subject_name = request.form["subject_name"]
    password = request.form["password"]
    content = request.form["content"]
    require = request.form["require"]

    print(require)
    print(password)

    if routes.word_too_long(content):
        flash("Description had a word that was too long", "error")
        return redirect(page)

    if int(require) == 1 and password == "":
        flash("You must give a password", "error")
        return redirect(page)

    if subject_service.create_subject(user_id, subject_name, password, content, require, db):
        flash("Subject created", "message")
        return redirect(url_for("subjects"))

    else:
        flash("Error creating subject - name might be taken", "error")
        return redirect(page)


@ app.route("/subject_login", methods=["POST"])
def subject_login():
    routes.check_token()
    subject_id = request.form["id"]
    password = request.form["password"]

    if subject_service.check_password(subject_id, password, db):
        subject_service.add_right_id(session["id"], subject_id, db)
        flash("Access granted", "message")
        return redirect(url_for("subject", id=subject_id))
    else:
        flash("Access denied", "error")
        return redirect(url_for("subject", id=subject_id))


@ app.route("/subject/id=<int:id>")
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
