from Quoridor.g_optim import QuoridorGraphicalBoardOptim
from Quoridor.b_optim import QuoridorBitboardOptim
from AI.mcts import roll_out, MCTS_NODE
import time
import os, csv
from datetime import datetime


from Quoridor.g_optim import QuoridorGraphicalBoardOptim
from AI.mcts import roll_out, MCTS_NODE
import time, copy


f = open(
    os.path.join(
        os.path.dirname(__file__),
        "Results",
        f"mcts 10 repeats to 500 {datetime.strftime(datetime.today(), '%Y-%m-%d_%H%M%S')}.csv",
    ),
    "w",
    newline="",
)
write = csv.writer(f)
fields = ["representation", "path finding mode", "rollouts", "time"]
data = []

# Graphical board
for mode in ["BFS", "DFS", "GBFS", "UCT", "Astar"]:
    root = MCTS_NODE(QuoridorGraphicalBoardOptim(mode))
    start = time.perf_counter()
    for i in range(500):
        roll_out(root)
        if i % 10 == 0 and i != 0:
            data.append(["g", mode, i, round(time.perf_counter() - start, 5)])
    print(
        [
            (c.games_won, c.games_played)
            for c in sorted(root.children, key=lambda x: x.games_played)
        ]
    )


# Bitboard
for mode in ["BFS", "DFS", "GBFS", "UCT", "Astar"]:
    root = MCTS_NODE(QuoridorBitboardOptim(mode))
    start = time.perf_counter()
    for i in range(500):
        roll_out(root)
        if i % 10 == 0 and i != 0:
            data.append(["b", mode, i, round(time.perf_counter() - start, 5)])
    print(
        [
            (c.games_won, c.games_played)
            for c in sorted(root.children, key=lambda x: x.games_played)
        ]
    )
write.writerow(fields)
write.writerows(data)
