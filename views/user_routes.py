from app import app
from flask import Flask, url_for, flash, redirect, render_template, request
from models import user_service
from db import db


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
