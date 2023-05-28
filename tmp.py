import timeit
import numpy as np
from numba import njit

bitboard = np.array([0, 0, 0, 0, 2**39], dtype=np.uint64)
zeros = np.zeros(5, dtype=np.uint64)


@njit(cache=True)
def check1(bitboard):
    return np.array_equal(bitboard, zeros)


@njit(cache=True)
def check2(bitboard):
    return np.sum(bitboard) == 0


@njit(cache=True)
def check3(bitboard):
    return not np.any(bitboard)


print(timeit.timeit("check1(bitboard)", globals=globals()) / 1e6)
print(timeit.timeit("check2(bitboard)", globals=globals()) / 1e6)
print(timeit.timeit("check3(bitboard)", globals=globals()) / 1e6)
