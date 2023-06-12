import numpy as np
from numba import njit
from timeit import timeit

# @njit(cache=True)


# function used in b_pathfinding_optim
def path_shift_bitboard(bitboard, shift):
    # right is positive shift EAST
    """
    Shift the bitboard by shift
    while ensuring that bits outside of the 17x17 are not set
    """
    if shift < 64 and shift > 0:
        rshift = np.uint64(shift)
        lshift = np.uint64(64 - shift)
        copy_bitboard = (bitboard >> rshift) + (np.roll(bitboard, 1) << lshift)
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        if bitboard[0] == 0:
            copy_bitboard[0] = 0
    elif shift < 0 and shift > -64:
        rshift = np.uint64(64 + shift)
        lshift = np.uint64(-shift)
        copy_bitboard = (bitboard << lshift) + (np.roll(bitboard, -1) >> rshift)
        if bitboard[4] == 0:
            copy_bitboard[4] = 0
    return copy_bitboard


# function used in b_optim
# @njit(cache=True)
def board_shift_bitboard(init_bitboard, shift):
    # right is positive shift EAST
    """
    Shift the bitboard by shift
    while ensuring that bits outside of the 17x17 are not set
    """
    bitboard = np.copy(init_bitboard)
    if shift < 128 and shift > 64:
        copy_bitboard = np.roll(bitboard, 1)
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        if bitboard[0] == 0:
            copy_bitboard[0] = 0
        rshift = np.uint64(shift - 64)
        lshift = np.uint64(128 - shift)
        copy_bitboard = (copy_bitboard >> rshift) + (
            np.roll(copy_bitboard, 1) << lshift
        )
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        # if bitboard[1] == 0:
        #     copy_bitboard[1] = 0
    elif shift == 64:
        copy_bitboard = np.roll(bitboard, 1)
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        if bitboard[0] == 0:
            copy_bitboard[0] = 0
    elif shift < 64 and shift > 0:
        rshift = np.uint64(shift)
        lshift = np.uint64(64 - shift)
        copy_bitboard = (bitboard >> rshift) + (np.roll(bitboard, 1) << lshift)
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        if bitboard[0] == 0:
            copy_bitboard[0] = 0
    elif shift < 0 and shift > -64:
        rshift = np.uint64(64 + shift)
        lshift = np.uint64(-shift)
        copy_bitboard = (bitboard << lshift) + (np.roll(bitboard, -1) >> rshift)
        if bitboard[4] == 0:
            copy_bitboard[4] = 0
    elif shift == -64:
        copy_bitboard = np.roll(bitboard, -1)
        if bitboard[4] == 0:
            copy_bitboard[4] = 0
    elif shift < -64 and shift > -128:
        copy_bitboard = np.roll(bitboard, -1)
        if bitboard[4] == 0:
            copy_bitboard[4] = 0
        rshift = np.uint64(64 + shift)
        lshift = np.uint64(-shift)
        copy_bitboard = (copy_bitboard << lshift) + (
            np.roll(copy_bitboard, -1) >> rshift
        )
        # if bitboard[4] == 0:
        #     copy_bitboard[4] = 0

    return copy_bitboard


# @profile
def shift_bitboard(init_bitboard, shift):
    bitboard = np.copy(init_bitboard)
    copy_bitboard = np.zeros(5, dtype=np.uint64)
    rolled_bitboard = np.zeros(5, dtype=np.uint64)
    rolled_again_bitboard = np.zeros(5, dtype=np.uint64)

    if shift > 64:
        rolled_bitboard[1:5] = bitboard[0:4]
        rshift = np.uint64(shift - 64)
        lshift = np.uint64(128 - shift)
        rolled_again_bitboard[1:5] = rolled_bitboard[0:4]
        copy_bitboard = (rolled_bitboard >> rshift) + (rolled_again_bitboard << lshift)
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        if init_bitboard[0] == 0:
            copy_bitboard[0] == 0
    elif shift == 64:
        copy_bitboard[1:5] = bitboard[0:4]
    elif shift < 64 and shift > 0:
        rolled_bitboard[1:5] = bitboard[0:4]
        rshift = np.uint64(shift)
        lshift = np.uint64(64 - shift)
        copy_bitboard = (bitboard >> rshift) + (rolled_bitboard << lshift)
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        if bitboard[0] == 0:
            copy_bitboard[0] = 0
    elif shift < 0 and shift > -64:
        rolled_bitboard[0:4] = bitboard[1:5]
        rshift = np.uint64(64 + shift)
        lshift = np.uint64(-shift)
        copy_bitboard = (bitboard << lshift) + (rolled_bitboard >> rshift)
        if init_bitboard[4] == 0:
            copy_bitboard[4] = 0
    elif shift == -64:
        copy_bitboard[0:4] = bitboard[1:5]
    elif shift < -64:
        rolled_bitboard[0:4] = bitboard[1:5]
        rshift = np.uint64(128 + shift)
        lshift = np.uint64(-64 - shift)
        rolled_again_bitboard[0:4] = rolled_bitboard[1:5]
        copy_bitboard = (rolled_bitboard << lshift) + (rolled_again_bitboard >> rshift)
        if init_bitboard[4] == 0:
            copy_bitboard[4] = 0
    return copy_bitboard


def test(func, input, shift, output):
    if np.array_equal(func(input, shift), output):
        return True, func(input, shift)
    else:
        return False, func(input, shift)


def test_suite(func):
    times_taken = dict()
    inputs = [
        np.array([0, 0, 0, 0, 2**31], dtype=np.uint64),
        np.array([0, 0, 0, 0, 2**31], dtype=np.uint64),
        np.array([0, 0, 0, 0, 2**31], dtype=np.uint64),
        np.array([0, 0, 0, 0, 2**31], dtype=np.uint64),
        np.array([0, 0, 0, 0, 2**31], dtype=np.uint64),
        np.array([0, 0, 0, 0, 2**31], dtype=np.uint64),
        np.array([0, 0, 0, 0, 2**31], dtype=np.uint64),
        np.array([0, 0, 0, 0, 2**31], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**59, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 0, 2**0, 0, 0], dtype=np.uint64),
        np.array([0, 0, 2**0, 0, 0], dtype=np.uint64),
        np.array([0, 0, 2**59, 0, 0], dtype=np.uint64),
        np.array([0, 0, 2**0, 0, 0], dtype=np.uint64),
        np.array([0, 0, 2**0, 0, 0], dtype=np.uint64),
        np.array([0, 0, 2**0, 0, 0], dtype=np.uint64),
        np.array([0, 0, 2**0, 0, 0], dtype=np.uint64),
        np.array([0, 0, 2**0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
    ]
    outputs = [
        np.array([0, 0, 0, 0, 0], dtype=np.uint64),  # 1 extreme right
        np.array([0, 0, 0, 0, 0], dtype=np.uint64),  # 64 extreme right
        np.array([0, 0, 0, 0, 0], dtype=np.uint64),  # 68 extreme right
        np.array([0, 0, 0, 0, 0], dtype=np.uint64),  # 127 extreme right
        np.array([0, 0, 0, 0, 2**32], dtype=np.uint64),  # -1 extreme right
        np.array([0, 0, 0, 2**31, 0], dtype=np.uint64),  # -64 extreme right
        np.array([0, 0, 0, 2**35, 0], dtype=np.uint64),  # -68 extreme right
        np.array([0, 0, 2**30, 0, 0], dtype=np.uint64),  # -127 extreme right
        np.array([0, 2**1, 0, 0, 0], dtype=np.uint64),  # -1 from 2nd
        np.array([2**0, 0, 0, 0, 0], dtype=np.uint64),  # -64 from 2nd
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),  # -68 from 2nd
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),  # -127 from 2nd
        np.array([0, 0, 2**63, 0, 0], dtype=np.uint64),  # 1 from 2nd
        np.array([0, 0, 2**0, 0, 0], dtype=np.uint64),  # 64 from 2nd
        np.array([0, 0, 0, 2**60, 0], dtype=np.uint64),  # 68 from 2nd
        np.array([0, 0, 0, 2**1, 0], dtype=np.uint64),  # 127 from 2nd
        np.array([0, 0, 2**1, 0, 0], dtype=np.uint64),  # -1 from 3rd
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),  # -64 from 3rd
        np.array([0, 2**63, 0, 0, 0], dtype=np.uint64),  # -68 from 3rd
        np.array([0, 2**63, 0, 0, 0], dtype=np.uint64),  # -127 from 3rd
        np.array([0, 0, 0, 2**63, 0], dtype=np.uint64),  # 1 from 3rd
        np.array([0, 0, 0, 2**0, 0], dtype=np.uint64),  # 64 from 3rd
        np.array([0, 0, 0, 0, 2**60], dtype=np.uint64),  # 68 from 3rd
        np.array([0, 0, 0, 0, 0], dtype=np.uint64),  # 127 from 3rd
        np.array([0, 0, 0, 0, 0], dtype=np.uint64),  # -1 extreme left
        np.array([0, 0, 0, 0, 0], dtype=np.uint64),  # -64 extreme left
        np.array([0, 0, 0, 0, 0], dtype=np.uint64),  # -68 extreme left
        np.array([0, 0, 0, 0, 0], dtype=np.uint64),  # -127 extreme left
        np.array([2**62, 0, 0, 0, 0], dtype=np.uint64),  # 1 extreme left
        np.array([0, 2**63, 0, 0, 0], dtype=np.uint64),  # 64 extreme left
        np.array([0, 2**59, 0, 0, 0], dtype=np.uint64),  # 68 extreme left
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),  # 127 extreme left
    ]
    shifts = [
        1,
        64,
        68,
        127,
        -1,
        -64,
        -68,
        -127,
        -1,
        -64,
        -68,
        -127,
        1,
        64,
        68,
        127,
        -1,
        -64,
        -68,
        -127,
        1,
        64,
        68,
        127,
        -1,
        -64,
        -68,
        -127,
        1,
        64,
        68,
        127,
    ]
    shift_bitboard(inputs[0], shifts[0])
    fail = False

    for io in zip(inputs, shifts, outputs):
        time_taken = timeit(
            "test(func, io[0], io[1], io[2])",
            globals=globals() | locals(),
            number=10000,
        )
        result = test(func, io[0], io[1], io[2])
        if times_taken.get(io[1]) == None:
            times_taken[io[1]] = time_taken
        else:
            times_taken[io[1]] += time_taken
        if result[0] == False:
            fail = True
            print(
                func.__name__,
                False,
                "shift:",
                io[1],
                "result:",
                result[1],
                "time:",
                time_taken,
            )
        else:
            pass
            # print(func.__name__, True, "shift:", io[1], "time:", time_taken)

    if fail == True:
        print(
            func.__name__,
            False,
        )
    else:
        print(func.__name__, True)
    for key, value in times_taken.items():
        print(str(key).rjust(5), str(round(value, 4)).ljust(9))


test_suite(shift_bitboard)


arr = np.array([1, 2, 3], dtype=np.uint64)
