import sqlite3
from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from restful_flask_sqlalchemy.code.models.item import ItemModel


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


    @jwt_required()
    def get(self, name):
        item = ItemModel.get_item_by_name(name)
        if item:
            return item.json()

        return {"message": "item not found ..."}, 404

    def post(self, name):
        if ItemModel.get_item_by_name(name):
            return "Item {} already exits".format(name), 400   # something goes wrong with the request
        # parsing to the json payload with the parse args as defined class Item RequestParser
        item_price = Item.parser.parse_args()
        item = ItemModel(name, item_price['price'])
        try:
            item.insert_into_table()
        except:
            return {"message": "Failed to insert into table ..."}, 500  # internal server error

        return {'Added item': item}, 201

    @jwt_required()
    def delete(self, name):
        if ItemModel.get_item_by_name(name) is None:
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
        item = ItemModel.get_item_by_name(name)
        updeted_item = ItemModel(name, req_price['price'])
        if item is None:
            try:
                ItemModel.insert_into_table(name, req_price['price'])
            except:
                return {"message": "Failed to insert into table ..."}, 500  # internal server error
        else:
            try:
                ItemModel.update_table(req_price['price'], name)
            except:
                return {"message": "Failed to update the table ..."}, 500  # internal server error

        return updeted_item, 201
