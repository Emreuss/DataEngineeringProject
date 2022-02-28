from fastapi import FastAPI,Path
from typing import Optional
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    brand: Optional[str] = None




'''
@app.get("/")
def home():
    return {"Data": "Test"}

@app.get("/about")
def about():
    return {"Data": "About"} '''

invertory = {
        1: {
            "name": "Milk",
            "price": 3.99,
            "brand": "Regular"
        }

   }

@app.get("/get-item/{item_id}")
def get_item(item_id: int = Path(None, description="The ID of the item yo'd like to view")):
    return invertory[item_id]

#127.0.0.1:8000/get-by-name?name=Milk --Response {"name":"Milk","price":3.99,"brand":"Regular"}
#http://127.0.0.1:8000/get-by-name?test=2&name=Milk --Response  {"name":"Milk","price":3.99,"brand":"Regular"}

'''
@app.get("/get-by-name")
def get_item(*, name: Optional[str] = None, test: int):
    for item_id in invertory:
        if invertory[item_id]["name"] == name:
            return invertory[item_id]

    return {"Data": "Not Found"} '''

#http://127.0.0.1:8000/get-by-name/1?test=2&name=Milk --Response {"name":"Milk","price":3.99,"brand":"Regular"}
@app.get("/get-by-name/{item_id}")
def get_item(*, item_id: int, name: Optional[str] = None, test: int):
    for item_id in invertory:
        if invertory[item_id]["name"] == name:
            return invertory[item_id]

    return {"Data": "Not Found"}

@app.post("/create-item/{item_id}")
def create_item(item_id: int, item: Item):
    if item_id in invertory:
        return {"Error": "Item ID already exists."}

    #invertory[item_id] = {"name": item.name, "brand": item.brand, "price": item.price}
    invertory[item_id] = item
    return invertory[item_id]
