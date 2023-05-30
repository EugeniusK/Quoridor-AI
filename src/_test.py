from Quoridor.game import Game
from datetime import datetime
import random
from multiprocessing import Pool
import numpy as np
import time
import sys

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
            # time.sleep(0.5)
            g.take_action(g.select(g.available_actions()))

        rounds.append(g.log())
        print(sum(g.generate_times))
    # with open(
    #     f'{os.path.join(os.path.dirname(__file__), "Logs/")}{datetime.strftime(datetime.today(), "%Y-%m-%d_%H%M%S")}_{player_one_mode}_vs_{player_two_mode}_as_{board_representation}.json',
    #     mode="w",
    #     encoding="ascii",
    # ) as f:
    #     json.dump(rounds, f)


def compare_moves(repeats, repr_1, repr_2, search_1, search_2):
    for repeat in range(repeats):
        total_moves = 0
        valid_moves = 0
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
            one_available_moves = np.array(g_one.available_actions())
            two_available_moves = np.array(g_two.available_actions())
            shared_action = g_one.select(one_available_moves & two_available_moves)

            if g_two.is_over() and g_one.is_over():
                over = True
                break
            elif g_two.is_over() or g_one.is_over():
                g_one.display()
                g_two.display()
                sys.exit()
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
                print(repr_2)
                g_two.display()
                print(
                    "Two unique: ", [x for x in two_algebraic if x not in one_algebraic]
                )
                print("Two: ", [x for x in two_algebraic if x])
                print(not np.array_equal(one_available_moves, two_available_moves))
                # raise KeyError
            g_one.take_action(shared_action)
            g_two.take_action(shared_action)
        print(repeat + 1, "over", g_one.is_over(), g_two.is_over())
        # g_one.display()


if __name__ == "__main__":
    compare_moves(10, "graph_optim", "bitboard_optim", "BFS", "BFS")
    compare_moves(10, "graph_optim", "bitboard_optim", "BFS", "DFS")
    compare_moves(10, "graph_optim", "bitboard_optim", "BFS", "GBFS")
    compare_moves(10, "graph_optim", "bitboard_optim", "BFS", "UCT")
    compare_moves(10, "graph_optim", "bitboard_optim", "BFS", "Astar")

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
