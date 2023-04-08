from Quoridor.log import Game
from datetime import datetime
import json
import os
import random
from multiprocessing import Pool

# ensure that a move made in one implementation is also valid in other
random.seed(0)


def simulate(
    number_games, player_one_mode, player_two_mode, board_representation, search_mode
):
    rounds = []
    for i in range(1, number_games + 1):
        g = Game(
            round=i,
            player_one=player_one_mode,
            player_two=player_two_mode,
            representation=board_representation,
            search_mode=search_mode,
        )
        while g.is_over() == False:
            g.make_move(g.select(g.available_moves()))
            # g.display()

        rounds.append(g.log())
        print(g.log()["Total time"])
    with open(
        f'{os.path.join(os.path.dirname(__file__), "Logs/")}{datetime.strftime(datetime.today(), "%Y-%m-%d_%H%M%S")}_{player_one_mode}_vs_{player_two_mode}_as_{board_representation}.json',
        mode="w",
        encoding="ascii",
    ) as f:
        json.dump(rounds, f)


def compare_moves(args):
    i = args[0]
    repr_1 = args[1]
    repr_2 = args[2]
    search_1 = args[3]
    search_2 = args[3]
    print(i)
    total_moves = 0
    valid_moves = 0
    bitboard_error = 0
    graph_error = 0

    valid = []
    difference_available = []

    g_bitboard = Game(round=i, representation=repr_1, search_mode=search_1)
    g_graph = Game(round=i, representation=repr_2, search_mode=search_2)
    over = False
    while over == False:
        bitboard_available_moves = g_bitboard.available_moves()
        graph_available_moves = g_graph.available_moves()
        if set(bitboard_available_moves) == set(graph_available_moves):
            total_moves += 1
            valid_moves += 1
            valid.append(True)
            move = random.choice(bitboard_available_moves)
            g_bitboard.make_move(move)
            g_graph.make_move(move)

            difference_available.append([])
        else:
            total_moves += 1
            valid.append(False)
            difference_available.append(
                sorted(list(set(bitboard_available_moves) ^ set(graph_available_moves)))
            )
            move = random.choice(
                list(set(bitboard_available_moves) & set(graph_available_moves))
            )

            if (set(bitboard_available_moves) ^ set(graph_available_moves)) & set(
                bitboard_available_moves
            ) != set():
                bitboard_error += len(
                    (set(bitboard_available_moves) ^ set(graph_available_moves))
                    & set(bitboard_available_moves)
                )
            if (set(bitboard_available_moves) ^ set(graph_available_moves)) & set(
                graph_available_moves
            ) != set():
                graph_error += len(
                    (set(bitboard_available_moves) ^ set(graph_available_moves))
                    & set(graph_available_moves)
                )

            g_bitboard.display()

            # print("Bitboard moves available", sorted(bitboard_available_moves))
            # print("Graph moves available", sorted(graph_available_moves))
            print(
                "Bitboard moves available unique",
                sorted(
                    list(
                        (set(bitboard_available_moves) ^ set(graph_available_moves))
                        & set(bitboard_available_moves)
                    )
                ),
            )
            print(
                "Graph moves available unique",
                sorted(
                    list(
                        (set(bitboard_available_moves) ^ set(graph_available_moves))
                        & set(graph_available_moves)
                    )
                ),
            )
            # print(g_graph.board.nodes)
            g_graph.make_move(move)
            g_bitboard.make_move(move)

        if g_bitboard.is_over() and g_graph.is_over():
            over = True
    one_round = {
        "Round": i,
        "Valid": valid,
        "Number moves": g_bitboard.number_moves,
        "Moves": " ".join(g_bitboard.moves),
        "Different available moves": difference_available,
    }

    return one_round, total_moves, valid_moves, graph_error, bitboard_error


def compare_moves_threaded(number_games, repr_1, repr_2, search_1, search_2):
    rounds = list(range(1, number_games + 1))
    args = [(x + 1, repr_1, repr_2, search_1, search_2) for x in range(number_games)]

    with Pool(processes=16) as pool:
        results = pool.imap_unordered(compare_moves, args)

        logs = []

        num_total_moves = 0
        num_valid_moves = 0
        num_graph_errors = 0
        num_bitboard_errors = 0
        for one_round, total_moves, valid_moves, graph_error, bitboard_error in results:
            num_total_moves += total_moves
            num_valid_moves += valid_moves
            num_graph_errors += graph_error
            num_bitboard_errors += bitboard_error
            logs.append(one_round)
        print(
            f"Number of moves made: {num_total_moves}\nNumber of moves without error: {num_valid_moves}"
        )
        print(
            f"Bitboard errors: {num_bitboard_errors}\nGraph errors: {num_graph_errors}"
        )
        with open(
            f'{os.path.join(os.path.dirname(__file__), "Logs/")}{datetime.strftime(datetime.today(), "%Y-%m-%d_%H%M%S")}_compare_moves.json',
            mode="w",
            encoding="ascii",
        ) as f:
            json.dump(logs, f)


if __name__ == "__main__":
    # simulate(10, "random", "random", "bitboard", "UCT")
    import time

    start = time.perf_counter()
    compare_moves_threaded(4, "bitboard", "graph", "BFS", "Astar")
    print(time.perf_counter() - start)
