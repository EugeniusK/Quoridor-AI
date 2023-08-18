# import timeit
# import numpy as np
# from numba import njit

# bitboard = np.array([0, 0, 0, 0, 2**39], dtype=np.uint64)
# zeros = np.zeros(5, dtype=np.uint64)


# @njit(cache=True)
# def check1(bitboard):
#     return np.array_equal(bitboard, zeros)


# @njit(cache=True)
# def check2(bitboard):
#     return np.sum(bitboard) == 0


# @njit(cache=True)
# def check3(bitboard):
#     return not np.any(bitboard)


# print(timeit.timeit("check1(bitboard)", globals=globals()) / 1e6)
# print(timeit.timeit("check2(bitboard)", globals=globals()) / 1e6)
# print(timeit.timeit("check3(bitboard)", globals=globals()) / 1e6)


# def display(bitboard):
#     line = "".join([np.binary_repr(x, 64) for x in bitboard])
#     for i in range(0, 17):
#         print(line[i * 17 : i * 17 + 17])
#     print()


# a = np.array(
#     [
#         9223301667573723135,
#         17870278923326062335,
#         18410715001810583535,
#         18444492256715866110,
#         18446603336221196287,
#     ],
#     dtype=np.uint64,
# )
# display(a)


# from _AI.mcts import MCTS_NODE, select, expand, simulate, backpropagate
# from Quoridor.b_optim import QuoridorBitboardOptim
# from Quoridor.g_optim import QuoridorGraphicalBoardOptim
# import time

# board = QuoridorGraphicalBoardOptim("GBFS")
# root = MCTS_NODE(board)
# import sys


# def roll_out(root):
#     path = select(root)
#     leaf = path[-1]
#     child = expand(leaf)
#     reward = simulate(child.state, child.state.turn)
#     backpropagate(path + [child], reward)


# import timeit

# start = time.perf_counter()
# for i in range(500):
#     roll_out(root)
# print(time.perf_counter() - start)
# print(
#     [
#         (c.games_won, c.games_played)
#         for c in sorted(root.children, key=lambda x: x.games_played)
#     ]
# )
# print(timeit.timeit(code, globals=globals(), number=1))


from Quoridor.b_optim import QuoridorBitboardOptim
from Quoridor.g_optim import QuoridorGraphicalBoardOptim

# # for i in range(128, 140):
# #     print(i)

# #     board = QuoridorBitboardOptim("BFS")
# #     if board.get_available_actions()[i]:
# #         board.take_action(i)
# #         board.display_beautiful()
# import numpy as np

board = QuoridorBitboardOptim("BFS")
for action in [
    111,
    90,
    1,
    29,
    60,
    70,
    100,
    121,
    15,
    96,
    99,
    63,
    21,
    7,
    123,
    45,
    25,
    112,
    43,
    97,
    131,
    129,
    129,
    129,
    131,
    129,
    128,
    131,
    129,
    131,
    128,
    129,
    129,
    130,
    129,
    128,
    129,
    130,
    128,
    131,
    129,
    129,
    128,
    128,
    130,
    129,
    128,
    129,
    128,
    131,
    130,
    129,
    131,
    131,
    128,
    131,
    128,
    129,
    131,
    131,
    128,
    136,
]:
    board.take_action(action)
    print(action)
    board.display_beautiful()

# import numpy as np
# from numba import njit

# p1 = np.array([0, 0, 0, 0, 2**39], dtype=np.uint64)


# def ashift_bitboard(init_bitboard, init_shift):
#     # right is positive shift EAST
#     """
#     Shift the bitboard by shift
#     while ensuring that bits outside of the 17x17 are not set
#     """
#     shift = np.int8(init_shift)
#     bitboard = np.copy(init_bitboard)
#     if shift < 128 and shift > 64:
#         copy_bitboard = shift_bitboard(shift_bitboard(bitboard, 64), shift - 64)
#     if shift < 64 and shift > 0:
#         rshift = np.uint64(shift)
#         lshift = np.uint64(64 - shift)
#         copy_bitboard = (bitboard >> rshift) + (np.roll(bitboard, 1) << lshift)
#         copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
#         if bitboard[0] == 0:
#             copy_bitboard[0] = 0
#     elif shift == 64:
#         copy_bitboard = np.roll(bitboard, 1)
#         copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
#         if bitboard[0] == 0:
#             copy_bitboard[0] = 0
#     elif shift < 0 and shift > -64:
#         rshift = np.uint64(64 + shift)
#         lshift = np.uint64(-shift)
#         copy_bitboard = (bitboard << lshift) + (np.roll(bitboard, -1) >> rshift)
#         if bitboard[4] == 0:
#             copy_bitboard[4] = 0
#     elif shift == -64:
#         copy_bitboard = np.roll(bitboard, -1)
#         if bitboard[4] == 0:
#             copy_bitboard[4] = 0
#     elif shift < -64 and shift > -128:
#         copy_bitboard = shift_bitboard(shift_bitboard(bitboard, -64), shift + 64)

#     return copy_bitboard


# @njit(cache=True)
# def shift_bitboard(init_bitboard, shift):
#     # right is positive shift EAST
#     """
#     Shift the bitboard by shift
#     while ensuring that bits outside of the 17x17 are not set
#     """
#     bitboard = np.copy(init_bitboard)
#     if shift < 128 and shift > 64:
#         copy_bitboard = np.roll(bitboard, 1)
#         copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
#         if bitboard[0] == 0:
#             copy_bitboard[0] = 0
#         rshift = np.uint64(shift)
#         lshift = np.uint64(64 - shift)
#         copy_bitboard = (bitboard >> rshift) + (np.roll(bitboard, 1) << lshift)
#         copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
#         if bitboard[0] == 0:
#             copy_bitboard[0] = 0
#     elif shift == 64:
#         copy_bitboard = np.roll(bitboard, 1)
#         copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
#         if bitboard[0] == 0:
#             copy_bitboard[0] = 0
#     elif shift < 64 and shift > 0:
#         rshift = np.uint64(shift)
#         lshift = np.uint64(64 - shift)
#         copy_bitboard = (bitboard >> rshift) + (np.roll(bitboard, 1) << lshift)
#         copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
#         if bitboard[0] == 0:
#             copy_bitboard[0] = 0
#     elif shift < 0 and shift > -64:
#         rshift = np.uint64(64 + shift)
#         lshift = np.uint64(-shift)
#         copy_bitboard = (bitboard << lshift) + (np.roll(bitboard, -1) >> rshift)
#         if bitboard[4] == 0:
#             copy_bitboard[4] = 0
#     elif shift == -64:
#         copy_bitboard = np.roll(bitboard, -1)
#         if bitboard[4] == 0:
#             copy_bitboard[4] = 0
#     elif shift < -64 and shift > -128:
#         copy_bitboard = np.roll(bitboard, -1)
#         if bitboard[4] == 0:
#             copy_bitboard[4] = 0
#         rshift = np.uint64(64 + shift)
#         lshift = np.uint64(-shift)
#         copy_bitboard = (bitboard << lshift) + (np.roll(bitboard, -1) >> rshift)
#         if bitboard[4] == 0:
#             copy_bitboard[4] = 0

#     return copy_bitboard


# import timeit

# print(timeit.timeit("ashift_bitboard(p1, 5)", globals=globals(), number=10000) / 10000)
# print(timeit.timeit("shift_bitboard(p1, 5)", globals=globals(), number=10000) / 10000)


for i in range(81):
    if 0 <= i < 9:
        print("elif bitboard[4] ==", 2 ** (i * 2 + 31), ":", sep="")
        print("    return", i)
    elif 9 <= i < 18:
        print("elif bitboard[3] ==", 2 ** (i * 2 - 17), ":", sep="")
        print("    return", i)
    elif 18 <= i < 27:
        print("elif bitboard[3] ==", 2 ** (i * 2 - 1), ":", sep="")
        print("    return", i)
    elif 27 <= i < 36:
        print("elif bitboard[2] ==", 2 ** (i * 2 - 49), ":", sep="")
        print("    return", i)
    elif 36 <= i < 45:
        print("elif bitboard[2] ==", 2 ** (i * 2 - 33), ":", sep="")
        print("    return", i)
    elif 45 <= i < 54:
        print("elif bitboard[1] ==", 2 ** (i * 2 - 81), ":", sep="")
        print("    return", i)
    elif 54 <= i < 63:
        print("elif bitboard[1] ==", 2 ** (i * 2 - 65), ":", sep="")
        print("    return", i)
    elif 63 <= i < 72:
        print("elif bitboard[0] ==", 2 ** (i * 2 - 113), ":", sep="")
        print("    return", i)
    elif 72 <= i < 81:
        print("elif bitboard[0] ==", 2 ** (i * 2 - 97), ":", sep="")
        print("    return", i)
