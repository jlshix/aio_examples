# coding: utf-8
# created by jlshix on 2021-02-04

"""https://fastapi.tiangolo.com/zh/tutorial/body-nested-models/

1. pydantic 的数据模型支持嵌套使用

2. 单一值类型除了 str, int, float 外, 还可以使用从 str 继承的更复杂的单一值类型,
   如 HttpUrl

3. 支持使用 `typing.List` 标记为列表

4. 简单类型即使不使用 Pydantic 的 BaseModel, 如声明为 `Dict[int, float]`, 仍会进行转换.
   所有支持的类型见 https://pydantic-docs.helpmanual.io/usage/types/

"""

from typing import List, Optional, Set, Dict

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel, HttpUrl

app = FastAPI()


class Image(BaseModel):
    url: HttpUrl
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = set()
    images: Optional[List[Image]] = None


class Offer(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    items: List[Item]


@app.post("/offers/")
async def create_offer(offer: Offer):
    return offer


@app.post("/images/multiple/")
async def create_multiple_images(images: List[Image]):
    return images


@app.post("/index-weights/")
async def create_index_weights(weights: Dict[int, float]):
    return {
        'data': weights,
        'all_keys_int': all(isinstance(k, int) for k in weights.keys()),
        'all_values_float': all(isinstance(v, float) for v in weights.values())
    }


client = TestClient(app)


def test_nested_model():
    data = {
        'name': 'some offer',
        'description': 'offer description',
        'price': 9.9,
        'items': [
            {
                "name": "Foo",
                "description": "The pretender",
                "price": 42.0,
                "tax": 3.2,
                "tags": [
                    "rock",
                    "metal",
                    "bar"
                ],
                "images": [
                    {
                        "url": "http://example.com/baz.jpg",
                        "name": "The Foo live"
                    },
                    {
                        "url": "http://example.com/dave.jpg",
                        "name": "The Baz"
                    }
                ]
            }
        ]
    }
    resp = client.post('/offers/', json=data)
    assert resp.status_code == 200


def test_model_list():
    images = [
        {
            "url": "http://example.com/baz.jpg",
            "name": "The Foo live"
        },
        {
            "url": "http://example.com/dave.jpg",
            "name": "The Baz"
        }
    ]
    resp = client.post('/images/multiple/', json=images)
    assert resp.status_code == 200
    assert resp.json() == images


def test_dict():
    data = {
        '1': '5.5',
        '2': 2
    }
    resp = client.post('/index-weights/', json=data)
    assert resp.status_code == 200
    assert resp.json() == {
        'data': {
            '1': 5.5,
            '2': 2
        },
        'all_keys_int': True,
        'all_values_float': True
    }
