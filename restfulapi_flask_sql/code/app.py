from flask import Flask
from uuid import uuid4
from flask_restful import Api
from flask_jwt import JWT
from restfulapi_flask_sql.code.security import authenticate, identity
from restfulapi_flask_sql.code.user import UserRegister
from restfulapi_flask_sql.code.items import Items, Item

app = Flask(__name__)

app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create an add address for the node 5000
node_address = str(uuid4()).replace('-', '')

api = Api(app)
app.secret_key = 'msbeni'
jwt = JWT(app, authenticate, identity)

api.add_resource(Item, '/item/<string:name>')
api.add_resource(Items, '/items')
api.add_resource(UserRegister, '/signup')

if __name__ == '__main__':
    app.run('127.0.0.1', port=5000, debug=True)
