# coding: utf-8
# created by jlshix on 2021-02-02

"""https://fastapi.tiangolo.com/zh/tutorial/path-params-numeric-validations/

1. `Path` 与 `Query` 参数相同, 首个参数 default 传入 `...` 或 `None` 都是必须,
    因为是路径的一部分, 仍建议使用 `...`

2. 使用 min_length, max_length, regex 等做字符串验证

3. 使用 ge, gt, le, lt 等做数字验证, int, float 均可

"""

from typing import Optional

from fastapi import FastAPI, Path, Query
from fastapi.testclient import TestClient

app = FastAPI()


@app.get('/items/{item_id}')
async def read_items(
        item_id: int = Path(..., title='', gt=0, le=1000),
        q: Optional[str] = Query(None, alias='item-query'),
        size: float = Query(..., ge=0, lt=10.5)
):
    rv = {'item_id': item_id}
    if q:
        rv['q'] = q
    rv['size'] = size
    return rv


client = TestClient(app)


def test_alias():
    resp = client.get('/items/42?q=query&size=1')
    assert 'q' not in resp.json()

    resp = client.get('/items/42?item-query=query&size=1')
    assert resp.json()['q'] == 'query'


def test_numeric_validation():
    resp = client.get('/items/42?size=10')
    assert resp.json() == {'item_id': 42, 'size': 10}

    resp = client.get('/items/42?size=11.5')
    assert resp.status_code == 422
    assert resp.json() == {
        'detail': [
            {
                'loc': ['query', 'size'],
                'msg': 'ensure this value is less than 10.5',
                'type': 'value_error.number.not_lt',
                'ctx': {'limit_value': 10.5}
            }
        ]
    }
