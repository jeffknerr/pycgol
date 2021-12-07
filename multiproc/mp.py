from multiprocessing import Pool
import time

COUNT = 500000000
def countdown(n):
    while n>0:
        n -= 1

if __name__ == '__main__':
    pool = Pool(processes=2)
    start = time.time()
    r1 = pool.apply_async(countdown, [COUNT//2])
    r2 = pool.apply_async(countdown, [COUNT//2])
    pool.close()
    pool.join()
    end = time.time()
    print('WITH Time taken in seconds -', end - start)

    # now without Pool
    start = time.time()
    countdown(COUNT)
    end = time.time()
    print('WITHOUT Time taken in seconds -', end - start)
