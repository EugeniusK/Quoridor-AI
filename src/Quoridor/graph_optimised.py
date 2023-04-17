import numpy as np
from numba import int8, boolean, njit
from numba.experimental import jitclass

from .path_finding_optimised import (
    Breadth_First_Search_Graph_Optim,
    Depth_First_Search_Graph_Optim,
    Greedy_Best_First_Search_Graph_Optim,
    Uniform_Cost_Search_Graph_Optim,
    A_Star_Search_Graph_Optim,
    Breadth_First_Search_Graph_More_Optim,
    # Depth_First_Search_Graph_More_Optim,
)
from .functions import roll_numba


# @jitclass(
#     [
#         ("nodes", int8[:, :, :, :]),
#         ("p1_pos", int8[:]),
#         ("p2_pos", int8[:]),
#         ("p1_walls_placed", int8),
#         ("p2_walls_placed", int8),
#         ("turn", int8),
#         ("over", boolean),
#     ]
# )
class QuoridorGraphicalBoardOptim:
    def __init__(self, path_finding_mode="BFS"):
        # Adjacenly list of 9x9x5x2 size
        # 0th index on dim. 3 is index [row, col]
        # 1-4th index on dim. 3 is index [row, col] of neighbours
        self.nodes = np.array(
            [
                [
                    [[0, 0], [-1, -1], [0, 1], [1, 0], [-1, -1]],
                    [[0, 1], [-1, -1], [0, 2], [1, 1], [0, 0]],
                    [[0, 2], [-1, -1], [0, 3], [1, 2], [0, 1]],
                    [[0, 3], [-1, -1], [0, 4], [1, 3], [0, 2]],
                    [[0, 4], [-1, -1], [0, 5], [1, 4], [0, 3]],
                    [[0, 5], [-1, -1], [0, 6], [1, 5], [0, 4]],
                    [[0, 6], [-1, -1], [0, 7], [1, 6], [0, 5]],
                    [[0, 7], [-1, -1], [0, 8], [1, 7], [0, 6]],
                    [[0, 8], [-1, -1], [-1, -1], [1, 8], [0, 7]],
                ],
                [
                    [[1, 0], [0, 0], [1, 1], [2, 0], [-1, -1]],
                    [[1, 1], [0, 1], [1, 2], [2, 1], [1, 0]],
                    [[1, 2], [0, 2], [1, 3], [2, 2], [1, 1]],
                    [[1, 3], [0, 3], [1, 4], [2, 3], [1, 2]],
                    [[1, 4], [0, 4], [1, 5], [2, 4], [1, 3]],
                    [[1, 5], [0, 5], [1, 6], [2, 5], [1, 4]],
                    [[1, 6], [0, 6], [1, 7], [2, 6], [1, 5]],
                    [[1, 7], [0, 7], [1, 8], [2, 7], [1, 6]],
                    [[1, 8], [0, 8], [-1, -1], [2, 8], [1, 7]],
                ],
                [
                    [[2, 0], [1, 0], [2, 1], [3, 0], [-1, -1]],
                    [[2, 1], [1, 1], [2, 2], [3, 1], [2, 0]],
                    [[2, 2], [1, 2], [2, 3], [3, 2], [2, 1]],
                    [[2, 3], [1, 3], [2, 4], [3, 3], [2, 2]],
                    [[2, 4], [1, 4], [2, 5], [3, 4], [2, 3]],
                    [[2, 5], [1, 5], [2, 6], [3, 5], [2, 4]],
                    [[2, 6], [1, 6], [2, 7], [3, 6], [2, 5]],
                    [[2, 7], [1, 7], [2, 8], [3, 7], [2, 6]],
                    [[2, 8], [1, 8], [-1, -1], [3, 8], [2, 7]],
                ],
                [
                    [[3, 0], [2, 0], [3, 1], [4, 0], [-1, -1]],
                    [[3, 1], [2, 1], [3, 2], [4, 1], [3, 0]],
                    [[3, 2], [2, 2], [3, 3], [4, 2], [3, 1]],
                    [[3, 3], [2, 3], [3, 4], [4, 3], [3, 2]],
                    [[3, 4], [2, 4], [3, 5], [4, 4], [3, 3]],
                    [[3, 5], [2, 5], [3, 6], [4, 5], [3, 4]],
                    [[3, 6], [2, 6], [3, 7], [4, 6], [3, 5]],
                    [[3, 7], [2, 7], [3, 8], [4, 7], [3, 6]],
                    [[3, 8], [2, 8], [-1, -1], [4, 8], [3, 7]],
                ],
                [
                    [[4, 0], [3, 0], [4, 1], [5, 0], [-1, -1]],
                    [[4, 1], [3, 1], [4, 2], [5, 1], [4, 0]],
                    [[4, 2], [3, 2], [4, 3], [5, 2], [4, 1]],
                    [[4, 3], [3, 3], [4, 4], [5, 3], [4, 2]],
                    [[4, 4], [3, 4], [4, 5], [5, 4], [4, 3]],
                    [[4, 5], [3, 5], [4, 6], [5, 5], [4, 4]],
                    [[4, 6], [3, 6], [4, 7], [5, 6], [4, 5]],
                    [[4, 7], [3, 7], [4, 8], [5, 7], [4, 6]],
                    [[4, 8], [3, 8], [-1, -1], [5, 8], [4, 7]],
                ],
                [
                    [[5, 0], [4, 0], [5, 1], [6, 0], [-1, -1]],
                    [[5, 1], [4, 1], [5, 2], [6, 1], [5, 0]],
                    [[5, 2], [4, 2], [5, 3], [6, 2], [5, 1]],
                    [[5, 3], [4, 3], [5, 4], [6, 3], [5, 2]],
                    [[5, 4], [4, 4], [5, 5], [6, 4], [5, 3]],
                    [[5, 5], [4, 5], [5, 6], [6, 5], [5, 4]],
                    [[5, 6], [4, 6], [5, 7], [6, 6], [5, 5]],
                    [[5, 7], [4, 7], [5, 8], [6, 7], [5, 6]],
                    [[5, 8], [4, 8], [-1, -1], [6, 8], [5, 7]],
                ],
                [
                    [[6, 0], [5, 0], [6, 1], [7, 0], [-1, -1]],
                    [[6, 1], [5, 1], [6, 2], [7, 1], [6, 0]],
                    [[6, 2], [5, 2], [6, 3], [7, 2], [6, 1]],
                    [[6, 3], [5, 3], [6, 4], [7, 3], [6, 2]],
                    [[6, 4], [5, 4], [6, 5], [7, 4], [6, 3]],
                    [[6, 5], [5, 5], [6, 6], [7, 5], [6, 4]],
                    [[6, 6], [5, 6], [6, 7], [7, 6], [6, 5]],
                    [[6, 7], [5, 7], [6, 8], [7, 7], [6, 6]],
                    [[6, 8], [5, 8], [-1, -1], [7, 8], [6, 7]],
                ],
                [
                    [[7, 0], [6, 0], [7, 1], [8, 0], [-1, -1]],
                    [[7, 1], [6, 1], [7, 2], [8, 1], [7, 0]],
                    [[7, 2], [6, 2], [7, 3], [8, 2], [7, 1]],
                    [[7, 3], [6, 3], [7, 4], [8, 3], [7, 2]],
                    [[7, 4], [6, 4], [7, 5], [8, 4], [7, 3]],
                    [[7, 5], [6, 5], [7, 6], [8, 5], [7, 4]],
                    [[7, 6], [6, 6], [7, 7], [8, 6], [7, 5]],
                    [[7, 7], [6, 7], [7, 8], [8, 7], [7, 6]],
                    [[7, 8], [6, 8], [-1, -1], [8, 8], [7, 7]],
                ],
                [
                    [[8, 0], [7, 0], [8, 1], [-1, -1], [-1, -1]],
                    [[8, 1], [7, 1], [8, 2], [-1, -1], [8, 0]],
                    [[8, 2], [7, 2], [8, 3], [-1, -1], [8, 1]],
                    [[8, 3], [7, 3], [8, 4], [-1, -1], [8, 2]],
                    [[8, 4], [7, 4], [8, 5], [-1, -1], [8, 3]],
                    [[8, 5], [7, 5], [8, 6], [-1, -1], [8, 4]],
                    [[8, 6], [7, 6], [8, 7], [-1, -1], [8, 5]],
                    [[8, 7], [7, 7], [8, 8], [-1, -1], [8, 6]],
                    [[8, 8], [7, 8], [-1, -1], [-1, -1], [8, 7]],
                ],
            ],
            dtype=np.int8,
        )

        # Position of both players represented as [row, col]
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
        # Ensures that if there are no walls left for the player in turn to place,
        # there are no path finding algorithms run to improve efficiency

        # Uses variable reference to simplify code with in_turn_pos, out_turn_pos
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

        # Retrieves the available moves for the both players in and out of turn
        in_turn_moves = self.nodes[in_turn_pos[0], in_turn_pos[1], 1:]
        out_turn_moves = self.nodes[out_turn_pos[0], out_turn_pos[1], 1:]

        # Blank array that will store the moves available as [[row, col], [row, col], ...]
        # Shape of blank array is 5x2 as there is a maximum of 5 places to move a piece to
        moves_available = np.full((5, 2), -1, dtype=np.int8)

        # Determines if the two pieces are directly next to each other
        # to calculate moves where player in turn jumps over other player
        # Otherwise, add moves to moves_available normally
        adjacent = np.bool8(False)
        for i in range(4):
            if (
                in_turn_moves[i][0] == out_turn_pos[0]
                and in_turn_moves[i][1] == out_turn_pos[1]
            ):
                adjacent = True

            else:
                moves_available[i] = in_turn_moves[i]

        # If the players are adjacent, determine if the player can jump over the other
        # or if there is no square to jump over to (due to wall, off the board)
        # find moves to the "left" and "right" (immediately adjacent)

        if adjacent:
            relative_pos = out_turn_pos - in_turn_pos
            if relative_pos[0] == -1 and relative_pos[1] == 0:
                can_jump = False
                for i in range(4):
                    if (
                        in_turn_pos[0] - 2 == out_turn_moves[i][0]
                        and in_turn_pos[1] == out_turn_moves[i][1]
                    ):
                        can_jump = True
                        break
                if can_jump:
                    moves_available[-1] = [in_turn_pos[0] - 2, in_turn_pos[1]]
                else:
                    for i in range(4):
                        if out_turn_moves[i][0] != -1 and not (
                            out_turn_moves[i][0] == in_turn_pos[0]
                            and out_turn_moves[i][1] == in_turn_pos[1]
                        ):
                            for j in range(0, 5):
                                if moves_available[j][0] == -1:
                                    moves_available[j] = out_turn_moves[i]
                                    break

            elif relative_pos[0] == 0 and relative_pos[1] == 1:
                can_jump = False
                for i in range(4):
                    if (
                        in_turn_pos[0] == out_turn_moves[i][0]
                        and in_turn_pos[1] + 2 == out_turn_moves[i][1]
                    ):
                        can_jump = True
                        break
                if can_jump:
                    moves_available[-1] = [in_turn_pos[0], in_turn_pos[1] + 2]
                else:
                    for i in range(4):
                        if out_turn_moves[i][0] != -1 and not (
                            out_turn_moves[i][0] == in_turn_pos[0]
                            and out_turn_moves[i][1] == in_turn_pos[1]
                        ):
                            for j in range(0, 5):
                                if moves_available[j][0] == -1:
                                    moves_available[j] = out_turn_moves[i]
                                    break
            elif relative_pos[0] == 1 and relative_pos[1] == 0:
                can_jump = False
                for i in range(4):
                    if (
                        in_turn_pos[0] + 2 == out_turn_moves[i][0]
                        and in_turn_pos[1] == out_turn_moves[i][1]
                    ):
                        can_jump = True
                        break
                if can_jump:
                    moves_available[-1] = [in_turn_pos[0] + 2, in_turn_pos[1]]

                else:
                    for i in range(4):
                        if out_turn_moves[i][0] != -1 and not (
                            out_turn_moves[i][0] == in_turn_pos[0]
                            and out_turn_moves[i][1] == in_turn_pos[1]
                        ):
                            for j in range(0, 5):
                                if moves_available[j][0] == -1:
                                    moves_available[j] = out_turn_moves[i]
                                    break
            elif relative_pos[0] == 0 and relative_pos[1] == -1:
                can_jump = False
                for i in range(4):
                    if (
                        in_turn_pos[0] == out_turn_moves[i][0]
                        and in_turn_pos[1] - 2 == out_turn_moves[i][1]
                    ):
                        can_jump = True
                        break
                if can_jump:
                    moves_available[-1] = [in_turn_pos[0], in_turn_pos[1] - 2]
                else:
                    for i in range(4):
                        if out_turn_moves[i][0] != -1 and not (
                            out_turn_moves[i][0] == in_turn_pos[0]
                            and out_turn_moves[i][1] == in_turn_pos[1]
                        ):
                            for j in range(0, 5):
                                if moves_available[j][0] == -1:
                                    moves_available[j] = out_turn_moves[i]
                                    break

        # Default array of what wall placeemnts and moves are possible
        # wall placeemnts are stored as [row, col, type]
        # where type - horizontal: 0 and vertical : 1
        # moves will be stored as [row, col, 2]
        walls_moves_available = np.array(
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
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1],
                [-1, -1, -1],
            ]
        )
        # Add moves to the end of walls_moves_available
        walls_moves_available[128:] = np.hstack(
            (moves_available, np.full((5, 1), 2, dtype=np.int8))
        )

        # If there are walls that can be placed,
        # ensure that there are no walls placed already
        # and no walls of other type preventing it from being placed
        if walls_left:
            if self.path_finding_mode == "BFS":
                search = Breadth_First_Search_Graph_Optim
            elif self.path_finding_mode == "DFS":
                search = Depth_First_Search_Graph_Optim
            elif self.path_finding_mode == "GBFS":
                search = Greedy_Best_First_Search_Graph_Optim
            elif self.path_finding_mode == "UCT":
                search = Uniform_Cost_Search_Graph_Optim
            elif self.path_finding_mode == "Astar":
                search = A_Star_Search_Graph_Optim
            for row in range(8):
                for col in range(8):
                    hor_found = False
                    ver_found = False
                    found = np.zeros(9, dtype=np.bool8)
                    for i in range(4):
                        if (
                            row == self.nodes[row + 1, col, i + 1, 0]
                            and col == self.nodes[row + 1, col, i + 1, 1]
                            and row == self.nodes[row + 1, col + 1, i + 1, 0]
                            and col + 1 == self.nodes[row + 1, col + 1, i + 1, 1]
                        ):
                            hor_found = True
                            for j in range(4):
                                if self.nodes[0, col, j, 1] == col + 1:
                                    found[0] = True
                                if self.nodes[1, col, j, 1] == col + 1:
                                    found[1] = True
                                if self.nodes[2, col, j, 1] == col + 1:
                                    found[2] = True
                                if self.nodes[3, col, j, 1] == col + 1:
                                    found[3] = True
                                if self.nodes[4, col, j, 1] == col + 1:
                                    found[4] = True
                                if self.nodes[5, col, j, 1] == col + 1:
                                    found[5] = True
                                if self.nodes[6, col, j, 1] == col + 1:
                                    found[6] = True
                                if self.nodes[7, col, j, 1] == col + 1:
                                    found[7] = True
                                if self.nodes[8, col, j, 1] == col + 1:
                                    found[8] = True
                            if (
                                (found[row] == True or found[row + 1] == True)
                                or (
                                    (row == 1 or row == 6)
                                    and found[row - 1] == False
                                    and found[row] == False
                                    and found[row + 1] == False
                                    and found[row + 2] == False
                                )
                                or (
                                    row > 1
                                    and row < 6
                                    and (found[row - 2] or found[row + 3])
                                    and found[row - 1] == False
                                    and found[row] == False
                                    and found[row + 1] == False
                                    and found[row + 2] == False
                                )
                                or (
                                    (row == 3 or row == 4)
                                    and found[row - 3] == False
                                    and found[row - 2] == False
                                    and found[row - 1] == False
                                    and found[row] == False
                                    and found[row + 1] == False
                                    and found[row + 2] == False
                                    and found[row + 3] == False
                                    and found[row + 4] == False
                                )
                            ):
                                if not search(
                                    self.nodes,
                                    self.p1_pos,
                                    np.int8(8),
                                    np.array([row, col, 0], dtype=np.int8),
                                ) or not search(
                                    self.nodes,
                                    self.p2_pos,
                                    np.int8(0),
                                    np.array([row, col, 0], dtype=np.int8),
                                ):
                                    walls_moves_available[row * 8 + col] = [-1, -1, -1]
                            else:
                                walls_moves_available[row * 8 + col] = [-1, -1, -1]

                    if hor_found == False:
                        walls_moves_available[row * 8 + col] = [-1, -1, -1]
                    found = np.zeros(9, dtype=np.bool8)
                    for i in range(4):
                        if (
                            row == self.nodes[row, col + 1, i + 1, 0]
                            and col == self.nodes[row, col + 1, i + 1, 1]
                            and row + 1 == self.nodes[row + 1, col + 1, i + 1, 0]
                            and col == self.nodes[row + 1, col + 1, i + 1, 1]
                        ):
                            ver_found = True
                            for j in range(4):
                                if self.nodes[row, 0, j, 0] == row + 1:
                                    found[0] = True
                                if self.nodes[row, 1, j, 0] == row + 1:
                                    found[1] = True
                                if self.nodes[row, 2, j, 0] == row + 1:
                                    found[2] = True
                                if self.nodes[row, 3, j, 0] == row + 1:
                                    found[3] = True
                                if self.nodes[row, 4, j, 0] == row + 1:
                                    found[4] = True
                                if self.nodes[row, 5, j, 0] == row + 1:
                                    found[5] = True
                                if self.nodes[row, 6, j, 0] == row + 1:
                                    found[6] = True
                                if self.nodes[row, 7, j, 0] == row + 1:
                                    found[7] = True
                                if self.nodes[row, 8, j, 0] == row + 1:
                                    found[8] = True
                            if (
                                (found[col] == True or found[col + 1] == True)
                                or (
                                    (col == 1 or col == 6)
                                    and found[col - 1] == False
                                    and found[col] == False
                                    and found[col + 1] == False
                                    and found[col + 2] == False
                                )
                                or (
                                    col > 1
                                    and col < 6
                                    and (found[col - 2] or found[col + 3])
                                    and found[col - 1] == False
                                    and found[col] == False
                                    and found[col + 1] == False
                                    and found[col + 2] == False
                                )
                                or (
                                    (col == 3 or col == 4)
                                    and found[col - 3] == False
                                    and found[col - 2] == False
                                    and found[col - 1] == False
                                    and found[col] == False
                                    and found[col + 1] == False
                                    and found[col + 2] == False
                                    and found[col + 3] == False
                                    and found[col + 4] == False
                                )
                            ):
                                if not search(
                                    self.nodes,
                                    self.p1_pos,
                                    np.int8(8),
                                    np.array([row, col, 1], dtype=np.int8),
                                ) or not search(
                                    self.nodes,
                                    self.p2_pos,
                                    np.int8(0),
                                    np.array([row, col, 1], dtype=np.int8),
                                ):
                                    walls_moves_available[64 + row * 8 + col] = [
                                        -1,
                                        -1,
                                        -1,
                                    ]
                            else:
                                walls_moves_available[64 + row * 8 + col] = [-1, -1, -1]

                    if ver_found == False:
                        walls_moves_available[64 + row * 8 + col] = [-1, -1, -1]
        return walls_moves_available
        # Array for all algebraic moves as strings
        algebraic_moves = []
        for i in range(133):
            if walls_moves_available[i][0] != -1:
                if walls_left:
                    if walls_moves_available[i][2] == 0:
                        algebraic_moves.append(
                            f"{chr(97+walls_moves_available[i][1])}{walls_moves_available[i][0]+1}h"
                        )
                    elif walls_moves_available[i][2] == 1:
                        algebraic_moves.append(
                            f"{chr(97+walls_moves_available[i][1])}{walls_moves_available[i][0]+1}v"
                        )
                if walls_moves_available[i][2] == 2:
                    algebraic_moves.append(
                        f"{chr(97+walls_moves_available[i][1])}{walls_moves_available[i][0]+1}"
                    )
        return algebraic_moves

    def take_action(self, action):
        if action[0] > 8 or action[1] > 8:
            raise IndexError
        # Converts algebraic notated move to numpy array

        # If the move is a normal move, change the player pos
        if action[2] == 2:  # player move
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
            if action[2] == 0:  # horizontal wall move
                for i in range(1, 5):
                    if (
                        self.nodes[action[0] + 1, action[1]][i][0]
                        == self.nodes[action[0], action[1]][0][0]
                        and self.nodes[action[0] + 1, action[1]][i][1]
                        == self.nodes[action[0], action[1]][0][1]
                    ):
                        self.nodes[action[0] + 1, action[1]][i] = [-1, -1]
                    if (
                        self.nodes[action[0], action[1]][i][0]
                        == self.nodes[action[0] + 1, action[1]][0][0]
                        and self.nodes[action[0], action[1]][i][1]
                        == self.nodes[action[0] + 1, action[1]][0][1]
                    ):
                        self.nodes[action[0], action[1]][i] = [-1, -1]
                    if (
                        self.nodes[action[0] + 1, action[1] + 1][i][0]
                        == self.nodes[action[0], action[1] + 1][0][0]
                        and self.nodes[action[0] + 1, action[1] + 1][i][1]
                        == self.nodes[action[0], action[1] + 1][0][1]
                    ):
                        self.nodes[action[0] + 1, action[1] + 1][i] = [-1, -1]
                    if (
                        self.nodes[action[0], action[1] + 1][i][0]
                        == self.nodes[action[0] + 1, action[1] + 1][0][0]
                        and self.nodes[action[0], action[1] + 1][i][1]
                        == self.nodes[action[0] + 1, action[1] + 1][0][1]
                    ):
                        self.nodes[action[0], action[1] + 1][i] = [-1, -1]
            else:  # vertical wall move
                for i in range(5):
                    if (
                        self.nodes[action[0], action[1] + 1][i][0]
                        == self.nodes[action[0], action[1]][0][0]
                        and self.nodes[action[0], action[1] + 1][i][1]
                        == self.nodes[action[0], action[1]][0][1]
                    ):
                        self.nodes[action[0], action[1] + 1][i] = [-1, -1]
                    if (
                        self.nodes[action[0], action[1]][i][0]
                        == self.nodes[action[0], action[1] + 1][0][0]
                        and self.nodes[action[0], action[1]][i][1]
                        == self.nodes[action[0], action[1] + 1][0][1]
                    ):
                        self.nodes[action[0], action[1]][i] = [-1, -1]
                    if (
                        self.nodes[action[0] + 1, action[1] + 1][i][0]
                        == self.nodes[action[0] + 1, action[1]][0][0]
                        and self.nodes[action[0] + 1, action[1] + 1][i][1]
                        == self.nodes[action[0] + 1, action[1]][0][1]
                    ):
                        self.nodes[action[0] + 1, action[1] + 1][i] = [-1, -1]
                    if (
                        self.nodes[action[0] + 1, action[1]][i][0]
                        == self.nodes[action[0] + 1, action[1] + 1][0][0]
                        and self.nodes[action[0] + 1, action[1]][i][1]
                        == self.nodes[action[0] + 1, action[1] + 1][0][1]
                    ):
                        self.nodes[action[0] + 1, action[1]][i] = [-1, -1]
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

                if [row, column + 1] in self.nodes[row, column, 1:].tolist():
                    line.append("\u2502")
                else:
                    if column != 8:
                        line.append("\u2503")
                if row != 8:
                    # if no horizontal wall below (row, column) place thin lines
                    # otherwise, place thick lines to show a wall
                    if [row + 1, column] in self.nodes[row, column, 1:].tolist():
                        line_below.append("\u2500\u2500\u2500")
                    else:
                        line_below.append("\u2501\u2501\u2501")
                    if column != 8:
                        # variables describing if there is part of a wall above the intersection
                        north = False
                        east = False
                        south = False
                        west = False

                        """
                        If row = 0, column = 0
                        X1 X2
                          I
                        X3 X4
                        looking at intersection I
                        """
                        if [row, column] not in self.nodes[row, column + 1].tolist():
                            # wall between X1 and X2
                            south = True
                        if [row, column + 1] not in self.nodes[
                            row + 1, column + 1, 1:
                        ].tolist():
                            # wall between X2 and X4
                            east = True
                        if [row + 1, column] not in self.nodes[
                            row + 1, column + 1, 1:
                        ].tolist():
                            # wall between X3 and X4
                            north = True
                        if [row, column] not in self.nodes[
                            row + 1, column, 1:
                        ].tolist():
                            west = True
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
