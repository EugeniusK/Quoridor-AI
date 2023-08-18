from Quoridor.g_optim import QuoridorGraphicalBoardOptim
from Quoridor.b_optim import QuoridorBitboardOptim
import csv, os, sys, time
from datetime import datetime
import AI.mcts as old_mcts
import AI.new_mcts as new_mcts

ROLLOUTS = 1000


f = open(
    os.path.join(
        os.path.dirname(__file__),
        "Results",
        f"mcts {ROLLOUTS} rollouts MCTS {datetime.strftime(datetime.today(), '%Y-%m-%d_%H%M%S')}.csv",
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

all_data = []


# # Graph
for mode in ["BFS", "DFS", "GBFS", "UCT", "Astar"]:
    data = []
    print("graph", mode)
    root = old_mcts.MCTS_NODE(QuoridorGraphicalBoardOptim(mode))
    start = time.perf_counter()
    for i in range(ROLLOUTS + 1):
        old_mcts.roll_out(root)
        if i % 10 == 0 and i != 0:
            data.append(
                [
                    "old",
                    "g",
                    mode,
                    i,
                    round(time.perf_counter() - start, 5),
                    sys.getsizeof(root) / 1e6,
                ]
            )
        if i % 200 == 0:
            print(i)
    all_data.extend(data)
write.writerows(all_data)
all_data = []

# # Bitboard
for mode in ["BFS", "DFS", "GBFS", "UCT", "Astar"]:
    data = []
    print("bitboard", mode)
    root = old_mcts.MCTS_NODE(QuoridorBitboardOptim(mode))
    start = time.perf_counter()
    for i in range(ROLLOUTS + 1):
        old_mcts.roll_out(root)
        if i % 10 == 0 and i != 0:
            data.append(
                [
                    "old",
                    "b",
                    mode,
                    i,
                    round(time.perf_counter() - start, 5),
                    sys.getsizeof(root) / 1e6,
                ]
            )
        if i % 200 == 0:
            print(i)
    all_data.extend(data)
write.writerows(all_data)
all_data = []


# # Graph
for mode in ["BFS", "DFS", "GBFS", "UCT", "Astar"]:
    data = []
    print("graph", mode)
    root = new_mcts.MCTS_NODE(QuoridorGraphicalBoardOptim(mode))
    start = time.perf_counter()
    for i in range(ROLLOUTS + 1):
        new_mcts.roll_out(root)
        if i % 10 == 0 and i != 0:
            data.append(
                [
                    "new",
                    "g",
                    mode,
                    i,
                    round(time.perf_counter() - start, 5),
                    sys.getsizeof(root) / 1e6,
                ]
            )
        if i % 200 == 0:
            print(i)
    all_data.extend(data)
write.writerows(all_data)
all_data = []

# Bitboard
for mode in ["BFS", "DFS", "GBFS", "UCT", "Astar"]:
    data = []
    print("bitboard", mode)
    root = new_mcts.MCTS_NODE(QuoridorBitboardOptim(mode))
    start = time.perf_counter()
    for i in range(ROLLOUTS + 1):
        new_mcts.roll_out(root)
        if i % 10 == 0 and i != 0:
            data.append(
                [
                    "new",
                    "b",
                    mode,
                    i,
                    round(time.perf_counter() - start, 5),
                    sys.getsizeof(root) / 1e6,
                ]
            )
        if i % 200 == 0:
            print(i)
    all_data.extend(data)

write.writerows(all_data)
f.close()
