from app import app
from views import routes
from flask import Flask, url_for, flash, redirect, render_template, request, session
from models import room_service, subject_service
from db import db


@app.route("/send", methods=["POST"])
def send():
    routes.check_token()
    content = request.form["content"]
    room_id = request.form["room_id"]
    user_id = session["id"]
    subect_id = room_service.get_subject(room_id, db)

    if routes.word_too_long(content):
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


@ app.route("/delete_message", methods=["GET", "POST"])
def delete_message():
    routes.check_token()
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
        return redirect(url_for(routes.search))

    username = session["username"]
    query = request.args["query"]

    sql = """SELECT username, room_name, content, messages.id AS messages_id FROM messages
        LEFT JOIN users ON user_id = users.id LEFT JOIN rooms on room_id = rooms.id
        WHERE lower(content) LIKE :query AND messages.visible = 1"""

    sql_not_admin = " AND username = :username"

    if session["admin"]:
        sql_query = db.session.execute(
            sql, {"query": "%"+query+"%"})
    else:
        sql2 = sql + sql_not_admin
        sql_query = db.session.execute(
            sql2, {"query": "%"+query.lower()+"%", "username": username})

    results = sql_query.fetchall()

    if not results:
        flash("No results", "message")
        return redirect(url_for("search"))
    else:
        return render_template("search.html", results=results, query=query)
