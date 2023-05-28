from Quoridor.bg_pathfinding import (
    Breadth_First_Search_Graph,
    Greedy_Best_First_Search_Graph,
    Depth_First_Search_Graph,
    Uniform_Cost_Search_Graph,
    A_Star_Search_Graph,
)

"""
This is the initial implementation of the graphical representation.
The board is represented using an undirected graph that is stored
as an adjacency list.

This implementation only uses pure "vanilla" Python with
no additional libraries.
"""


class QuoridorGraphicalBoard:
    def __init__(self, search_mode="BFS"):
        # Blank adjacency list
        self.nodes = [
            ((0, 0), [(0, 1), (1, 0)]),
            ((0, 1), [(0, 2), (1, 1), (0, 0)]),
            ((0, 2), [(0, 3), (1, 2), (0, 1)]),
            ((0, 3), [(0, 4), (1, 3), (0, 2)]),
            ((0, 4), [(0, 5), (1, 4), (0, 3)]),
            ((0, 5), [(0, 6), (1, 5), (0, 4)]),
            ((0, 6), [(0, 7), (1, 6), (0, 5)]),
            ((0, 7), [(0, 8), (1, 7), (0, 6)]),
            ((0, 8), [(1, 8), (0, 7)]),
            ((1, 0), [(0, 0), (1, 1), (2, 0)]),
            ((1, 1), [(0, 1), (1, 2), (2, 1), (1, 0)]),
            ((1, 2), [(0, 2), (1, 3), (2, 2), (1, 1)]),
            ((1, 3), [(0, 3), (1, 4), (2, 3), (1, 2)]),
            ((1, 4), [(0, 4), (1, 5), (2, 4), (1, 3)]),
            ((1, 5), [(0, 5), (1, 6), (2, 5), (1, 4)]),
            ((1, 6), [(0, 6), (1, 7), (2, 6), (1, 5)]),
            ((1, 7), [(0, 7), (1, 8), (2, 7), (1, 6)]),
            ((1, 8), [(0, 8), (2, 8), (1, 7)]),
            ((2, 0), [(1, 0), (2, 1), (3, 0)]),
            ((2, 1), [(1, 1), (2, 2), (3, 1), (2, 0)]),
            ((2, 2), [(1, 2), (2, 3), (3, 2), (2, 1)]),
            ((2, 3), [(1, 3), (2, 4), (3, 3), (2, 2)]),
            ((2, 4), [(1, 4), (2, 5), (3, 4), (2, 3)]),
            ((2, 5), [(1, 5), (2, 6), (3, 5), (2, 4)]),
            ((2, 6), [(1, 6), (2, 7), (3, 6), (2, 5)]),
            ((2, 7), [(1, 7), (2, 8), (3, 7), (2, 6)]),
            ((2, 8), [(1, 8), (3, 8), (2, 7)]),
            ((3, 0), [(2, 0), (3, 1), (4, 0)]),
            ((3, 1), [(2, 1), (3, 2), (4, 1), (3, 0)]),
            ((3, 2), [(2, 2), (3, 3), (4, 2), (3, 1)]),
            ((3, 3), [(2, 3), (3, 4), (4, 3), (3, 2)]),
            ((3, 4), [(2, 4), (3, 5), (4, 4), (3, 3)]),
            ((3, 5), [(2, 5), (3, 6), (4, 5), (3, 4)]),
            ((3, 6), [(2, 6), (3, 7), (4, 6), (3, 5)]),
            ((3, 7), [(2, 7), (3, 8), (4, 7), (3, 6)]),
            ((3, 8), [(2, 8), (4, 8), (3, 7)]),
            ((4, 0), [(3, 0), (4, 1), (5, 0)]),
            ((4, 1), [(3, 1), (4, 2), (5, 1), (4, 0)]),
            ((4, 2), [(3, 2), (4, 3), (5, 2), (4, 1)]),
            ((4, 3), [(3, 3), (4, 4), (5, 3), (4, 2)]),
            ((4, 4), [(3, 4), (4, 5), (5, 4), (4, 3)]),
            ((4, 5), [(3, 5), (4, 6), (5, 5), (4, 4)]),
            ((4, 6), [(3, 6), (4, 7), (5, 6), (4, 5)]),
            ((4, 7), [(3, 7), (4, 8), (5, 7), (4, 6)]),
            ((4, 8), [(3, 8), (5, 8), (4, 7)]),
            ((5, 0), [(4, 0), (5, 1), (6, 0)]),
            ((5, 1), [(4, 1), (5, 2), (6, 1), (5, 0)]),
            ((5, 2), [(4, 2), (5, 3), (6, 2), (5, 1)]),
            ((5, 3), [(4, 3), (5, 4), (6, 3), (5, 2)]),
            ((5, 4), [(4, 4), (5, 5), (6, 4), (5, 3)]),
            ((5, 5), [(4, 5), (5, 6), (6, 5), (5, 4)]),
            ((5, 6), [(4, 6), (5, 7), (6, 6), (5, 5)]),
            ((5, 7), [(4, 7), (5, 8), (6, 7), (5, 6)]),
            ((5, 8), [(4, 8), (6, 8), (5, 7)]),
            ((6, 0), [(5, 0), (6, 1), (7, 0)]),
            ((6, 1), [(5, 1), (6, 2), (7, 1), (6, 0)]),
            ((6, 2), [(5, 2), (6, 3), (7, 2), (6, 1)]),
            ((6, 3), [(5, 3), (6, 4), (7, 3), (6, 2)]),
            ((6, 4), [(5, 4), (6, 5), (7, 4), (6, 3)]),
            ((6, 5), [(5, 5), (6, 6), (7, 5), (6, 4)]),
            ((6, 6), [(5, 6), (6, 7), (7, 6), (6, 5)]),
            ((6, 7), [(5, 7), (6, 8), (7, 7), (6, 6)]),
            ((6, 8), [(5, 8), (7, 8), (6, 7)]),
            ((7, 0), [(6, 0), (7, 1), (8, 0)]),
            ((7, 1), [(6, 1), (7, 2), (8, 1), (7, 0)]),
            ((7, 2), [(6, 2), (7, 3), (8, 2), (7, 1)]),
            ((7, 3), [(6, 3), (7, 4), (8, 3), (7, 2)]),
            ((7, 4), [(6, 4), (7, 5), (8, 4), (7, 3)]),
            ((7, 5), [(6, 5), (7, 6), (8, 5), (7, 4)]),
            ((7, 6), [(6, 6), (7, 7), (8, 6), (7, 5)]),
            ((7, 7), [(6, 7), (7, 8), (8, 7), (7, 6)]),
            ((7, 8), [(6, 8), (8, 8), (7, 7)]),
            ((8, 0), [(7, 0), (8, 1)]),
            ((8, 1), [(7, 1), (8, 2), (8, 0)]),
            ((8, 2), [(7, 2), (8, 3), (8, 1)]),
            ((8, 3), [(7, 3), (8, 4), (8, 2)]),
            ((8, 4), [(7, 4), (8, 5), (8, 3)]),
            ((8, 5), [(7, 5), (8, 6), (8, 4)]),
            ((8, 6), [(7, 6), (8, 7), (8, 5)]),
            ((8, 7), [(7, 7), (8, 8), (8, 6)]),
            ((8, 8), [(7, 8), (8, 7)]),
        ]
        """
        Array represents positions in this following order
        0, 1, 2, 3, ...,
        9, 10, 11, 12, ...
        ...
        72, 73 ,74 ,75, 80
        

        index 0 in nodes will be position a1 and index 80 in nodes will be e9 in Quoridor notation

        so player 1 will start at e1 (index 4)
        and player 2 will start at e9 (index 76)

        However, when the board is displayed, a1 will be bottom left and e9 will be top left
        """
        # Position of both players stored as (row, col)
        self.p1_pos = (0, 4)
        self.p2_pos = (8, 4)

        # Number of walls that each player has placed
        self.p1_walls_placed = 0
        self.p2_walls_placed = 0

        # Player who is in turn
        self.turn = 1

        # If the game is over or not
        self.over = False

        # Search mode to be used when verifying if a wall is allowed
        self.search_mode = search_mode

        # Previously, an adjacency list was created from scratch everytime
        # a new board was created. However, as the inital state is always the same,
        # it is now coded into self.nodes in advance

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
        available_actions = [
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
            False,
        ]

        # If the player in turn has no walls left (placed all 10),
        # there is no need to find all the available walls.
        walls_left = True

        # Depending on the player whose turn it is,
        # in_turn_pos, out_turn_pos are temporarily used to reference
        # the corrent positions(according to their name)
        # in_turn_moves, out_turn_moves are also temporarily used to refrence
        # the correct possible moves from each player's position
        if self.turn == 1:
            in_turn_pos = self.p1_pos
            out_turn_pos = self.p2_pos

            if self.p1_walls_placed == 10:
                walls_left = False

            in_turn_moves = self.nodes[self.p1_pos[0] * 9 + self.p1_pos[1]][1][:]
            out_turn_moves = self.nodes[self.p2_pos[0] * 9 + self.p2_pos[1]][1][:]
        elif self.turn == 2:
            in_turn_pos = self.p2_pos
            out_turn_pos = self.p1_pos

            if self.p2_walls_placed == 10:
                walls_left = False

            in_turn_moves = self.nodes[self.p2_pos[0] * 9 + self.p2_pos[1]][1][:]
            out_turn_moves = self.nodes[self.p1_pos[0] * 9 + self.p1_pos[1]][1][:]

        # If the position of the player not in turn (out_turn_pos) is in the list of nodes adjacent to
        # the player in turn (in_turn_moves), the two players are adjacent to each other
        # So determine if the player in turn can jump over the other player
        # or if there are moves available to the side
        if out_turn_pos in in_turn_moves:
            # As the players are adjacent, it is impossible for the player in turn to move to the
            # square where the out of turn player is as this would lead to players sharing the square
            # Therefore the position of the out of turn player is removed
            in_turn_moves.remove(out_turn_pos)

            # Calculate the relative position of player out of turn from player in turn
            relative_pos = (
                out_turn_pos[0] - in_turn_pos[0],
                out_turn_pos[1] - in_turn_pos[1],
            )

            if relative_pos == (-1, 0):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move NN as possible
                if (in_turn_pos[0] - 2, in_turn_pos[1]) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0] - 2, in_turn_pos[1]))
                else:
                    # Add the neighbours of the player in turn but not the position of the
                    # player in turn
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)
            elif relative_pos == (0, 1):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move EE as possible
                if (in_turn_pos[0], in_turn_pos[1] + 2) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0], in_turn_pos[1] + 2))
                else:
                    # Add the neighbours of the player in turn but not the position of the
                    # player in turn
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)
            elif relative_pos == (1, 0):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move SS as possible
                if (in_turn_pos[0] + 2, in_turn_pos[1]) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0] + 2, in_turn_pos[1]))
                else:
                    # Add the neighbours of the player in turn but not the position of the
                    # player in turn
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)
            elif relative_pos == (0, -1):
                # If the player in turn can jump over the player out of turn
                # without going over a wall, set the move WW as possible
                if (in_turn_pos[0], in_turn_pos[1] - 2) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0], in_turn_pos[1] - 2))
                else:
                    # Add the neighbours of the player in turn but not the position of the
                    # player in turn
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)

        # Only attempt to find the possible walls if the player has walls available
        # Otherwise, only focus on the possible movements
        if walls_left == True:
            # Set the pathfinding mode based on parameter during initialisation of board
            if self.search_mode == "BFS":
                search = Breadth_First_Search_Graph
            elif self.search_mode == "DFS":
                search = Depth_First_Search_Graph
            elif self.search_mode == "GBFS":
                search = Greedy_Best_First_Search_Graph
            elif self.search_mode == "UCT":
                search = Uniform_Cost_Search_Graph
            elif self.search_mode == "Astar":
                search = A_Star_Search_Graph
            # wall calculations are only made if there are walls left for player in turn to place
            # self.display_beautiful()
            for row in range(8):
                for column in range(8):
                    # Check if horizontal wall at position (row, col) can be placed
                    # taking into account the possibility of multiple walls being placed in a line
                    if (
                        self.nodes[row * 9 + column][0]
                        in self.nodes[row * 9 + column + 9][1]
                        and self.nodes[row * 9 + column + 1][0]
                        in self.nodes[row * 9 + column + 10][1]
                    ):
                        if (
                            (
                                self.nodes[row * 9 + column][0]
                                in self.nodes[row * 9 + column + 1][1]
                                or self.nodes[row * 9 + column + 9][0]
                                in self.nodes[row * 9 + column + 10][1]
                            )
                            or (
                                (row == 1 or row == 6)
                                and (
                                    self.nodes[row * 9 + column - 9][0]
                                    not in self.nodes[row * 9 + column - 9 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column][0]
                                    not in self.nodes[row * 9 + column + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 9][0]
                                    not in self.nodes[row * 9 + column + 9 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 18][0]
                                    not in self.nodes[row * 9 + column + 18 + 1][1]
                                )
                            )
                            or (
                                row > 1
                                and row < 6
                                and (
                                    self.nodes[row * 9 + column - 18][0]
                                    in self.nodes[row * 9 + column - 18 + 1][1]
                                    or self.nodes[row * 9 + column + 27][0]
                                    in self.nodes[row * 9 + column + 27 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column - 9][0]
                                    not in self.nodes[row * 9 + column - 9 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column][0]
                                    not in self.nodes[row * 9 + column + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 9][0]
                                    not in self.nodes[row * 9 + column + 9 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 18][0]
                                    not in self.nodes[row * 9 + column + 18 + 1][1]
                                )
                            )
                            or (
                                (row == 3 or row == 4)
                                and (
                                    self.nodes[row * 9 + column - 27][0]
                                    not in self.nodes[row * 9 + column - 27 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column - 18][0]
                                    not in self.nodes[row * 9 + column - 18 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column - 9][0]
                                    not in self.nodes[row * 9 + column - 9 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column][0]
                                    not in self.nodes[row * 9 + column + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 9][0]
                                    not in self.nodes[row * 9 + column + 9 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 18][0]
                                    not in self.nodes[row * 9 + column + 18 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 27][0]
                                    not in self.nodes[row * 9 + column + 27 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 36][0]
                                    not in self.nodes[row * 9 + column + 36 + 1][1]
                                )
                            )
                        ):
                            # Check if the vertical wall placed at (row, column)
                            # still allows both players to reach their destinations
                            # using the pathfinding algorithm set above
                            move = ((row, column), "h")
                            BFS_1 = search(self.nodes, self.p1_pos, 8, move)
                            BFS_2 = search(self.nodes, self.p2_pos, 0, move)
                            if BFS_1 == True and BFS_2 == True:
                                # Set True only if pathfinding successful for both players
                                available_actions[row * 8 + column] = True
                    if (
                        self.nodes[row * 9 + column][0]
                        in self.nodes[row * 9 + column + 1][1]
                        and self.nodes[row * 9 + column + 9][0]
                        in self.nodes[row * 9 + column + 10][1]
                    ):
                        # Check if vertical wall at position (row, col) can be placed
                        # taking into account the possibility of multiple walls being placed in a line
                        if (
                            (
                                self.nodes[row * 9 + column][0]
                                in self.nodes[row * 9 + column + 9][1]
                                or self.nodes[row * 9 + column + 1][0]
                                in self.nodes[row * 9 + column + 10][1]
                            )
                            or (
                                (column == 1 or column == 6)
                                and (
                                    self.nodes[row * 9 + column - 1][0]
                                    not in self.nodes[row * 9 + column + 9 - 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column][0]
                                    not in self.nodes[row * 9 + column + 9][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 1][0]
                                    not in self.nodes[row * 9 + column + 9 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 2][0]
                                    not in self.nodes[row * 9 + column + 9 + 2][1]
                                )
                            )
                            or (
                                column > 1
                                and column < 6
                                and (
                                    self.nodes[row * 9 + column - 2][0]
                                    in self.nodes[row * 9 + column + 9 - 2][1]
                                    or self.nodes[row * 9 + column + 3][0]
                                    in self.nodes[row * 9 + column + 9 + 3][1]
                                )
                                and (
                                    self.nodes[row * 9 + column - 1][0]
                                    not in self.nodes[row * 9 + column + 9 - 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column][0]
                                    not in self.nodes[row * 9 + column + 9][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 1][0]
                                    not in self.nodes[row * 9 + column + 9 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 2][0]
                                    not in self.nodes[row * 9 + column + 9 + 2][1]
                                )
                            )
                            or (
                                (column == 3 or column == 4)
                                and (
                                    self.nodes[row * 9 + column - 3][0]
                                    not in self.nodes[row * 9 + column + 9 - 3][1]
                                )
                                and (
                                    self.nodes[row * 9 + column - 2][0]
                                    not in self.nodes[row * 9 + column + 9 - 2][1]
                                )
                                and (
                                    self.nodes[row * 9 + column - 1][0]
                                    not in self.nodes[row * 9 + column + 9 - 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column][0]
                                    not in self.nodes[row * 9 + column + 9][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 1][0]
                                    not in self.nodes[row * 9 + column + 9 + 1][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 2][0]
                                    not in self.nodes[row * 9 + column + 9 + 2][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 3][0]
                                    not in self.nodes[row * 9 + column + 9 + 3][1]
                                )
                                and (
                                    self.nodes[row * 9 + column + 4][0]
                                    not in self.nodes[row * 9 + column + 9 + 4][1]
                                )
                            )
                        ):
                            # Check if the vertical wall placed at (row, column)
                            # still allows both players to reach their destinations
                            # using the pathfinding algorithm set above
                            move = ((row, column), "v")
                            BFS_1 = search(self.nodes, self.p1_pos, 8, move)
                            BFS_2 = search(self.nodes, self.p2_pos, 0, move)
                            if BFS_1 == True and BFS_2 == True:
                                # Set True only if pathfinding successful for both players
                                available_actions[64 + row * 8 + column] = True

        # For each move that can be taken by the player in turn,
        # add to available_actions by setting True at index
        for move in in_turn_moves:
            rel_move = (move[0] - in_turn_pos[0], move[1] - in_turn_pos[1])
            if rel_move == (1, 0):  # N
                available_actions[128] = True
            elif rel_move == (0, 1):  # E
                available_actions[129] = True
            elif rel_move == (-1, 0):  # S
                available_actions[130] = True
            elif rel_move == (0, -1):  # W
                available_actions[131] = True
            elif rel_move == (2, 0):  # NN
                available_actions[132] = True
            elif rel_move == (1, 1):  # NE
                available_actions[133] = True
            elif rel_move == (0, 2):  # EE
                available_actions[134] = True
            elif rel_move == (-1, 1):  # SE
                available_actions[135] = True
            elif rel_move == (-2, 0):  # SS
                available_actions[136] = True
            elif rel_move == (-1, -1):  # SW
                available_actions[137] = True
            elif rel_move == (0, -2):  # WW
                available_actions[138] = True
            elif rel_move == (1, -1):  # NW
                available_actions[139] = True

        return available_actions

    def take_action(self, action_number):
        """
        For the player in turn, perform the action inputed

        Actions 0~63 represent horizontal wall placements
        where 0 represents a1h, 1 represents b1h, ..., 63 represents i8h

        Actions 64~127 represent vertical wall placements
        where 0 represents a1v, 1 represents b1v, ..., 63 represents i8v

        Actions 128~139 represent the moves from the player's position
        -  N, E, S, W, NN, NE, EE, SE, SS, SW, WW, NW
        """

        rel_move = [
            (1, 0),
            (0, 1),
            (-1, 0),
            (0, -1),
            (2, 0),
            (1, 1),
            (0, 2),
            (-1, 1),
            (-2, 0),
            (-1, -1),
            (0, -2),
            (1, -1),
        ]

        # Action is a movement
        if action_number >= 128:
            if self.turn == 1:
                # Move player 1 according to the relative motion defined in rel_move
                self.p1_pos = (
                    self.p1_pos[0] + rel_move[action_number - 128][0],
                    self.p1_pos[1] + rel_move[action_number - 128][1],
                )
                # If the new position of player 1 is on the winning row, the game is over
                # Otherwise, set the turn to player 2
                if self.p1_pos[0] == 8:
                    self.over = True
                else:
                    self.turn = 2

            elif self.turn == 2:
                # Move player 2 according to the relative motion defined in rel_move
                self.p2_pos = (
                    self.p2_pos[0] + rel_move[action_number - 128][0],
                    self.p2_pos[1] + rel_move[action_number - 128][1],
                )
                # If the new position of player 2 is on the winning row, the game is over
                # Otherwise, set the turn to player 1
                if self.p2_pos[0] == 0:
                    self.over = True
                else:
                    self.turn = 1

        # Action is a wall placement
        else:
            # Horizontal wall
            if action_number < 64:
                pos = (action_number // 8, action_number % 8)
                self.nodes[pos[0] * 9 + pos[1]][1].remove((pos[0] + 1, pos[1]))
                self.nodes[pos[0] * 9 + pos[1] + 9][1].remove((pos[0], pos[1]))
                self.nodes[pos[0] * 9 + pos[1] + 1][1].remove((pos[0] + 1, pos[1] + 1))
                self.nodes[pos[0] * 9 + pos[1] + 10][1].remove((pos[0], pos[1] + 1))
            # Vertical wall
            elif action_number < 128:
                pos = ((action_number - 64) // 8, action_number % 8)
                self.nodes[pos[0] * 9 + pos[1]][1].remove((pos[0], pos[1] + 1))
                self.nodes[pos[0] * 9 + pos[1] + 1][1].remove((pos[0], pos[1]))
                self.nodes[pos[0] * 9 + pos[1] + 9][1].remove((pos[0] + 1, pos[1] + 1))
                self.nodes[pos[0] * 9 + pos[1] + 10][1].remove((pos[0] + 1, pos[1]))

            # Increment the number of walls placed for the relevant player
            # Set the turn to the other player
            if self.turn == 1:
                self.p1_walls_placed += 1
                self.turn = 2
            elif self.turn == 2:
                self.p2_walls_placed += 1
                self.turn = 1

    def display_beautiful(self):
        # array is structured so that index 0 (A1) is at top left and index 80 (I9) is bottom right
        # however, this is the wrong way around - index 0 shoudl be displayed at bottom left and index 80 should be top right
        # so the array is printed in reverse
        for row in range(8, -1, -1):
            line = []
            line_below = []
            for column in range(9):
                if self.p1_pos == (row, column):
                    line.append(" 1 ")
                elif self.p2_pos == (row, column):
                    line.append(" 2 ")
                else:
                    line.append("   ")

                if (row, column + 1) in self.nodes[row * 9 + column][1]:
                    line.append("\u2502")
                else:
                    if column != 8:
                        line.append("\u2503")
                if row != 8:
                    # if no horizontal wall below (row, column) place thin lines
                    # otherwise, place thick lines to show a wall
                    if (row + 1, column) in self.nodes[row * 9 + column][1]:
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
                        if (row, column) not in self.nodes[row * 9 + column + 1][1]:
                            # wall between X1 and X2
                            south = True
                        if (row, column + 1) not in self.nodes[row * 9 + column + 10][
                            1
                        ]:
                            # wall between X2 and X4
                            east = True
                        if (row + 1, column) not in self.nodes[row * 9 + column + 10][
                            1
                        ]:
                            # wall between X3 and X4
                            north = True
                        if (row, column) not in self.nodes[row * 9 + column + 9][1]:
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
        # returns if the game is over
        # if the game is over, return the player who won
        return self.over

    def winner(self):
        return self.turn


if __name__ == "__main__":
    board = QuoridorGraphicalBoard()
    print(board.nodes)
    print(board.get_available_actions())
    board.take_action(131)
    board.display_beautiful()
    print("not supposed to be run")
    raise ImportError
