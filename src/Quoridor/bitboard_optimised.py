import numpy as np
import time
import sys
from numba import njit, int32, uint32, int64, uint64, int8, boolean
from numba.experimental import jitclass
from bitboard_pathfinding import (
    BreadthFirstSearch_Bitboard,
    DepthFirstSearch_Bitboard,
    GreedyBestFirstSearch_Bitboard,
    UniformCostSearch_Bitboard,
    AStarSearch_Bitboard,
)

# spec = [
#     ("p1", uint64[:]),
#     ("p2", uint64[:]),
#     ("walls", uint64[:]),
#     ("p1_walls_placed", int8),
#     ("p2_walls_placed", int8),
#     ("turn", int8),
#     ("over", boolean),
# ]


@njit(cache=True)
def shift_bitboard(bitboard, shift):
    # right is positive shift EAST
    """
    0001 0000 0000 --> 0000 1000 0000 = everything >> 1 and add 0000 1000 0000
    0000 1000 0000 is equal to roll init (0000 0001 0000) and << 4-1
    BUT IF 0000 0001 >> 1 = 0000 0000
    using above, 0000 0001 >> 1 ??= 0000 0000 + 1000 0000

    """
    if shift > 0 and shift < 64:
        rshift = np.uint64(shift)
        lshift = np.uint64(64 - shift)
        copy_bitboard = (bitboard >> rshift) + (np.roll(bitboard, 1) << lshift)
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        if bitboard[0] == 0:
            copy_bitboard[0] = 0
    elif shift < 0 and shift > -64:
        rshift = np.uint64(64 + shift)
        lshift = np.uint64(-shift)
        copy_bitboard = (bitboard << lshift) + (np.roll(bitboard, -1) >> rshift)
        if bitboard[4] == 0:
            copy_bitboard[4] = 0
    return copy_bitboard


# @jitclass(spec)
class QuoridorBitBoard:
    def __init__(self, path_finding_mode="BFS"):
        # Methods of representing Quoridor bitboards are
        # - use 3 17x17 array of bits to represent location of p1, p2 and walls
        #   which requires 3 sets of 6 64 bit integers (384)
        #   31 bits are UNUSED at the end
        # 0~32 are 5th
        # 33~96 are 4th
        # 97~160 are 3th
        # 161~224 are 2nd
        # 225~288 are 1st

        self.path_finding_mode = path_finding_mode
        self.p1 = np.array([0, 0, 0, 0, 2**39], dtype=np.uint64)
        self.p2 = np.array([2**55, 0, 0, 0, 0], dtype=np.uint64)
        self.walls = np.array([0, 0, 0, 0, 0], dtype=np.uint64)

        # board is represented as
        # 9   │   │   │   │ 2 │   │   │   │
        # .───┼───┼───┼───┼───┼───┼───┼───┼───
        # 8   │   │   │   │   │   │   │   │
        # .───┼───┼───┼───┼───┼───┼───┼───┼───
        # 7   │   │   │   │   │   │   │   │
        # .───┼───┼───┼───┼───┼───┼───┼───┼───
        # 6   │   │   │   │   │   │   │   │
        # .───┼───┼───┼───┼───┼───┼───┼───┼───
        # 5   │   │   │   │   │   │   │   │
        # .───┼───┼───┼───┼───┼───┼───┼───┼───
        # 4   │   │   │   │   │   │   │   │
        # .───┼───┼───┼───┼───┼───┼───┼───┼───
        # 3   │   │   │   │   │   │   │   │
        # .───┼───┼───┼───┼───┼───┼───┼───┼───
        # 2   │   │   │   │   │   │   │   │
        # .───┼───┼───┼───┼───┼───┼───┼───┼───
        # 1   │   │   │   │ 1 │   │   │   │
        # . a   b   c   d   e   f   g   h   i
        # location a9 is MSB of 1st 64 bit, horizontal wall below g8 is LSB
        # location i1 is 31st bit of 5th 64 bit (from LSB), insection to NE of a1 is MSB of

        self.p1_walls_placed = np.int8(0)
        self.p2_walls_placed = np.int8(0)

        # Player who is in turn
        self.turn = np.int8(1)

        # If the game is over or not
        self.over = np.bool8(False)
        # 63~60 bits represent the number of walls p1 has placed
        # 59~56 bits represent the number of walls p2 has placed
        # 1 bit represents the player who is in turn - 0: p1, 1: p2
        # 0 bit represents if the game is over - 0: False, 1: True
        # All above counted from RHS

    def _place_wall(self, wall_number):
        # wall number indexed from 0 to 127
        # 0~63 are horizontal 64~127 are vertical

        # On bitboard, idx x is in
        # 0~32 are 5th int
        # 33~96 are 4th int
        # 97~160 are 3th int
        # 161~224 are 2nd int
        # 225~288 are 1st int

        if wall_number < 64:
            # horizontal wall placed
            idx_wall = (
                (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
                (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
                (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
            )
        elif wall_number < 128:
            # vertical wall placed
            idx_wall = (
                ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8),
                ((wall_number % 64) // 8 + 1) * 34
                - 19
                - 2 * ((wall_number % 64) % 8)
                + 17,
                ((wall_number % 64) // 8 + 1) * 34
                - 19
                - 2 * ((wall_number % 64) % 8)
                + 34,
            )
        else:
            raise IndexError

        for idx in idx_wall:
            # depending on the index of the wall that has to be placed, different uint64 has to be modified
            # idx 0 is i1, idx 288 is a9
            if 0 <= idx <= 32:
                self.walls[4] += 2 ** (idx + 31)
            elif 33 <= idx <= 96:
                self.walls[3] += 2 ** (idx - 33)
            elif 97 <= idx <= 160:
                self.walls[2] += 2 ** (idx - 97)
            elif 161 <= idx <= 224:
                self.walls[1] += 2 ** (idx - 161)
            elif 225 <= idx <= 288:
                self.walls[0] += 2 ** (idx - 225)

    def _move_player(self, bitboard_in_turn, bitboard_out_turn, move_number):
        """
        Returns the player bitboard with the move applied"""
        # move number from 128 to 143
        # corresponds to NW, NN, NE, N - EN, EE, ES, E - SE, SS, SW, S - WS, WW, WN, W
        # North, West are negative shifts
        # South, West are negative shifts

        if move_number == 128:  # NW
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, -2)
        elif move_number == 129:  # NN
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, -34)
        elif move_number == 130:  # NE
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, 2)
        elif move_number == 131:  # N
            bitboard_in_turn = shift_bitboard(bitboard_in_turn, -34)
        elif move_number == 132:  # EN
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, -34)
        elif move_number == 133:  # EE
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, 2)
        elif move_number == 134:  # ES
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, 34)
        elif move_number == 135:  # E
            bitboard_in_turn = shift_bitboard(bitboard_in_turn, 2)
        elif move_number == 136:  # SE
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, 2)
        elif move_number == 137:  # SS
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, 34)
        elif move_number == 138:  # SW
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, -2)
        elif move_number == 139:  # S
            bitboard_in_turn = shift_bitboard(bitboard_in_turn, 34)
        elif move_number == 140:  # WS
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, 34)
        elif move_number == 141:  # WW
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, -2)
        elif move_number == 142:  # WN
            bitboard_in_turn = shift_bitboard(bitboard_out_turn, -34)
        elif move_number == 143:  # W
            bitboard_in_turn = shift_bitboard(bitboard_in_turn, -2)

    def take_action(self, move_number):
        if self.turn == 1:
            if 0 <= move_number < 128:
                self._place_wall(move_number)
                self.p1_walls_placed += 1
            elif 128 <= move_number < 144:
                self._move_player(self.p1, self.p2, move_number)

        if self.turn == 2:
            if 0 <= move_number < 128:
                self._place_wall(move_number)
                self.p2_walls_placed += 1
            elif 128 <= move_number < 144:
                self._move_player(self.p2, self.p1, move_number)

        if self.is_over():
            self.over = True

    def get_available_actions(self):
        walls_left = True
        if self.turn == 1:
            bitboard_in_turn = self.p1
            bitboard_out_turn = self.p2
            if self.p1_walls_placed == 10:
                walls_left = False
        elif self.turn == 2:
            bitboard_in_turn = self.p2
            bitboard_out_turn = self.p1
            if self.p1_walls_placed == 10:
                walls_left = False

        actions = np.zeros(144, dtype=np.bool8)

        # There are only 64 possible horizontal wall placements
        # There are only 64 possible vertical wall placements
        # There are 4 possible NESW moves
        # There are 4 possible NESW moves which jump over the other player
        # For each NESW move that jumps over the other player, there can potentially be
        # a move to the sides due to a blockage by a wall or the edge of the board

        # There are 64 + 64 + 4 + 4 + 8 possible set of moves in total
        # 128 of them are absolute moves
        # 16 of them are relative moves
        # relative moves are in this order:
        # NW, NN, NE, N - EN, EE, ES, E - SE, SS, SW, S - WS, WW, WN, W
        # 144 moves in total

        # get the move in NESW
        cardinal_moves = np.zeros(5, dtype=np.uint64)
        blank = np.zeros(5, dtype=np.int64)

        if np.array_equal(
            shift_bitboard(bitboard_in_turn, -17) & self.walls, blank
        ):  # North
            cardinal_moves += shift_bitboard(bitboard_in_turn, -34)
            actions[131] = True
        if np.array_equal(
            shift_bitboard(bitboard_in_turn, 1) & self.walls, blank
        ):  # East
            cardinal_moves += shift_bitboard(bitboard_in_turn, 12)
            actions[135] = True
        if np.array_equal(
            shift_bitboard(bitboard_in_turn, 17) & self.walls, blank
        ):  # South
            cardinal_moves += shift_bitboard(bitboard_in_turn, 34)
            actions[139] = True
        if np.array_equal(
            shift_bitboard(bitboard_in_turn, -1) & self.walls, blank
        ):  # West
            cardinal_moves += shift_bitboard(bitboard_in_turn, -2)
            actions[143] = True

        if not np.array_equal(cardinal_moves & bitboard_out_turn, blank):
            # There is an overlap between the player in turn and out turn
            if np.array_equal(
                shift_bitboard(bitboard_in_turn, -34),
                bitboard_out_turn & cardinal_moves,
            ):
                # out turn player is to North of in turn player
                # and there is no wall between them (by AND with playre moves)
                if np.array_equal(
                    shift_bitboard(bitboard_out_turn, -17) & self.walls, blank
                ):
                    actions[129] = True  # NN is possible
                else:
                    if np.array_equal(
                        shift_bitboard(bitboard_out_turn, -1) & self.walls, blank
                    ):
                        actions[128] = True  # NW is possible
                    if np.array_equal(
                        shift_bitboard(bitboard_out_turn, 1) & self.walls, blank
                    ):
                        actions[130] = True  # NE is possible
            elif np.array_equal(
                shift_bitboard(bitboard_in_turn, 2), bitboard_out_turn & cardinal_moves
            ):
                # out turn player is to East of in turn player
                # and there is no wall between them (by AND with playre moves)
                if np.array_equal(
                    shift_bitboard(bitboard_out_turn, 1) & self.walls, blank
                ):
                    actions[133] = True  # EE is possible
                else:
                    if np.array_equal(
                        shift_bitboard(bitboard_out_turn, -17) & self.walls, blank
                    ):
                        actions[132] = True  # EN is possible
                    if np.array_equal(
                        shift_bitboard(bitboard_out_turn, 17) & self.walls, blank
                    ):
                        actions[134] = True  # ES is possible
            elif np.array_equal(
                shift_bitboard(bitboard_in_turn, 34), bitboard_out_turn & cardinal_moves
            ):
                # out turn player is to South of in turn player
                # and there is no wall between them (by AND with playre moves)
                if np.array_equal(
                    shift_bitboard(bitboard_out_turn, 17) & self.walls, blank
                ):
                    actions[137] = True  # SS is possible
                else:
                    if np.array_equal(
                        shift_bitboard(bitboard_out_turn, 1) & self.walls, blank
                    ):
                        actions[136] = True  # SE is possible
                    if np.array_equal(
                        shift_bitboard(bitboard_out_turn, -1) & self.walls, blank
                    ):
                        actions[138] = True  # SW is possible
            elif np.array_equal(
                shift_bitboard(bitboard_in_turn, -2), bitboard_out_turn & cardinal_moves
            ):
                # out turn player is to West of in turn player
                # and there is no wall between them (by AND with playre moves)
                if np.array_equal(
                    shift_bitboard(bitboard_out_turn, -1) & self.walls, blank
                ):
                    actions[141] = True  # WW is possible
                else:
                    if np.array_equal(
                        shift_bitboard(bitboard_out_turn, 17) & self.walls, blank
                    ):
                        actions[140] = True  # WS is possible
                    if np.array_equal(
                        shift_bitboard(bitboard_out_turn, -17) & self.walls, blank
                    ):
                        actions[142] = True  # WN is possible

        # get the wall actions available by iterating through all 128 possible,
        # see if wall can be placed and then run pathfinding algorithm
        if walls_left:
            if self.path_finding_mode == "BFS":
                search = BreadthFirstSearch_Bitboard
            elif self.path_finding_mode == "DFS":
                search = DepthFirstSearch_Bitboard
            elif self.path_finding_mode == "GBFS":
                search = GreedyBestFirstSearch_Bitboard
            elif self.path_finding_mode == "UCT":
                search = UniformCostSearch_Bitboard
            elif self.path_finding_mode == "Astar":
                search = AStarSearch_Bitboard
            for wall_number in range(128):
                if wall_number < 64:
                    # horizontal wall placed
                    idx_wall = (
                        (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
                        (wall_number // 8 + 1) * 34 - 2 - 2 * (wall_number % 8),
                        (wall_number // 8 + 1) * 34 - 3 - 2 * (wall_number % 8),
                    )
                elif wall_number < 128:
                    # vertical wall placed
                    idx_wall = (
                        ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * (wall_number % 8),
                        ((wall_number % 64) // 8 + 1) * 34
                        - 19
                        - 2 * (wall_number % 8)
                        + 17,
                        ((wall_number % 64) // 8 + 1) * 34
                        - 19
                        - 2 * (wall_number % 8)
                        + 34,
                    )
                else:
                    raise IndexError
                valid = True
                for idx in idx_wall:
                    # depending on the index of the wall that has to be placed, different uint64 has to be modified
                    # idx 0 is i1, idx 288 is a9
                    if 0 <= idx <= 32:
                        if self.walls[4] & np.uint64(2 ** (idx + 31)) != 0:
                            valid = False
                    elif 33 <= idx <= 96:
                        if self.walls[3] & np.uint64(2 ** (idx - 33)) != 0:
                            valid = False
                    elif 97 <= idx <= 160:
                        if self.walls[2] & np.uint64(2 ** (idx - 97)) != 0:
                            valid = False
                    elif 161 <= idx <= 224:
                        if self.walls[1] & np.uint64(2 ** (idx - 161)) != 0:
                            valid = False
                    elif 225 <= idx <= 288:
                        if self.walls[0] & np.uint64(2 ** (idx - 225)) != 0:
                            valid = False

                if valid and search(
                    bitboard_in_turn, self.turn, self.walls, wall_number
                ):
                    actions[wall_number] = True

        return actions

    def is_over(self):
        if self.p1[0] >= 140737488355328 or 140737488355328 <= self.p2[4]:
            return True

    def display(self):
        line = "".join([np.binary_repr(x, 64) for x in self.walls])
        for i in range(0, 17):
            print(line[i * 17 : i * 17 + 17])
        print()


board = QuoridorBitBoard("BFS")
# board.take_action(64 + 5)

import timeit

print(
    timeit.timeit("board.get_available_actions()", globals=globals(), number=100) / 100
)
