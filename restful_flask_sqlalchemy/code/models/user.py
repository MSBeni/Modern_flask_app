import sqlite3

class User(object):
    def __init__(self, id_, username, password):
        self.id = id_
        self.username = username
        self.password = password

    @classmethod
    def get_user_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM users WHERE users.username=?", (username,))
        user_ = result.fetchone()
        if user_:
            user_f = cls(*user_)

        else:
            user_f = None

        connection.close()
        return user_f

    @classmethod
    def get_user_by_id(cls, id_):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        result = cursor.execute("SELECT * FROM users WHERE users.id=?", (id_,))
        id_ = result.fetchone()
        if id_:
            id_f = cls(*id_)

        else:
            id_f = None

        connection.close()
        return id_f

