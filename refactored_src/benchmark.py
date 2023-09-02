from Py_Quoridor.vanilla_graph import (
    VanillaPythonStaticGraph,
    VanillaPythonDynamicGraph,
)
from Py_Quoridor.numpy_graph import NumpyPythonStaticGraph, NumpyPythonDynamicGraph
from Py_Quoridor.numba_graph import NumbaPythonStaticGraph, NumbaPythonDynamicGraph
import timeit
from Py_Quoridor.actions import is_action_available
from Py_Quoridor.display import output_to_cli


from Py_Quoridor.bitboard import QuoridorBitboardOptim

# board = QuoridorBitboardOptim("BFS")
# moves = board.get_available_actions()
# print([x for x in range(140) if moves[x]])


def test(pathfinding, get_available_actions=1, repeat=1):
    actions = [52, 20, 15, 0, 65, 82, 127, 62, 56, 32, 6, 38, 9]

    boards = [
        VanillaPythonDynamicGraph(pathfinding),
        VanillaPythonStaticGraph(pathfinding),
        NumpyPythonDynamicGraph(pathfinding),
        NumpyPythonStaticGraph(pathfinding),
        NumbaPythonDynamicGraph(pathfinding),
        NumbaPythonStaticGraph(pathfinding),
    ]
    for board in boards:
        for a in actions:
            board.take_action(a)

        print(str(type(board)))
        for n in range(repeat):
            print(
                timeit.timeit(
                    f"board.get_available_actions({get_available_actions})",
                    globals=locals(),
                    number=1,
                )
                * 1e6
            )


import random
import time


def compare(path1, path2, get1, get2, n=1):
    for i in range(n):
        board1 = VanillaPythonStaticGraph(path1)
        board2 = NumbaPythonDynamicGraph(path2)

        time_taken = 0
        moves_played = 0
        while True:
            start = time.perf_counter()
            moves1 = board1.get_available_actions(get1)
            moves2 = board2.get_available_actions()

            time_taken += time.perf_counter() - start
            moves1_ones = [
                x for x in range(140) if is_action_available(board1, x) != None
            ]
            moves2_ones = [
                x for x in range(140) if is_action_available(board2, x) != None
            ]
            if set(moves1) != set(moves2):
                print("ERROR", board1.turn)
                print(moves1)
                print(moves2)
                output_to_cli(board1)
                output_to_cli(board2)
                break
            elif set(moves1_ones) != set(moves1):
                print("ERROR ONES", board1.turn)
                output_to_cli(board2)
                print(moves1_ones, moves1)
                break
            elif set(moves1_ones) != set(moves2_ones):
                print("ERROR ONES ONLY", board1.turn)
                output_to_cli(board2)
                break
            else:
                move = random.choice(moves1)
                board1.take_action(move)
                board2.take_action(move)
                moves_played += 1

            if board1.is_over() or board2.is_over():
                if board1.is_over() and board2.is_over():
                    print("OVER")
                    print(time_taken, time_taken / moves_played)
                    break
                else:
                    print("OVER ERROR")
                    break


# test("BFS", 2)
# test("BFS", 2)
# print()
# test("DFS", 2)
# test("DFS", 2)


# compare("BFS", "BFS", 1, 1, 100)
# compare("BFS", "DFS", 1, 1, 100)

# board = NumbaPythonStaticGraph("GBFS")
# # print(is_action_available(board, 0))
# print(board.get_available_actions(1))
# board = VanillaPythonStaticGraph("GBFS")
# print(board.get_available_actions(1))

# print(board.get_available_actions(2))
# board = NumpyPythonStaticGraph("BFS")
# is_action_available(board, 0)

# test("GBFS")
test("BFS", 1, 1)
test("BFS", 2, 1)


board = VanillaPythonDynamicGraph()
# board.get_available_actions(2)
from Py_Quoridor.display import board_to_string

board.take_action(127)
print(board_to_string(board))
