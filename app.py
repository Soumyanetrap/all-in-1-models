import streamlit as st
import json

# Sample data
data = {
    1: {'name': 'Item 1', 'description': 'This is item 1'},
    2: {'name': 'Item 2', 'description': 'This is item 2'},
}

# Define a function to return items as JSON
def get_items():
    return data

def get_item(item_id):
    return data.get(item_id, {'error': 'Item not found'})

# Main function
def main():
    # Set up a basic routing mechanism
    route = st.experimental_get_query_params().get("route", [None])[0]

    if route == "api/items":
        st.json(get_items())
    elif route and route.startswith("api/items/"):
        try:
            item_id = int(route.split("/")[-1])
            st.json(get_item(item_id))
        except ValueError:
            st.json({'error': 'Invalid item ID'})
    else:
        st.json({'error': 'Invalid route'})

if __name__ == "__main__":
    main()
