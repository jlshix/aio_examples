# coding: utf-8
# created by jlshix on 2021-01-28

"""hello world
ref: https://docs.python.org/zh-cn/3/library/asyncio.html
"""

import asyncio


async def main():
    print('Hello ...')
    await asyncio.sleep(1)
    print('... World!')


if __name__ == '__main__':
    asyncio.run(main())
