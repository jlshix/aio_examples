# coding: utf-8
# created by jlshix on 2021-03-15

"""https://fastapi.tiangolo.com/zh/tutorial/cookie-params/

可以像定义 Query 参数和 Path 参数一样来定义 Header 参数.

与 Path, Query, Cookie 不同的是, 大多数标准 header 使用连词符分隔,
如 `Content-Type`, `user-agent`. 在 python 中, 连词符也是减号,
不可出现在变量名中. 因此 Header 默认将连词符`-`转为下划线`-`.

若出于某些原因要禁用此功能, 可在声明时使用 `convert_underscores=False`.

若预期可能重复, 可在声明时将 `Optional[str]` 改为 `Optional[List[str]]`.

另, headers 大小写不敏感.
"""

from typing import Optional, List

from fastapi import FastAPI, Header
from fastapi.testclient import TestClient

app = FastAPI()


@app.get("/items/")
async def read_items(user_agent: Optional[str] = Header(None)):
    return {"User-Agent": user_agent}


@app.post('/items/')
async def post_items(user_agent: Optional[str] = Header(None, convert_underscores=False)):
    return {'User-Agent': user_agent}


@app.patch('/items/')
async def patch_items(user_agent: Optional[List[str]] = Header(None)):
    return {'User-Agent': user_agent}


client = TestClient(app)

headers = {'User-Agent': 'fastapi test client'}


def test_header():
    rv = client.get('/items/', headers=headers)
    assert rv.json() == headers


def test_header_not_convert_underscores():
    rv = client.post('/items/', headers=headers)
    assert rv.json() == {'User-Agent': None}

    tmp_headers = {'User_Agent': 'fastapi test client'}
    rv = client.post('/items/', headers=tmp_headers)
    assert rv.json() == {'User-Agent': 'fastapi test client'}


def test_header_value_list():
    rv = client.patch('/items/', headers=headers)
    assert rv.json() == {'User-Agent': ['fastapi test client', ]}
