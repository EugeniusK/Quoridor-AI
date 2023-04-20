import numpy as np
from numba import njit


# print(shift(board.reshape((17 * 17)), -1, False))
# https://stackoverflow.com/questions/30399534/shift-elements-in-a-numpy-array
@njit(cache=True)
def roll_numba(
    arr,
    num,
):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = arr[-num:]
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = arr[:-num]
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result


@njit(cache=True)
def is_in_2d_numba(test_arr, arr):
    for i in range(len(arr)):
        if arr[i][0] == test_arr[0] and arr[i][1] == test_arr[1]:
            return True
    return False


if __name__ == "__main__":
    print(roll_numba(np.arange(9), -2))
    print("not supposed to be run")
    raise ImportError
