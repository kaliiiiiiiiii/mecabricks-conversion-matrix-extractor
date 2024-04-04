# Mecabricks-conversion-matrix-extractor

* Extract conversion matrices for mecabricks using the api
  at [www.mecabricks.com/api/part-manager/parts/get](https://www.mecabricks.com/api/part-manager/parts/get)

### Feel free to test my code!

## Getting Started

### Dependencies

* [Python >= 3.7](https://www.python.org/downloads/)
* python requests

### Installing

* ```pip install aiohttp```
* download `extractor.py` to your local directory

### Example script

```python
import asyncio
import json

from extractor import get_bricks
import time


async def main():
    start = time.perf_counter()
    _range = range(1, 19900)
    bricks = await get_bricks(_range, max_conn=100, lang="en", scope="official")
    print("requests/sec. = " + str(
        (_range.stop - _range.start) /
        (time.perf_counter() - start)
    ))
    with open("file.json") as f:
        f.write(json.dumps(bricks))


asyncio.run(main())
```

## Help

Please feel free to open an issue or fork!

## Authors

[Aurin Aegerter](mailto:aurinliun@gmx.ch)

## License

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

This work is licensed under a
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa].

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/

[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png

[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg

## Disclaimer

I am not responsible for what you use the code for!!! Also no warranty!

