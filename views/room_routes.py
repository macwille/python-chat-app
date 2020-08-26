from app import app
from views import routes
from flask import Flask, url_for, flash, redirect, render_template, request, session
from models import room_service, subject_service
from db import db


@app.route("/create_room", methods=["POST", "GET"])
def create_room():
    routes.check_token()
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


@app.route("/delete_room", methods=["GET", "POST"])
def delete_room():
    routes.check_token()
    user_id = session["id"]
    room_id = request.form["room_id"]
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
