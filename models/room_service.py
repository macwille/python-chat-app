from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash


def create_room(user_id, room_name, subject_id, db):
    try:
        sql = "INSERT INTO rooms (room_name, user_id, subject_id, visible) values(:room_name, :user_id, :subject_id, 1)"
        db.session.execute(
            sql, {"room_name": room_name.strip(), "user_id": user_id, "subject_id": subject_id})
        db.session.commit()
        return True
    except:
        return False


def delete_room(room_id, db):
    if is_owner(session["id"], room_id, db) or session["admin"]:
        try:
            sql = "UPDATE rooms SET visible = 0 WHERE id = :id"
            db.session.execute(sql, {"id": room_id})
            db.session.commit()
            return True

        except:
            return False
    else:
        return False


def get_room(room_id, db):
    sql = "SELECT rooms.id AS room_id, room_name, username FROM rooms LEFT JOIN users ON user_id = users.id WHERE rooms.id=:id AND rooms.visible=1"
    result = db.session.execute(sql, {"id": room_id})
    roomData = result.fetchone()

    return roomData


def get_messages(room_id, db):
    sql = "SELECT content, username, messages.created_at AS datetime, messages.id AS message_id FROM messages LEFT JOIN users ON user_id = users.id LEFT JOIN rooms ON room_id = rooms.id WHERE rooms.id=:id AND messages.visible = 1 ORDER BY messages.created_at"
    result = db.session.execute(sql, {"id": room_id})
    messages = result.fetchall()

    return messages


def get_subject(room_id, db):
    sql = "SELECT subject_id FROM rooms WHERE id = :room_id"
    result = db.session.execute(sql, {"room_id": room_id})
    subject_id = result.fetchone()[0]

    return subject_id


def is_owner(user_id, room_id, db):
    if session["admin"]:
        print("Admin rights")
        return True

    else:
        sql = "SELECT COUNT(*) FROM rooms WHERE user_id = :user_id AND id = :room_id"
        result = db.session.execute(
            sql, {"user_id": user_id, "room_id": room_id})
        is_owner = result.fetchone()[0]

        return is_owner > 0
