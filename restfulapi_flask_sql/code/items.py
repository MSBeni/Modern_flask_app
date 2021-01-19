from flask_jwt import jwt_required
from flask_restful import Resource, reqparse


class Items(Resource):
    def get(self):
        return {'items': items}


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field cannot be empty')

    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x:x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x:x['name'] == name, items), None):
            return "Item {} already exits".format(name), 400
        # parsing to the json payload with the parse args as defined class Item RequestParser
        item_price = Item.parser.parse_args()

        item = {'name': name, 'price': item_price['price']}
        items.append(item)
        return {'Added item': item}, 201

    @jwt_required()
    def delete(self, name):
        global items
        if next(filter(lambda x: x['name'] == name, items), None) is None:
            return "There is no item named {} to be deleted".format(name), 400
        # item = next(filter(lambda x: x['name'] == name, items), None)
        # items.remove(item)
        items = list(filter(lambda x: x['name'] != name, items))
        return {'message': "item deleted"}, 200

    def put(self, name):
        # parsing to the json payload with the parse args as defined class Item RequestParser
        req_price = Item.parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            item = {'name': name, 'price': req_price['price']}
            items.append(item)
        else:
            item.update(req_price)
        return item