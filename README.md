# Mecabricks-conversion-matrix-extractor

* Extract conversion matrices for mecabricks using the api
  at [www.mecabricks.com/api/part-manager/parts/get](https://www.mecabricks.com/api/part-manager/parts/get)

### Feel free to test my code!

## Getting Started

### Dependencies

* [Python >= 3.7](https://www.python.org/downloads/)
* python requests

### Installing

* ```pip install requests```
* download `extractor.py` and `timer.py` to your local directory

### Example script

```python
from extractor import *

from timer import Timer

my_timer = Timer()

print(get_brick(1))

my_timer.start()
my_range = range(1, 19900)

get_threaded(my_range, n_threads=2,
             file_name="export.json")  # 11.7 requests/sec. || 0.75 Mbit/s || ca. 5.75 requests/sec. per thread
# this will create 2 files => 1_export.json, 2_export.json

time = my_timer.stop()
print("requests/sec. = " + str((my_range.stop - my_range.start) / time))
```

## Help

Please feel free to open an issue or fork!

## Todo

## Deprecated

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

I am not responsible what you use the code for!!! Also no warranty!

## Acknowledgments

Inspiration, code snippets, etc.

* [Timer](https://www.nickmccullum.com/python-timer-functions-performance-measurement/)
