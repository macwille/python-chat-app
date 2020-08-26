CREATE TABLE users
(
    id SERIAL PRIMARY KEY,
    username varchar(21) NOT NULL,
    password TEXT NOT NULL,
    role INTEGER,
    CONSTRAINT unique_username UNIQUE(username)
);
CREATE TABLE subjects
(
    id SERIAL PRIMARY KEY,
    subject_name TEXT NOT NULL,
    password TEXT,
    content TEXT,
    require_permission INTEGER,
    CONSTRAINT unique_subjectname UNIQUE(subject_name)

);
CREATE TABLE rooms
(
    id SERIAL PRIMARY KEY,
    room_name TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    visible INTEGER NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
            REFERENCES users(id),
    CONSTRAINT fk_subject
        FOREIGN KEY (subject_id)
            REFERENCES subjects(id)
);
CREATE TABLE messages
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    room_id INTEGER NOT NULL,
    content TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    visible INTEGER NOT NULL,
    CONSTRAINT fk_user
            FOREIGN KEY (user_id)
                REFERENCES users(id),
    CONSTRAINT fk_room
            FOREIGN KEY (room_id)
                REFERENCES rooms(id)
);
CREATE TABLE subject_rights
(
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL,
    subject_id INTEGER NOT NULL,
    CONSTRAINT fk_user
        FOREIGN KEY (user_id)
            REFERENCES users(id),
    CONSTRAINT fk_subject
        FOREIGN KEY (subject_id)
            REFERENCES subjects(id)
);

