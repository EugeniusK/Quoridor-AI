from Quoridor.game import Game
from datetime import datetime
import random
from multiprocessing import Pool
import numpy as np
import time
import sys
import os
import json
import csv
from datetime import datetime, timezone

# ensure that a move made in one implementation is also valid in other
random.seed(0)


def action_to_algebra(action_number):
    if action_number < 64:
        return f"{chr(97+action_number%8)}{action_number//8+1}h"
    elif action_number < 128:
        return f"{chr(97+action_number%8)}{(action_number%64)//8+1}v"
    elif action_number < 140:
        return ["N", "E", "S", "W", "NN", "NE", "EE", "SE", "SS", "SW", "WW", "NW"][
            action_number % 128
        ]


def simulate(
    number_games,
    player_one_mode,
    player_two_mode,
    board_representation,
    path_finding_mode,
):
    print()
    print(path_finding_mode)
    rounds = []
    for i in range(1, number_games + 1):
        g = Game(
            round=i,
            player_one=player_one_mode,
            player_two=player_two_mode,
            representation=board_representation,
            path_finding_mode=path_finding_mode,
        )
        while g.is_over() == False:
            g.take_action(g.select(g.available_actions()))
        rounds.append(g.log())
        print(sum(g.generate_times))
    with open(
        f'{os.path.join(os.path.dirname(__file__), "Logs/")}{datetime.strftime(datetime.today(), "%Y-%m-%d_%H%M%S")}_{player_one_mode}_vs_{player_two_mode}_as_{board_representation}.json',
        mode="w",
        encoding="ascii",
    ) as f:
        json.dump(rounds, f)


def compare_moves(repeats, repr_1, repr_2, search_1, search_2):
    total_moves = 0
    valid_moves = 0
    for repeat in range(repeats):
        # print(repeat)
        two_error = 0
        one_error = 0

        valid = []
        difference_available = []

        g_two = Game(
            round=repeat + 1, representation=repr_2, path_finding_mode=search_2
        )
        g_one = Game(
            round=repeat + 1, representation=repr_1, path_finding_mode=search_1
        )
        over = False
        while not over:
            if g_two.is_over() and g_one.is_over():
                over = True
                break
            one_available_moves = np.array(g_one.available_actions())
            two_available_moves = np.array(g_two.available_actions())
            shared_action = g_one.select(one_available_moves & two_available_moves)
            # print(one_available_moves, two_available_moves)

            if not np.array_equal(one_available_moves, two_available_moves):
                one_algebraic = [
                    action_to_algebra(move)
                    for move in range(140)
                    if one_available_moves[move]
                ]
                two_algebraic = [
                    action_to_algebra(move)
                    for move in range(140)
                    if two_available_moves[move]
                ]
                print("Turn: ", g_one.board.turn)
                print(repr_1)
                g_one.display()
                print(
                    "One unique: ", [x for x in one_algebraic if x not in two_algebraic]
                )
                print("One: ", [x for x in one_algebraic])
                print("One actions taken", g_one.board.actions_taken)
                print(repr_2)
                g_two.display()
                print(
                    "Two unique: ", [x for x in two_algebraic if x not in one_algebraic]
                )
                print("Two: ", [x for x in two_algebraic if x])
                print("Two actions taken", g_two.board.actions_taken)
                print(not np.array_equal(one_available_moves, two_available_moves))
                raise IndexError
            else:
                valid_moves += 1
            g_one.take_action(int(shared_action))
            g_two.take_action(int(shared_action))
            total_moves += 1

    print("Repeat", repeats, repr_1, repr_2, search_1, search_2)
    print(f"Valid moves {valid_moves}/{total_moves}")


def load_test(args):
    print(args[1]["Round"])
    # Times taken for each wall count in current repetition
    times_repeat = []
    for repeat in range(args[2]):
        start = time.time()
        bitboard_BFS = Game(representation="bitboard_optim", path_finding_mode="BFS")
        bitboard_DFS = Game(representation="bitboard_optim", path_finding_mode="DFS")
        bitboard_GBFS = Game(representation="bitboard_optim", path_finding_mode="GBFS")
        bitboard_UCT = Game(representation="bitboard_optim", path_finding_mode="UCT")
        bitboard_Astar = Game(
            representation="bitboard_optim", path_finding_mode="Astar"
        )

        graph_BFS = Game(representation="graph_optim", path_finding_mode="BFS")
        graph_DFS = Game(representation="graph_optim", path_finding_mode="DFS")
        graph_GBFS = Game(representation="graph_optim", path_finding_mode="GBFS")
        graph_UCT = Game(representation="graph_optim", path_finding_mode="UCT")
        graph_Astar = Game(representation="graph_optim", path_finding_mode="Astar")
        for idx, action in enumerate(args[1]["Actions"].split(" ")):
            b_start_BFS = time.perf_counter()
            bitboard_BFS.available_actions()
            b_end_BFS = time.perf_counter()
            b_start_DFS = time.perf_counter()
            bitboard_DFS.available_actions()
            b_end_DFS = time.perf_counter()
            b_start_GBFS = time.perf_counter()
            bitboard_GBFS.available_actions()
            b_end_GBFS = time.perf_counter()
            b_start_UCT = time.perf_counter()
            bitboard_UCT.available_actions()
            b_end_UCT = time.perf_counter()
            b_start_Astar = time.perf_counter()
            bitboard_Astar.available_actions()
            b_end_Astar = time.perf_counter()

            g_start_BFS = time.perf_counter()
            graph_BFS.available_actions()
            g_end_BFS = time.perf_counter()
            g_start_DFS = time.perf_counter()
            graph_DFS.available_actions()
            g_end_DFS = time.perf_counter()
            g_start_GBFS = time.perf_counter()
            graph_GBFS.available_actions()
            g_end_GBFS = time.perf_counter()
            g_start_UCT = time.perf_counter()
            graph_UCT.available_actions()
            g_end_UCT = time.perf_counter()
            g_start_Astar = time.perf_counter()
            graph_Astar.available_actions()
            g_end_Astar = time.perf_counter()
            times_repeat.append(
                [
                    args[0],
                    args[1]["Walls placed"].split(" ")[idx],
                    round(b_end_BFS - b_start_BFS, 8),
                    round(b_end_DFS - b_start_DFS, 8),
                    round(b_end_GBFS - b_start_GBFS, 8),
                    round(b_end_UCT - b_start_UCT, 8),
                    round(b_end_Astar - b_start_Astar, 8),
                    round(g_end_BFS - g_start_BFS, 8),
                    round(g_end_DFS - g_start_DFS, 8),
                    round(g_end_GBFS - g_start_GBFS, 8),
                    round(g_end_UCT - g_start_UCT, 8),
                    round(g_end_Astar - g_start_Astar, 8),
                ]
            )
            graph_BFS.take_action(int(action))
            graph_DFS.take_action(int(action))
            graph_GBFS.take_action(int(action))
            graph_UCT.take_action(int(action))
            graph_Astar.take_action(int(action))
            bitboard_BFS.take_action(int(action))
            bitboard_DFS.take_action(int(action))
            bitboard_GBFS.take_action(int(action))
            bitboard_UCT.take_action(int(action))
            bitboard_Astar.take_action(int(action))
        print(time.time() - start, args[1]["Round"], repeat)
    return times_repeat


def load_test_threaded(file_name, repeats, games):
    f = open(f'{os.path.join(os.path.dirname(__file__), "Logs/")}{file_name}')
    data = json.load(f)
    args = [(x + 1, data[x], repeats) for x in range(games)]
    with Pool() as pool:
        times = pool.imap_unordered(load_test, args)
        results_file = open(
            os.path.join(
                os.path.dirname(__file__),
                "Results",
                f"performance test {repeats}-{games}-{datetime.strftime(datetime.today(), '%Y-%m-%d_%H%M%S')}.csv",
            ),
            "w",
            newline="",
        )

        # using csv.writer method from CSV package
        write = csv.writer(results_file)

        fields = [
            "Game",
            "Walls",
            "bBFS",
            "bDFS",
            "bGBFS",
            "bUCT",
            "bA*",
            "gBFS",
            "gDFS",
            "gGBFS",
            "gUCT",
            "gA*",
        ]
        write.writerow(fields)
        for one_game_data in times:
            for one_action_data in one_game_data:
                write.writerow(one_action_data)
        results_file.close()
        f.close()


if __name__ == "__main__":
    # compare_moves(100, "graph_optim", "bitboard_optim", "BFS", "BFS")
    # compare_moves(100, "graph_optim", "bitboard_optim", "BFS", "DFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "Astar", "BFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "Astar", "DFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "Astar", "GBFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "Astar", "UCT")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "Astar", "Astar")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "BFS", "BFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "BFS", "DFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "BFS", "GBFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "BFS", "UCT")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "BFS", "Astar")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "DFS", "BFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "DFS", "DFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "DFS", "GBFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "DFS", "UCT")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "DFS", "Astar")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "GBFS", "BFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "GBFS", "DFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "GBFS", "GBFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "GBFS", "UCT")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "GBFS", "Astar")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "UCT", "BFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "UCT", "DFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "UCT", "GBFS")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "UCT", "UCT")
    # compare_moves(1000, "graph_optim", "bitboard_optim", "UCT", "Astar")

    # compare_moves(100, "graph_optim", "bitboard_optim", "BFS", "UCT")
    # compare_moves(100, "graph_optim", "bitboard_optim", "BFS", "Astar")
    # compare_moves(100, "graph", "bitboard_optim", "BFS", "BFS")
    # compare_moves(100, "graph", "bitboard_optim", "BFS", "DFS")
    # compare_moves(100, "graph", "bitboard_optim", "GBFS", "BFS")
    # compare_moves(100, "graph", "bitboard_optim", "BFS", "UCT")
    # compare_moves(100, "graph", "bitboard_optim", "BFS", "Astar")
    simulate(10, "random", "random", "graph_optim", "BFS")
    # simulate(10, "random", "random", "graph_optim", "DFS")
    # simulate(10, "random", "random", "graph_optim", "GBFS")
    # simulate(10, "random", "random", "graph_optim", "UCT")
    # simulate(10, "random", "random", "graph_optim", "Astar")
    simulate(10, "random", "random", "graph", "BFS")
    # simulate(10, "random", "random", "graph", "DFS")
    # simulate(10, "random", "random", "graph", "GBFS")
    # simulate(10, "random", "random", "graph", "UCT")
    # simulate(10, "random", "random", "graph", "Astar")
    # simulate(10, "random", "random", "bitboard", "BFS")
    # simulate(10, "random", "random", "bitboard", "DFS")
    # simulate(10, "random", "random", "bitboard", "GBFS")
    # simulate(10, "random", "random", "bitboard", "UCT")
    # simulate(10, "random", "random", "bitboard", "Astar")
    # simulate(10, "random", "random", "bitboard_optim", "BFS")
    # simulate(10, "random", "random", "bitboard_optim", "DFS")
    # simulate(10, "random", "random", "bitboard_optim", "GBFS")
    # simulate(10, "random", "random", "bitboard_optim", "UCT")
    # simulate(10, "random", "random", "bitboard_optim", "Astar")

    # simulate(10000, "random", "random", "graph_optim", "GBFS")

    # load_test_threaded(
    #     "2023-05-30_161034_random_vs_random_as_graph_optim.json",
    #     repeats=10,
    #     games=8,
    # )
