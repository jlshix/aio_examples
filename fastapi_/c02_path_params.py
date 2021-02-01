# coding: utf-8
# created by jlshix on 2021-02-01

"""https://fastapi.tiangolo.com/zh/tutorial/path-params/
"""
from enum import Enum

import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient

app = FastAPI()


class ModelName(Enum):
    """枚举模型名称, 类似于一个密封类
    可定义为 `class ModelName(str, Enum)` 继承 str 用于类型标注
    """
    alexnet = 'alexnet'
    resnet = 'resnet'
    lenet = 'lenet'


@app.get('/items/{item_id}')
async def read_item_without_annotation(item_id):
    """文档字符串编写的说明可以作为文档"""
    return {'item_id': item_id}


@app.post('/items/{item_id}')
async def read_item_with_annotations(item_id: int):
    return {'item_id': item_id}


@app.get("/users/me")
async def read_user_me():
    return {"user_id": "the current user"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


@app.get('/models/{model_name}')
async def get_model(model_name: ModelName):
    if model_name == ModelName.alexnet:
        return {'model_name': model_name, 'message': 'Deep Learning FTW!'}

    if model_name.value == 'lenet':
        return {'model_name': model_name, 'message': 'LeCNN all the images'}

    return {'model_name': model_name, 'message': 'Have some residuals'}


@app.get('/files/{file_path:path}')
async def read_file_path(file_path: str):
    """将 file_path 标记为 path, 允许包含 '/'"""
    return {'file_path': file_path}


@app.get('/not_path/{file_path}')
async def read_file(file_path: str):
    """不添加`:path` 标记则可能返回 `{'detail': 'Not Found'}`"""
    return {'file_path': file_path}


# --- 以下为基于 pytest 的单元测试


client = TestClient(app)


@pytest.mark.parametrize('item_id', ['3', 'foo'])
def test_without_annotation(item_id):
    """不使用类型注解时, 原样返回输入"""
    resp = client.get(f'items/{item_id}')
    assert resp.status_code == 200
    assert resp.json() == {'item_id': item_id}


def test_with_annotation_good():
    """使用类型注解时, 转换为对应类型"""
    resp = client.post(f'/items/3')
    assert resp.status_code == 200
    assert resp.json() == {'item_id': 3}


@pytest.mark.parametrize('item', ['foo', '3.14'])
def test_with_annotation_bad(item):
    """使用类型注解时, 转换失败返回 422"""
    resp = client.post(f'/items/{item}')
    # 422 Unprocessable Entity
    # ref: https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status/422
    assert resp.status_code == 422
    assert resp.json() == {
        'detail': [
            {
                'loc': ['path', 'item_id'],
                'msg': 'value is not a valid integer',
                'type': 'type_error.integer'
            }
        ]
    }


@pytest.mark.parametrize('user_in, user_out', [
    ('me', 'the current user'), ('someone', 'someone')
])
def test_read_user(user_in, user_out):
    """路由匹配时 '/users/me' 在 '/users/{user_id}' 前,
    因此 user_in 为 me 时, user_out 为 'the current user' 而不是 'me'
    """
    resp = client.get(f"/users/{user_in}")
    assert resp.json() == {'user_id': user_out}


def test_model_name():
    """ModelName 作为枚举类, 只允许传入允许的值"""
    m = ModelName('alexnet')
    assert m.value == 'alexnet'
    with pytest.raises(ValueError):
        ModelName('internet')


def test_get_model():
    """传入允许的值时返回正确, 不正确的值就返回 422"""
    for item in ModelName:
        value = item.value
        resp = client.get(f'/models/{value}')
        assert resp.json()['model_name'] == value

    resp = client.get(f'/models/internet')
    assert resp.status_code == 422
    assert resp.json() == {
        'detail': [
            {
                'loc': ['path', 'model_name'],
                'msg': "value is not a valid enumeration member; permitted: 'alexnet', 'resnet', 'lenet'",
                'type': 'type_error.enum',
                'ctx': {'enum_values': ['alexnet', 'resnet', 'lenet']}
            }
        ]
    }


@pytest.mark.parametrize('path', [
    'a/b/c', '/a/b/c', '~/', 'a.txt'
])
def test_read_file_with_path(path):
    """指定为 ':path' 时兼容各种路径表示"""
    resp = client.get(f'/files/{path}')
    assert resp.status_code == 200
    assert resp.json() == {'file_path': path}


def test_read_file_without_path():
    """不指定为 path 的各种情况"""
    # 正常返回
    path = 'a.txt'
    resp = client.get(f'not_path/{path}')
    assert resp.status_code == 200
    assert resp.json() == {'file_path': path}

    # 找不到路径
    for path in ('a/b/c', '/a/b/c'):
        resp = client.get(f'not_path/{path}')
        assert resp.status_code == 404
        assert resp.json() == {'detail': 'Not Found'}

    # 去掉了结尾的 '/'
    path = '~/'
    resp = client.get(f'not_path/{path}')
    assert resp.status_code == 200
    assert resp.json() == {'file_path': '~'}
