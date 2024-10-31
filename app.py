from flask import Flask, jsonify, request
from flask_cors import CORS
import os

# Flask app
app = Flask(__name__)
CORS(app)

# Sample data
data = {
    1: {'name': 'Item 1', 'description': 'This is item 1'},
    2: {'name': 'Item 2', 'description': 'This is item 2'},
}

@app.route('/api/items', methods=['GET'])
def get_items():
    return jsonify(data)

@app.route('/api/items/<int:item_id>', methods=['GET'])
def get_item(item_id):
    item = data.get(item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({'error': 'Item not found'}), 404

@app.route('/api/items', methods=['POST'])
def create_item():
    new_id = max(data.keys()) + 1
    new_item = request.json
    data[new_id] = new_item
    return jsonify({'id': new_id, **new_item}), 201

if __name__ == '__main__':
    app.run()
