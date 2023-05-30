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


from _AI.mcts import MCTS_NODE, select, expand, simulate, backpropagate
from Quoridor.b_optim import QuoridorBitboardOptim
from Quoridor.g_optim import QuoridorGraphicalBoardOptim
import time

board = QuoridorGraphicalBoardOptim("GBFS")
root = MCTS_NODE(board)
import sys


def roll_out(root):
    path = select(root)
    leaf = path[-1]
    child = expand(leaf)
    reward = simulate(child.state, child.state.turn)
    backpropagate(path + [child], reward)


import timeit

start = time.perf_counter()
for i in range(500):
    roll_out(root)
print(time.perf_counter() - start)
print(
    [
        (c.games_won, c.games_played)
        for c in sorted(root.children, key=lambda x: x.games_played)
    ]
)
# print(timeit.timeit(code, globals=globals(), number=1))
