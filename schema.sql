CREATE TABLE users (
   id SERIAL PRIMARY KEY, 
   username TEXT UNIQUE, 
   password TEXT, 
   is_admin BOOLEAN
);

CREATE TABLE announcements (
   id SERIAL PRIMARY KEY, 
   content TEXT
);

CREATE TABLE topics (
   id SERIAL PRIMARY KEY,
   name TEXT UNIQUE,
   fk_user_id INTEGER REFERENCES users
);

CREATE TABLE threads (
   id SERIAL PRIMARY KEY,
   name TEXT,
   fk_user_id INTEGER REFERENCES users,
   fk_topics_id INTEGER REFERENCES topics
);

CREATE TABLE messages (
   id SERIAL PRIMARY KEY,
   name TEXT,
   content TEXT,
   fk_user_id INTEGER REFERENCES users,
   fk_threads_id INTEGER REFERENCES threads
);