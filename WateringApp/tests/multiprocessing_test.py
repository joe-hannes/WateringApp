import time
import multiprocessing

import concurrent.futures

start = time.perf_counter()


def do_something():
    print(f'Sleeping {1} Second(s)...')
    time.sleep(1)
    return f'Done Sleeping...{1}'


p1 = multiprocessing.Process(target=do_something)
p2 = multiprocessing.Process(target=do_something)


p1.start()
p2.start()

p1.join()
p2.join()

finish = time.perf_counter()

print(f'finished in {round(finish-start, 2)} second(s)')
