# coding: utf-8
# created by jlshix on 2021-02-02

"""https://fastapi.tiangolo.com/zh/tutorial/query-params-str-validations/

1. 使用 fastapi.Query 作为函数参数的默认值从而执行校验.

2. Query 实际上是一个函数, 最终返回一个 `pydantic.fields.FieldInfo`

3. Query 的第一个参数为 default, 若为必选, 可传入 `...`, 即 `Ellipsis`, 是一个特殊的单独值.

4. Ellipses 参见 https://docs.python.org/zh-cn/3/library/constants.html#Ellipsis

5. Query 可指定 title, description, deprecated 等元数据用于生成文档;

6. Query 可指定 alias 用于在 url 中查找参数值; 指定 min_length, ge, regex 等进行长度, 大小, 正则匹配等验证条件.
"""

from typing import Optional, List

from fastapi import FastAPI, Query
from fastapi.testclient import TestClient

app = FastAPI()


@app.get('/items/')
async def read_items(q: Optional[str] = Query(default=None, max_length=5)):
    rv = {}
    if q:
        rv.update({"q": q})
    return rv


@app.get('/multi_q/')
async def multi_q(q: Optional[List[str]] = Query(None)):
    return {'q': q}


client = TestClient(app)


def test_optional_q():
    resp = client.get('/items/')
    assert resp.json() == {}

    resp = client.get('/items/?q=four')
    assert resp.json() == {'q': 'four'}

    resp = client.get('/items/?q=four&q=five')
    assert resp.json() == {'q': 'five'}

    resp = client.get('/items/?q=eleven')
    assert resp.status_code == 422
    assert resp.json() == {
        'detail': [
            {
                'loc': ['query', 'q'],
                'msg': 'ensure this value has at most 5 characters',
                'type': 'value_error.any_str.max_length',
                'ctx': {'limit_value': 5}
            }
        ]
    }


def test_optional_multi_q():
    resp = client.get('/multi_q/')
    assert resp.json() == {'q': None}

    resp = client.get('/multi_q/?q=four')
    assert resp.json() == {'q': ['four']}

    resp = client.get('/multi_q/?q=four&q=five')
    assert resp.json() == {'q': ['four', 'five']}
