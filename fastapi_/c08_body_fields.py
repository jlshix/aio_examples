# coding: utf-8
# created by jlshix on 2021-02-04

"""https://fastapi.tiangolo.com/zh/tutorial/body-fields/

1. 与在函数参数中使用 `Query`, `Path`, `Body` 进行数据校验类似,
   可使用 Pydantic 的 `Field` 在数据模型内部声明校验和元数据.

2. `1` 中的四者虽然首字母大写, 但都是函数, 参数完全相同, 且最终都返回一个
   `pydantic.fields.FieldInfo` 实例.

3. `1` 中的四者的额外信息如 `title`, `description` 等将包含在生成的 JSON Schema 中.

"""

from typing import Optional

from fastapi import Body, FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, Field

app = FastAPI()


class Item(BaseModel):
    name: str
    description: Optional[str] = Field(
        None, title='description of the item', max_length=300
    )
    price: float = Field(..., gt=0, description="The price must be greater than zero")
    tax: Optional[float] = None


@app.put('/items/{item_id}')
async def update_item(item_id: int, item: Item = Body(..., embed=True)):
    rv = {'item_id': item_id, 'item': item}
    return rv


client = TestClient(app)


def test_price_validation_good():
    resp = client.put('/items/42', json={
        'item': {
            'name': 'something',
            'price': 10,
        }
    })
    assert resp.status_code == 200
    assert resp.json() == {
        'item_id': 42,
        'item': {
            'name': 'something',
            'price': 10,
            'description': None,
            'tax': None,
        }
    }


def test_price_validation_bad():
    resp = client.put('/items/42', json={
        'item': {
            'name': 'something',
            'price': -5,
        }
    })
    assert resp.status_code == 422
    assert resp.json() == {
        'detail': [{
            'loc': ['body', 'item', 'price'],
            'msg': 'ensure this value is greater than 0',
            'type': 'value_error.number.not_gt',
            'ctx': {'limit_value': 0}
        }]
    }
