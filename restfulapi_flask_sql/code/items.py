import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Items(Resource):
    def get(self):
        connection = sqlite3.connect('data.db')
        cur = connection.cursor()
        data = cur.execute("SELECT * FROM items")
        row = data.fetchall()
        connection.close()
        return {'items': row}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be empty')

    @classmethod
    def get_item_by_name(cls, name):
        connection = sqlite3.connect('data.db')
        cur = connection.cursor()
        data = cur.execute("SELECT * FROM items WHERE items.name=?", (name,))
        row = data.fetchone()
        connection.close()
        if row:
            return {'item': {"name": row[0], "price": row[1]}}

    @jwt_required()
    def get(self, name):
        item = self.get_item_by_name(name)
        if item:
            return item

        return {"message": "item not found ..."}, 404

    def post(self, name):
        if self.get_item_by_name(name):
            return "Item {} already exits".format(name), 400
        # parsing to the json payload with the parse args as defined class Item RequestParser
        item_price = Item.parser.parse_args()
        connection = sqlite3.connect('data.db')
        cur = connection.cursor()
        cur.execute("INSERT INTO items VALUES (?,?)", (name, item_price['price']))
        connection.commit()
        connection.close()
        item = {'name': name, 'price': item_price['price']}

        return {'Added item': item}, 201

    @jwt_required()
    def delete(self, name):
        if self.get_item_by_name(name) is None:
            return "There is no item named {} to be deleted".format(name), 400
        connection = sqlite3.connect('data.db')
        cur = connection.cursor()
        cur.execute("DELETE FROM items WHERE items.name=?", (name,))
        connection.commit()
        connection.close()
        return {'message': "item deleted"}, 200

    def put(self, name):
        # parsing to the json payload with the parse args as defined class Item RequestParser
        req_price = Item.parser.parse_args()
        item = self.get_item_by_name(name)
        connection = sqlite3.connect('data.db')
        cur = connection.cursor()
        if item is None:
            cur.execute("INSERT INTO items VALUES (?,?)", (name, req_price['price']))
            return {"message": "Item Added"}, 201
        else:
            cur.execute("UPDATE items SET price=? WHERE items.name=?", (req_price['price'], name))

        connection.commit()
        connection.close()
        return item
