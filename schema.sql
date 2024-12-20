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
   fk_user_id INTEGER REFERENCES users,
   removed BOOLEAN DEFAULT FALSE,
   is_hidden BOOLEAN DEFAULT FALSE
);

CREATE TABLE threads (
   id SERIAL PRIMARY KEY,
   name TEXT,
   fk_user_id INTEGER REFERENCES users,
   fk_topics_id INTEGER REFERENCES topics,
   removed BOOLEAN DEFAULT FALSE
);

CREATE TABLE messages (
   id SERIAL PRIMARY KEY,
   name TEXT,
   content TEXT,
   fk_threads_id INTEGER REFERENCES threads,
   creation_time TIMESTAMP DEFAULT NOW(),
   fk_created_by_user_id INTEGER REFERENCES users,
   modification_time TIMESTAMP DEFAULT NULL,
   fk_modified_by_user_id INTEGER REFERENCES users DEFAULT NULL,
   removed BOOLEAN DEFAULT FALSE
);

CREATE TABLE user_rights (
   id SERIAL PRIMARY KEY,
   fk_user_id INTEGER REFERENCES users NOT NULL,
   fk_topics_id INTEGER REFERENCES topics NOT NULL
);