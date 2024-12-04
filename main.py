from fastapi import FastAPI
from pydantic import BaseModel
import asyncio
import httpx
from datetime import datetime
import pytz

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

# Time zone for India Standard Time (IST)
IST = pytz.timezone('Asia/Kolkata')

# Define a background task to call the URL every 14 minutes
async def call_external_url():
    url = "https://all-in-1-server.onrender.com/keep-alive"  # Replace with your actual URL
    async with httpx.AsyncClient() as client:
        while True:
            # Get the current time in IST
            current_time = datetime.now(IST)
            current_hour = current_time.hour

            # Check if the current time is between 1:00 AM and 5:59 AM IST
            if 1 <= current_hour < 6:
                print("Skipping URL call: Time is between 1:00 AM and 5:59 AM IST")
            else:
                try:
                    response = await client.get(url)
                    if response.status_code == 200:
                        print("Service is alive!")
                    else:
                        print(f"Failed to call URL, status code: {response.status_code}")
                except Exception as e:
                    print(f"Error calling the URL: {e}")

            # Sleep for 14 minutes before the next check
            await asyncio.sleep(14.5 * 60)