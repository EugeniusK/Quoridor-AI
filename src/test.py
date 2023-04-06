from Quoridor.log import Game
from datetime import datetime
import json
import os
import random
from multiprocessing import Pool

# ensure that a move made in one implementation is also valid in other
random.seed(0)


def simulate(number_games, player_one_mode, player_two_mode, board_representation):
    rounds = []
    for i in range(1, number_games + 1):
        g = Game(
            round=i,
            player_one=player_one_mode,
            player_two=player_two_mode,
            representation=board_representation,
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


def compare_moves(i):
    total_moves = 0
    valid_moves = 0

    valid = []
    difference_available = []

    g_bitboard = Game(
        round=i,
        representation="bitboard",
    )
    g_graph = Game(
        round=i,
        representation="graph",
    )
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
            g_bitboard.make_move(move)
            g_graph.make_move(move)

        if g_bitboard.is_over() and g_graph.is_over():
            over = True
    one_round = {
        "Round": i,
        "Valid": valid,
        "Number moves": g_bitboard.number_moves,
        "Moves": " ".join(g_bitboard.moves),
        "Different available moves": difference_available,
    }

    return one_round, total_moves, valid_moves


def compare_moves_threaded(number_games):
    rounds = list(range(1, number_games + 1))
    with Pool() as pool:
        results = pool.imap_unordered(compare_moves, rounds)

        logs = []

        num_total_moves = 0
        num_valid_moves = 0
        for one_round, total_moves, valid_moves in results:
            num_total_moves += total_moves
            num_valid_moves += valid_moves
            logs.append(one_round)
        print(
            f"Number of moves made: {num_total_moves}\nNumber of moves without error: {num_valid_moves}"
        )
        with open(
            f'{os.path.join(os.path.dirname(__file__), "Logs/")}{datetime.strftime(datetime.today(), "%Y-%m-%d_%H%M%S")}_compare_moves.json',
            mode="w",
            encoding="ascii",
        ) as f:
            json.dump(logs, f)


if __name__ == "__main__":
    # simulate(1000)
    compare_moves_threaded(1000)