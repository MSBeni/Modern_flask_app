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

    @classmethod
    def insert_into_table(cls, name, price):

        connection = sqlite3.connect('data.db')
        cur = connection.cursor()
        cur.execute("INSERT INTO items VALUES (?,?)", (name, price))
        connection.commit()
        connection.close()

    @classmethod
    def update_table(cls, price, name):

        connection = sqlite3.connect('data.db')
        cur = connection.cursor()
        cur.execute("UPDATE items SET price=? WHERE items.name=?", (price, name))
        connection.commit()
        connection.close()

    @jwt_required()
    def get(self, name):
        item = self.get_item_by_name(name)
        if item:
            return item

        return {"message": "item not found ..."}, 404

    def post(self, name):
        if self.get_item_by_name(name):
            return "Item {} already exits".format(name), 400   # something goes wrong with the request
        # parsing to the json payload with the parse args as defined class Item RequestParser
        item_price = Item.parser.parse_args()
        item = {'name': name, 'price': item_price['price']}
        try:
            self.insert_into_table(name, item_price['price'])
        except:
            return {"message": "Failed to insert into table ..."}, 500  # internal server error

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
        if item is None:
            self.insert_into_table(name, req_price['price'])
        else:
            self.update_table(req_price['price'], name)

        return {"message": "Item Added or update"}, 201
