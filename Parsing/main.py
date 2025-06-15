from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import date


app = FastAPI()


class Item(BaseModel):  # ITEM
    name: str = Field("banana", max_length=100)
    price: float = Field(0, ge=0, lt=9999, max_digits=6)
    amount: int = Field(None, le=500, max_digits=3)
    is_available: Optional[bool] = False


class ItemLaptop(Item):
    battery: str = Field(..., title="microsoft", description="microsoft це різнокольорові розробники які зробили"
                                                             " цей ноутбук")


class User(BaseModel):  # USER
    name: str = Field("Oscar6952", max_length=20)
    age: date = Field()


class Birthday(User):
    user_age: int = Field(ge=14, lt=99)


class UserRegistration(User):
    username: str = Field("user", max_length=30)
    password: str = Field("password1234")
    email: EmailStr = Field()


class OrderItem(Item):
    product_id: int = Field()
    quantity: int = Field()


class ShippingAddress(BaseModel):
    username: str = Field()
    city: str = Field()
    street: str = Field()
    apartment: int = Field()


class PaymentInfo(BaseModel):
    customer: User = Field()
    amount: float = Field(max_digits=6)
    payment_type: str = Field(max_length=30)  # готівка, картка


class ImageUploadMetadata(BaseModel):
    file_name: str = Field(max_length=50)  # печиво.png
    file_type: str = Field(max_length=10)  # .img, .png


# class Login(User):
@app.get("/main/")
async def main():
    ...
