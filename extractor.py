import json
import threading
import traceback
import warnings

import requests


def get_brick(my_id: int, proxy: dict = None, lang: str = "en", scope: str = "official"):
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
    if proxy:
        response = requests.post('https://www.mecabricks.com/api/part-manager/parts/get', headers=headers, data=data,
                                 proxies=proxy)
    else:
        response = requests.post('https://www.mecabricks.com/api/part-manager/parts/get', headers=headers, data=data)
    status_code = response.status_code
    try:
        content = json.loads(response.content.decode())
    except json.decoder.JSONDecodeError:
        # noinspection PyUnresolvedReferences
        input("Response status code was: " + str(
            status_code) + "\n" + response.content.decode() + "\n, press ENTER to continue\n")
        content = {"status": str(status_code)}
    finally:
        if status_code != 200:
            input("Response status code was: " + str(
                status_code) + "\n" + response.content.decode() + "\n, press ENTER to continue\n")
            content = {"status": str(status_code)}
    return content


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
        res = {}
    return res


def threaded_helper(my_range: range, thread_n: int = 0, proxy: dict = None,
                    file_name="export.json"):
    for i in my_range:
        res = get_brick(i + thread_n, proxy=proxy)
        parsed = parse_brick(res)
        if parsed:
            with open(str(thread_n) + "_" + file_name, "a") as my_file:
                my_file.write("," + json.dumps(parsed)[1:-1])


def get_threaded(my_range: range, proxy: dict = None, file_name="export.json", n_threads=2):
    threads = []
    for i in range(n_threads):
        thread = threading.Thread(target=threaded_helper, kwargs={
            "my_range": range(my_range.start, my_range.stop, n_threads),
            "thread_n": i,
            "proxy": proxy,
            "file_name": file_name
        })
        thread.start()
        threads.append(thread)
    for my_thread in threads:
        my_thread.join()


def get_bricks(my_range: range, proxy: dict = None, file_name="export.json"):
    for i in my_range:
        res = get_brick(i, proxy=proxy)
        parsed = parse_brick(res)
        if parsed:
            with open(file_name, "a") as my_file:
                my_file.write("," + json.dumps(parsed)[1:-1])


def search_brick(query: str, page: int = 1, proxy: dict = None, lang: str = "en", hidden: bool = True,
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
    if proxy:
        response = requests.post('https://www.mecabricks.com/api/part-manager/parts/search',
                                 headers=headers, data=data, proxies=proxy)
    else:
        response = requests.post('https://www.mecabricks.com/api/part-manager/parts/search',
                                 headers=headers, data=data)

    try:
        content = json.loads(response.content.decode())
    except json.decoder.JSONDecodeError:
        content = {"status": "failed_decode_json: Query='" + query + "'"}
        traceback.print_exc()
    return content


# noinspection PyTypeChecker
def brick_by_number(number: str, proxy: dict = None):
    search = search_brick(number, proxy=proxy)
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
