from Quoridor.g_optim import QuoridorGraphicalBoardOptim
from Quoridor.b_optim import QuoridorBitboardOptim
import csv, os, sys, time
from datetime import datetime


ROLLOUTS = 500
MODE = "new"
if MODE == "old":
    from AI.mcts import roll_out, choose, MCTS_NODE
elif MODE == "new":
    from AI.new_mcts import roll_out, choose, MCTS_NODE


f = open(
    os.path.join(
        os.path.dirname(__file__),
        "Results",
        f"mcts 10 repeats to {ROLLOUTS} {MODE} MCTS {datetime.strftime(datetime.today(), '%Y-%m-%d_%H%M%S')}.csv",
    ),
    "w",
    newline="",
)
write = csv.writer(f)
fields = [
    "mcts type",
    "representation",
    "path finding mode",
    "rollouts",
    "time (s)",
    "memory (MB)",
]
write.writerow(fields)

# # # Graphical board
# for mode in ["BFS", "DFS", "GBFS", "UCT", "Astar"]:
#     print("graph", mode)
#     root = MCTS_NODE(QuoridorGraphicalBoardOptim(mode))
#     start = time.perf_counter()
#     for i in range(ROLLOUTS + 1):
#         roll_out(root)
#         if i % 10 == 0 and i != 0:
#             write.writerow(
#                 [
#                     MODE,
#                     "g",
#                     mode,
#                     i,
#                     round(time.perf_counter() - start, 5),
#                     sys.getsizeof(root) / 1e6,
#                 ]
#             )


# Bitboard
for mode in ["BFS", "DFS", "GBFS", "UCT", "Astar"]:
    print("bitboard", mode)
    root = MCTS_NODE(QuoridorBitboardOptim(mode))
    start = time.perf_counter()
    for i in range(ROLLOUTS + 1):
        roll_out(root)
        if i % 10 == 0 and i != 0:
            print(i)
            write.writerow(
                [
                    MODE,
                    "b",
                    mode,
                    i,
                    round(time.perf_counter() - start, 5),
                    sys.getsizeof(root) / 1e6,
                ]
            )

f.close()
