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
                pass
                # one_algebraic = [
                #     action_to_algebra(move)
                #     for move in range(140)
                #     if one_available_moves[move]
                # ]
                # two_algebraic = [
                #     action_to_algebra(move)
                #     for move in range(140)
                #     if two_available_moves[move]
                # ]
                # print("Turn: ", g_one.board.turn)
                # print(repr_1)
                # g_one.display()
                # print(
                #     "One unique: ", [x for x in one_algebraic if x not in two_algebraic]
                # )
                # print("One: ", [x for x in one_algebraic])
                # print("One actions taken", g_one.board.actions_taken)
                # print(repr_2)
                # g_two.display()
                # print(
                #     "Two unique: ", [x for x in two_algebraic if x not in one_algebraic]
                # )
                # print("Two: ", [x for x in two_algebraic if x])
                # print("Two actions taken", g_two.board.actions_taken)
                # print(not np.array_equal(one_available_moves, two_available_moves))
            else:
                valid_moves += 1
            g_one.take_action(int(shared_action))
            g_two.take_action(int(shared_action))
            total_moves += 1

    print("Repeat", repeats, repr_1, repr_2, search_1, search_2)
    print(f"Valid moves {valid_moves}/{total_moves}")


def load_test(file_name, repeats=1, games=100):
    error_count = 0
    f = open(f'{os.path.join(os.path.dirname(__file__), "Logs/")}{file_name}')
    data = json.load(f)

    times = []

    for round, simulation in enumerate(data[0:games]):
        print("Game ", round + 1)

        # Stores [walls placed, BFS1, DFS1, ..., Astar2]
        tmp_bitboard = []
        tmp_graph = []

        # Array for times taken by all 5 path finding for ONE round
        for path_finding_mode in ["BFS", "DFS", "GBFS", "UCT", "Astar"]:
            # Arrays for times taken for ONE path finding
            # records
            # -----------------------
            # walls placed, mean time
            # walls placed, mean time
            # -----------------------
            bitboard_time_path_finding = []
            graph_board_time_path_finding = []
            for r in range(repeats):
                bitboard = Game(
                    representation="bitboard_optim", path_finding_mode=path_finding_mode
                )
                graph_board = Game(
                    representation="graph_optim", path_finding_mode=path_finding_mode
                )
                for idx, move in enumerate(simulation["Actions"].split(" ")):
                    start_bitboard = time.perf_counter()
                    bitboard_available = bitboard.available_actions()
                    end_bitboard = time.perf_counter()

                    start_graph_board = time.perf_counter()
                    graph_board_available = graph_board.available_actions()
                    end_graph_board = time.perf_counter()
                    if (
                        not bitboard_available[int(move)]
                        or not graph_board_available[int(move)]
                    ):
                        error_count += 1
                    if r == 0:
                        bitboard_time_path_finding.append(
                            [bitboard.walls_placed[-1], end_bitboard - start_bitboard]
                        )
                        graph_board_time_path_finding.append(
                            [
                                graph_board.walls_placed[-1],
                                end_graph_board - start_graph_board,
                            ]
                        )
                    else:
                        bitboard_time_path_finding[idx][1] += (
                            end_bitboard - start_bitboard
                        )
                        graph_board_time_path_finding[idx][1] += (
                            end_graph_board - start_graph_board
                        )

                    bitboard.take_action(int(move))
                    graph_board.take_action(int(move))
            for i in range(len(bitboard_time_path_finding)):
                bitboard_time_path_finding[i][1] /= repeats
            for i in range(len(graph_board_time_path_finding)):
                graph_board_time_path_finding[i][1] /= repeats

            tmp_bitboard.append(bitboard_time_path_finding)
            tmp_graph.append(graph_board_time_path_finding)

        for row in range(len(tmp_bitboard[0])):
            tmp_row = [tmp_bitboard[0][row][0]]
            tmp_row.extend([tmp_bitboard[x][row][1] for x in range(5)])
            tmp_row.extend([tmp_graph[x][row][1] for x in range(5)])
            times.append(tmp_row)

    results_file = open(
        f'{os.path.join(os.path.dirname(__file__), "Results", f"bg_optim {repeats}-{games}.csv")}',
        "w",
    )

    # using csv.writer method from CSV package
    write = csv.writer(results_file)

    fields = [
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
    write.writerows(times)

    results_file.close()
    f.close()


if __name__ == "__main__":
    # compare_moves(100, "graph_optim", "bitboard_optim", "BFS", "BFS")
    # compare_moves(100, "graph_optim", "bitboard_optim", "BFS", "DFS")
    # compare_moves(100, "graph_optim", "bitboard_optim", "GBFS", "BFS")
    # compare_moves(100, "graph_optim", "bitboard_optim", "BFS", "UCT")
    # compare_moves(100, "graph_optim", "bitboard_optim", "BFS", "Astar")
    # compare_moves(100, "graph", "bitboard_optim", "BFS", "BFS")
    # compare_moves(100, "graph", "bitboard_optim", "BFS", "DFS")
    # compare_moves(100, "graph", "bitboard_optim", "GBFS", "BFS")
    # compare_moves(100, "graph", "bitboard_optim", "BFS", "UCT")
    # compare_moves(100, "graph", "bitboard_optim", "BFS", "Astar")
    # simulate(10, "random", "random", "graph_optim", "BFS")
    # simulate(10, "random", "random", "graph_optim", "DFS")
    # simulate(10, "random", "random", "graph_optim", "GBFS")
    # simulate(10, "random", "random", "graph_optim", "UCT")
    # simulate(10, "random", "random", "graph_optim", "Astar")
    # simulate(10, "random", "random", "graph", "BFS")
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

    load_test(
        "2023-05-30_161034_random_vs_random_as_graph_optim.json", repeats=100, games=5
    )
