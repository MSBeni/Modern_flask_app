from flask import Flask

app = Flask(__name__)


stores = [
    {
        'name': 'my_new_store',
        'items': [
            {
                'item_name': 'the name of the item',
                'price': 100
            }
        ]
    }
]

# Create a store
@app.route('/store', methods=['POST'])
def create_store():
    pass


# Get the name of all stores
@app.route('/store', methods=['GET'])
def get_all_stores():
    pass


# Get the name of a specific store
@app.route('/store/<string:name>', methods=['GET'])   # 127.0.0.1:5000/store/store_name
def get_store(name):
    pass


# Get the name of a specific store
@app.route('/store/<string:name>/item', methods=['POST'])   # 127.0.0.1:5000/store/store_name/item
def create_item_in_store(name):
    pass


# Get all the items in a specific store
@app.route('/store/<string:name>/item', methods=['GET'])   # 127.0.0.1:5000/store/store_name/item
def get_all_items_in_store(name):
    pass


if __name__ == '__main__':
    app.run('127.0.0.1', port=5000)
