from Quoridor.vanilla_graph import GraphVanilla
from Quoridor.numpy_graph import GraphNumpy
import timeit


actions = [52, 20, 15, 0, 65, 82, 127, 62, 56, 32, 6, 38, 9]
board = GraphVanilla("DFS")
board.p1_pos = 58
board.p2_pos = 59
for a in actions:
    board.take_action(a)
board1 = GraphNumpy("DFS")
board1.p1_pos = 58
board1.p2_pos = 59
for a in actions:
    board1.take_action(a)
print(timeit.timeit("board.get_available_actions()", globals=globals(), number=1))
print(timeit.timeit("board1.get_available_actions()", globals=globals(), number=1))
# board = GraphVanilla("BFS")
# board.p1_pos = 58
# board.p2_pos = 59
# for a in actions:
#     board.take_action(a)
# board1 = GraphNumpy("BFS")
# board1.p1_pos = 58
# board1.p2_pos = 59
# for a in actions:
#     board1.take_action(a)
# print(timeit.timeit("board.get_available_actions()", globals=globals(), number=1))
# print(timeit.timeit("board1.get_available_actions()", globals=globals(), number=1))
