import secrets
from flask import render_template, request, session, redirect, url_for
from app import app
from werkzeug.security import check_password_hash
import src.db
from src.common import check_csrf_token, login_required

@app.route("/")
def index():
    return render_template("index.html", messages=src.db.fetch_motd())

@app.route("/main")
@login_required
def main():
    user = src.db.get_user(session.get("username"))
    return render_template("main.html", topics = src.db.fetch_current_topics(), is_admin = user.is_admin)

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

        # Generate new csrf_token
        session["csrf_token"] = secrets.token_hex(16)

        return redirect("/main")

    # Password is wrong
    return render_template("index.html", error = {'message': 'Salasanasi on väärin'})

@app.route("/logout")
def logout():
    del session["username"]

    # Delete csrf_token to prevent reuse
    del session["csrf_token"]
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
    user = src.db.get_user(session.get("username"))
    return render_template("topic.html", topic = src.db.fetch_topic_by_id(topic_id), is_admin = user.is_admin, threads = src.db.fetch_threads_by_topic_id(topic_id))

@app.route("/topic/newtopic", methods = ["GET", "POST"])
@login_required
def new_topic():
    user = src.db.get_user(session.get("username"))

    if user.is_admin:
        if request.method == "GET":
            return render_template("newtopic.html")
        if request.method == "POST":
            if not request.form["topic_name"]:
                return render_template("newtopic.html", error = {'message': "Keskustelualueen nimi ei voi olla tyhjä, anna keskustelualueen nimi"})
            if src.db.create_new_topic(request.form["topic_name"], user.id):
                return render_template("main.html", topics = src.db.fetch_current_topics(), is_admin = user.is_admin)
            return render_template("newtopic.html", error = {'message': "Uuden keskustelualueen luominen epäonnistui, kokeile uudestaan."})
    
    # If user is not admin, return main page
    return render_template("main.html", topics = src.db.fetch_current_topics(), is_admin = user.is_admin)

@app.route("/topic/<int:topic_id>/edit", methods = ["GET", "POST"])
@login_required
def edit_topic(topic_id):
    user = src.db.get_user(session.get("username"))
    topic = src.db.fetch_topic_by_id(topic_id)

    if user.is_admin:
        if request.method == "GET":
            return render_template("edittopic.html", topic = topic)
        if request.method == "POST":
            if not request.form["topic_name"]:
                return render_template("edittopic.html", topic = topic, error = {'message': "Keskustelualueen nimi ei voi olla tyhjä, anna keskustelualueen nimi"})
            if src.db.edit_topic(topic_id, request.form["topic_name"]):
                return redirect(url_for('main'))
            return render_template("edittopic.html", topic = topic, error = {'message': "Uuden keskustelualueen luominen epäonnistui, kokeile uudestaan."})

@app.route("/topic/<int:topic_id>/delete", methods = ["POST"])
@login_required
def delete_topic(topic_id):
    user = src.db.get_user(session.get("username"))
    
    if user.is_admin:
        src.db.delete_topic(topic_id, user.id)
    
    return redirect(url_for('main'))

@app.route("/topic/<int:topic_id>/thread/<int:thread_id>")
@login_required
def thread(topic_id, thread_id):
    user = src.db.get_user(session.get("username"))
    return render_template("thread.html", topic_id = topic_id, thread_id = thread_id, is_admin = user.is_admin, messages = src.db.fetch_messages_by_threads_id(thread_id, session.get("username")))

@app.route("/topic/<int:topic_id>/newthread", methods=["GET", "POST"])
@login_required
def new_thread(topic_id):
    if request.method == "GET":
        return render_template("newthread.html", topic_id = topic_id)
    
    if request.method == "POST":
        check_csrf_token(request)

        # Basic validations
        if not request.form["thread_name"]:
            return render_template("newthread.html", topic_id = topic_id, error = {'message': "Ketjun nimi tyhjä, anna ketjun nimi."})
    
        if not request.form["message_name"]:
            return render_template("newthread.html", topic_id = topic_id, error = {'message': "Viestin otsikko on tyhjä, anna viestin otsikko."})

        if not request.form["message_content"]:
            return render_template("newthread.html", topic_id = topic_id, error = {'message': "Viestin sisältö on tyhjä, anna viestin sisältö."})

        if src.db.create_new_thread(topic_id, request.form["thread_name"], request.form["message_name"], request.form["message_content"], session.get("username")):
            return redirect(url_for('topic', topic_id = topic_id))
        return render_template("newthread.html", topic_id = topic_id, error = {'message': "Uuden ketjun luominen epäonnistui, yritä uudelleen."})

@app.route("/topic/<int:topic_id>/thread/<int:thread_id>/delete", methods = ["POST"])
@login_required
def delete_thread(topic_id, thread_id):
    user = src.db.get_user(session.get("username"))
    
    if user.is_admin:
        src.db.delete_thread(thread_id, user.id)
    
    return redirect(url_for('topic', topic_id = topic_id))

# Slightly too smart way to use the same route for both creating a new message as well as editing an existing message
@app.route("/topic/<int:topic_id>/thread/<int:thread_id>/message/", methods=["GET", "POST"])
@app.route("/topic/<int:topic_id>/thread/<int:thread_id>/message/<int:message_id>", methods=["GET", "POST"])
@login_required
def message(topic_id, thread_id, message_id = None):
    if request.method == "GET":
        # Create new message
        if not message_id:
            return render_template("message.html", topic_id = topic_id, thread_id = thread_id, message = None)
        
        user = src.db.get_user(session.get("username"))
        message = src.db.get_message(message_id)

        if user_can_modify(message_id, user):
                return render_template("message.html", topic_id = topic_id, thread_id = thread_id, message = message)
        
        # Else redirect to threads.html
        return redirect(url_for('thread', topic_id = topic_id, thread_id = thread_id))

    if request.method == "POST":
        check_csrf_token(request)

        message = None
        if message_id:
            message = src.db.get_message(message_id)

        # Basic validations
        if not request.form["message_name"]:
            return render_template("message.html", topic_id = topic_id, thread_id = thread_id, message = message, error = {'message': "Viestin otsikko on tyhjä, anna viestin otsikko."})
    
        if not request.form["message_content"]:
            return render_template("message.html", topic_id = topic_id, thread_id = thread_id, message = message, error = {'message': "Viestin sisältö on tyhjä, anna viestin sisältö."})
        
        # Create new message
        if not message:
            src.db.create_new_message(thread_id, request.form["message_name"], request.form["message_content"], session.get("username"))
        
        # Else update existing message
        else:
            # If User is the creator of the message OR is admin then accept the edits
            user = src.db.get_user(session.get("username"))
            
            if user.id == message.fk_created_by_user_id or user.is_admin:
                src.db.update_message(message_id, request.form["message_name"], request.form["message_content"], user.id)

        return redirect(url_for('thread', topic_id = topic_id, thread_id = thread_id))

@app.route("/topic/<int:topic_id>/thread/<int:thread_id>/message/<int:message_id>/delete", methods=["POST"])
@login_required
def delete_message(topic_id, thread_id, message_id):
    check_csrf_token(request)

    user = src.db.get_user(session.get("username"))

    if user_can_modify(message_id, user):
        src.db.delete_message(message_id, user.id)
    
    return redirect(url_for('thread', topic_id = topic_id, thread_id = thread_id))

def user_can_modify(message_id, user):
    message = src.db.get_message(message_id)

    if not message.removed:
        if user.id == message.fk_created_by_user_id or user.is_admin:
            return True