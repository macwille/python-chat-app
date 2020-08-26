from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash


def create_subject(user_id, subject_name, password, content, require, db):
    hash_value = generate_password_hash(password)

    if password == "":
        password = "1234"

    try:
        sql = """INSERT INTO subjects (subject_name, password, content, require_permission) 
        VALUES (:subject_name, :password, :content, :require_permission)"""

        db.session.execute(
            sql, {"subject_name": subject_name, "password": hash_value, "content": content, "require_permission": require})
        db.session.commit()
    except:
        return False
    else:
        add_right(session["id"], subject_name, db)
        return True


def get_subjects(db):
    sql = "SELECT id, subject_name, require_permission FROM subjects"
    result = db.session.execute(sql)
    subjectsData = result.fetchall()

    return subjectsData


def get_subject(subject_id, db):
    sql = "SELECT * FROM subjects WHERE id=:id"
    result = db.session.execute(sql, {"id": subject_id})
    subject = result.fetchone()

    return subject


def get_rooms(subject_id, db):
    sql = "SELECT id, room_name FROM rooms WHERE subject_id=:id AND visible=1"
    result = db.session.execute(sql, {"id": subject_id})
    roomsData = result.fetchall()

    return roomsData


def is_secret(subject_id, db):
    sql = "SELECT COUNT(*) FROM subjects WHERE id=:id AND require_permission=1"
    result = db.session.execute(sql, {"id": subject_id})
    secret = result.fetchone()[0]

    return secret > 0


def add_right(user_id, subject_name, db):
    try:
        sql = """INSERT INTO subject_rights (user_id, subject_id) 
        VALUES (:user_id, (SELECT id FROM subjects WHERE subject_name = :subject_name))"""
        db.session.execute(
            sql, {"user_id": user_id, "subject_name": subject_name.strip()})
        db.session.commit()
    except:
        print("Error adding rights")
    else:
        print("Rights added")


def add_right_id(user_id, subject_id, db):
    try:
        sql = "INSERT INTO subject_rights(user_id, subject_id) VALUES(:user_id, :subject_id)"
        db.session.execute(
            sql, {"user_id": user_id, "subject_id": subject_id})
        db.session.commit()
    except:
        print("Error adding rights")
    else:
        print("Rights added")


def has_right(user_id, subject_id, db):
    if session["admin"]:
        print("Admin rights")
        return True
    else:
        if is_secret(subject_id, db):
            sql = "SELECT COUNT(*) FROM subject_rights WHERE user_id = :user_id AND subject_id = :subject_id"
            result = db.session.execute(
                sql, {"user_id": user_id, "subject_id": subject_id})
            hasRight = result.fetchone()[0]

            if hasRight > 0:
                print("User has rights to subject_id", subject_id)
                return True
            else:
                print("User doesn't have rights to subject_id", subject_id)
                return False
        else:
            return True


def check_password(subject_id, password, db):
    try:
        sql = "SELECT password, id FROM subjects WHERE id = :subject_id"
        result = db.session.execute(sql, {"subject_id": subject_id})
        subjectData = result.fetchone()
    except:
        return False
    else:
        if subjectData == None:
            return False
        else:
            hash_value = subjectData[0]
            if check_password_hash(hash_value, password):
                return True
            else:
                return False
