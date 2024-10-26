from flask import Flask, jsonify, request
from threading import Thread
import os
import streamlit as st
import requests

# Flask app
app = Flask(__name__)

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

def run_flask():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

# Start the Flask app in a separate thread
thread = Thread(target=run_flask)
thread.start()

# Streamlit interface
st.title("Flask API with Streamlit")

# Fetch and display items
response = requests.get('http://127.0.0.1:8080/api/items')
if response.status_code == 200:
    items = response.json()
    st.write("Items:")
    for item_id, item in items.items():
        st.write(f"**ID:** {item_id} - **Name:** {item['name']} - **Description:** {item['description']}")
else:
    st.error("Failed to fetch items.")

# Form to create a new item
st.subheader("Add New Item")
new_name = st.text_input("Item Name")
new_description = st.text_area("Item Description")
if st.button("Create Item"):
    new_item = {'name': new_name, 'description': new_description}
    create_response = requests.post('http://127.0.0.1:8080/api/items', json=new_item)
    if create_response.status_code == 201:
        st.success("Item created successfully!")
    else:
        st.error("Failed to create item.")
