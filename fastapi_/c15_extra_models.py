# coding: utf-8
# created by jlshix on 2021-03-15

"""https://fastapi.tiangolo.com/zh/tutorial/extra-models/

对于一个用户模型 User, API in, API out, DB 三处会有细微不同,
如 API in 包含密码明文, API out 不包含密码, DB 包含密码散列值.

可以使用继承定义多个模型使用.

另外, response_model 支持使用 Union 来指定多个其中的一个,
支持使用 List 来指定一个列表, 支持使用非 Pydantic 模型指定任意输出.

"""

from typing import Optional, Union, List, Dict

from fastapi import FastAPI
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None


class UserIn(UserBase):
    password: str


class UserOut(UserBase):
    pass


class UserInDB(UserBase):
    hashed_password: str


def fake_password_hasher(raw_password: str):
    return "supersecret" + raw_password


def fake_save_user(user_in: UserIn):
    hashed_password = fake_password_hasher(user_in.password)
    user_in_db = UserInDB(**user_in.dict(), hashed_password=hashed_password)
    print("User saved! ..not really")
    return user_in_db


@app.post("/user/", response_model=UserOut)
async def create_user(user_in: UserIn):
    user_saved = fake_save_user(user_in)
    return user_saved


@app.put("/user/", response_model=Union[UserInDB, UserOut])
def put_user(user_in: UserIn):
    return user_in


@app.patch("/users/", response_model=List[UserOut])
def patch_users(user_in: UserIn):
    return [user_in, ] * 3


@app.get("/keyword-weights/", response_model=Dict[str, float])
async def read_keyword_weights():
    return {"foo": 2.3, "bar": 3.4}
