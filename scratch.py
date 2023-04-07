from extractor import *

from timer import Timer

my_timer = Timer()

print(get_brick(1))

my_timer.start()
my_range = range(1, 19900)
get_threaded(my_range, n_threads=2,
             file_name="export.json")  # 11.7 requests/sec. || 0.75 Mbit/s || ca. 5.75 requests/sec. per thread
time = my_timer.stop()
print("requests/sec. = " + str((my_range.stop - my_range.start) / time))
