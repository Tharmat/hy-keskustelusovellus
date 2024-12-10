INSERT INTO users (username, password, is_admin) 
VALUES (
    'admin', 
    'scrypt:32768:8:1$IZEnb0ytTCGZnFlU$299ce713be4e45a6c90f1769ffeb83b65e4030b4aac78bdf5f0aa698d27b9d1b0bdb9b9b34391070b8bcf70573fedbb37e15ad237af629e82bc9ec0bfa5706ee',
    't'
);

INSERT INTO announcements (content)
VALUES (
    'This is a test server'
);

INSERT INTO topics (name, fk_user_id)
VALUES (
    'This is a test topic',
    (SELECT id FROM users WHERE username = 'admin')
);

INSERT INTO threads (name, fk_user_id, fk_topics_id)
VALUES (
    'Read this before posting',
    (SELECT id FROM users WHERE username = 'admin'),
    (SELECT id FROM topics WHERE name = 'This is a test topic')
);

INSERT INTO messages (name, content, fk_created_by_user_id, fk_threads_id)
VALUES (
    'Just a friendly reminder',
    'Have fun!',
    (SELECT id FROM users WHERE username = 'admin'),
    (SELECT id FROM topics WHERE name = 'This is a test topic')
);