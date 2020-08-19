from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash


def hasRight(user_id, subject_id, db):
    sql = "SELECT COUNT(*) FROM subject_rights WHERE user_id=:user_id AND subject_id=:subejct_id"
    result = db.session.execute(
        sql, {"user_id": user_id, "subject_id": subect_id})
    hasRight = result.fetchone()[0]
    if hasRight > 0:
        return True
    else:
        return False


def hasRightToRoom(user_id, room_id, db):
    sql = "SELECT COUNT(*) FROM subject_rights WHERE user_id = :user_id"
    result = db.session.execute(
        sql, {"user_id": user_id, "subject_id": subect_id})
    hasRight = result.fetchone()[0]
    if hasRight > 0:
        return True
    else:
        return False


def isOwner(user_id, room_id, db):
    sql = "SELECT COUNT(*) FROM rooms WHERE user_id = :user_id AND id = :room_id"
    result = db.session.execute(
        sql, {"user_id": user_id, "room_id": room_id})
    isOwner = result.fetchone()[0]
    if isOwner > 0:
        return True
    else:
        return False


def setRight(user_id, subject_id, db):
    if not hasRight(user_id, subject_id, db):
        sql = "INSERT INTO subject_rights (user_id, subject_id) values(:user_id, :subject_id"
        db.session.execute(sql, {"user_id": user_id, "subject_id": subject_id})
        db.session.commit()


def createRoom(user_id, room_name, subject_id, db):
    try:
        sql = "INSERT INTO rooms (room_name, user_id, subject_id, visible) values(:room_name, :user_id, :subject_id, 1)"
        db.session.execute(
            sql, {"room_name": room_name, "user_id": user_id, "subject_id": subject_id})
        db.session.commit()
    except:
        return False
    else:
        return True


def deleteRoom(id, db):
    if isOwner(session["id"], id, db) or session["admin"]:
        print("room id", id)
        try:
            sql = "UPDATE rooms SET visible = 0 WHERE id = :id"
            db.session.execute(sql, {"id": id})
            db.session.commit()
            return True
        except:
            return False
    else:
        return False


def getRoom(room_id, db):
    try:
        sql = "SELECT rooms.id AS room_id, room_name, username FROM rooms LEFT JOIN users ON user_id = users.id WHERE rooms.id=:id AND rooms.visible=1"
        result = db.session.execute(sql, {"id": room_id})
        roomData = result.fetchone()
    except:
        return None
    else:
        return roomData


def getMessages(room_id, db):
    sql1 = "SELECT content, username, messages.created_at AS datetime, messages.id AS message_id FROM messages LEFT JOIN users ON user_id = users.id LEFT JOIN rooms ON room_id = rooms.id WHERE rooms.id=:id AND messages.visible = 1 ORDER BY messages.created_at"
    result = db.session.execute(sql1, {"id": room_id})
    messages = result.fetchall()
    if not messages:
        return None
    else:
        return messages
