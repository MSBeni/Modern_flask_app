from flask import Flask, request
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

items = []

items_2 = [{'name': 'book', 'price': 12}, {'name': 'piano', 'price': 20}]
x = filter(lambda x: x['name'] == 'book', items_2)
print(*x)


class Items(Resource):
    def get(self):
        return {'items': items}


class Item(Resource):
    def get(self, name):
        item = next(filter(lambda x:x['name'] == name, items), None)
        return {'item': item}, 200 if item is not None else 404

    def post(self, name):
        item_price = request.get_json(silent=True)

        item = {'name': name, 'price': item_price['price']}
        items.append(item)
        return {'Added item': item}, 201


api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
