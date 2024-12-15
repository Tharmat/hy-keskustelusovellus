INSERT INTO users (username, password, is_admin) 
VALUES 
    ('admin', 
    'scrypt:32768:8:1$IZEnb0ytTCGZnFlU$299ce713be4e45a6c90f1769ffeb83b65e4030b4aac78bdf5f0aa698d27b9d1b0bdb9b9b34391070b8bcf70573fedbb37e15ad237af629e82bc9ec0bfa5706ee',
    't'),
    ('alice', 
    'scrypt:32768:8:1$ILvPQX127eZhX3gz$6970c0c285f9004c09de9d2bca5d82c4479bc550f3922725ecd4e4e06e0ce0981b3104087873fdd75a1ec51f8d5d561533491f17f9cfcd440a2f3172c620b7a0',
    'f'),
    ('bob',
    'scrypt:32768:8:1$HapUqfG9YnS4TGqX$d255cb33746f4bc017abe12cf7c53c48f1cc685043e26645bab17d18f1d35f2e498e0a338430d0bd16f25c75c3d00588b2281a7504f2823b74e63c59aa01ed77',
    'f');

INSERT INTO announcements (content)
VALUES (
    'This is a test server'
);

INSERT INTO topics (name, fk_user_id, removed, is_hidden)
VALUES 
    ('This is a test topic', (SELECT id FROM users WHERE username = 'admin'), 'f', 'f'),
    ('Alice <3 admin', 2, 'f', 't');

INSERT INTO threads (name, fk_user_id, fk_topics_id)
VALUES 
    ('Read this before posting', (SELECT id FROM users WHERE username = 'admin'), (SELECT id FROM topics WHERE name = 'This is a test topic')),
    ('Secret thread', 2, 2);

INSERT INTO messages (name, content, fk_created_by_user_id, fk_threads_id)
VALUES 
    ('Just a friendly reminder', 'Have fun!', (SELECT id FROM users WHERE username = 'admin'), (SELECT id FROM topics WHERE name = 'This is a test topic')),
    ('Secret message', 'Byvfcn byyhg nvxnn gruqn xhaabyyn', 1, 2);

INSERT INTO user_right (fk_user_id, fk_topics_id) 
VALUES (2, 2)