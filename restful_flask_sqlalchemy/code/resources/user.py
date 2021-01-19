import sqlite3
from flask_restful import Resource, reqparse


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


class UserRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='The username field cannot be empty')

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='The password field cannot be empty')

    def post(self):
        reg_credential = UserRegister.parser.parse_args()

        if User.get_user_by_username(reg_credential['username']):
            return {"message": "This Username already exists, please try another username"}, 400
        connection = sqlite3.connect('data.db')
        cur = connection.cursor()

        cur.execute("INSERT INTO users VALUES (NULL,?,?)", (reg_credential['username'], reg_credential['password']))

        connection.commit()
        connection.close()

        return {"message": "User {} is created successfully".format(reg_credential['username'])}, 201

