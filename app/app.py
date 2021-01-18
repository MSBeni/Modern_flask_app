from flask import Flask, jsonify, request, render_template
from uuid import uuid4

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = False

# Create an add address for the node 5000
node_address = str(uuid4()).replace('-', '')

stores = [
    {
        "name": "my_new_store",
        "items": [
            {
                "item_name": "the name of the item",
                "price": 100
            }
        ]
    }
]


# Create a store
@app.route('/', methods=['GET'])
def hello_mng():
    return render_template('index.html')


# Create a store
@app.route('/store', methods=['POST'])
def create_store():
    new_store = request.get_json()
    posted_data = {
        'name': new_store['name'],
        'items': []
    }
    stores.append(posted_data)
    return jsonify({"stores": stores})


# Get the name of all stores
@app.route('/store', methods=['GET'])
def get_all_stores():
    return jsonify({'stores': stores}), 200


# Get the name of a specific store
@app.route('/store/<string:name>', methods=['GET'])   # 127.0.0.1:5000/store/store_name
def get_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"store": store})
    return "No such a Store is available"


# Post the name of a specific item to a specific store
@app.route('/store/<string:name>/item', methods=['POST'])   # 127.0.0.1:5000/store/store_name/item
def create_item_in_store(name):
    req_item = request.get_json()
    new_item = {
        'item_name': req_item["name"],
        'price': req_item["price"]
    }
    for store in stores:
        if store["name"] == name:
            store["items"].append(new_item)
            return jsonify({'items': new_item})

    return jsonify({'message': 'store not found'})


# Get the name of a specific item to a specific store
@app.route('/store/<string:name>/item', methods=['GET'])   # 127.0.0.1:5000/store/store_name/item
def get_all_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})

    return "No data to show -- there is not such  a store"


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000)
