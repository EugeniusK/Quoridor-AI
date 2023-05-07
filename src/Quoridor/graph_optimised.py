import numpy as np
from numba import int8, boolean, njit
from numba.experimental import jitclass

from .path_finding_optimised import (
    Breadth_First_Search_Graph_More_Optim,
)
from .functions import roll_numba


class QuoridorGraphicalBoardMoreOptim:
    def __init__(self, path_finding_mode="BFS"):
        # Adjaceny list stores valid edges as boolean instead of representing 2D index
        # 9x9x4 size as each position has 4 possible - North, East, South, West
        # Each node has [1, 2, 3, 4] whichrepresents valid in North, East, South, West <-- in this order
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

        # Position of both players represented as [row, col]
        # From perspective of player 1, [0,0] is a1 and [8,8] is h9
        self.p1_pos = np.array([0, 4], dtype=np.int8)
        self.p2_pos = np.array([8, 4], dtype=np.int8)

        # Number of walls that each player has placed
        self.p1_walls_placed = np.int8(0)
        self.p2_walls_placed = np.int8(0)

        # Player who is in turn
        self.turn = np.int8(1)

        # If the game is over or not
        self.over = np.bool8(False)

        # Search mode to be used
        self.path_finding_mode = path_finding_mode

    def get_available_actions(self):
        walls_left = True
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

        # Boolean array indicating if S,E,N,W moves are possible
        in_turn_moves = np.copy(self.nodes[in_turn_pos[0], in_turn_pos[1]])

        # Array to hold a maximum of 133 actions
        # Theoretically, 64 horizontal walls, 64 vertical walls and 5 moves are possible
        actions = np.array(
            [
                [0, 0, 0],
                [0, 1, 0],
                [0, 2, 0],
                [0, 3, 0],
                [0, 4, 0],
                [0, 5, 0],
                [0, 6, 0],
                [0, 7, 0],
                [1, 0, 0],
                [1, 1, 0],
                [1, 2, 0],
                [1, 3, 0],
                [1, 4, 0],
                [1, 5, 0],
                [1, 6, 0],
                [1, 7, 0],
                [2, 0, 0],
                [2, 1, 0],
                [2, 2, 0],
                [2, 3, 0],
                [2, 4, 0],
                [2, 5, 0],
                [2, 6, 0],
                [2, 7, 0],
                [3, 0, 0],
                [3, 1, 0],
                [3, 2, 0],
                [3, 3, 0],
                [3, 4, 0],
                [3, 5, 0],
                [3, 6, 0],
                [3, 7, 0],
                [4, 0, 0],
                [4, 1, 0],
                [4, 2, 0],
                [4, 3, 0],
                [4, 4, 0],
                [4, 5, 0],
                [4, 6, 0],
                [4, 7, 0],
                [5, 0, 0],
                [5, 1, 0],
                [5, 2, 0],
                [5, 3, 0],
                [5, 4, 0],
                [5, 5, 0],
                [5, 6, 0],
                [5, 7, 0],
                [6, 0, 0],
                [6, 1, 0],
                [6, 2, 0],
                [6, 3, 0],
                [6, 4, 0],
                [6, 5, 0],
                [6, 6, 0],
                [6, 7, 0],
                [7, 0, 0],
                [7, 1, 0],
                [7, 2, 0],
                [7, 3, 0],
                [7, 4, 0],
                [7, 5, 0],
                [7, 6, 0],
                [7, 7, 0],
                [0, 0, 1],
                [0, 1, 1],
                [0, 2, 1],
                [0, 3, 1],
                [0, 4, 1],
                [0, 5, 1],
                [0, 6, 1],
                [0, 7, 1],
                [1, 0, 1],
                [1, 1, 1],
                [1, 2, 1],
                [1, 3, 1],
                [1, 4, 1],
                [1, 5, 1],
                [1, 6, 1],
                [1, 7, 1],
                [2, 0, 1],
                [2, 1, 1],
                [2, 2, 1],
                [2, 3, 1],
                [2, 4, 1],
                [2, 5, 1],
                [2, 6, 1],
                [2, 7, 1],
                [3, 0, 1],
                [3, 1, 1],
                [3, 2, 1],
                [3, 3, 1],
                [3, 4, 1],
                [3, 5, 1],
                [3, 6, 1],
                [3, 7, 1],
                [4, 0, 1],
                [4, 1, 1],
                [4, 2, 1],
                [4, 3, 1],
                [4, 4, 1],
                [4, 5, 1],
                [4, 6, 1],
                [4, 7, 1],
                [5, 0, 1],
                [5, 1, 1],
                [5, 2, 1],
                [5, 3, 1],
                [5, 4, 1],
                [5, 5, 1],
                [5, 6, 1],
                [5, 7, 1],
                [6, 0, 1],
                [6, 1, 1],
                [6, 2, 1],
                [6, 3, 1],
                [6, 4, 1],
                [6, 5, 1],
                [6, 6, 1],
                [6, 7, 1],
                [7, 0, 1],
                [7, 1, 1],
                [7, 2, 1],
                [7, 3, 1],
                [7, 4, 1],
                [7, 5, 1],
                [7, 6, 1],
                [7, 7, 1],
                [-1, -1, 2],
                [-1, -1, 2],
                [-1, -1, 2],
                [-1, -1, 2],
                [-1, -1, 2],
            ],
            dtype=np.int8,
        )

        # Ensures that any moves calculated will be added to unused index
        moves_added = 0

        adjacent = False

        NORTH_MOVE = in_turn_pos + np.array([1, 0], dtype=np.int8)
        EAST_MOVE = in_turn_pos + np.array([0, 1], dtype=np.int8)
        SOUTH_MOVE = in_turn_pos + np.array([-1, 0], dtype=np.int8)
        WEST_MOVE = in_turn_pos + np.array([0, -1], dtype=np.int8)

        # Code below follows this structure:
        # If the move in a direction is valid
        # --> If the move causes the player in turn
        #     to land on player out of turn
        #         Record that players are adjacent
        #     Otherwise, add the move to actions array
        if in_turn_moves[0]:
            if NORTH_MOVE[0] == out_turn_pos[0] and NORTH_MOVE[1] == out_turn_pos[1]:
                adjacent = True
            else:
                actions[128 + moves_added, 0:2] = NORTH_MOVE
                moves_added += 1
        if in_turn_moves[1]:
            if EAST_MOVE[0] == out_turn_pos[0] and EAST_MOVE[1] == out_turn_pos[1]:
                adjacent = True
            else:
                actions[128 + moves_added, 0:2] = EAST_MOVE
                moves_added += 1
        if in_turn_moves[2]:
            if SOUTH_MOVE[0] == out_turn_pos[0] and SOUTH_MOVE[1] == out_turn_pos[1]:
                adjacent = True
            else:
                actions[128 + moves_added, 0:2] = SOUTH_MOVE
                moves_added += 1
        if in_turn_moves[3]:
            if WEST_MOVE[0] == out_turn_pos[0] and WEST_MOVE[1] == out_turn_pos[1]:
                adjacent = True
            else:
                actions[128 + moves_added, 0:2] = WEST_MOVE
                moves_added += 1

        # If the 2 players are adjacent,
        # Determine if the player in turn can jump over the other player
        # or if there are moves available to the side
        if adjacent:
            relative_pos = out_turn_pos - in_turn_pos
            # player in turn is North of player out of turn
            if relative_pos[0] == np.int8(1) and relative_pos[1] == np.int8(0):
                # If double North move is possible, add
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:
                    actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                        [2, 0], dtype=np.int8
                    )
                    moves_added += 1
                else:
                    # Otherwise add North East, North West moves
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:
                        actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                            [1, 1], dtype=np.int8
                        )
                        moves_added += 1
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:
                        actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                            [
                                1,
                                -1,
                            ],
                            dtype=np.int8,
                        )
                        moves_added += 1
            # player in turn is East of player out of turn
            elif relative_pos[0] == np.int8(0) and relative_pos[1] == np.int8(1):
                # If double East move is possible, add
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:
                    actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                        [0, 2], dtype=np.int8
                    )
                    moves_added += 1
                else:
                    # Otherwise add South East, North East moves
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:
                        actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                            [-1, 1], dtype=np.int8
                        )
                        moves_added += 1
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:
                        actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                            [
                                1,
                                1,
                            ],
                            dtype=np.int8,
                        )
                        moves_added += 1
            # player in turn is South of player out of turn
            elif relative_pos[0] == np.int8(-1) and relative_pos[1] == np.int8(0):
                # If double South move is possible, add
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:
                    actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                        [-2, 0], dtype=np.int8
                    )
                    moves_added += 1
                else:
                    # Otherwise add South East, South West moves
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:
                        actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                            [-1, 1], dtype=np.int8
                        )
                        moves_added += 1
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:
                        actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                            [
                                -1,
                                -1,
                            ],
                            dtype=np.int8,
                        )
                        moves_added += 1
            # player in turn is West of player out of turn
            elif relative_pos[0] == np.int8(0) and relative_pos[1] == np.int8(-1):
                # If double West move is possible, add
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:
                    actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                        [0, -2], dtype=np.int8
                    )
                    moves_added += 1
                else:
                    # Otherwise add South West, North West moves
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:
                        actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                            [-1, -1], dtype=np.int8
                        )
                        moves_added += 1
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:
                        actions[128 + moves_added, 0:2] = in_turn_pos + np.array(
                            [
                                1,
                                -1,
                            ],
                            dtype=np.int8,
                        )
                        moves_added += 1

        if walls_left:
            if self.path_finding_mode == "BFS":
                search = Breadth_First_Search_Graph_More_Optim
            # elif self.path_finding_mode == "DFS":
            #     search = Depth_First_Search_Graph_More_Optim
            # elif self.path_finding_mode == "GBFS":
            #     search = Greedy_Best_First_Search_Graph_More_Optim
            # elif self.path_finding_mode == "UCT":
            #     search = Uniform_Cost_Search_Graph_More_Optim
            # elif self.path_finding_mode == "Astar":
            #     search = A_Star_Search_Graph_More_Optim
            for row in range(8):
                for col in range(8):
                    # Checks if horizontal wall position is empty
                    # - can move North from both places
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
                            if not search(
                                self.nodes,
                                self.p1_pos,
                                8,
                                np.array([row, col, 0], dtype=np.int8),
                            ) or not search(
                                self.nodes,
                                self.p2_pos,
                                0,
                                np.array([row, col, 0], dtype=np.int8),
                            ):
                                actions[row * 8 + col] = [-1, -1, -1]
                        else:
                            actions[row * 8 + col] = [-1, -1, -1]

                    else:
                        actions[row * 8 + col] = [-1, -1, -1]

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
                            # Validate vertical wall allows a path to end
                            if not search(
                                self.nodes,
                                self.p1_pos,
                                8,
                                np.array([row, col, 1], dtype=np.int8),
                            ) or not search(
                                self.nodes,
                                self.p2_pos,
                                0,
                                np.array([row, col, 1], dtype=np.int8),
                            ):
                                actions[64 + row * 8 + col] = [-1, -1, -1]
                        else:
                            actions[64 + row * 8 + col] = [-1, -1, -1]

                    else:
                        actions[64 + row * 8 + col] = [-1, -1, -1]
        else:
            actions[0:128] = [-1, -1, -1]
        return actions
        algebraic_moves = []
        for i in range(133):
            if actions[i][0] != -1:
                if walls_left:
                    if actions[i][2] == 0:
                        algebraic_moves.append(
                            f"{chr(97+actions[i][1])}{actions[i][0]+1}h"
                        )
                    elif actions[i][2] == 1:
                        algebraic_moves.append(
                            f"{chr(97+actions[i][1])}{actions[i][0]+1}v"
                        )
                if actions[i][2] == 2:
                    algebraic_moves.append(f"{chr(97+actions[i][1])}{actions[i][0]+1}")
        return algebraic_moves

    def take_action(self, action):
        if action[2] == 2:
            if self.turn == 1:
                self.p1_pos = action[0:2]
                if self.p1_pos[0] == 8:
                    self.over = True
                else:
                    self.turn = 2
            else:
                self.p2_pos = action[0:2]
                if self.p2_pos[0] == 0:
                    self.over = True
                else:
                    self.turn = 1
        else:
            if action[2] == 0:
                self.nodes[action[0], action[1], 0] = False
                self.nodes[action[0] + 1, action[1], 2] = False
                self.nodes[action[0], action[1] + 1, 0] = False
                self.nodes[action[0] + 1, action[1] + 1, 2] = False
            if action[2] == 1:
                self.nodes[action[0], action[1], 1] = False
                self.nodes[action[0], action[1] + 1, 3] = False
                self.nodes[action[0] + 1, action[1], 1] = False
                self.nodes[action[0] + 1, action[1] + 1, 3] = False
            if self.turn == 1:
                self.p1_walls_placed += 1
                self.turn = 2
            else:
                self.p2_walls_placed += 1
                self.turn = 1

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
