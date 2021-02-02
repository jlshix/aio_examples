# coding: utf-8
# created by jlshix on 2021-02-01

"""https://fastapi.tiangolo.com/zh/tutorial/query-params/

1. 路径参数和查询参数无需按顺序进行声明, FastAPI 可自动识别.

2. `q: Optional[str] = None` 与 `q: str = None` 等价, 建议使用前者

3. 查询参数若要声明为必选, 可不为其指定默认值. 或使用下一节的 `Query(...)`

"""
from typing import Optional

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()

fake_items_db = [{"item_name": "Foo"}, {"item_name": "Bar"}, {"item_name": "Baz"}]


@app.get('/items/')
async def read_item(skip: int = 0, limit: int = 10):
    """以下四者等价:
    1. GET /items/
    2. GET /items/?skip=0&limit=10
    3. GET /items/?skip=0
    4. GET /items/?limit=10

    以下二者等价:
    1. GET /items/skip=10
    2. GET /items/skip=10&limit=10
    """
    return fake_items_db[skip: skip + limit]


@app.get('/items/{item_id}')
async def read_item_by_id(item_id: str, q: Optional[str] = None, short: bool = None):
    item = {'item_id': item_id}
    if q:
        item['q'] = q
    if not short:
        item['description'] = 'This is an amazing item that has a long description'
    return item


client = TestClient(app)


def test_read_item_by_id_optional():
    """`q` 使用 Optional 标记, 作为可选参数"""
    resp = client.get('/items/5')
    assert 'q' not in resp.json()

    resp = client.get('/items/42?q=query')
    assert resp.json()['q'] == 'query'


@pytest.mark.parametrize('short', ['1', 'yes', 'on', 'true', 'True'])
def test_read_item_by_id_bool_true(short):
    """short 作为布尔型, 以上值作为 True"""
    resp = client.get(f'/items/42?short={short}')
    assert 'description' not in resp.json()


@pytest.mark.parametrize('short', ['0', 'False', 'off', 'no'])
def test_read_item_by_id_bool_no(short):
    """short 作为布尔型, 以上值作为 False"""
    resp = client.get(f'/items/42?short={short}')
    assert 'description' in resp.json()
