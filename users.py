from flask import session, flash
from werkzeug.security import check_password_hash, generate_password_hash


def login(username, password, db):
    try:
        sql = "SELECT password, id, role FROM users WHERE username=:username"
        result = db.session.execute(sql, {"username": username})
        user = result.fetchone()
    except:
        return False
    else:
        if user == None:
            print("no user found")
            return False
        else:
            hash_value = user[0]

            if check_password_hash(hash_value, password):
                session["username"] = username
                session["id"] = user[1]
                session["admin"] = False
                if user[2] == 0:
                    print("Admin session")
                    session["admin"] = True
                return True
            else:
                print("wrong password")
                return False


def logout():
    session.pop("username", None)
    session.pop("id", None)
    session.pop("admin", False)


def register(username, password, db):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username,password, role) VALUES (:username,:password, 1)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    else:
        return login(username, password, db)
