from flask import Flask
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)

items = []

class Item(Resource):
    # def get(self):
    #     return {'items': items}

    def get(self, name):
        for item in items:
            if item['name'] == name:
                return {'item': item}

        return {'message': 'No such a item available ...'}, 404


    def post(self, name):
        item = {'name': name, 'price': 12}
        items.append(item)
        return {'Added item': item}, 201


api.add_resource(Item, '/item/<string:name>')

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000)
