# https://stackoverflow.com/questions/65199943/python-multiprocessing-when-share-a-numpy-array


import numpy as np
import multiprocessing

from multiprocessing import RawArray, Array


def initpool(arr):
    global array
    array = arr

def change_array(i, j):
    X_np = np.frombuffer(array.get_obj(), dtype=np.float64).reshape(2, 3)
    X_np[i, j] = 100
    print(np.frombuffer(array.get_obj()))

if __name__ == '__main__':
    X_shape = (2, 3)
    data = np.array([[1.1, 2.2, 3.3], [4.4, 5.5, 6.6]])
    print("="*30)
    print(data)  
    X = multiprocessing.Array('d', X_shape[0] * X_shape[1], lock=True)
    # Wrap X as an numpy array so we can easily manipulates its data.
    X_np = np.frombuffer(X.get_obj()).reshape(X_shape)
    # Copy data to our shared array.
    np.copyto(X_np, data)
    print("-"*30)
    print(X_np)  
    print("-"*30)

    pool = multiprocessing.Pool(processes=3, initializer=initpool, initargs=(X,))

    result = []
    for i in range(2):
        for j in range(3):
            result.append(pool.apply_async(change_array, (i, j,)))

    result = [r.get() for r in result]
    pool.close()
    pool.join()

    print(np.frombuffer(X.get_obj()).reshape(2, 3))

    print(X)
    print("data:")
    print(data)
    print("X_np:")
    print(X_np)  # <-- this is the updated array
