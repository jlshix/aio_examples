# coding: utf-8
# created by jlshix on 2021-02-03

"""https://fastapi.tiangolo.com/zh/tutorial/body-multiple-params/

1. 如前文, 在函数参数无默认值标记时, 函数参数的识别优先级:
    1. 在路径中声明了该参数则作为路径参数;
    2. 为单一类型(如 int, float, str, bool等), 作为查询参数;
    3. 为 Pydantic 模型, 作为请求体.

2. 可使用 `Path` 标记为路径参数, `Query` 标记为查询参数, `Body` 标记为请求体.

3. 多个 `Body` 时以参数名为 key 放置于同一个字典中组成最终的请求体.

3. 只有一个请求体参数时, 可显式指定 `Body` 的 `embed` 参数为 True 增加层级.

"""

from typing import Optional

from fastapi import FastAPI, Body
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None


class User(BaseModel):
    username: str
    full_name: Optional[str] = None


@app.post("/multi_body/{item_id}")
async def multi_body(item_id: int, item: Item, user: User):
    results = {"item_id": item_id, "item": item, "user": user}
    return results


@app.post('/body_mark/{item_id}')
async def body_mark(
        item_id: int, item: Item, user: User, importance: int = Body(...)
):
    results = {"item_id": item_id, "item": item, "user": user, "importance": importance}
    return results


@app.post("/body_embed/{item_id}")
async def body_embed(item_id: int, item: Item = Body(..., embed=True)):
    rv = {"item_id": item_id, "item": item}
    return rv


client = TestClient(app)


def default_data() -> dict:
    return {
        "item": {
            "name": "Foo",
            "description": "The pretender",
            "price": 42.0,
            "tax": 3.2
        },
        "user": {
            "username": "dave",
            "full_name": "Dave Grohl"
        }
    }


def test_multi_body():
    data = default_data()
    resp = client.post('/multi_body/42', json=data)
    assert resp.status_code == 200
    data['item_id'] = 42
    assert resp.json() == data


def test_body_mark():
    data = default_data()
    data['importance'] = 5
    resp = client.post('/body_mark/42', json=data)
    assert resp.status_code == 200
    data['item_id'] = 42
    assert resp.json() == data


def test_body_embed():
    data = default_data()
    data.pop('user')
    resp = client.post('/body_embed/42', json=data)
    assert resp.status_code == 200
    data['item_id'] = 42
    assert resp.json() == data
