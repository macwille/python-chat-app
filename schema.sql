CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    name varchar(21) NOT NULL,
    password TEXT NOT NULL,
    role INTEGER,
    CONSTRAINT unique_username UNIQUE(name)
);

CREATE TABLE messages
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    content TEXT,
    created_at TIMESTAMP
);

CREATE TABLE rooms
(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL
);

CREATE TABLE subjects
(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    content TEXT,
    CONSTRAINT unique_subjectname UNIQUE(name)

);

CREATE TABLE subject_rights
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL
);

