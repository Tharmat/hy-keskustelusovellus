from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import text
from os import getenv
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

def fetch_motd():
    result = db.session.execute(text("SELECT content FROM announcements"))
    return result.fetchall()

def fetch_current_topics():
    result = db.session.execute(text("SELECT topics.name as name, topics.id as id, users.username as username FROM topics JOIN users ON users.id = topics.fk_user_id"))
    return result.fetchall()

def fetch_topic_by_id(id):
    result = db.session.execute(text("SELECT topics.name as name, topics.id as id, users.username as username FROM topics JOIN users ON users.id = topics.fk_user_id where topics.id= :id"), {"id" : id})
    return result.fetchone()

def fetch_threads_by_topic_id(id):
    result = db.session.execute(text("SELECT threads.id as id, threads.name as name, users.username as username from threads JOIN users on users.id = threads.fk_user_id where threads.fk_topics_id = :id"), {"id" : id})
    return result.fetchall()

def fetch_messages_by_threads_id(threads_id):
    result = db.session.execute(text("SELECT * FROM messages where fk_threads_id = :threads_id"), {"threads_id" : threads_id})
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

def get_user(username):
    sql = text("SELECT id, password FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()
