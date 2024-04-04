import asyncio
import json

from extractor import get_bricks
import time


async def main():
    start = time.perf_counter()
    _range = range(1, 19900)
    bricks = await get_bricks(_range, max_conn=3, lang="en", scope="official")
    print("requests/sec. = " + str(
        (_range.stop - _range.start) /
        (time.perf_counter() - start)
    ))
    with open("file.json", "w+") as f:
        f.write(json.dumps(bricks))


asyncio.run(main())
