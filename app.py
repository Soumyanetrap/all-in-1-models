from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict

# FastAPI app
app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust this as needed for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Sample data
data: Dict[int, dict] = {
    1: {'name': 'Item 1', 'description': 'This is item 1'},
    2: {'name': 'Item 2', 'description': 'This is item 2'},
}

# Pydantic model for new items
class Item(BaseModel):
    name: str
    description: str

@app.get("/api/items")
def get_items():
    return data

@app.get("/api/items/{item_id}")
def get_item(item_id: int):
    item = data.get(item_id)
    if item:
        return item
    else:
        raise HTTPException(status_code=404, detail="Item not found")

@app.post("/api/items", response_model=Item)
def create_item(item: Item):
    new_id = max(data.keys()) + 1
    data[new_id] = item.dict()
    return {**item.dict(), "id": new_id}

# if __name__ == "__main__":
#     import uvicorn
#     import os
#     uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
