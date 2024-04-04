import asyncio
import json
import traceback
import warnings

import aiohttp


class IPBannedException(Exception):
    pass


async def get_brick(my_id: int, lang: str = "en", scope: str = "official", max_retries=5, retrie_timeout=0.5, lock=asyncio.Lock()):
    headers = {
        'authority': 'www.mecabricks.com',
        'accept': '*/*',
        'accept-language': lang + ',en-US;q=0.9,de-DE;q=0.8,de;q=0.7',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'origin': 'https://www.mecabricks.com',
        'referer': 'https://www.mecabricks.com/' + lang + '/partmanager',
        'sec-ch-ua': '"Google Chrome";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'scope': scope,
        'id': str(my_id),
        'lang': lang,
    }
    async with aiohttp.ClientSession() as s:
        resp = await s.post('https://www.mecabricks.com/api/part-manager/parts/get', headers=headers, data=data)
    if resp.status != 200:
        if resp.status == 429:
            raise IPBannedException()
        print(await resp.text(encoding="utf-8"))
        raise AssertionError(f"got status of {resp.status}")
    try:
        return json.loads(await resp.text(encoding="utf-8"))
    except aiohttp.ContentTypeError as e:
        print(await resp.text())
        raise e
    except (aiohttp.ClientConnectorError,aiohttp.ClientOSError) as e:
        if max_retries == 1:
            raise e
        async with lock:
            await asyncio.sleep(retrie_timeout)
        return get_brick(my_id, lang, scope, max_retries - 1)


# noinspection PyUnresolvedReferences
def parse_brick(content: object):
    if content["status"] == "pass":
        brick_number = content['data']['part']['references']['mecabricks']
        my_id = content['data']['part']['id']
        if "d" in brick_number:  # Guard Clause
            print(brick_number + ":" + str(my_id) + " d in it:)")
            return None
        name = content['data']['part']['names']['english']
        if content['data']['part']['ldraw']['convertible']:
            coordinates = content['data']['part']['ldraw']['transform']
        else:
            coordinates = {'position': [0, 0, 0], 'rotation': [0, 0, 0]}

        res = {brick_number: {"id": my_id, "name": name, "coordinates": coordinates,
                              "c": content['data']['part']['ldraw']['convertible']}}
    else:
        print(content)
        res = None
    return res


async def get_bricks(my_range: range, max_conn=1000, lang: str = "en", scope: str = "official", max_retries=5,
                     retrie_timeout=0.5):
    sema = asyncio.Semaphore(max_conn)
    lock = asyncio.Lock()

    async def get_brick_helper(_id):
        async with sema as _:
            try:
                return await get_brick(_id, lang=lang, scope=scope, max_retries=max_retries,
                                       retrie_timeout=retrie_timeout, lock=lock)
            except (AssertionError, aiohttp.ClientConnectorError,aiohttp.ClientOSError):
                traceback.print_exc()

    coro = []
    for _id in my_range:
        coro.append(get_brick_helper(_id))
    return await asyncio.gather(*coro)


async def search_brick(query: str, page: int = 1, lang: str = "en", hidden: bool = True,
                       scope: str = 'official'):
    headers = {
        'authority': 'www.mecabricks.com',
        'accept': '*/*',
        'accept-language': 'de,de-DE;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6,fr;q=0.5,de-CH;q=0.4,es;q=0.3',
        'cache-control': 'no-cache',
        'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
        'dnt': '1',
        'origin': 'https://www.mecabricks.com',
        'pragma': 'no-cache',
        'referer': 'https://www.mecabricks.com/' + lang + '/partmanager',
        'sec-ch-ua': '"Microsoft Edge";v="111", "Not(A:Brand";v="8", "Chromium";v="111"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/111.0.0.0 Safari/537.36 Edg/111.0.1661.44',
        'x-requested-with': 'XMLHttpRequest',
    }

    data = {
        'scope': scope,
        'query': query,
        'page': int(page),
        'hidden': json.dumps(hidden),
        'lang': lang,
    }
    async with aiohttp.ClientSession() as s:
        resp = await s.post('https://www.mecabricks.com/api/part-manager/parts/search',
                            headers=headers, data=data)
    return json.loads(await resp.text(encoding="utf-8"))


async def brick_by_number(number: str):
    search = await search_brick(number)
    item_len = len(search["data"]["items"])
    if search["status"] == "pass":
        if item_len < 1:
            raise LookupError("Number not found: " + number)
        elif item_len == 1:
            return search["data"]["items"][0]
        elif item_len > 1:
            warnings.warn(
                "Got " + str(item_len) + " items for query: " + number + ", returning first one.")
            return search["data"]["items"][0]
