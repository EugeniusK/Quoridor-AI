import numpy as np
from numba import njit, int32, uint32, int64, uint64, int8, boolean
from numba.experimental import jitclass

try:
    from Quoridor.b_pathfinding_optim import (
        BreadthFirstSearch_Bitboard,
        DepthFirstSearch_Bitboard,
        GreedyBestFirstSearch_Bitboard,
        UniformCostSearch_Bitboard,
        AStarSearch_Bitboard,
    )
except:
    from b_pathfinding_optim import (
        BreadthFirstSearch_Bitboard,
        DepthFirstSearch_Bitboard,
        GreedyBestFirstSearch_Bitboard,
        UniformCostSearch_Bitboard,
        AStarSearch_Bitboard,
    )

"""
This is an improved version of the bitboard representation in bitboard.py that is
closer to a true bitboard.

Multiple 64 bit integers are used to represent the board instead of using an array
of booleans that would behave similarly.
"""

blank = np.zeros(5, dtype=np.uint64)
full = np.array(
    [
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446744071562067968,
    ],
    dtype=np.uint64,
)

short_north_mask = np.array(
    [
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446462598732840960,
    ],
    dtype=np.uint64,
)
short_east_mask = np.array(
    [
        9223301667573723135,
        17870278923326062335,
        18410715001810583535,
        18444492256715866110,
        18446603336221196287,
    ],
    dtype=np.uint64,
)
short_south_mask = np.array(
    [
        140737488355327,
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446744071562067968,
    ],
    dtype=np.uint64,
)
short_west_mask = np.array(
    [
        18446603335147446271,
        17293813772942573055,
        18374685929911615455,
        18442240439722180605,
        18446462594437873664,
    ],
    dtype=np.uint64,
)


@njit(cache=True)
def shift_bitboard(bitboard, shift):
    # right is positive shift EAST
    """
    Shift the bitboard by shift
    while ensuring that bits outside of the 17x17 are not set
    """
    if shift > 0 and shift < 64:
        rshift = np.uint64(shift)
        lshift = np.uint64(64 - shift)
        copy_bitboard = (bitboard >> rshift) + (np.roll(bitboard, 1) << lshift)
        # copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        if bitboard[0] == 0:
            copy_bitboard[0] = 0
    elif shift < 0 and shift > -64:
        rshift = np.uint64(64 + shift)
        lshift = np.uint64(-shift)
        copy_bitboard = (bitboard << lshift) + (np.roll(bitboard, -1) >> rshift)
        if bitboard[4] == 0:
            copy_bitboard[4] = 0
    return copy_bitboard


@njit(cache=True)
def shift_bitboard_check_wall(player_bitboard, wall_bitboard, shift, mask):
    """
    Shift the bitboard right by shift
    Then bitwise AND with wall bitboard and compare to blank bitboard
    to ensure that the player doesn't go through a wal
    Then AND with full bitboard to ensure the player is on the board
    """
    if shift > 0 and shift < 64:
        rshift = np.uint64(shift)
        lshift = np.uint64(64 - shift)
        copy_bitboard = (player_bitboard >> rshift) + (
            np.roll(player_bitboard, 1) << lshift
        )
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        # if player_bitboard[0] == 0:
        #     copy_bitboard[0] = 0
    elif shift < 0 and shift > -64:
        rshift = np.uint64(64 + shift)
        lshift = np.uint64(-shift)
        copy_bitboard = (player_bitboard << lshift) + (
            np.roll(player_bitboard, -1) >> rshift
        )
        # if player_bitboard[4] == 0:
        #     copy_bitboard[4] = 0
    return np.array_equal(copy_bitboard & wall_bitboard, blank) and ~np.array_equal(
        copy_bitboard & mask, blank
    )


@njit(cache=True)
def bitboard_get_index(bitboard, row, col):
    idx = row * 17 + col
    if 0 <= idx <= 32:
        return bitboard[4] & np.uint64(2 ** (idx + 31)) != 0
    elif 33 <= idx <= 96:
        return bitboard[3] & np.uint64(2 ** (idx - 33)) != 0
    elif 97 <= idx <= 160:
        return bitboard[2] & np.uint64(2 ** (idx - 97)) != 0
    elif 161 <= idx <= 224:
        return bitboard[1] & np.uint64(2 ** (idx - 161)) != 0
    elif 225 <= idx <= 288:
        return bitboard[0] & np.uint64(2 ** (idx - 225)) != 0


spec = [
    ("p1", uint64[:]),
    ("p2", uint64[:]),
    ("walls", uint64[:]),
    ("p1_walls_placed", int8),
    ("p2_walls_placed", int8),
    ("turn", int8),
    ("over", boolean),
    ("path_finding_mode", int8),
]


# @jitclass(spec)
class QuoridorBitboardOptim:
    def __init__(self, path_finding_mode):
        # 0~32 are 5th
        # 33~96 are 4th
        # 97~160 are 3th
        # 161~224 are 2nd
        # 225~288 are 1st
        # index 288 is a9 while index 0 is i1

        # Bitboards for players and the walls
        # 5 64 bit integers are being used to represent the 17x17 board
        # as there are a minimum of 17x17 = 289 bits needed while
        # 5 64 bit inegers provide 5x64 = 320 bits.
        self.p1 = np.array([0, 0, 0, 0, 2**39], dtype=np.uint64)
        self.p2 = np.array([2**55, 0, 0, 0, 0], dtype=np.uint64)
        self.walls = np.array([0, 0, 0, 0, 0], dtype=np.uint64)

        # Number of walls that each player has placed
        self.p1_walls_placed = np.int8(0)
        self.p2_walls_placed = np.int8(0)

        # Player who is in turn
        self.turn = np.int8(1)

        # If the game is over or not
        self.over = np.bool8(False)

        # Search mode to be used when verifying if a wall is allowed
        self.path_finding_mode = path_finding_mode

    def _place_wall(self, wall_number):
        """
        Place the wall at wall_number where
        0~63 represents horizontal walls
        64~127 represent vertical walls
        """

        # Horizontal wall
        if wall_number < 64:
            # Get the indexes of bitboard where bits should be set
            idx_wall = (
                (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
                (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
                (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
            )

        # Vertical wall
        else:
            # Get the indexes of bitboard where bits should be set
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

        # Depending on the index, it is in different uint64 so correct one
        # has to be found
        for idx in idx_wall:
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

    def take_action(self, action_number):
        """
        Depending on the action_number, call the function
        _place_wall() or _move_player()
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

        if self.turn == 1:
            if 0 <= action_number < 128:
                self._place_wall(action_number)
                self.p1_walls_placed += 1
            elif 128 <= action_number < 144:
                self.p1 = shift_bitboard(
                    self.p1,
                    rel_move[action_number - 128, 0] * -34
                    + rel_move[action_number - 128, 1] * 2,
                )
            self.turn = 2

        elif self.turn == 2:
            if 0 <= action_number < 128:
                self._place_wall(action_number)
                self.p2_walls_placed += 1
            elif 128 <= action_number < 144:
                self.p2 = shift_bitboard(
                    self.p2,
                    rel_move[action_number - 128, 0] * -34
                    + rel_move[action_number - 128, 1] * 2,
                )
            self.turn = 1
        if self.is_over():
            self.over = True

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
        # the corrent bitboard (according to their name)
        if self.turn == 1:
            bitboard_in_turn = self.p1
            bitboard_out_turn = self.p2

            if self.p1_walls_placed == 10:
                walls_left = False
        elif self.turn == 2:
            bitboard_in_turn = self.p2
            bitboard_out_turn = self.p1

            if self.p2_walls_placed == 10:
                walls_left = False

        # Move the player in each cardinal direction (N, E, S, W) by 1
        # If the player lands on a wall (check through bitwise AND with wall bitboard)
        # the movement in that direction isn't possible as it is blocked by a wall
        # Otherwise, add the move in that direction to cardinal_moves, a bitboard
        # that stores the possible moves of one square
        #
        # Masks are required because sometimes, the method used to get available moves
        # in each direction can lead to the player going off the board
        cardinal_moves = np.zeros(5, dtype=np.uint64)

        if shift_bitboard_check_wall(
            bitboard_in_turn, self.walls, -17, short_north_mask
        ):  # North
            cardinal_moves += shift_bitboard(bitboard_in_turn, -34)
            available_actions[128] = True
        if shift_bitboard_check_wall(
            bitboard_in_turn, self.walls, 1, short_east_mask
        ):  # East
            cardinal_moves += shift_bitboard(bitboard_in_turn, 2)
            available_actions[129] = True
        if shift_bitboard_check_wall(
            bitboard_in_turn, self.walls, 17, short_south_mask
        ):  # South
            cardinal_moves += shift_bitboard(bitboard_in_turn, 34)
            available_actions[130] = True
        if shift_bitboard_check_wall(
            bitboard_in_turn, self.walls, -1, short_west_mask
        ):  # West
            cardinal_moves += shift_bitboard(bitboard_in_turn, -2)
            available_actions[131] = True

        # If the 2 players are adjacent,
        # determine if the player in turn can jump over the other player
        # or if there are moves available to the side
        if not np.array_equal(cardinal_moves & bitboard_out_turn, blank):
            # Player in turn is North of player out of turn
            if np.array_equal(
                shift_bitboard(bitboard_in_turn, -34),
                bitboard_out_turn & cardinal_moves,
            ):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move NN as possible
                if shift_bitboard_check_wall(
                    bitboard_out_turn, self.walls, -17, short_north_mask
                ):  # NN
                    available_actions[132] = True
                else:
                    if shift_bitboard_check_wall(
                        bitboard_out_turn, self.walls, -1, short_west_mask
                    ):  # NW
                        available_actions[139] = True
                    if shift_bitboard_check_wall(
                        bitboard_out_turn, self.walls, 1, short_east_mask
                    ):  # NE
                        available_actions[133] = True
            # Player in turn is East of player out of turn
            elif np.array_equal(
                shift_bitboard(bitboard_in_turn, 2), bitboard_out_turn & cardinal_moves
            ):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move EE as possible
                if shift_bitboard_check_wall(
                    bitboard_out_turn, self.walls, 1, short_east_mask
                ):  # EE
                    available_actions[134] = True
                else:
                    if shift_bitboard_check_wall(
                        bitboard_out_turn, self.walls, -17, short_north_mask
                    ):  # NE
                        available_actions[133] = True
                    if shift_bitboard_check_wall(
                        bitboard_out_turn, self.walls, 17, short_south_mask
                    ):  # SE
                        available_actions[135] = True
            # Player in turn is South of player out of turn
            elif np.array_equal(
                shift_bitboard(bitboard_in_turn, 34), bitboard_out_turn & cardinal_moves
            ):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move SS as possible
                if shift_bitboard_check_wall(
                    bitboard_out_turn, self.walls, 17, short_south_mask
                ):  # SS
                    available_actions[136] = True
                else:
                    if shift_bitboard_check_wall(
                        bitboard_out_turn, self.walls, 1, short_east_mask
                    ):  # SE
                        available_actions[135] = True
                    if shift_bitboard_check_wall(
                        bitboard_out_turn, self.walls, -1, short_west_mask
                    ):  # SW
                        available_actions[137] = True
            # Player in turn is West of player out of turn
            elif np.array_equal(
                shift_bitboard(bitboard_in_turn, -2), bitboard_out_turn & cardinal_moves
            ):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move WW as possible
                if shift_bitboard_check_wall(
                    bitboard_out_turn, self.walls, -1, short_west_mask
                ):  # WW
                    available_actions[138] = True
                else:
                    if shift_bitboard_check_wall(
                        bitboard_out_turn, self.walls, 17, short_south_mask
                    ):  # SW
                        available_actions[137] = True
                    if shift_bitboard_check_wall(
                        bitboard_out_turn, self.walls, -17, short_north_mask
                    ):  # NW
                        available_actions[139] = True

        # Only attempt to find the possible walls if the player has walls available
        # Otherwise, only focus on the possible movements
        if walls_left:
            # Set the pathfinding mode based on parameter during initialisation of board
            if self.path_finding_mode == 1:
                search = BreadthFirstSearch_Bitboard
            elif self.path_finding_mode == 2:
                search = DepthFirstSearch_Bitboard
            elif self.path_finding_mode == 3:
                search = GreedyBestFirstSearch_Bitboard
            elif self.path_finding_mode == 4:
                search = UniformCostSearch_Bitboard
            elif self.path_finding_mode == 5:
                search = AStarSearch_Bitboard
            else:
                raise KeyError
            # For each possible wall,
            # verify the space isn't occupied by a wall
            # and that it doens't prevent either player from reaching their destination
            for wall_number in range(128):
                # Get indexes where the wall would go
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

                # Verify that the indexes aren't occupied by a wall
                valid = True
                for idx in idx_wall:
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

                # If the space isn't occupied by a wall and it doesn't prevent
                # either player from reaching tehir destination,
                # set action to True
                if (
                    valid
                    and search(bitboard_in_turn, self.turn, self.walls, wall_number)
                    # and search(
                    #     bitboard_out_turn, 3 - self.turn, self.walls, wall_number
                ):
                    available_actions[wall_number] = True

        return available_actions

    def is_over(self):
        try:
            if self.p1[0] >= 140737488355328 or 140737488355328 <= self.p2[4]:
                return True
            else:
                return False
        except:
            print(self.p1, self.p2)
            raise KeyError

    def display(self, bitboard):
        line = "".join([np.binary_repr(x, 64) for x in bitboard])
        for i in range(0, 17):
            print(line[i * 17 : i * 17 + 17])
        print()

    def display_beautiful(self):
        for row in range(8, -1, -1):
            line = []
            line_below = []
            for column in range(9):
                if bitboard_get_index(self.p1, row * 2, column * 2):
                    line.append(" 1 ")
                elif bitboard_get_index(self.p2, row * 2, column * 2):
                    line.append(" 2 ")
                else:
                    line.append("   ")

                if column != 8:
                    if bitboard_get_index(self.walls, row * 2, column * 2 + 1) == False:
                        line.append("\u2502")
                    else:
                        line.append("\u2503")
                if row != 8:
                    if bitboard_get_index(self.walls, row * 2 + 1, column * 2) == False:
                        line_below.append("\u2500\u2500\u2500")
                    else:
                        line_below.append("\u2501\u2501\u2501")
                    if column != 8:
                        south = bitboard_get_index(self.walls, row * 2, column * 2 + 1)
                        west = bitboard_get_index(
                            self.walls, row * 2 + 1, column * 2 + 2
                        )
                        north = bitboard_get_index(
                            self.walls, row * 2 + 2, column * 2 + 1
                        )
                        east = bitboard_get_index(self.walls, row * 2 + 1, column * 2)
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

            print(" " + "".join(reversed(line_below)))
            print(str(row + 1) + "".join(reversed(line)))
        print("  a   b   c   d   e   f   g   h   i ")