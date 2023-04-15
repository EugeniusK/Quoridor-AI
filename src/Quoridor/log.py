from .bitboard import QuoridorBitBoard
from .graph import QuoridorGraphicalBoard
from .graph_optimised import (
    QuoridorGraphicalBoardOptim,
    QuoridorGraphicalBoardMoreOptim,
)
from AI.base import random_select
import time
import random
import json
from datetime import datetime, timezone
import numpy as np

random.seed(0)

# logging system inspired by PGN logging for chess
# http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm

# tags for each game/round played
# Date
# Round
# Player 1 - algorithm used or human
# Player 2 - algorithm used or human
# Representation - how the board was represented - bitboard or graph
# Result - who won the game - 1 or 2
# Termination - was the game ended normally
# Number moves - number of moves played in total - combine both players
# Total time - total time to get available moves and choose
# Moves - record the moves made by players
# Times - record the time taken to get available moves and choose for each move made

# times taken to get available moves and choose recorded in order to compare performance of algrithms
# some algorithms may rely on trying out multiple possible moves before choosing


"""
Below will be stored as json file
[Datetime "yyyy-mm-ddT hh:mm:ss"]
[Round N]
[PlayerOne "XXXXXXXXX"]
[PlayerTwo "XXXXXXXXX"]
[Representation "XXXXXXXXX"]
[Result "N-N"]
[Termination "XXXXXXXXX"]
[TotalTime ss.ssssss]
[NumberMoves N]
[Notes ""]
[Moves "1. ___ timeForMove ___ timeForMove 2. ___ timeForMove ___ timeForMove ___ ... "]


each round will be stored with identifier of yyyy-mm-ddThh:mm:ss_PlayerOne_PlayerTwo_Representation
"""


class Game:
    def __init__(
        self,
        load=False,
        round=False,
        player_one="random",
        player_two="random",
        path_finding_mode="BFS",
        representation="graph",
        notes=False,
        round_data=None,
    ):
        if load == True:
            self.board = QuoridorGraphicalBoard()
            log = json.loads(round_data)
            print(log)
        else:
            self.date = datetime.now(tz=timezone.utc)
            self.round = round
            self.p1 = player_one
            self.p2 = player_two
            self.representation = representation
            self.result = None
            self.termination = None
            self.total_time = 0
            self.number_moves = 0
            self.notes = notes
            self.path_finding_mode = path_finding_mode

            if self.representation == "graph":
                self.board = QuoridorGraphicalBoard(path_finding_mode)
            elif self.representation == "bitboard":
                self.board = QuoridorBitBoard(path_finding_mode)
            elif self.representation == "graph_optim":
                self.board = QuoridorGraphicalBoardOptim(path_finding_mode)
            elif self.representation == "graph_optim_more":
                self.board = QuoridorGraphicalBoardMoreOptim()

        self.moves = []
        self.generate_times = []
        self.choose_times = []

        self.total_time = 0

    def available_moves(self):
        generate_start = time.perf_counter()
        moves = self.board.get_available_actions()
        # print(moves, type(self).__name__)
        generate_end = time.perf_counter()
        self.generate_times.append(round((generate_end - generate_start), 8))

        available_moves = []
        for move in moves:
            if self.representation == "graph":
                available_moves.append(move)
            elif (
                self.representation == "graph_optim"
                or self.representation == "graph_optim_more"
            ):
                available_moves.append(move)
            elif self.representation == "bitboard":
                if move[2] == 0:
                    available_moves.append(f"{chr(97 + move[1])}{move[0] + 1}h")
                elif move[2] == 1:
                    available_moves.append(f"{chr(97 + move[1])}{move[0] + 1}v")
                elif move[2] == 2:
                    available_moves.append(f"{chr(97 + move[1]//2)}{move[0]//2 + 1}")
        return available_moves

    def select(self, moves):
        if self.board.turn == False or self.board.turn == 1:
            mode = self.p1
        elif self.board.turn == True or self.board.turn == 2:
            mode = self.p2

        if mode == "random":
            choose_start = time.perf_counter()
            move = random_select(moves)
            choose_end = time.perf_counter()
            self.choose_times.append(round(choose_end - choose_start, 8))
        return move

    def make_move(self, move):
        if self.representation == "graph":
            self.moves.append(move)
            self.board.take_action(move)
        elif (
            self.representation == "graph_optim"
            or self.representation == "graph_optim_more"
        ):
            self.moves.append(move)
            self.board.take_action(move)
        elif self.representation == "bitboard":
            self.moves.append(move)
            if len(move) == 2:
                self.board.take_action(
                    np.array(
                        [(int(move[1]) - 1) * 2, (ord(move[0]) - 97) * 2, 2],
                        dtype=np.int8,
                    )
                )
            else:
                if move[2] == "h":
                    self.board.take_action(
                        np.array(
                            [int(move[1]) - 1, ord(move[0]) - 97, 0], dtype=np.int8
                        )
                    )
                elif move[2] == "v":
                    self.board.take_action(
                        np.array(
                            [int(move[1]) - 1, ord(move[0]) - 97, 1], dtype=np.int8
                        )
                    )
        else:
            print(self.representation)
            raise TypeError
        self.number_moves += 1

    def display(self):
        self.board.display_beautiful()

    def is_over(self):
        return self.board.is_over()

    def log(self):
        self.result = int(self.board.turn) + 1
        if self.is_over() == True:
            self.termination = "normal"
        else:
            if self.termination == None:
                self.termination = "abnormal"
        self.total_time = round(sum(self.generate_times) + sum(self.choose_times), 8)
        return {
            "Date": datetime.strftime(self.date, "%Y-%m-%d %H:%M:%S+%z"),
            "Round": self.round,
            "P1 mode": self.p1,
            "P2 mode": self.p2,
            "Path finding mode": self.path_finding_mode,
            "Representation": self.representation,
            "Result": self.result,
            "Termination": self.termination,
            "Number moves": self.number_moves,
            "Total time": self.total_time,
            "Notes": self.notes,
            "Moves": " ".join(self.moves),
            "Generate times": " ".join([str(x) for x in self.generate_times]),
            "Choose times": " ".join([str(x) for x in self.choose_times]),
        }


if __name__ == "__main__":
    print("not supposed to be run")
    raise ImportError
