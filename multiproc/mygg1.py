#https://www.geeksforgeeks.org/multiprocessing-python-set-2/

import multiprocessing
import time
import random

def square_list(mylist, result, square_sum, start, stop):
    """
    function to square a given list
    """
    # append squares of mylist to result array
    for idx, num in enumerate(mylist):
        if random.random() > 0.6:
            time.sleep(0.1)
        if idx < stop and idx >= start:
            result[idx] = num * num

    # square_sum value
    square_sum.value = sum(result)

    # print result Array
    print("Result(in process px): {}".format(result[:]))

    # print square_sum Value
    print("Sum of squares(in process px): {}".format(square_sum.value))
    print("-"*20)

if __name__ == "__main__":
    # input list
    N = 1000
    mylist = list(range(N))

    # creating Array of int data type with space for 4 integers
    result = multiprocessing.Array('i', len(mylist))

    # creating Value of int data type
    square_sum = multiprocessing.Value('i')

    # creating new process
    start = 0
    stop = int(len(mylist)/2)
    p1 = multiprocessing.Process(target=square_list, args=(mylist, result, square_sum, start, stop))
    start = stop
    stop = len(mylist)
    p2 = multiprocessing.Process(target=square_list, args=(mylist, result, square_sum, start, stop))

    # starting process
    p1.start()
    p2.start()

    # wait until the process is finished
    p1.join()
    p2.join()

    # print result array
    print("Result(in main program): {}".format(result[:]))

    # print square_sum Value
    print("Sum of squares(in main program): {}".format(square_sum.value))

