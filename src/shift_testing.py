import numpy as np
from numba import njit


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


def shift_bitboard(init_bitboard, shift):
    bitboard = np.copy(init_bitboard)
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


def test(func, input, shift, output):
    if np.array_equal(func(input, shift), output):
        return True, func(input, shift)
    else:
        return False, func(input, shift)


def test_suite(func):
    inputs = [
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
    ]
    outputs = [
        np.array([2**62, 0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**63, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**59, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**0, 0, 0, 0], dtype=np.uint64),
        np.array([0, 2**1, 0, 0, 0], dtype=np.uint64),
        np.array([2**0, 0, 0, 0, 0], dtype=np.uint64),
        np.array([2**63, 0, 0, 0, 0], dtype=np.uint64),
    ]
    shifts = [1, 64, 68, 127, -1, -64, -127]
    for io in zip(inputs, shifts, outputs):
        if test(func, io[0], io[1], io[2])[0] == False:
            print(
                func.__name__,
                False,
                "shift:",
                io[1],
                "result:",
                test(func, io[0], io[1], io[2])[1],
            )
            return -1
    print(func.__name__, True)
    return -1


test_suite(board_shift_bitboard)
