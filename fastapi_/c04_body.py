# coding: utf-8
# created by jlshix on 2021-02-02

"""https://fastapi.tiangolo.com/zh/tutorial/body/

1. 数据作为请求体从客户端发往 API, 得到响应体.

2. 使用 `Pydantic` 模型声明请求体, 但不能使用 GET 方法发送, 可以使用 POST, PUT, DELETE 等.

3. 数据模型若一个字段是可选的, 则这个字段的值为 None 和这个字段不存在等价

4. 函数参数的识别优先级:
    1. 在路径中声明了该参数则作为路径参数;
    2. 为单一类型(如 int, float, str, bool等), 作为查询参数;
    3. 为 Pydantic 模型, 作为请求体.

"""
from typing import Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


app = FastAPI()


@app.post('/items/')
async def create_item(item: Item):
    dic = item.dict()
    if item.tax:
        dic['price_with_tax'] = item.price + item.tax
    return dic


@app.put('/items/{item_id}')
async def create_item_by_put(item_id: int, item: Item, q: Optional[str] = None):
    rv = {'item_id': item_id, **item.dict()}
    if q:
        rv['q'] = q
    return rv


client = TestClient(app)


def test_item():
    dic = {
        'name': 'coca cola',
        'description': 'cola',
        'price': 2.99,
        'tax': 0.9
    }
    item = Item(**dic)
    assert item.dict() == dic
