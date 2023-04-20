# Import game implementations
from .bitboard import QuoridorBitBoard
from .graph import QuoridorGraphicalBoard
from .graph_optimised import (
    QuoridorGraphicalBoardOptim,
    QuoridorGraphicalBoardMoreOptim,
)

# Import AI algorithms
from AI.base import random_select

# Import rest
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
        round=1,
        player_one="random",
        player_two="random",
        path_finding_mode="BFS",
        representation="graph",
        notes=False,
    ):
        if load == True:
            raise NotImplementedError
        elif load == False:
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
                self.board = QuoridorGraphicalBoardMoreOptim(path_finding_mode)
            else:
                raise ValueError

        # All moves made until game over
        self.actions = []
        # Times taken to generate available actions each turn
        self.generate_times = []
        # Times taken to choose each turn
        self.choose_times = []
        # Total time taken - generate and select
        self.total_time = 0

    def available_actions(self):
        """
        Gets an array of available actions for current move state
        in algebraic format like a1v, e9, d7h
        """
        # Get available actions and record time taken to generate
        generate_start = time.perf_counter()
        generated_actions = self.board.get_available_actions()
        generate_end = time.perf_counter()
        self.generate_times.append(round((generate_end - generate_start), 8))

        # Get available actions in algebraic notation
        available_actions = []
        # Bitboard, Graph (more) optimised returns available actions as ndarray
        # of [row, col, type]
        # where type 0 = horizontal wall
        #       type 1 = vertical wall
        #       type 2 = move
        for action in generated_actions:
            if self.representation == "graph":
                available_actions.append(action)
            elif (
                self.representation == "graph_optim"
                or self.representation == "graph_optim_more"
            ):
                if action[2] == 0 and action[0] != -1:
                    available_actions.append(f"{chr(97 + action[1])}{action[0] + 1}h")
                elif action[2] == 1 and action[0] != -1:
                    available_actions.append(f"{chr(97 + action[1])}{action[0] + 1}v")
                elif action[2] == 2 and action[0] != -1:
                    available_actions.append(f"{chr(97 + action[1])}{action[0] + 1}")

            elif self.representation == "bitboard":
                if action[2] == 0 and action[0] != -1:
                    available_actions.append(f"{chr(97 + action[1])}{action[0] + 1}h")
                elif action[2] == 1 and action[0] != -1:
                    available_actions.append(f"{chr(97 + action[1])}{action[0] + 1}v")
                elif action[2] == 2 and action[0] != -1:
                    available_actions.append(
                        f"{chr(97 + (action[1] // 2))}{(action[0]//2) + 1}"
                    )
        return available_actions

    def select(self, moves):
        """
        Randomly selects a move based on method defined on init
        """
        if self.board.turn == 1:
            mode = self.p1
        elif self.board.turn == 2:
            mode = self.p2

        if mode == "random":
            choose_start = time.perf_counter()
            move = random_select(moves)
            choose_end = time.perf_counter()
            self.choose_times.append(round(choose_end - choose_start, 8))
        return move

    def take_action(self, action):
        if self.representation == "graph":
            self.actions.append(action)
            self.board.take_action(action)
        elif (
            self.representation == "graph_optim"
            or self.representation == "graph_optim_more"
        ):
            self.actions.append(action)
            if len(action) == 2:
                self.board.take_action(
                    np.array(
                        [int(action[1]) - 1, ord(action[0]) - 97, 2],
                        dtype=np.int8,
                    )
                )
            else:
                if action[2] == "h":
                    self.board.take_action(
                        np.array(
                            [int(action[1]) - 1, ord(action[0]) - 97, 0], dtype=np.int8
                        )
                    )
                elif action[2] == "v":
                    self.board.take_action(
                        np.array(
                            [int(action[1]) - 1, ord(action[0]) - 97, 1], dtype=np.int8
                        )
                    )
        elif self.representation == "bitboard":
            self.actions.append(action)
            if len(action) == 2:
                self.board.take_action(
                    np.array(
                        [(int(action[1]) - 1) * 2, (ord(action[0]) - 97) * 2, 2],
                        dtype=np.int8,
                    )
                )
            else:
                if action[2] == "h":
                    self.board.take_action(
                        np.array(
                            [int(action[1]) - 1, ord(action[0]) - 97, 0], dtype=np.int8
                        )
                    )
                elif action[2] == "v":
                    self.board.take_action(
                        np.array(
                            [int(action[1]) - 1, ord(action[0]) - 97, 1], dtype=np.int8
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
            "Moves": " ".join(self.actions),
            "Generate times": " ".join([str(x) for x in self.generate_times]),
            "Choose times": " ".join([str(x) for x in self.choose_times]),
        }


if __name__ == "__main__":
    print("not supposed to be run")
    raise ImportError
