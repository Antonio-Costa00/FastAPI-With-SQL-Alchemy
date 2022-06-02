from typing import List, Optional

from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel

import models
from database import SessionLocal

app = FastAPI()


class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    on_sale: bool

    class Config:
        orm_mode = True


db = SessionLocal()


@app.get("/items", response_model=List[Item], status_code=status.HTTP_200_OK)
def get_all_items():
    items = db.query(models.Item).all()

    return items


@app.get("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_item_by_id(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()

    return item


@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_item(item: Item):

    db_item = db.query(models.Item).filter(models.Item.name == item.name).first()

    if db_item is not None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Item already exists"
        )
    new_item = models.Item(
        name=item.name,
        description=item.description,
        price=item.price,
        on_sale=item.on_sale,
    )

    db.add(new_item)
    db.commit()

    return new_item


@app.put("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: Item):
    item_to_updt = db.query(models.Item).filter(models.Item.id == item_id).first()
    item_to_updt.name = item.name
    item_to_updt.price = item.price
    item_to_updt.description = item.description
    item_to_updt.on_sale = item.on_sale

    db.commit()

    return item_to_updt


@app.delete("/item/{item_id}")
def delete_item(item_id: int):
    item_to_del = db.query(models.Item).filter(models.Item.id == item_id).first()

    if item_to_del is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Item not found"
        )

    db.delete(item_to_del)
    db.commit()
    return item_to_del
