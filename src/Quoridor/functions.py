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


@njit(cache=True)
def shift_bitboard(bitboard, shift):
    # right is positive shift EAST
    if shift > 0 and shift < 64:
        rshift = np.uint64(shift)
        lshift = np.uint64(64 - shift)
        copy_bitboard = (bitboard >> rshift) + (np.roll(bitboard, 1) << lshift)
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
    elif shift < 0 and shift > -64:
        rshift = np.uint64(64 + shift)
        lshift = np.uint64(-shift)
        copy_bitboard = (bitboard << lshift) + (np.roll(bitboard, -1) >> rshift)
    return copy_bitboard
