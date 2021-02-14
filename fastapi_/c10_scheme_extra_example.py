# coding: utf-8
# created by jlshix on 2021-03-15

"""https://fastapi.tiangolo.com/zh/tutorial/schema-extra-example/

Pydantic 模型类中可定义一个嵌套类 Config, 用于指定此模型类的配置.
关于 Pydantic 此特性的更多信息, 参见
https://pydantic-docs.helpmanual.io/usage/schema/#schema-customization

展示在文档页面的示例有三种提供方式:

1. Config 的 `schema_extra` 属性可以为此模型指定一个示例

2. 模型类的默认值可以使用 Field 的 example 属性

3. 视图函数的参数默认值可以使用 Body 的 examp 属性


以上三者等价
"""

from typing import Optional

from fastapi import FastAPI, Body
from pydantic import BaseModel, Field

app = FastAPI()

item_example = {
    "name": "Foo",
    "description": "A very nice Item",
    "price": 35.4,
    "tax": 3.2,
}


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None

    class Config:
        scheme_extra = {
            'example': item_example
        }


class ItemWithExample(BaseModel):
    name: str = Field(..., example='Foo')
    description: Optional[str] = Field(None, example="A very nice Item")
    price: float = Field(..., example=35.4)
    tax: Optional[float] = Field(None, example=3.2)


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item):
    rv = {
        'item_id': item_id,
        'item': item
    }
    return rv


@app.post('/items/{item_id}')
async def post_item(item_id: int, item: ItemWithExample):
    rv = {
        'item_id': item_id,
        'item': item
    }
    return rv


@app.patch('/items/{item_id}')
async def patch_item(item_id: int, item: Item = Body(..., example=item_example)):
    rv = {
        'item_id': item_id,
        'item': item
    }
    return rv
