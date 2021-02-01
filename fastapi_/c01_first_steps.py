# coding: utf-8
# created by jlshix on 2021-02-01

"""https://fastapi.tiangolo.com/zh/tutorial/first-steps/

1. http://127.0.0.1:8000/ 为 index 的请求处理

2. http://127.0.0.1:8000/docs 为自动生成的交互式 API 文档 (Swagger UI)

3. http://127.0.0.1:8000/redoc 为可选的自动生成文档 (ReDoc)

4. http://127.0.0.1:8000/openapi.json 为 OpenAPI 定义

5. 可以使用 "uvicorn file_name:app_instance --reload" 这样的命令启动

6. 同时支持 `async def index()` 和 `def index()` 两种形式
"""

from fastapi import FastAPI
from fastapi.testclient import TestClient


app = FastAPI()


@app.get('/')
async def index():
    return {'message': 'hello world'}


client = TestClient(app)


def test_index():
    resp = client.get('/')
    assert resp.status_code == 200
    assert resp.json() == {'message': 'hello world'}
