# coding: utf-8
# created by jlshix on 2021-03-15

"""https://fastapi.tiangolo.com/zh/tutorial/response-model/

可以在 `@app.get`, `@app.post` 等装饰器中使用 `response_model` 参数.

FastAPI 将使用此 response_model 来：

- 将输出数据转换为其声明的类型
- 校验数据
- 在 OpenAPI 的路径操作中为响应添加一个 JSON Schema
- 并在自动生成文档系统中使用

最重要的是, 将输出数据限制在该模型定义内.

可以为输入输出各指定一个模型, 若只是相差一两个字段, 可以使用 `response_model_exclude`,
`response_model_include` 方法, 通过传入字段集合来指定排除或只允许的字段.

另外还有 `response_model_exclude_unset` 用于排除未设定值的字段,
`response_model_exclude_defaults` 用于排除默认值的字段,
`response_model_exclude_none` 用于排除值为 None 的字段.

参见 Pydantic 文档: https://pydantic-docs.helpmanual.io/usage/exporting_models/#modeldict

"""

from typing import Optional

from fastapi import FastAPI
from fastapi.testclient import TestClient
from pydantic import BaseModel

app = FastAPI()


class UserIn(BaseModel):
    user_name: str
    password: str
    email: str
    full_name: Optional[str] = None


class UserOut(BaseModel):
    user_name: str
    email: str
    full_name: Optional[str] = None


@app.post("/users/", response_model=UserOut)
async def create_user(user: UserIn):
    return user


@app.put('/users/', response_model=UserIn, response_model_exclude={'password'})
async def put_user(user: UserIn):
    return user


client = TestClient(app)


def test_user_out():
    user_without_password = {
        'user_name': 'leo',
        'email': 'leo@github.com',
        'full_name': 'leo leo'
    }
    user = {**user_without_password, 'password': 'pass_w0rd'}
    rv = client.post('/users/', json=user)
    assert rv.json() == user_without_password

    rv = client.put('/users/', json=user)
    assert rv.json() == user_without_password
