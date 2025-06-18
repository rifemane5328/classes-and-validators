from fastapi import FastAPI
from pydantic import BaseModel, Field, EmailStr, validator
from typing import Optional, Literal
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
    password: str = Field("password1234", ge=8)
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
    payment_type: Literal["card", "cash"] = Field(...)  # готівка, картка


class CardInfo(BaseModel):
    card_number: str = Field(...)
    expiration_date: date = Field(...)
    cvv: int = Field(...)


class SuccessMessageCash(BaseModel):
    message: str = "Оплата готівкою пройшла успішно"


class ImageUploadMetadata(BaseModel):
    file_name: str = Field(max_length=50)  # печиво.png
    file_type: str = Field(max_length=10)  # .img, .png


class CorporateEmail(BaseModel):
    email: EmailStr = Field(max_length=40)

    @validator("email")
    def corporate_only(cls, email):
        if not email.endswith("goiteens.com"):
            raise ValueError("Е-пошта має закінчуватися на `goiteens.com`")
        return email


class DateModel(BaseModel):
    created_at: date = Field(...)

    @validator("created_at")
    def not_future(cls, created_at):
        if created_at > date.today():
            raise ValueError("Дата не може бути майбутньою")
        return created_at


@app.post('/pay')
async def payment_process(payment: PaymentInfo):
    if payment.payment_type == "cash":
        return SuccessMessageCash()
    elif payment.type == "card":
        card_info = CardInfo


@app.get("/get_item")
async def get_item(item: Item):
    return {"name": item.name, "price": item.price, "amount": item.amount, "is_available": item.is_available}


@app.post("/check_password")
async def check_password(user: UserRegistration):
    numbers = "1234567890"
    high_letters = "QWERTYUIOPASDFGHJKLZXCVBNM"
    if not any(number in user.password for number in numbers):
        raise ValueError("Пароль має містити хоча б одну цифру")
    if not any(letter in user.password for letter in high_letters):
        raise ValueError("Пароль має містити хоча б одну велику букву")
    return "Ваш пароль надійний"

