# coding: utf-8
# created by jlshix on 2021-03-15

"""https://fastapi.tiangolo.com/zh/tutorial/extra-data-types/

支持的数据类型除之前提到的 int, float, str, bool 之外, 还可以支持更复杂的, 如:
`UUID`, `datetime`, `date`, `timedelta`, `frozenset`, `bytes`, `Decimal` 等.

参见页面上的简单说明, 若要查看 Pydantic 支持的所有数据类型, 参见:
https://pydantic-docs.helpmanual.io/usage/types

"""

from datetime import datetime, time, timedelta
from typing import Optional
from uuid import UUID

from fastapi import Body, FastAPI

app = FastAPI()


@app.put("/items/{item_id}")
async def read_items(
    item_id: UUID,
    start_datetime: Optional[datetime] = Body(None),
    end_datetime: Optional[datetime] = Body(None),
    repeat_at: Optional[time] = Body(None),
    process_after: Optional[timedelta] = Body(None),
):
    start_process = start_datetime + process_after
    duration = end_datetime - start_process
    return {
        "item_id": item_id,
        "start_datetime": start_datetime,
        "end_datetime": end_datetime,
        "repeat_at": repeat_at,
        "process_after": process_after,
        "start_process": start_process,
        "duration": duration,
    }
