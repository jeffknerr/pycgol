
# https://stackoverflow.com/questions/34824382/sharing-numpy-arrays-between-multiple-processes-without-inheritance

import numpy as np
from multiprocessing import shared_memory
import random
import time
import multiprocessing 


def update(mylist, start, stop):
    rand = random.randrange(20)
    print("start: %d   stop: %d    rand: %d" % (start,stop,rand))
    for i in range(start, stop):
        mylist[i] = mylist[i]*rand
        print("---> i: %d (start: %d, stop: %d)" % (i,start,stop))
        time.sleep(1)

def main():
    a = np.array([1,1,2,3,4,5,8,9,5,6,6,77,43])
    print(a, id(a))
    shm = shared_memory.SharedMemory(create=True, size=a.nbytes)
    b = np.ndarray(a.shape, dtype=a.dtype, buffer=shm.buf)
    b[:] = a[:]
    b[-1] = 888
    print(b, id(b))
    print(shm.name)

    start = 0
    stop = int(len(b)/2)
    p1 = multiprocessing.Process(target=update, args=(b,start,stop))
    start = stop
    stop = len(b)
    p2 = multiprocessing.Process(target=update, args=(b,start,stop))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    print("-"*40)
    print(shm.name)
    print(b, id(b))
    print(a, id(a))

    shm.close()
    shm.unlink()

main()
