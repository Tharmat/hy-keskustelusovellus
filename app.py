from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from dotenv import load_dotenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

# Load secret from an separate .env file
load_dotenv(".secret_env")
app.secret_key = getenv("SECRET_KEY")

@app.route("/")
def index():
    return render_template("index.html", messages=fetch_motd(db)) 

def fetch_motd(db):
    result = db.session.execute(text("SELECT content FROM messages"))
    return result.fetchall()
    