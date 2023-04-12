import numpy as np
from numba import int8, boolean, njit
from numba.experimental import jitclass

from .path_finding_optimised import Breadth_First_Search_Graph_Optim
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
    def __init__(self):
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
        self.p1_pos = np.array([0, 4], dtype=np.int8)
        self.p2_pos = np.array([8, 4], dtype=np.int8)

        self.p1_walls_placed = np.int8(0)
        self.p2_walls_placed = np.int8(0)

        self.turn = np.int8(1)
        self.over = np.bool8(False)

    # @profile
    def get_available_moves(self):
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

        in_turn_moves = self.nodes[in_turn_pos[0], in_turn_pos[1], 1:]
        out_turn_moves = self.nodes[out_turn_pos[0], out_turn_pos[1], 1:]

        moves_available = np.full((5, 2), -1, dtype=np.int8)

        adjacent = np.bool8(False)
        for i in range(4):
            if (
                in_turn_moves[i][0] == out_turn_pos[0]
                and in_turn_moves[i][1] == out_turn_pos[1]
            ):
                adjacent = True

            else:
                moves_available[i] = in_turn_moves[i]
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
        walls_moves_available[128:] = np.hstack(
            (moves_available, np.full((5, 1), 2, dtype=np.int8))
        )

        if walls_left:
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
                            # print(found, row, col, "h")
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
                                if not Breadth_First_Search_Graph_Optim(
                                    self.nodes,
                                    self.p1_pos,
                                    np.int8(8),
                                    np.array([row, col, 0], dtype=np.int8),
                                ) or not Breadth_First_Search_Graph_Optim(
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
                                if not Breadth_First_Search_Graph_Optim(
                                    self.nodes,
                                    self.p1_pos,
                                    np.int8(8),
                                    np.array([row, col, 1], dtype=np.int8),
                                ) or not Breadth_First_Search_Graph_Optim(
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

    def make_move(self, alg_move):
        if len(alg_move) == 2:
            move = np.array([int(alg_move[1]) - 1, ord(alg_move[0]) - 97, 2])
        elif len(alg_move) == 3:
            if alg_move[2] == "h":
                move = np.array([int(alg_move[1]) - 1, ord(alg_move[0]) - 97, 0])
            elif alg_move[2] == "v":
                move = np.array([int(alg_move[1]) - 1, ord(alg_move[0]) - 97, 1])

        # move is of format (row, column, type - 0: hor, 1: ver, 2: nor)
        if move[2] == 2:  # player move
            if self.turn == 1:
                self.p1_pos = move[0:2]
                if self.p1_pos[0] == 8:
                    self.over = True
                else:
                    self.turn = 2
            else:
                self.p2_pos = move[0:2]
                if self.p2_pos[0] == 0:
                    self.over = True
                else:
                    self.turn = 1
        else:
            if move[2] == 0:  # horizontal wall move
                for i in range(1, 5):
                    if (
                        self.nodes[move[0] + 1, move[1]][i][0]
                        == self.nodes[move[0], move[1]][0][0]
                        and self.nodes[move[0] + 1, move[1]][i][1]
                        == self.nodes[move[0], move[1]][0][1]
                    ):
                        self.nodes[move[0] + 1, move[1]][i] = [-1, -1]
                    if (
                        self.nodes[move[0], move[1]][i][0]
                        == self.nodes[move[0] + 1, move[1]][0][0]
                        and self.nodes[move[0], move[1]][i][1]
                        == self.nodes[move[0] + 1, move[1]][0][1]
                    ):
                        self.nodes[move[0], move[1]][i] = [-1, -1]
                    if (
                        self.nodes[move[0] + 1, move[1] + 1][i][0]
                        == self.nodes[move[0], move[1] + 1][0][0]
                        and self.nodes[move[0] + 1, move[1] + 1][i][1]
                        == self.nodes[move[0], move[1] + 1][0][1]
                    ):
                        self.nodes[move[0] + 1, move[1] + 1][i] = [-1, -1]
                    if (
                        self.nodes[move[0], move[1] + 1][i][0]
                        == self.nodes[move[0] + 1, move[1] + 1][0][0]
                        and self.nodes[move[0], move[1] + 1][i][1]
                        == self.nodes[move[0] + 1, move[1] + 1][0][1]
                    ):
                        self.nodes[move[0], move[1] + 1][i] = [-1, -1]
            else:  # vertical wall move
                for i in range(5):
                    if (
                        self.nodes[move[0], move[1] + 1][i][0]
                        == self.nodes[move[0], move[1]][0][0]
                        and self.nodes[move[0], move[1] + 1][i][1]
                        == self.nodes[move[0], move[1]][0][1]
                    ):
                        self.nodes[move[0], move[1] + 1][i] = [-1, -1]
                    if (
                        self.nodes[move[0], move[1]][i][0]
                        == self.nodes[move[0], move[1] + 1][0][0]
                        and self.nodes[move[0], move[1]][i][1]
                        == self.nodes[move[0], move[1] + 1][0][1]
                    ):
                        self.nodes[move[0], move[1]][i] = [-1, -1]
                    if (
                        self.nodes[move[0] + 1, move[1] + 1][i][0]
                        == self.nodes[move[0] + 1, move[1]][0][0]
                        and self.nodes[move[0] + 1, move[1] + 1][i][1]
                        == self.nodes[move[0] + 1, move[1]][0][1]
                    ):
                        self.nodes[move[0] + 1, move[1] + 1][i] = [-1, -1]
                    if (
                        self.nodes[move[0] + 1, move[1]][i][0]
                        == self.nodes[move[0] + 1, move[1] + 1][0][0]
                        and self.nodes[move[0] + 1, move[1]][i][1]
                        == self.nodes[move[0] + 1, move[1] + 1][0][1]
                    ):
                        self.nodes[move[0] + 1, move[1]][i] = [-1, -1]
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


# board = QuoridorGraphicalBoardOptim()
# board.make_move(np.array([0, 4, 0]))
# board.display_beautiful()
# board.get_available_moves()
# # print(board.nodes)
# board.display_beautiful()


# @njit
# def custom_isin(out_turn_pos, out_turn_moves):
#     return ~(
#         np.count_nonzero(
#             (out_turn_moves - out_turn_pos - np.array([-1, 0]))
#             .astype(np.bool8)
#             .sum(axis=1)
#         )
#         == 4
#     )


# @njit
# def custom_isin_for(out_turn_pos, out_turn_moves):
#     for i in range(4):
#         if (
#             out_turn_moves[i][0] == out_turn_pos[0] - 1
#             and out_turn_moves[i][1] == out_turn_pos[1]
#         ):
#             return True
#         return False
#     # return (
#     #         np.count_nonzero(
#     #             np.array(
#     #                 out_turn_moves - out_turn_pos - np.array[-1, 0],
#     #                 dtype=np.bool8,
#     #             ).sum(axis=1)
#     #         )
#     #         == 4
#     #     )


# setup = """
# import numpy as np
# from numba import njit, int8, boolean

# a = np.array([[-1, -1], [0, 5], [1, 4], [0, 3]], dtype=np.int8)
# b = np.array([0, 4], dtype=np.int8)

# @njit(boolean(int8[:], int8[:,:]))
# def custom_isin_one(out_turn_pos, out_turn_moves):
#     for move in out_turn_moves:
#         if np.array_equal(move, out_turn_pos + np.array([-1, 0])):
#             return True
#     return False

# @njit(boolean(int8[:], int8[:,:]))
# def custom_isin_two(out_turn_pos, out_turn_moves):
#     for i in range(4):
#         if (
#             out_turn_moves[i][0] == out_turn_pos[0] - 1
#             and out_turn_moves[i][1] == out_turn_pos[1]
#         ):
#             return True
#     return False

# """

# # print(a - b)


# # import timeit

# # print(timeit.timeit("custom_isin_one(b,a)", setup=setup, number=1))
# # print(timeit.timeit("custom_isin_two(b,a)", setup=setup, number=1))

# # print(timeit.timeit("custom_isin_one(b,a)", setup=setup) / 1_000_000)
# # print(timeit.timeit("custom_isin_two(b,a)", setup=setup) / 1_000_000)

# # # if __name__ == "__main__":
# # #     print("not supposed to be run")
# # #     raise ImportError

# print(
#     np.vstack(
#         (
#             np.hstack(
#                 (
#                     np.indices((8, 8), dtype=np.int8).reshape(2, -1).T,
#                     np.full((64, 1), 0, dtype=np.int8),
#                 )
#             ),
#             np.hstack(
#                 (
#                     np.indices((8, 8), dtype=np.int8).reshape(2, -1).T,
#                     np.full((64, 1), 1, dtype=np.int8),
#                 )
#             ),
#             np.full((5, 3), -1, dtype=np.int8),
#         )
#     )
# )
