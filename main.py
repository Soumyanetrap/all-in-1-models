from fastapi import FastAPI
from pydantic import BaseModel

# FastAPI app
app = FastAPI()

@app.get('/')
async def hello_world():
    return "Hello World"

@app.get('/api/health')
async def get_health():
    return "I am Alive and Kicking!"

# Define a Pydantic model for input validation
class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/api/items")
async def create_item(item: Item):
    total_price = item.price + (item.tax or 0)
    return {
        "name": item.name,
        "description": item.description,
        "price": item.price,
        "tax": item.tax,
        "total_price": total_price
    }
