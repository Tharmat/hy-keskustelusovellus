from werkzeug.security import check_password_hash
from flask import render_template, request, session, redirect, url_for
from app import app
from src.decorators import login_required

import src.db

@app.route("/")
def index():
    return render_template("index.html", messages=src.db.fetch_motd())

@app.route("/main")
@login_required
def main():
    return render_template("main.html", topics = src.db.fetch_current_topics())

@app.route("/login",methods=["GET", "POST"])
def login():

    # TODO: Hack, but will work for now
    if request.method == "GET":
        if session.get("username") is not None:
            return redirect("/main")

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

        # Basic validation and error handling
        if not username:
            return render_template("register.html", error = {'message': "Käyttäjänimi ei voi olla tyhjä, anna käyttäjänimi."})

        if src.db.user_exists(username):
            return render_template("register.html", error = {'message': "Käyttäjänimi jo käytössä, valitse uusi käyttäjänimi."})

        if not password1 or not password2:
            return render_template("register.html", username = username, error = {'message': "Anna salasana kahteen kertaan."})

        if password1 != password2:
            return render_template("register.html", username = username, error = {'message': "Salasanat eroavat, tarkasta salasana."})

        if src.db.register_user(username, password1):
            return redirect("/")

        return render_template("register.html", username = username, error = {'message': "Rekisteröinti ei onnistunut, yritä myöhemmin uudelleen."})

@app.route("/topic/<int:topic_id>")
@login_required
def topic(topic_id):
    return render_template("topic.html", topic = src.db.fetch_topic_by_id(topic_id), threads = src.db.fetch_threads_by_topic_id(topic_id))

@app.route("/topic/<int:topic_id>/thread/<int:thread_id>")
@login_required
def thread(topic_id, thread_id):
    return render_template("thread.html", topic_id = topic_id, thread_id = thread_id, messages = src.db.fetch_messages_by_threads_id(thread_id))

@app.route("/topic/<int:topic_id>/newthread", methods=["GET", "POST"])
@login_required
def new_thread(topic_id):
    if request.method == "GET":
        return render_template("newthread.html", topic_id = topic_id)
    
    if request.method == "POST":

        # Basic validations
        if not request.form["thread_name"]:
            return render_template("newthread.html", topic_id = topic_id, error = {'message': "Ketjun nimi tyhjä, anna ketjun nimi."})
    
        if not request.form["message_name"]:
            return render_template("newthread.html", topic_id = topic_id, error = {'message': "Viestin otsikko on tyhjä, anna viestin otsikko."})

        if not request.form["message_content"]:
            return render_template("newthread.html", topic_id = topic_id, error = {'message': "Viestin sisältö on tyhjä, anna viestin sisältö."})

        src.db.create_new_thread(topic_id, request.form["thread_name"], request.form["message_name"], request.form["message_content"], session.get("username"))

        return redirect(url_for('topic', topic_id = topic_id))
    
@app.route("/topic/<int:topic_id>/thread/<int:thread_id>/newmessage/", methods=["GET", "POST"])
@login_required
def new_message(topic_id, thread_id):
    if request.method == "GET":
        return render_template("newmessage.html", topic_id = topic_id, thread_id = thread_id)
    
    if request.method == "POST":

        # Basic validations
        if not request.form["message_name"]:
            return render_template("newmessage.html", topic_id = topic_id, thread_id = thread_id, error = {'message': "Viestin otsikko on tyhjä, anna viestin otsikko."})
    
        if not request.form["message_content"]:
            return render_template("newmessage.html", topic_id = topic_id, thread_id = thread_id, error = {'message': "Viestin sisältö on tyhjä, anna viestin sisältö."})
        
        src.db.create_new_message(thread_id, request.form["message_name"], request.form["message_content"], session.get("username"))

        return redirect(url_for('thread', topic_id = topic_id, thread_id = thread_id))