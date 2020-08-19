from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash


def createSubject(user_id, subject_name, password, content, require, db):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO subjects (subject_name, password, content, require_permission) values (:subject_name, :password, :content, :require_permission)"
        db.session.execute(
            sql, {"subject_name": subject_name, "password": hash_value, "content": content, "require_permission": require})
        db.session.commit()
    except:
        return False
    else:
        setRights(session["id"], subject_name, db)
        return True


def getSubjects(db):
    try:
        sql = "SELECT id, subject_name, require_permission FROM subjects"
        result = db.session.execute(sql)
        subjectsData = result.fetchall()
    except:
        return None
    else:
        return subjectsData


def getSubject(subject_id, db):
    try:
        sql = "SELECT * FROM subjects WHERE id=:id"
        result = db.session.execute(sql, {"id": subject_id})
        subject = result.fetchone()
    except:
        return None
    else:
        return subject


def getRooms(subject_id, db):
    try:
        sql = "SELECT id, room_name FROM rooms WHERE subject_id=:id AND visible=1"
        result = db.session.execute(sql, {"id": subject_id})
        roomsData = result.fetchall()
    except:
        return None
    else:
        return roomsData


def setRights(user_id, subject_name, db):
    try:
        sql = "INSERT INTO subject_rights (user_id, subject_id) values (:user_id, (SELECT id FROM subjects WHERE subject_name = :subject_name))"
        db.session.execute(
            sql, {"user_id": user_id, "subject_name": subject_name})
        db.session.commit()
    except:
        print("Error adding rights")
    else:
        print("Rights added")


def setRightsById(user_id, subject_id, db):
    try:
        sql = "INSERT INTO subject_rights (user_id, subject_id) values (:user_id, :subject_id)"
        db.session.execute(
            sql, {"user_id": user_id, "subject_id": subject_id})
        db.session.commit()
    except:
        print("Error adding rights")
    else:
        print("Rights added")


def hasRights(user_id, subject_id, db):
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


def checkPassword(subject_id, password, db):
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
