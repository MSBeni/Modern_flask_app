from flask import Flask, request
from uuid import uuid4
from flask_restful import Api, Resource
from flask_jwt import JWT, jwt_required
from simple_RESTFUL_app.code.security import authenticate, identity

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create an add address for the node 5000
node_address = str(uuid4()).replace('-', '')

api = Api(app)
app.secret_key = 'msbeni'
jwt = JWT(app, authenticate, identity)

items = []


class Items(Resource):
    def get(self):
        return {'items': items}


class Item(Resource):
    @jwt_required()
    def get(self, name):
        item = next(filter(lambda x:x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        if next(filter(lambda x:x['name'] == name, items), None):
            return "Item {} already exits".format(name), 400
        item_price = request.get_json(silent=True)

        item = {'name': name, 'price': item_price['price']}
        items.append(item)
        return {'Added item': item}, 201

    @jwt_required()
    def delete(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is None:
            return "There is no item named {} to be deleted".format(name), 400
        global items
        item = next(filter(lambda x: x['name'] == name, items), None)
        items.remove(item)
        return {'items': items}, 200


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
