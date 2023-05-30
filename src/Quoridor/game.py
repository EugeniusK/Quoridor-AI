# Import game implementations
from Quoridor.b import QuoridorBitBoard
from Quoridor.g import QuoridorGraphicalBoard
from Quoridor.g_optim import QuoridorGraphicalBoardOptim
from Quoridor.b_optim import QuoridorBitboardOptim

# Import AI algorithms
from AI.base import random_select
from AI.mcts import MCTS_NODE, select, expand, simulate, backpropagate

# Import rest
import time
import random
import json
from datetime import datetime, timezone
import numpy as np

random.seed(0)

# logging system inspired by PGN logging for chess
# http://www.saremba.de/chessgml/standards/pgn/pgn-complete.htm


class Game:
    def __init__(
        self,
        round=None,
        player_one="random",
        player_two="random",
        path_finding_mode="BFS",
        representation="graph",
    ):
        self.date = datetime.now(tz=timezone.utc)
        self.round = round
        self.p1 = player_one
        self.p2 = player_two
        self.representation = representation
        self.result = None
        self.path_finding_mode = path_finding_mode

        if self.representation == "graph":
            self.board = QuoridorGraphicalBoard(path_finding_mode)
        elif self.representation == "bitboard":
            self.board = QuoridorBitBoard(path_finding_mode)
        elif self.representation == "graph_optim":
            self.board = QuoridorGraphicalBoardOptim(path_finding_mode)
        elif self.representation == "bitboard_optim":
            self.board = QuoridorBitboardOptim(path_finding_mode)
        else:
            print(self.representation, self.path_finding_mode)
            raise NotImplementedError

        # All moves made until game over
        self.actions = []
        # Times taken to generate available actions each turn
        self.generate_times = []
        # Times taken to choose each turn
        self.choose_times = []
        # Number of walls placed when get_available_moves() called
        self.walls_placed = []

    def available_actions(self):
        """
        Gets an array of available actions for current move state
        in boolean format of arrray 140 length
        """
        # Get available actions and record time taken to generate
        generate_start = time.perf_counter()
        generated_actions = self.board.get_available_actions()
        generate_end = time.perf_counter()

        self.generate_times.append(round((generate_end - generate_start), 8))
        self.walls_placed.append(
            int(self.board.p1_walls_placed + self.board.p2_walls_placed)
        )
        return generated_actions

    def select(self, moves=None, rollout=100):
        """
        Selects a move based on method defined in __init__

        Methods
        - random where a psuedo random number generator is used to pick an action
        - MCTS where Monte-Carlo Tree Search is used to pick an action
        - human where a direct input is used
        """

        if self.board.turn == 1:
            mode = self.p1
        elif self.board.turn == 2:
            mode = self.p2

        if mode == "random":
            choose_start = time.perf_counter()
            try:
                move = random_select(moves)
            except:
                pass
                self.display()
            choose_end = time.perf_counter()
            self.choose_times.append(round(choose_end - choose_start, 8))
        elif mode == "mcts_pure":
            root = MCTS_NODE(self.board)
            for r in range(rollout):
                rollout(root)
            self.board = [
                c for c in sorted(root.children, key=lambda x: x.games_played)
            ][-1]
        elif mode == "human":
            move = input("Action number")

        return move

    def take_action(self, action):
        self.board.take_action(action)
        self.actions.append(str(action))

    def display(self):
        self.board.display_beautiful()

    def is_over(self):
        return self.board.is_over()

    def log(self):
        self.result = self.board.turn
        self.total_time = round(sum(self.generate_times) + sum(self.choose_times), 8)
        return {
            "Date": datetime.strftime(self.date, "%Y-%m-%d %H:%M:%S+%z"),
            "Round": self.round,
            "P1 mode": self.p1,
            "P2 mode": self.p2,
            "Path finding mode": self.path_finding_mode,
            "Representation": self.representation,
            "Result": self.result,
            "Actions": " ".join(self.actions),
            "Generate times": " ".join([str(x) for x in self.generate_times]),
            "Walls placed": " ".join([str(x) for x in self.walls_placed]),
            "Choose times": " ".join([str(x) for x in self.choose_times]),
        }


if __name__ == "__main__":
    print("not supposed to be run")
    raise ImportError
