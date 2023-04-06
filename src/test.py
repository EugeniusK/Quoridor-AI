from Quoridor.log import Game
from datetime import datetime
import json
import os
import random

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


def compare_moves(number_games):
    total_moves = 0
    valid_moves = 0

    rounds = []
    valid = []
    difference_available = []
    for i in range(1, number_games + 1):
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
            if set(g_bitboard.available_moves()) == set(g_graph.available_moves()):
                total_moves += 1
                valid_moves += 1
                valid.append(True)
                move = random.choice(g_bitboard.available_moves())
                g_bitboard.make_move(move)
                g_graph.make_move(move)

                difference_available.append([])
            else:
                total_moves += 1
                valid.append(False)
                # g_bitboard.display()
                # g_graph.display()
                difference_available.append(
                    sorted(
                        list(
                            set(g_bitboard.available_moves())
                            ^ set(g_graph.available_moves())
                        )
                    )
                )
                move = random.choice(
                    list(
                        set(g_bitboard.available_moves())
                        & set(g_graph.available_moves())
                    )
                )
                g_bitboard.make_move(move)
                g_graph.make_move(move)

            if g_bitboard.is_over() and g_graph.is_over():
                over = True
        rounds.append(
            {
                "Round": g_bitboard.round,
                "Valid": valid,
                "Number moves": g_bitboard.number_moves,
                "Moves": " ".join(g_bitboard.moves),
                "Different available moves": difference_available,
            }
        )

        print(
            f"Total moves made: {total_moves}\nNumber of times different moves available: {valid_moves}"
        )
    with open(
        f'{os.path.join(os.path.dirname(__file__), "Logs/")}{datetime.strftime(datetime.today(), "%Y-%m-%d_%H%M%S")}_compare_moves.json',
        mode="w",
        encoding="ascii",
    ) as f:
        json.dump(rounds, f)
