from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash
from sqlalchemy.sql import text
from os import getenv
from app import app

app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
db = SQLAlchemy(app)

def fetch_motd():
    result = db.session.execute(text("""SELECT 
                                            content 
                                        FROM announcements"""))
    return result.fetchall()

def fetch_user_right_for_topic(topic_id):
    sql = """SELECT 
            users.id as id, 
            users.username as name,
            CASE
                WHEN user_rights.fk_user_id = users.id THEN TRUE
                ELSE FALSE
                END AS has_rights
        FROM users
        LEFT JOIN user_rights ON user_rights.fk_user_id = users.id and user_rights.fk_topics_id = :topic_id
        WHERE 
            users.is_admin = FALSE"""
    result = db.session.execute(text(sql), {"topic_id" : topic_id})
    return result.fetchall()

def fetch_current_topics_for_non_admin_user(user_id):
    sql = """SELECT 
                topics.name as name, 
                topics.id as id, 
                COUNT(messages.id) as message_count, 
                COALESCE(MAX(messages.creation_time), CURRENT_TIMESTAMP) as latest
            FROM topics
            LEFT JOIN threads ON threads.fk_topics_id = topics.id
            LEFT JOIN messages ON messages.fk_threads_id = threads.id
            LEFT JOIN user_rights ON user_rights.fk_topics_id = topics.id
            WHERE 
                topics.removed != TRUE
                AND CASE
                    WHEN topics.is_hidden = FALSE THEN TRUE
                    ELSE user_rights.fk_user_id = :user_id
                    END
            GROUP BY topics.name, topics.id
            ORDER BY latest DESC"""
    result = db.session.execute(text(sql), {"user_id": user_id})
    return result.fetchall()

def fetch_current_topics_for_admin():
    sql = """SELECT 
                topics.name as name, 
                topics.id as id, 
                COUNT(messages.id) as message_count, 
                COALESCE(MAX(messages.creation_time), CURRENT_TIMESTAMP) as latest
            FROM topics
            LEFT JOIN threads ON threads.fk_topics_id = topics.id
            LEFT JOIN messages ON messages.fk_threads_id = threads.id
            LEFT JOIN user_rights ON user_rights.fk_topics_id = topics.id
            WHERE 
                topics.removed != TRUE    
            GROUP BY topics.name, topics.id
            ORDER BY latest DESC"""
    result = db.session.execute(text(sql))
    return result.fetchall()    

def fetch_topic_by_id(id):
    result = db.session.execute(text("""SELECT 
                                            topics.name as name, 
                                            topics.id as id,
                                            topics.is_hidden as is_hidden,
                                            users.username as username
                                        FROM topics 
                                        JOIN users ON users.id = topics.fk_user_id 
                                        WHERE topics.id= :id and topics.removed = FALSE"""),
                                     {"id" : id})
    return result.fetchone()

def fetch_threads_by_topic_id(id):
    result = db.session.execute(text("""SELECT 
                                        threads.id as id, 
                                        threads.name as name, 
                                        users.username as username 
                                    FROM threads 
                                    JOIN users on users.id = threads.fk_user_id 
                                    WHERE threads.fk_topics_id = :id and threads.removed = FALSE"""),
                                    {"id" : id})
    return result.fetchall()

def fetch_thread_by_thread_id(thread_id):
    result = db.session.execute(text("""SELECT
                                        threads.id as id, 
                                        threads.name as name 
                                    FROM threads 
                                    WHERE threads.id = :thread_id and threads.removed = FALSE"""),
                                    {"thread_id" : thread_id})
    return result.fetchone()
    
def fetch_messages_by_threads_id(threads_id, username):
    user_id = get_user_id(username)

    result = db.session.execute(text("""SELECT
                                            messages.id as id,
                                            messages.name as name, 
                                            messages.content as content, 
                                            messages.creation_time as creation_time, 
                                            users1.username as username,
                                            CASE 
                                                WHEN messages.fk_created_by_user_id = :user_id 
                                                    THEN 1
                                                    ELSE 0 END
                                            as can_edit,
                                            messages.modification_time as modification_time,
                                            users2.username as modified_by
                                        FROM messages
                                        JOIN users users1 on users1.id = messages.fk_created_by_user_id
                                        LEFT JOIN users users2 on users2.id = messages.fk_modified_by_user_id
                                        WHERE messages.fk_threads_id = :threads_id
                                        AND messages.removed = FALSE"""), 
                                        {"threads_id" : threads_id, "user_id" : user_id})
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

def user_exists(username):
    sql = text("SELECT 1 FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def get_user(username):
    sql = text("SELECT * FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()

def get_user_id(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    return result.fetchone()[0]

def create_new_thread(topic_id, thread_name, message_name, message_content, username):
    try:
        user_id = get_user_id(username)
        sql = text("INSERT INTO threads (name, fk_user_id, fk_topics_id) values (:thread_name, :user_id, :topic_id) RETURNING id;" )
        result = db.session.execute(sql, {"thread_name" : thread_name, "user_id" : user_id, "topic_id" : topic_id})
        new_thread_id = result.fetchone()[0]

        sql = text("""INSERT INTO messages (name, content, fk_created_by_user_id, fk_threads_id) 
                   VALUES (:message_name, :message_content, :user_id, :new_thread_id);""")
        db.session.execute(sql, {"message_name" : message_name, "message_content" : message_content, "user_id" : user_id, "new_thread_id" : new_thread_id})

        db.session.commit()
    except Exception as error:
        print(error)
        return False
    return True

def create_new_message(thread_id, message_name, message_content, username):
    try:
        user_id = get_user_id(username)

        sql = text("""INSERT INTO messages (name, content, fk_created_by_user_id, fk_threads_id) 
                   VALUES (:message_name, :message_content, :user_id, :thread_id);""")
        db.session.execute(sql, {"message_name" : message_name, "message_content" : message_content, "user_id" : user_id, "thread_id" : thread_id})
        db.session.commit()
    except Exception as error:
        print(error)
        return False
    return True

def update_message(message_id, message_name, message_content, modified_by_user_id):
    try:
        sql = text("""UPDATE messages
                   SET name = :message_name, content = :message_content, fk_modified_by_user_id = :modified_by, modification_time = NOW()
                   WHERE
                   id = :message_id""")
        db.session.execute(sql, {"message_name" : message_name, "message_content" : message_content, "message_id" : message_id, "modified_by" : modified_by_user_id})
        db.session.commit()
    except Exception as error:
        print(error)
        return False
    return True

def delete_message(message_id, modified_by_user_id):
    try:
        sql = text("""UPDATE messages
                   SET removed = TRUE, fk_modified_by_user_id = :modified_by, modification_time = NOW()
                   WHERE
                   id = :message_id""")
        db.session.execute(sql, {"message_id" : message_id, "modified_by" : modified_by_user_id})
        db.session.commit()
    except Exception as error:
        print(error)
        return False
    return True


# TODO: Probably should use user_id instead as it is more strictly enforced on db level than username
def user_is_admin(username):
    sql = text("SELECT 1 FROM users WHERE username=:username and is_admin = true")
    result = db.session.execute(sql, {"username" : username})
    return result.fetchone()

def get_message(message_id):
    sql = text("SELECT * FROM messages where id = :message_id")
    result = db.session.execute(sql, {"message_id" : message_id})
    return result.fetchone()

def delete_thread(threads_id, user_id):
    try:
        sql = text("""SELECT messages.id as id from messages
                   JOIN threads on threads.id = messages.fk_threads_id
                   where threads.id = :threads_id""")
        message_ids = db.session.execute(sql, {"threads_id" : threads_id})

        for message_id in message_ids:
            delete_message(message_id.id, user_id)

        sql = text("""UPDATE threads
                   SET removed = TRUE
                   WHERE
                   id = :threads_id""")
        db.session.execute(sql, {"threads_id" : threads_id})
        db.session.commit()
    except Exception as error:
        print(error)
        return False
    return True

def delete_topic(topics_id, user_id):
    try:
        for threads_id in fetch_threads_by_topic_id(topics_id):
            delete_thread(threads_id.id, user_id)

        sql = text("""UPDATE topics
                    SET removed = TRUE
                    WHERE
                    id = :topics_id""")
        db.session.execute(sql, {"topics_id" : topics_id})
        db.session.commit()
    except Exception as error:
        print(error)
        return False
    return True

def create_new_topic(topic_name, user_id, is_hidden):
    try:
        sql = text("INSERT INTO topics (name, fk_user_id, is_hidden) VALUES (:topic_name, :user_id, :is_hidden)")
        db.session.execute(sql, {"topic_name" : topic_name, "user_id" : user_id, "is_hidden" : is_hidden})
        db.session.commit()
    except Exception as error:
        print(error)
        return False
    return True

def edit_topic_name(topic_id, topic_name):
    try:
        sql = text("UPDATE topics SET name = :topic_name WHERE id = :topic_id") 
        db.session.execute(sql, {"topic_name" : topic_name, "topic_id" : topic_id})
        db.session.commit()
    except Exception as error:
        print(error)
        return False
    return True

def edit_topic(topic_id, topic_name, is_hidden):
    try:
        sql = text("UPDATE topics SET name = :topic_name, is_hidden = :is_hidden WHERE id = :topic_id") 
        db.session.execute(sql, {"topic_name" : topic_name, "topic_id" : topic_id, "is_hidden" : is_hidden})
        db.session.commit()
    except Exception as error:
        print(error)
        return False
    return True

        

def search_messages(search_string):
    # Seems to be the only way to work with raw SQL like in SqlAlchemy. Seems hacky.
    search_string = "%" + search_string + "%"

    sql = text("""SELECT 
                    messages.id as message_id, 
                    messages.name as message_name, 
                    messages.content as message_content,
                    topics.id as topic_id,
                    topics.name as topic_name,
                    threads.id as thread_id,
                    threads.name as thread_name
                FROM messages
                JOIN threads on threads.id = messages.fk_threads_id
                JOIN topics on topics.id = threads.fk_topics_id
                WHERE 
                    messages.content like :search_string
                    AND messages.removed = FALSE
                    AND threads.removed = FALSE
                    AND topics.removed = FALSE
                LIMIT 10
               """)
    result = db.session.execute(sql, {"search_string" : search_string})
    return result.fetchall()