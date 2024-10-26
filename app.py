from flask import Flask, jsonify, request

app = Flask(__name__)

# Sample data
data = {
    1: {'name': 'Item 1', 'description': 'This is item 1'},
    2: {'name': 'Item 2', 'description': 'This is item 2'},
}

@app.route('/api/items', methods=['GET'])
def get_items():
    print("Here")
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

# Only include this if running directly (not for WSGI)
if __name__ == '__main__':
    app.run(port=8080)
