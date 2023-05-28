import numpy as np
from Quoridor.bg_pathfinding import (
    Depth_First_Search_BitBoard,
    Breadth_First_Search_BitBoard,
    Greedy_Best_First_Search_BitBoard,
    Uniform_Cost_Search_Bitboard,
    A_Star_Search_Bitboard,
)

"""
This is the initial implementation of the bitboard representation.
Instead of using individual bits to represent each possible position, 
a boolean data type of 8 bits (1 byte) is used to represent a 
corresponding 1 or a 0.

Therefore, this implementation cannot be considered a true bitboard.
A true bitboard would use multiple (u)int16, (u)int32, or (u)int64
but in this implementation, a 17x17 array of bools are used
"""

# Binary masks which are used to prevent the player going off the board
# when "rolling" the bitboard array
north_mask = np.ones((17, 17), dtype=np.bool8)
north_mask[15:] = False
east_mask = np.rot90(north_mask, 3)
south_mask = np.rot90(north_mask, 2)
west_mask = np.rot90(north_mask, 1)

short_north_mask = np.ones((17, 17), dtype=np.bool8)
short_north_mask[16:] = False
short_east_mask = np.rot90(short_north_mask, 3)
short_south_mask = np.rot90(short_north_mask, 2)
short_west_mask = np.rot90(short_north_mask, 1)


class QuoridorBitBoard:
    def __init__(self, search_mode="GBFS"):
        # Bitboards to represent the walls and players' position
        # as well as having the inital positions of players set
        self.walls = np.zeros((17, 17), dtype=np.bool8)
        self.p1_pos = np.zeros((17, 17), dtype=np.bool8)
        self.p1_pos[0][8] = True
        self.p2_pos = np.zeros((17, 17), dtype=np.bool8)
        self.p2_pos[16][8] = True

        # Number of walls that each player has placed
        self.p1_walls_placed = np.int8(0)
        self.p2_walls_placed = np.int8(0)

        # Player who is in turn
        self.turn = np.int8(1)

        # If the game is over or not
        self.over = np.bool8(False)

        # Search mode to be used when verifying if a wall is allowed
        self.search_mode = search_mode

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
            in_turn_pos = self.p1_pos
            out_turn_pos = self.p2_pos

            if self.p1_walls_placed == 10:
                walls_left = False
        elif self.turn == 2:
            in_turn_pos = self.p2_pos
            out_turn_pos = self.p1_pos

            if self.p2_walls_placed == 10:
                walls_left = False

        # Move the player in each cardinal direction (N, E, S, W) by 1
        # If the player lands on a wall (check through bitwise AND with wall bitboard)
        # the movement in that direction isn't possible as it is blocked by a wall
        # Otherwise, add the move in that direction to player_moves, a bitboard
        # that stores the possible moves of one square
        player_moves = np.zeros((17, 17), dtype=np.bool8)
        if True in np.roll(in_turn_pos, -17) & short_north_mask:  # North
            if True not in np.roll(in_turn_pos, -17) & self.walls:
                player_moves += np.roll(in_turn_pos, -34)
        if True in np.roll(in_turn_pos, 1) & short_east_mask:  # East
            if True not in np.roll(in_turn_pos, 1) & self.walls:
                player_moves += np.roll(in_turn_pos, 2)
        if True in np.roll(in_turn_pos, 17) & short_south_mask:  # South
            if True not in np.roll(in_turn_pos, 17) & self.walls:
                player_moves += np.roll(in_turn_pos, 34)
        if True in np.roll(in_turn_pos, -1) & short_west_mask:  # West
            if True not in np.roll(in_turn_pos, -1) & self.walls:
                player_moves += np.roll(in_turn_pos, -2)

        # If the 2 players are adjacent,
        # determine if the player in turn can jump over the other player
        # or if there are moves available to the side
        if True in player_moves & out_turn_pos:
            # Calculate the relative position of player out of turn from player in turn
            relative_pos = np.subtract(
                np.where(in_turn_pos == True), np.where(out_turn_pos == True)
            )
            # Player in turn is North of player out of turn
            if np.array_equal(
                relative_pos,
                np.array([[2], [0]]),
            ):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move NN as possible
                if (
                    True in np.roll(out_turn_pos, -17) & short_north_mask
                    and True not in np.roll(out_turn_pos, -17) & self.walls
                ):  # NN
                    player_moves += np.roll(out_turn_pos, -34)
                else:
                    # Check if the moves to the sides of player out of turn
                    # are possible
                    if True in np.roll(out_turn_pos, 1) & short_east_mask:  # NE
                        if True not in np.roll(out_turn_pos, 1) & self.walls:
                            player_moves += np.roll(out_turn_pos, 2)
                    if True in np.roll(out_turn_pos, -1) & short_west_mask:  # NW
                        if True not in np.roll(out_turn_pos, -1) & self.walls:
                            player_moves += np.roll(out_turn_pos, -2)

            # Player in turn is East of player out of turn
            elif np.array_equal(
                relative_pos,
                np.array([[0], [-2]]),
            ):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move EE as possible
                if (
                    True in np.roll(out_turn_pos, 1) & short_east_mask
                    and True not in np.roll(out_turn_pos, 1) & self.walls
                ):  # EE
                    player_moves += np.roll(out_turn_pos, 2)
                else:
                    # Check if the moves to the sides of player out of turn
                    # are possible
                    if True in np.roll(out_turn_pos, -17) & short_north_mask:  # NE
                        if True not in np.roll(out_turn_pos, -17) & self.walls:
                            player_moves += np.roll(out_turn_pos, -34)
                    if True in np.roll(out_turn_pos, 17) & short_south_mask:  # SE
                        if True not in np.roll(out_turn_pos, 17) & self.walls:
                            player_moves += np.roll(out_turn_pos, 34)

            # Player in turn is South of player out of turn
            elif np.array_equal(
                relative_pos,
                np.array([[-2], [0]]),
            ):  # SS
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move WW as possible
                if (
                    True in np.roll(out_turn_pos, 17) & short_south_mask
                    and True not in np.roll(out_turn_pos, 17) & self.walls
                ):
                    player_moves += np.roll(out_turn_pos, 34)
                else:
                    # Check if the moves to the sides of player out of turn
                    # are possible
                    if True in np.roll(out_turn_pos, 1) & short_east_mask:  # SE
                        if True not in np.roll(out_turn_pos, 1) & self.walls:
                            player_moves += np.roll(out_turn_pos, 2)
                    if True in np.roll(out_turn_pos, -1) & short_west_mask:  # SW
                        if True not in np.roll(out_turn_pos, -1) & self.walls:
                            player_moves += np.roll(out_turn_pos, -2)

            # Player in turn is West of player out of turn
            elif np.array_equal(
                relative_pos,
                np.array([[0], [2]]),
            ):  # WW
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move WW as possible
                if (
                    True in np.roll(out_turn_pos, -1) & short_west_mask
                    and True not in np.roll(out_turn_pos, -1) & self.walls
                ):
                    player_moves += np.roll(out_turn_pos, -2)
                else:
                    # Check if the moves to the sides of player out of turn
                    # are possible
                    if True in np.roll(out_turn_pos, -17) & short_north_mask:  # NW
                        if True not in np.roll(out_turn_pos, -17) & self.walls:
                            player_moves += np.roll(out_turn_pos, -34)
                    if True in np.roll(out_turn_pos, 17) & short_south_mask:  # SW
                        if True not in np.roll(out_turn_pos, 17) & self.walls:
                            player_moves += np.roll(out_turn_pos, 34)

        # The indexes of where the player in turn can move to excluding the position of
        # the player out of turn
        player_moves_index = np.array(
            np.where(player_moves & ~out_turn_pos), dtype=np.int8
        ).T

        # Only attempt to find the possible walls if the player has walls available
        # Otherwise, only focus on the possible movements
        if walls_left == True:
            # Get the indexes of the horizontal walls possible
            # by getting indexes of 3 zeros in a line
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
                            np.zeros((8, 1), dtype=np.bool8),
                        )
                    ),
                    np.zeros((1, 9), dtype=np.bool8),
                )
            )
            horizontal_walls_index = np.array(
                np.where(horizontal_walls), dtype=np.int8
            ).T

            # Get the indexes of the verrtical walls possible
            # by getting indexes of 3 zeros in a line
            sliding_vertical_walls = np.reshape(
                np.lib.stride_tricks.sliding_window_view(
                    np.fliplr(np.rot90(self.walls, 3)), (1, 3)
                ),
                (17, 15, 3),
            )
            vertical_walls = np.vstack(
                (
                    np.hstack(
                        (
                            np.fliplr(np.rot90(~sliding_vertical_walls.any(axis=2), 3))[
                                ::2, 1::2
                            ],
                            np.zeros((8, 1), dtype=np.bool8),
                        )
                    ),
                    np.zeros((1, 9), dtype=np.bool8),
                )
            )
            vertical_walls_index = np.array(np.where(vertical_walls), dtype=np.int8).T
        # Maximum number of horizontal wall placements is 8*8 = 64
        # Maxmium number of vertical wall placements is 8*8 = 64
        # Maximum number of moves is 5
        # So, combining them into an array of 133*2 is possible
        # Row 0~63 will be filled with possible horizontal wall placements
        # Row 64~127 will be filled with possible vertical wall placements
        # Row 128~132 will be filled with possible player moves
        # Unused indexes will be filled with -1 (maximum value allowed with np.int8)
        # Final column in array represents type of move - 0: horizontal wall, 1: vertical wall, 2: player move
        # THIS IS AN INTERMEDIARY TO THE FULL 140 LENGTH ARRAY
        actions = np.full((133, 3), -1, dtype=np.int8)
        if walls_left == True:
            actions[0 : 0 + len(horizontal_walls_index)] = np.hstack(
                (
                    horizontal_walls_index,
                    np.zeros((len(horizontal_walls_index), 1), dtype=np.int8),
                )
            )
            actions[64 : 64 + len(vertical_walls_index)] = np.hstack(
                (
                    vertical_walls_index,
                    np.ones((len(vertical_walls_index), 1), dtype=np.int8),
                )
            )
        actions[128 : 128 + len(player_moves_index)] = np.hstack(
            (
                player_moves_index,
                np.full((len(player_moves_index), 1), 2, dtype=np.int8),
            )
        )

        # Validate that the walls are possible only when the player in turn has walls left
        if walls_left == True:
            # Set the pathfinding mode based on parameter during initialisation of board
            if self.search_mode == "BFS":
                search = Breadth_First_Search_BitBoard
            elif self.search_mode == "DFS":
                search = Depth_First_Search_BitBoard
            elif self.search_mode == "GBFS":
                search = Greedy_Best_First_Search_BitBoard
            elif self.search_mode == "UCT":
                search = Uniform_Cost_Search_Bitboard
            elif self.search_mode == "Astar":
                search = A_Star_Search_Bitboard
            for m in range(128):
                if (
                    search(self.p1_pos, self.walls, np.int8(16), actions[m]) == False
                    or search(self.p2_pos, self.walls, np.int8(0), actions[m]) == False
                ):
                    # Set move as invalid if one or more of pathfinding fails
                    actions[m] = [-1, -1, -1]

        # Add the actions in actions to available_actions
        for h in range(0, 128):
            if actions[h][0] != -1 and actions[h][1] != -1 and actions[h][2] != -1:
                available_actions[
                    actions[h][0] * 8 + actions[h][1] + actions[h][2] * 64
                ] = True
        for i in range(128, 133):
            if actions[i][0] != -1 and actions[i][1] != -1 and actions[i][2] != -1:
                player_in_turn_pos = np.array(np.where(in_turn_pos), dtype=np.int8).T[0]
                rel_move = (actions[i, 0:2] - player_in_turn_pos) >> 1
                if np.array_equal(rel_move, [1, 0]):  # N
                    available_actions[128] = True
                elif np.array_equal(rel_move, [0, 1]):  # E
                    available_actions[129] = True
                elif np.array_equal(rel_move, [-1, 0]):  # S
                    available_actions[130] = True
                elif np.array_equal(rel_move, [0, -1]):  # W
                    available_actions[131] = True
                elif np.array_equal(rel_move, [2, 0]):  # NN
                    available_actions[132] = True
                elif np.array_equal(rel_move, [1, 1]):  # NE
                    available_actions[133] = True
                elif np.array_equal(rel_move, [0, 2]):  # EE
                    available_actions[134] = True
                elif np.array_equal(rel_move, [-1, 1]):  # SE
                    available_actions[135] = True
                elif np.array_equal(rel_move, [-2, 0]):  # SS
                    available_actions[136] = True
                elif np.array_equal(rel_move, [-1, -1]):  # SW
                    available_actions[137] = True
                elif np.array_equal(rel_move, [0, -2]):  # WW
                    available_actions[138] = True
                elif np.array_equal(rel_move, [1, -1]):  # NW
                    available_actions[139] = True

        return available_actions

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
                in_turn_pos = np.array(np.where(self.p1_pos), dtype=np.int8).T[0]
                self.p1_pos = np.zeros((17, 17), dtype=np.bool8)
                self.p1_pos[in_turn_pos[0] + rel_move[action - 128, 0] * 2][
                    in_turn_pos[1] + rel_move[action - 128, 1] * 2
                ] = True
                if in_turn_pos[0] + rel_move[action - 128, 0] * 2 == 16:
                    self.over = True
                else:
                    self.turn = np.int8(2)
            elif self.turn == 2:  # player 2's turn
                in_turn_pos = np.array(np.where(self.p2_pos), dtype=np.int8).T[0]
                self.p2_pos = np.zeros((17, 17), dtype=np.bool8)
                self.p2_pos[in_turn_pos[0] + rel_move[action - 128, 0] * 2][
                    in_turn_pos[1] + rel_move[action - 128, 1] * 2
                ] = True
                if in_turn_pos[0] + rel_move[action - 128, 0] * 2 == 0:
                    self.over = True
                else:
                    self.turn = np.int8(1)

        # Action is a wall placement
        else:
            # Horizontal wall
            if action < 64:
                self.walls[
                    action // 8 * 2 + 1, action % 8 * 2 : action % 8 * 2 + 3
                ] = True
            # Vertical wall
            else:  # vertical wall
                self.walls[
                    (action - 64) // 8 * 2 : (action - 64) // 8 * 2 + 3,
                    action % 8 * 2 + 1,
                ] = True

            # Increment the number of walls placed for the relevant player
            # Set the turn to the other player
            if self.turn == 1:
                self.p1_walls_placed += 1
                self.turn = 2
            elif self.turn == 2:
                self.p2_walls_placed += 1
                self.turn = 1

    def display_beautiful(self):
        for row in range(8, -1, -1):
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

                        south = self.walls[row * 2][column * 2 + 1]
                        east = self.walls[row * 2 + 1][column * 2 + 2]
                        north = self.walls[row * 2 + 2][column * 2 + 1]
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
            print(" " + "".join(line_below))
            print(str(row + 1) + "".join(line))
        print("  a   b   c   d   e   f   g   h   i ")

    def is_over(self):
        return self.over

    def winner(self):
        if self.turn == np.int8(1):
            return 1
        elif self.turn == np.int8(2):
            return 2


if __name__ == "__main__":
    # board = QuoridorBitBoard()
    # board.display_beautiful()
    # board.take_action(0)
    # board.display_beautiful()
    # print(board.get_available_actions())
    # print(board.walls * 1)
    # board.display_beautiful()
    print("not supposed to be run")
    raise ImportError
