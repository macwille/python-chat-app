from app import app
from views import subject_routes, room_routes, user_routes, message_routes
from models import user_service
from flask import Flask, flash, render_template, request, session, abort
from db import db


# Rest of the routes are imported from /views

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/create/id=<int:id>")
def create(id):
    return render_template("create.html", id=id)


@ app.route("/search")
def search():
    return render_template("search.html")


# Utilties
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
    print(error)
    flash("Unexpected Error", "error")
    return render_template("index.html")
