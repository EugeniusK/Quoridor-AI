import numpy as np
import time
import sys
from path_finding import (
    Breadth_First_Search_BitBoard,
    Greedy_Best_First_Search_BitBoard,
)

north_mask = np.ones((17, 17), dtype=np.bool_)
north_mask[15:] = False
east_mask = np.rot90(north_mask, 3)
south_mask = np.rot90(north_mask, 2)
west_mask = np.rot90(north_mask, 1)

short_north_mask = np.ones((17, 17), dtype=np.bool_)
short_north_mask[16:] = False
short_east_mask = np.rot90(short_north_mask, 3)
short_south_mask = np.rot90(short_north_mask, 2)
short_west_mask = np.rot90(short_north_mask, 1)


class QuoridorBitBoard:
    def __init__(self):
        self.walls = np.zeros((17, 17), dtype=np.bool_)

        self.p1_pos = np.zeros((17, 17), dtype=np.bool_)
        self.p1_pos[0][8] = True

        self.p2_pos = np.zeros((17, 17), dtype=np.bool_)
        self.p2_pos[16][8] = True

        self.p1_walls_placed = np.int8(0)
        self.p2_walls_placed = np.int8(0)

        self.turn = np.bool_(False)  # False if player 1 turn, True if player 2 turn

        self.over = np.bool_(False)

    def get_available_moves(self):
        # in_turn_pos references the 17x17 array that stores location of player in turn
        # out_turn_pos references the 17x17 array that stores location of the player out of turn
        walls_left = True  # possible wall placements calculated only when player in turn hasn't placed 10 walls
        if self.turn == False:
            # player 1's turn
            in_turn_pos = self.p1_pos
            out_turn_pos = self.p2_pos

            if self.p1_walls_placed == np.uint(10):
                walls_left = False
        elif self.turn == True:
            # player 2's turn
            in_turn_pos = self.p2_pos
            out_turn_pos = self.p1_pos

            if self.p2_walls_placed == np.uint(10):
                walls_left = False

        player_moves = np.zeros((17, 17), dtype=np.bool_)
        # moves the player in each cardinal direction
        # then checks if the direction of move doesn't go off board using a mask and AND operation
        # then checks if the move doesn't land on a wall
        # then adds move if it doesn't land on a wall

        # If the player doesn't go off the board
        # and If it doesn't land on a wall
        # add move

        if True in np.roll(in_turn_pos, -17) & short_north_mask:
            if True not in np.roll(in_turn_pos, -17) & self.walls:
                player_moves += np.roll(in_turn_pos, -34)
        if True in np.roll(in_turn_pos, 1) & short_east_mask:
            if True not in np.roll(in_turn_pos, 1) & self.walls:
                player_moves += np.roll(in_turn_pos, 2)
        if True in np.roll(in_turn_pos, 17) & short_south_mask:
            if True not in np.roll(in_turn_pos, 17) & self.walls:
                player_moves += np.roll(in_turn_pos, 34)
        if True in np.roll(in_turn_pos, -1) & short_west_mask:
            if True not in np.roll(in_turn_pos, -1) & self.walls:
                player_moves += np.roll(in_turn_pos, -2)
        # if there is a overlap in the two player positions
        if True in player_moves & out_turn_pos:
            # finds the position of out of turn player relative to in turn player
            # then if the jump over the out of turn player is allowed - doesn't go off board and no wall,
            #     add the move that jumps in a straight line above out of turn player
            # if there is a wall or the edgee of the board blocking the move,
            #     check if each move to the side is possible then add
            relative_pos = np.subtract(
                np.where(in_turn_pos == True), np.where(out_turn_pos == True)
            )
            if np.array_equal(
                relative_pos,
                np.array([[2], [0]]),
            ):
                # out of turn player is north of in turn player
                if (
                    True in np.roll(out_turn_pos, -17) & short_north_mask
                    and True not in np.roll(out_turn_pos, -17) & self.walls
                ):
                    player_moves += np.roll(out_turn_pos, -34)
                else:
                    if True in np.roll(out_turn_pos, 1) & short_east_mask:
                        if True not in np.roll(out_turn_pos, 1) & self.walls:
                            player_moves += np.roll(out_turn_pos, 2)
                    if True in np.roll(out_turn_pos, -1) & short_west_mask:
                        if True not in np.roll(out_turn_pos, -1) & self.walls:
                            player_moves += np.roll(out_turn_pos, -2)
            elif np.array_equal(
                relative_pos,
                np.array([[0], [-2]]),
            ):
                # out of turn player is east of in turn player
                if (
                    True in np.roll(out_turn_pos, 1) & short_east_mask
                    and True not in np.roll(out_turn_pos, 1) & self.walls
                ):
                    player_moves += np.roll(out_turn_pos, 2)
                else:
                    if True in np.roll(out_turn_pos, -17) & short_north_mask:
                        if True not in np.roll(out_turn_pos, -17) & self.walls:
                            player_moves += np.roll(out_turn_pos, -34)
                    if True in np.roll(out_turn_pos, 17) & short_south_mask:
                        if True not in np.roll(out_turn_pos, 17) & self.walls:
                            player_moves += np.roll(out_turn_pos, 34)
            elif np.array_equal(
                relative_pos,
                np.array([[-2], [0]]),
            ):
                # out of turn player is south of in turn player
                if (
                    True in np.roll(out_turn_pos, 17) & short_south_mask
                    and True not in np.roll(out_turn_pos, 17) & self.walls
                ):
                    player_moves += np.roll(out_turn_pos, 34)
                else:
                    if True in np.roll(out_turn_pos, 1) & short_east_mask:
                        if True not in np.roll(out_turn_pos, 1) & self.walls:
                            player_moves += np.roll(out_turn_pos, 2)
                    if True in np.roll(out_turn_pos, -1) & short_west_mask:
                        if True not in np.roll(out_turn_pos, -1) & self.walls:
                            player_moves += np.roll(out_turn_pos, -2)
            elif np.array_equal(
                relative_pos,
                np.array([[0], [2]]),
            ):
                # out of turn player is west of in turn player
                if (
                    True in np.roll(out_turn_pos, -1) & short_west_mask
                    and True not in np.roll(out_turn_pos, -1) & self.walls
                ):
                    player_moves += np.roll(out_turn_pos, -2)
                else:
                    if True in np.roll(out_turn_pos, -17) & short_north_mask:
                        if True not in np.roll(out_turn_pos, -17) & self.walls:
                            player_moves += np.roll(out_turn_pos, -34)
                    if True in np.roll(out_turn_pos, 17) & short_south_mask:
                        if True not in np.roll(out_turn_pos, 17) & self.walls:
                            player_moves += np.roll(out_turn_pos, 34)
        player_moves_index = np.array(
            np.where(player_moves & ~out_turn_pos), dtype=np.int8
        ).T

        if walls_left == True:
            sliding_horizontal_walls = np.reshape(
                np.lib.stride_tricks.sliding_window_view(self.walls[1::2], (1, 3)),
                (120, 3),
            )
            horizontal_walls = np.vstack(
                (
                    np.hstack(
                        (
                            np.reshape(~sliding_horizontal_walls.any(axis=1), (8, 15))[
                                :, ::2
                            ],
                            np.zeros((8, 1), dtype=np.bool_),
                        )
                    ),
                    np.zeros((1, 9), dtype=np.bool_),
                )
            )
            horizontal_walls_index = np.array(
                np.where(horizontal_walls), dtype=np.int8
            ).T
            sliding_vertical_walls = np.reshape(
                np.lib.stride_tricks.sliding_window_view(
                    np.fliplr(np.rot90(self.walls, 3)), (1, 3)
                ),
                (17, 15, 3),
            )  # [1::2, ::2]
            vertical_walls = np.vstack(
                (
                    np.hstack(
                        (
                            np.fliplr(np.rot90(~sliding_vertical_walls.any(axis=2), 3))[
                                ::2, 1::2
                            ],
                            np.zeros((8, 1), dtype=np.bool_),
                        )
                    ),
                    np.zeros((1, 9), dtype=np.bool_),
                )
            )

            vertical_walls_index = np.array(np.where(vertical_walls), dtype=np.int8).T
        # maximum number of horizontal wall placements is 8*8 = 64
        # maxmium number of vertical wall placements is 8*8 = 64
        # maximum number of moves is 5
        # so, combining them into an array of 133*2 is possible
        # the 0~63 rows will be filled with possible horizontal wall placements
        # the 64~127 rows will be filled with possible vertical wall placements
        # the 128~132 rows will be filled with possible player moves
        # unused indexes will be filled with -1 (maximum value allowed with np.int8)
        # final column in array represents type of move - 0: horizontal wall, 1: vertical wall, 2: player move
        moves = np.zeros((133, 3), dtype=np.int8)
        moves.fill(-1)
        if walls_left == True:
            moves[0 : 0 + len(horizontal_walls_index)] = np.hstack(
                (
                    horizontal_walls_index,
                    np.zeros((len(horizontal_walls_index), 1), dtype=np.int8),
                )
            )
            moves[64 : 64 + len(vertical_walls_index)] = np.hstack(
                (
                    vertical_walls_index,
                    np.ones((len(vertical_walls_index), 1), dtype=np.int8),
                )
            )
        moves[128 : 128 + len(player_moves_index)] = np.hstack(
            (
                player_moves_index,
                np.full((len(player_moves_index), 1), 2, dtype=np.int8),
            )
        )
        # print(moves)
        if walls_left == True:
            for m in range(128):
                # print(moves[m])
                # start = time.time()
                if (
                    Breadth_First_Search_BitBoard(
                        self.p1_pos, self.walls, np.int8(16), moves[m]
                    )
                    == False
                    or Breadth_First_Search_BitBoard(
                        self.p2_pos, self.walls, np.int8(0), moves[m]
                    )
                    == False
                ):
                    moves[m] = [-1, -1, -1]
                # print(time.time() - start)
        return moves

    def make_move(self, move):

        if move[2] == 2:  # player move
            if self.turn == False:  # player 1's turn
                self.p1_pos = np.zeros((17, 17), dtype=np.bool_)
                self.p1_pos[move[0]][move[1]] = True
                if move[0] == 16:
                    self.over = True
                else:
                    self.turn = True
            else:  # player 2's turn
                self.p2_pos = np.zeros((17, 17), dtype=np.bool_)
                self.p2_pos[move[0]][move[1]] = True
                if move[0] == 0:
                    self.over = True
                else:
                    self.turn = False
        else:
            if move[2] == 0:  # horizontal wall
                self.walls[move[0] * 2 + 1, move[1] * 2 : move[1] * 2 + 3] = True
            elif move[2] == 1:  # vertical wall
                self.walls[move[0] * 2 : move[0] * 2 + 3, move[1] * 2 + 1] = True
            else:
                raise ValueError
            if self.turn == False:
                self.p1_walls_placed += 1
                self.turn = True
            elif self.turn == True:
                self.p2_walls_placed += 1
                self.turn = False

    def display_beautiful(self):
        for row in range(9):
            line = []
            line_below = []
            for column in range(9):
                if self.p1_pos[row * 2][column * 2] == True:
                    line.append(" 1 ")
                elif self.p2_pos[row * 2][column * 2] == True:
                    line.append(" 2 ")
                else:
                    line.append("   ")

                if column != 8:
                    if self.walls[row * 2][column * 2 + 1] == False:
                        line.append("\u2502")
                    else:
                        line.append("\u2503")
                if row != 8:
                    if self.walls[row * 2 + 1][column * 2] == False:
                        line_below.append("\u2500\u2500\u2500")
                    else:
                        line_below.append("\u2501\u2501\u2501")
                    if column != 8:
                        """
                        NWN
                        WWW
                        NWN

                        """

                        north = self.walls[row * 2][column * 2 + 1]
                        east = self.walls[row * 2 + 1][column * 2 + 2]
                        south = self.walls[row * 2 + 2][column * 2 + 1]
                        west = self.walls[row * 2 + 1][column * 2]
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
            print("".join(line))
            print("".join(line_below))

    def is_over(self):
        if self.over == True:
            return True
        else:
            return False
