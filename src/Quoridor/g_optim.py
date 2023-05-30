import numpy as np
from numba import int8, boolean, njit
from numba.experimental import jitclass
import copy

try:
    from Quoridor.g_pathfinding_optim import (
        Breadth_First_Search_Graph_More_Optim,
        Depth_First_Search_Graph_More_Optim,
        Greedy_Best_First_Search_Graph_More_Optim,
        Uniform_Cost_Search_Graph_More_Optim,
        A_Star_Search_Graph_More_Optim,
    )
except:
    from g_pathfinding_optim import (
        Breadth_First_Search_Graph_More_Optim,
        Depth_First_Search_Graph_More_Optim,
        Greedy_Best_First_Search_Graph_More_Optim,
        Uniform_Cost_Search_Graph_More_Optim,
        A_Star_Search_Graph_More_Optim,
    )
from .functions import roll_numba

"""
This is an improved version of the graphical representation in graph.py.

Instead of implementing the typical adjacency list with the indexes of neighbouring
nodes, it has been modified so each vertex records the presence of an edge in each 
cardinal direction as a boolean.
"""


class QuoridorGraphicalBoardOptim:
    def __init__(self, path_finding_mode="BFS", **kwargs):
        # Starting state of the adjacency list
        self.nodes = np.array(
            [
                [
                    [True, True, False, False],
                    [True, True, False, True],
                    [True, True, False, True],
                    [True, True, False, True],
                    [True, True, False, True],
                    [True, True, False, True],
                    [True, True, False, True],
                    [True, True, False, True],
                    [True, False, False, True],
                ],
                [
                    [True, True, True, False],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, False, True, True],
                ],
                [
                    [True, True, True, False],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, False, True, True],
                ],
                [
                    [True, True, True, False],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, False, True, True],
                ],
                [
                    [True, True, True, False],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, False, True, True],
                ],
                [
                    [True, True, True, False],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, False, True, True],
                ],
                [
                    [True, True, True, False],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, False, True, True],
                ],
                [
                    [True, True, True, False],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, True, True, True],
                    [True, False, True, True],
                ],
                [
                    [False, True, True, False],
                    [False, True, True, True],
                    [False, True, True, True],
                    [False, True, True, True],
                    [False, True, True, True],
                    [False, True, True, True],
                    [False, True, True, True],
                    [False, True, True, True],
                    [False, False, True, True],
                ],
            ],
            dtype=np.bool8,
        )

        # Position of both players stored as [row, col]
        self.p1_pos = np.array([0, 4], dtype=np.int8)
        self.p2_pos = np.array([8, 4], dtype=np.int8)

        # Number of walls that each player has placed
        self.p1_walls_placed = np.int8(0)
        self.p2_walls_placed = np.int8(0)

        # Player who is in turn
        self.turn = 1

        # If the game is over or not
        self.over = np.bool8(False)

        # Search mode to be used when verifying if a wall is allowed
        self.path_finding_mode = path_finding_mode

        self.available_states = []

    def get_available_actions(self):
        """
        For the player in turn, return available actions with a boolean array
        where if index X is True, action X is valid and vice versa.

        Actions 0~63 represent horizontal wall placements
        where 0 represents a1h, 1 represents b1h, ..., 63 represents i8h

        Actions 64~127 represent vertical wall placements
        where 0 represents a1v, 1 represents b1v, ..., 63 represents i8v

        Actions 128~139 represent the moves from the player's position
        -  N, E, S, W, NN, NE, EE, SE, SS, SW, WW, NW
        """

        # Boolean array where index X records if action X is possible
        available_actions = np.zeros(140, dtype=np.bool8)

        # If the player in turn has no walls left (placed all 10),
        # there is no need to find all the available walls.
        walls_left = True

        # Depending on the player whose turn it is,
        # in_turn_pos, out_turn_pos are temporarily used to reference
        # the corrent positions (according to their name)
        if self.turn == 1:
            in_turn_pos = self.p1_pos
            out_turn_pos = self.p2_pos

            if self.p1_walls_placed == 10:
                walls_left = False
        else:
            in_turn_pos = self.p2_pos
            out_turn_pos = self.p1_pos

            if self.p2_walls_placed == 10:
                walls_left = False

        # Booleans indicating if NESW moves are possible for player in turn
        in_turn_moves = np.copy(self.nodes[in_turn_pos[0], in_turn_pos[1]])

        # Determines if the player in turn is adjacent to the player not in turn
        # If adjacent, more moves can be possible
        adjacent = False

        # If in_turn_pos says a move in given direction is possible,
        # check if the move in given direction makes player in turn
        # land on the player not in turn. If so, set adjacent to True
        # Otherwise, the move in given direction is definitely possible
        # so set move as possible
        if in_turn_moves[0]:  # North
            if np.array_equal(
                in_turn_pos + np.array([1, 0], dtype=np.int8), out_turn_pos
            ):
                adjacent = True
            else:
                available_actions[128] = True

        if in_turn_moves[1]:  # East
            if np.array_equal(
                in_turn_pos + np.array([0, 1], dtype=np.int8), out_turn_pos
            ):
                adjacent = True
            else:
                available_actions[129] = True

        if in_turn_moves[2]:  # South
            if np.array_equal(
                in_turn_pos + np.array([-1, 0], dtype=np.int8), out_turn_pos
            ):
                adjacent = True
            else:
                available_actions[130] = True

        if in_turn_moves[3]:  # West
            if np.array_equal(
                in_turn_pos + np.array([0, -1], dtype=np.int8), out_turn_pos
            ):
                adjacent = True
            else:
                available_actions[131] = True

        # If the 2 players are adjacent,
        # determine if the player in turn can jump over the other player
        # or if there are moves available to the side
        if adjacent:
            # Calculate the relative position of player out of turn from player in turn
            relative_pos = out_turn_pos - in_turn_pos

            # Player in turn is North of player out of turn
            if relative_pos[0] == np.int8(1) and relative_pos[1] == np.int8(0):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move NN as possible
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:  # NN
                    available_actions[132] = True
                else:
                    # Check if the moves to the sides of player out of turn
                    # are possible and set move(s) as possible
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:  # NE
                        available_actions[133] = True
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:  # NW
                        available_actions[139] = True

            # Player in turn is East of player out of turn
            elif relative_pos[0] == np.int8(0) and relative_pos[1] == np.int8(1):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move NN as possible
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:  # EE
                    available_actions[134] = True
                else:
                    # Check if the moves to the sides of player out of turn
                    # are possible and set move(s) as possible
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:  # SE
                        available_actions[135] = True
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:  # NE
                        available_actions[133] = True

            # Player in turn is South of player out of turn
            elif relative_pos[0] == np.int8(-1) and relative_pos[1] == np.int8(0):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move NN as possible
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:  # SS
                    available_actions[136] = True
                else:
                    # Check if the moves to the sides of player out of turn
                    # are possible and set move(s) as possible
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:  # SE
                        available_actions[135] = True
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:  # SW
                        available_actions[137] = True

            # Player in turn is West of player out of turn
            elif relative_pos[0] == np.int8(0) and relative_pos[1] == np.int8(-1):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move NN as possible
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:  # WW
                    available_actions[138] = True
                else:
                    # Check if the moves to the sides of player out of turn
                    # are possible and set move(s) as possible
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:  # SW
                        available_actions[137] = True
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:  # NW
                        available_actions[139] = True

        # Only attempt to find the possible walls if the player has walls available
        # Otherwise, only focus on the possible movements
        if walls_left:
            # Set the pathfinding mode based on parameter during initialisation of board
            if self.path_finding_mode == "BFS":
                search = Breadth_First_Search_Graph_More_Optim
            elif self.path_finding_mode == "DFS":
                search = Depth_First_Search_Graph_More_Optim
            elif self.path_finding_mode == "GBFS":
                search = Greedy_Best_First_Search_Graph_More_Optim
            elif self.path_finding_mode == "UCT":
                search = Uniform_Cost_Search_Graph_More_Optim
            elif self.path_finding_mode == "Astar":
                search = A_Star_Search_Graph_More_Optim
            for row in range(8):
                for col in range(8):
                    # Check if horizontal wall at position (row, col) can be placed
                    # taking into account the possibility of multiple walls being placed in a line
                    if self.nodes[row, col, 0] and self.nodes[row, col + 1, 0]:
                        if (
                            (self.nodes[row, col, 1] or self.nodes[row + 1, col, 1])
                            or (
                                (row == 1 or row == 6)
                                and ~self.nodes[row - 1, col, 1]
                                and ~self.nodes[row, col, 1]
                                and ~self.nodes[row + 1, col, 1]
                                and ~self.nodes[row + 2, col, 1]
                            )
                            or (
                                row > 1
                                and row < 6
                                and (
                                    self.nodes[row - 2, col, 1]
                                    or self.nodes[row + 3, col, 1]
                                )
                                and ~self.nodes[row - 1, col, 1]
                                and ~self.nodes[row, col, 1]
                                and ~self.nodes[row + 1, col, 1]
                                and ~self.nodes[row + 2, col, 1]
                            )
                            or (
                                (row == 3 or row == 4)
                                and ~self.nodes[row - 3, col, 1]
                                and ~self.nodes[row - 2, col, 1]
                                and ~self.nodes[row - 1, col, 1]
                                and ~self.nodes[row, col, 1]
                                and ~self.nodes[row + 1, col, 1]
                                and ~self.nodes[row + 2, col, 1]
                                and ~self.nodes[row + 3, col, 1]
                                and ~self.nodes[row + 4, col, 1]
                            )
                        ):
                            # Check if the horizontal wall placed at (row, column)
                            # still allows both players to reach their destinations
                            # using the pathfinding algorithm set above
                            if search(
                                self.nodes,
                                self.p1_pos,
                                8,
                                np.array([row, col, 0], dtype=np.int8),
                            ) and search(
                                self.nodes,
                                self.p2_pos,
                                0,
                                np.array([row, col, 0], dtype=np.int8),
                            ):
                                # Set True only if pathfinding successful for both players
                                available_actions[row * 8 + col] = True
                    # Check if vertical wall at position (row, col) can be placed
                    # taking into account the possibility of multiple walls being placed in a line
                    if self.nodes[row, col, 1] and self.nodes[row + 1, col, 1]:
                        if (
                            (self.nodes[row, col, 0] or self.nodes[row, col + 1, 0])
                            or (
                                (col == 1 or col == 6)
                                and ~self.nodes[row, col - 1, 0]
                                and ~self.nodes[row, col, 0]
                                and ~self.nodes[row, col + 1, 0]
                                and ~self.nodes[row, col + 2, 0]
                            )
                            or (
                                col > 1
                                and col < 6
                                and (
                                    self.nodes[row, col - 2, 0]
                                    or self.nodes[row, col + 3, 0]
                                )
                                and ~self.nodes[row, col - 1, 0]
                                and ~self.nodes[row, col, 0]
                                and ~self.nodes[row, col + 1, 0]
                                and ~self.nodes[row, col + 2, 0]
                            )
                            or (
                                (col == 3 or col == 4)
                                and ~self.nodes[row, col - 3, 0]
                                and ~self.nodes[row, col - 2, 0]
                                and ~self.nodes[row, col - 1, 0]
                                and ~self.nodes[row, col, 0]
                                and ~self.nodes[row, col + 1, 0]
                                and ~self.nodes[row, col + 2, 0]
                                and ~self.nodes[row, col + 3, 0]
                                and ~self.nodes[row, col + 4, 0]
                            )
                        ):
                            # Check if the vertical wall placed at (row, column)
                            # still allows both players to reach their destinations
                            # using the pathfinding algorithm set above
                            if search(
                                self.nodes,
                                self.p1_pos,
                                8,
                                np.array([row, col, 1], dtype=np.int8),
                            ) and search(
                                self.nodes,
                                self.p2_pos,
                                0,
                                np.array([row, col, 1], dtype=np.int8),
                            ):
                                # Set True only if pathfinding successful for both players
                                available_actions[64 + row * 8 + col] = True

        return available_actions

    def is_action_available(self, action):
        # Boolean array where index X records if action X is possible
        available_actions = np.zeros(140, dtype=np.bool8)

        # If the player in turn has no walls left (placed all 10),
        # there is no need to find all the available walls.
        walls_left = True

        # Depending on the player whose turn it is,
        # in_turn_pos, out_turn_pos are temporarily used to reference
        # the corrent positions (according to their name)
        if self.turn == 1:
            in_turn_pos = self.p1_pos
            out_turn_pos = self.p2_pos

            if self.p1_walls_placed == 10:
                walls_left = False
        else:
            in_turn_pos = self.p2_pos
            out_turn_pos = self.p1_pos

            if self.p2_walls_placed == 10:
                walls_left = False
        if action >= 128:
            # Booleans indicating if NESW moves are possible for player in turn
            in_turn_moves = np.copy(self.nodes[in_turn_pos[0], in_turn_pos[1]])

            # Determines if the player in turn is adjacent to the player not in turn
            # If adjacent, more moves can be possible
            adjacent = False

            # If in_turn_pos says a move in given direction is possible,
            # check if the move in given direction makes player in turn
            # land on the player not in turn. If so, set adjacent to True
            # Otherwise, the move in given direction is definitely possible
            # so set move as possible
            if in_turn_moves[0]:  # North
                if np.array_equal(
                    in_turn_pos + np.array([1, 0], dtype=np.int8), out_turn_pos
                ):
                    adjacent = True
                else:
                    available_actions[128] = True

            if in_turn_moves[1]:  # East
                if np.array_equal(
                    in_turn_pos + np.array([0, 1], dtype=np.int8), out_turn_pos
                ):
                    adjacent = True
                else:
                    available_actions[129] = True

            if in_turn_moves[2]:  # South
                if np.array_equal(
                    in_turn_pos + np.array([-1, 0], dtype=np.int8), out_turn_pos
                ):
                    adjacent = True
                else:
                    available_actions[130] = True

            if in_turn_moves[3]:  # West
                if np.array_equal(
                    in_turn_pos + np.array([0, -1], dtype=np.int8), out_turn_pos
                ):
                    adjacent = True
                else:
                    available_actions[131] = True

            # If the 2 players are adjacent,
            # determine if the player in turn can jump over the other player
            # or if there are moves available to the side
            if adjacent:
                # Calculate the relative position of player out of turn from player in turn
                relative_pos = out_turn_pos - in_turn_pos

                # Player in turn is North of player out of turn
                if relative_pos[0] == np.int8(1) and relative_pos[1] == np.int8(0):
                    # If the player in turn can jump over the player out of turn
                    # without going over a wall, set the move NN as possible
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:  # NN
                        available_actions[132] = True
                    else:
                        # Check if the moves to the sides of player out of turn
                        # are possible and set move(s) as possible
                        if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:  # NE
                            available_actions[133] = True
                        if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:  # NW
                            available_actions[139] = True

                # Player in turn is East of player out of turn
                elif relative_pos[0] == np.int8(0) and relative_pos[1] == np.int8(1):
                    # If the player in turn can jump over the player out of turn
                    # without going over a wall, set the move NN as possible
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:  # EE
                        available_actions[134] = True
                    else:
                        # Check if the moves to the sides of player out of turn
                        # are possible and set move(s) as possible
                        if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:  # SE
                            available_actions[135] = True
                        if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:  # NE
                            available_actions[133] = True

                # Player in turn is South of player out of turn
                elif relative_pos[0] == np.int8(-1) and relative_pos[1] == np.int8(0):
                    # If the player in turn can jump over the player out of turn
                    # without going over a wall, set the move NN as possible
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:  # SS
                        available_actions[136] = True
                    else:
                        # Check if the moves to the sides of player out of turn
                        # are possible and set move(s) as possible
                        if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:  # SE
                            available_actions[135] = True
                        if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:  # SW
                            available_actions[137] = True

                # Player in turn is West of player out of turn
                elif relative_pos[0] == np.int8(0) and relative_pos[1] == np.int8(-1):
                    # If the player in turn can jump over the player out of turn
                    # without going over a wall, set the move NN as possible
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:  # WW
                        available_actions[138] = True
                    else:
                        # Check if the moves to the sides of player out of turn
                        # are possible and set move(s) as possible
                        if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:  # SW
                            available_actions[137] = True
                        if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:  # NW
                            available_actions[139] = True
            return available_actions[action]
        elif action < 128:
            # Only attempt to find the possible walls if the player has walls available
            # Otherwise, only focus on the possible movements
            if walls_left:
                # Set the pathfinding mode based on parameter during initialisation of board
                if self.path_finding_mode == "BFS":
                    search = Breadth_First_Search_Graph_More_Optim
                elif self.path_finding_mode == "DFS":
                    search = Depth_First_Search_Graph_More_Optim
                elif self.path_finding_mode == "GBFS":
                    search = Greedy_Best_First_Search_Graph_More_Optim
                elif self.path_finding_mode == "UCT":
                    search = Uniform_Cost_Search_Graph_More_Optim
                elif self.path_finding_mode == "Astar":
                    search = A_Star_Search_Graph_More_Optim
                if action < 64:
                    row = action // 8
                    col = action % 8
                    # Check if horizontal wall at position (row, col) can be placed
                    # taking into account the possibility of multiple walls being placed in a line
                    if self.nodes[row, col, 0] and self.nodes[row, col + 1, 0]:
                        if (
                            (self.nodes[row, col, 1] or self.nodes[row + 1, col, 1])
                            or (
                                (row == 1 or row == 6)
                                and ~self.nodes[row - 1, col, 1]
                                and ~self.nodes[row, col, 1]
                                and ~self.nodes[row + 1, col, 1]
                                and ~self.nodes[row + 2, col, 1]
                            )
                            or (
                                row > 1
                                and row < 6
                                and (
                                    self.nodes[row - 2, col, 1]
                                    or self.nodes[row + 3, col, 1]
                                )
                                and ~self.nodes[row - 1, col, 1]
                                and ~self.nodes[row, col, 1]
                                and ~self.nodes[row + 1, col, 1]
                                and ~self.nodes[row + 2, col, 1]
                            )
                            or (
                                (row == 3 or row == 4)
                                and ~self.nodes[row - 3, col, 1]
                                and ~self.nodes[row - 2, col, 1]
                                and ~self.nodes[row - 1, col, 1]
                                and ~self.nodes[row, col, 1]
                                and ~self.nodes[row + 1, col, 1]
                                and ~self.nodes[row + 2, col, 1]
                                and ~self.nodes[row + 3, col, 1]
                                and ~self.nodes[row + 4, col, 1]
                            )
                        ):
                            # Check if the horizontal wall placed at (row, column)
                            # still allows both players to reach their destinations
                            # using the pathfinding algorithm set above
                            if search(
                                self.nodes,
                                self.p1_pos,
                                8,
                                np.array([row, col, 0], dtype=np.int8),
                            ) and search(
                                self.nodes,
                                self.p2_pos,
                                0,
                                np.array([row, col, 0], dtype=np.int8),
                            ):
                                # Set True only if pathfinding successful for both players
                                return True
                elif action < 128:
                    row = (action - 64) // 8
                    col = action % 8
                    # Check if vertical wall at position (row, col) can be placed
                    # taking into account the possibility of multiple walls being placed in a line
                    if self.nodes[row, col, 1] and self.nodes[row + 1, col, 1]:
                        if (
                            (self.nodes[row, col, 0] or self.nodes[row, col + 1, 0])
                            or (
                                (col == 1 or col == 6)
                                and ~self.nodes[row, col - 1, 0]
                                and ~self.nodes[row, col, 0]
                                and ~self.nodes[row, col + 1, 0]
                                and ~self.nodes[row, col + 2, 0]
                            )
                            or (
                                col > 1
                                and col < 6
                                and (
                                    self.nodes[row, col - 2, 0]
                                    or self.nodes[row, col + 3, 0]
                                )
                                and ~self.nodes[row, col - 1, 0]
                                and ~self.nodes[row, col, 0]
                                and ~self.nodes[row, col + 1, 0]
                                and ~self.nodes[row, col + 2, 0]
                            )
                            or (
                                (col == 3 or col == 4)
                                and ~self.nodes[row, col - 3, 0]
                                and ~self.nodes[row, col - 2, 0]
                                and ~self.nodes[row, col - 1, 0]
                                and ~self.nodes[row, col, 0]
                                and ~self.nodes[row, col + 1, 0]
                                and ~self.nodes[row, col + 2, 0]
                                and ~self.nodes[row, col + 3, 0]
                                and ~self.nodes[row, col + 4, 0]
                            )
                        ):
                            # Check if the vertical wall placed at (row, column)
                            # still allows both players to reach their destinations
                            # using the pathfinding algorithm set above
                            if search(
                                self.nodes,
                                self.p1_pos,
                                8,
                                np.array([row, col, 1], dtype=np.int8),
                            ) and search(
                                self.nodes,
                                self.p2_pos,
                                0,
                                np.array([row, col, 1], dtype=np.int8),
                            ):
                                # Set True only if pathfinding successful for both players
                                return True

    def take_action(self, action):
        """
        For the player in turn, perform the action inputed

        Actions 0~63 represent horizontal wall placements
        where 0 represents a1h, 1 represents b1h, ..., 63 represents i8h

        Actions 64~127 represent vertical wall placements
        where 0 represents a1v, 1 represents b1v, ..., 63 represents i8v

        Actions 128~139 represent the moves from the player's position
        -  N, E, S, W, NN, NE, EE, SE, SS, SW, WW, NW
        """

        rel_move = np.array(
            [
                [1, 0],
                [0, 1],
                [-1, 0],
                [0, -1],
                [2, 0],
                [1, 1],
                [0, 2],
                [-1, 1],
                [-2, 0],
                [-1, -1],
                [0, -2],
                [1, -1],
            ],
            dtype=np.int8,
        )

        # Action is a movement
        if action >= 128:
            if self.turn == 1:
                # Move player 1 according to the relative motion defined in rel_move
                self.p1_pos += rel_move[action - 128]
                # If the new position of player 1 is on the winning row, the game is over
                # Otherwise, set the turn to player 2
                if self.p1_pos[0] == 8:
                    self.over = True
                else:
                    self.turn = 2

            elif self.turn == 2:
                # Move player 2 according to the relative motion defined in rel_move
                self.p2_pos += rel_move[action - 128]
                # If the new position of player 2 is on the winning row, the game is over
                # Otherwise, set the turn to player 1
                if self.p2_pos[0] == 0:
                    self.over = True
                else:
                    self.turn = 1

        # Action is a wall placement
        else:
            # Horizontal wall
            if action < 64:
                self.nodes[action // 8, action % 8, 0] = False
                self.nodes[action // 8 + 1, action % 8, 2] = False
                self.nodes[action // 8, action % 8 + 1, 0] = False
                self.nodes[action // 8 + 1, action % 8 + 1, 2] = False
            # Vertical wall
            else:
                self.nodes[(action % 64) // 8, (action % 64) % 8, 1] = False
                self.nodes[(action % 64) // 8, (action % 64) % 8 + 1, 3] = False
                self.nodes[(action % 64) // 8 + 1, (action % 64) % 8, 1] = False
                self.nodes[(action % 64) // 8 + 1, (action % 64) % 8 + 1, 3] = False

            # Increment the number of walls placed for the relevant player
            # Set the turn to the other player
            if self.turn == 1:
                self.p1_walls_placed += 1
                self.turn = 2
            else:
                self.p2_walls_placed += 1
                self.turn = 1

    def get_available_states(self):
        if self.available_states == []:
            tmp_available_state = []
            available_actions = self.get_available_actions()
            for action in [x for x in range(140) if available_actions[x]]:
                tmp_state = copy.deepcopy(self)
                tmp_state.take_action(action)
                tmp_available_state.append(tmp_state)
            self.available_states = tmp_available_state
        return self.available_states

    def display_beautiful(self):
        for row in range(8, -1, -1):
            line = []
            line_below = []
            for column in range(9):
                if np.array_equal(self.p1_pos, [row, column]):
                    line.append(" 1 ")
                elif np.array_equal(self.p2_pos, [row, column]):
                    line.append(" 2 ")
                else:
                    line.append("   ")

                if self.nodes[row, column, 1] and self.nodes[row, column + 1, 3]:
                    line.append("\u2502")
                else:
                    if column != 8:
                        line.append("\u2503")
                if row != 8:
                    # if no horizontal wall below (row, column) place thin lines
                    # otherwise, place thick lines to show a wall
                    if self.nodes[row, column, 0] and self.nodes[row + 1, column, 2]:
                        line_below.append("\u2500\u2500\u2500")
                    else:
                        line_below.append("\u2501\u2501\u2501")
                    if column != 8:
                        # variables describing if there is part of a wall above the intersection
                        north = ~self.nodes[row + 1, column, 1]
                        east = ~self.nodes[row, column + 1, 0]
                        south = ~self.nodes[row, column, 1]
                        west = ~self.nodes[row, column, 0]

                        """
                        If row = 0, column = 0
                        X1 X2
                          I
                        X3 X4
                        looking at intersection I
                        """

                        # wall between X1 and X3

                        # add Unicode characters based on what combination of walls are around the intersection
                        if (
                            north == False
                            and east == False
                            and south == False
                            and west == False
                        ):
                            line_below.append("\u253c")
                        elif (
                            north == False
                            and east == False
                            and south == False
                            and west == True
                        ):
                            line_below.append("\u253d")
                        elif (
                            north == False
                            and east == True
                            and south == False
                            and west == False
                        ):
                            line_below.append("\u253e")
                        elif (
                            north == False
                            and east == True
                            and south == False
                            and west == True
                        ):
                            line_below.append("\u253f")
                        elif (
                            north == True
                            and east == False
                            and south == False
                            and west == False
                        ):
                            line_below.append("\u2540")
                        elif (
                            north == False
                            and east == False
                            and south == True
                            and west == False
                        ):
                            line_below.append("\u2541")
                        elif (
                            north == True
                            and east == False
                            and south == True
                            and west == False
                        ):
                            line_below.append("\u2542")
                        elif (
                            north == True
                            and east == False
                            and south == False
                            and west == True
                        ):
                            line_below.append("\u2543")
                        elif (
                            north == True
                            and east == True
                            and south == False
                            and west == False
                        ):
                            line_below.append("\u2544")
                        elif (
                            north == False
                            and east == False
                            and south == True
                            and west == True
                        ):
                            line_below.append("\u2545")
                        elif (
                            north == False
                            and east == True
                            and south == True
                            and west == False
                        ):
                            line_below.append("\u2546")
                        elif (
                            north == True
                            and east == True
                            and south == False
                            and west == True
                        ):
                            line_below.append("\u2547")
                        elif (
                            north == False
                            and east == True
                            and south == True
                            and west == True
                        ):
                            line_below.append("\u2548")
                        elif (
                            north == True
                            and east == False
                            and south == True
                            and west == True
                        ):
                            line_below.append("\u2549")
                        elif (
                            north == True
                            and east == True
                            and south == True
                            and west == False
                        ):
                            line_below.append("\u254A")
                        elif (
                            north == True
                            and east == True
                            and south == True
                            and west == True
                        ):
                            line_below.append("\u254B")
            print(" " + "".join(line_below))
            print(str(row + 1) + "".join(line))
        print("  a   b   c   d   e   f   g   h   i  ")

    def is_over(self):
        return self.over

    def winner(self):
        return self.turn
