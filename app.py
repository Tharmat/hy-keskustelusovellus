from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from dotenv import load_dotenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

# Load secret from an separate .env file
load_dotenv(".secret_env")
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html", messages=fetch_motd())

@app.route("/main")
def main():
    return render_template("main.html")
    
@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    
    if not user:
        # Non-existing username, redirect to registration page
        return redirect("/register")
    else:
        # Existing user, check password next
        hash_value = user.password
    
    if check_password_hash(hash_value, password):
        session["username"] = username
        return redirect("/main")
    else:
        # Password is wrong
        return render_template("index.html", error = {'message': 'Salasanasi on väärin'})
    return redirect("/")

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
        if register_user(username, password1):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut")

def fetch_motd():
    result = db.session.execute(text("SELECT content FROM messages"))
    return result.fetchall()

def register_user(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, false)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    return True
