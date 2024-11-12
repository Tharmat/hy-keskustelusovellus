from werkzeug.security import check_password_hash
from flask import render_template, request, session, redirect
from app import app
from src.decorators import login_required

import src.db

@app.route("/")
def index():
    return render_template("index.html", messages=src.db.fetch_motd())

@app.route("/main")
@login_required
def main():
    return render_template("main.html", topics= src.db.fetch_current_topics())

@app.route("/login",methods=["POST"])
def login():
    # TODO: Handle loading login page when user is already logged in. Should redirect to the main page
    username = request.form["username"]
    password = request.form["password"]

    user = src.db.get_user(username)

    if not user:
        # Non-existing username, redirect to registration page
        return redirect("/register")
    
    # Existing user, check password next
    hash_value = user.password

    if check_password_hash(hash_value, password):
        session["username"] = username
        return redirect("/main")

    # Password is wrong
    return render_template("index.html", error = {'message': 'Salasanasi on väärin'})

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            return render_template("error.html", message="Salasanat eroavat")

        if src.db.register_user(username, password1):
            return redirect("/")

        return render_template("error.html", message="Rekisteröinti ei onnistunut")
