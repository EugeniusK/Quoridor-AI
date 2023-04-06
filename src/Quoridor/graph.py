from .path_finding import (
    Breadth_First_Search_Graph,
    Greedy_Best_First_Search_Graph,
)


class QuoridorGraphicalBoard:
    def __init__(self):
        self.nodes = []  # all 81 positions possible
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
        self.p1_pos = (0, 4)
        self.p2_pos = (8, 4)

        self.p1_walls_placed = 0
        self.p2_walls_placed = 0

        self.turn = 0  # False if player 1 turn, True if player 2 turn

        self.over = False
        for row in range(0, 9):
            for column in range(0, 9):
                # adds the neighbours for each node
                position = (row, column)
                neighbours = [
                    (row - 1, column),
                    (row, column + 1),
                    (row + 1, column),
                    (row, column - 1),
                ]
                # removes neighbours if they are beyond what is allowed
                # like row = -1 and column = -1
                if row == 0:
                    neighbours.remove((row - 1, column))
                if column == 8:
                    neighbours.remove((row, column + 1))
                if row == 8:
                    neighbours.remove((row + 1, column))
                if column == 0:
                    neighbours.remove((row, column - 1))

                self.nodes.append((position, neighbours))

    def get_available_moves(self):
        # for the player in turn, find the places the player can move to
        # as well as finding the location of walls that can be placed
        # while allowing the other player to reach their winning side

        # in_turn_moves stores the moves possible by the player in turn
        # out_turn_moves stores the moves posisble by the player not in turn
        # in_turn_pos stores the location of the player in turn
        # out_turn_pos stores the location of the player out of turn

        walls_left = True
        if self.turn == 0:
            # It's player 1's turn
            in_turn_moves = self.nodes[self.p1_pos[0] * 9 + self.p1_pos[1]][1][:]
            out_turn_moves = self.nodes[self.p2_pos[0] * 9 + self.p2_pos[1]][1][:]

            in_turn_pos = self.p1_pos
            out_turn_pos = self.p2_pos

            if self.p1_walls_placed == 10:
                walls_left = False
        elif self.turn == 1:
            # It's the player 2's turn
            in_turn_moves = self.nodes[self.p2_pos[0] * 9 + self.p2_pos[1]][1][:]
            out_turn_moves = self.nodes[self.p1_pos[0] * 9 + self.p1_pos[1]][1][:]

            in_turn_pos = self.p2_pos
            out_turn_pos = self.p1_pos

            if self.p2_walls_placed == 10:
                walls_left = False

        if out_turn_pos in in_turn_moves:
            # removes any moves that goes to the out of turn player's position - will lead to overlap
            # this means that it may be possible for the player in turn to jump over the other player
            in_turn_moves.remove(out_turn_pos)

            relative_pos = (
                out_turn_pos[0] - in_turn_pos[0],
                out_turn_pos[1] - in_turn_pos[1],
            )  # calculates relative position of out of turn player from in turn player

            # IF the move that jumps over out of turn player is available, add the move
            # OTHERWISE, add the moves from the position of out of turn player
            # and remove the in turn position as this will just move player in turn to its original position

            if relative_pos == (-1, 0):
                # player out of turn is North of player in turn
                if (in_turn_pos[0] - 2, in_turn_pos[1]) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0] - 2, in_turn_pos[1]))
                else:
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)
            elif relative_pos == (0, 1):
                # player out of turn is East of player in turn
                if (in_turn_pos[0], in_turn_pos[1] + 2) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0], in_turn_pos[1] + 2))
                else:
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)
            elif relative_pos == (1, 0):
                # player out of turn is South of player in turn
                if (in_turn_pos[0] + 2, in_turn_pos[1]) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0] + 2, in_turn_pos[1]))
                else:
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)
            elif relative_pos == (0, -1):
                # player out of turn is West of player in turn
                if (in_turn_pos[0], in_turn_pos[1] - 2) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0], in_turn_pos[1] - 2))
                else:
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)

        walls_available = []  # walls that players can place
        if walls_left == True:
            # wall calculations are only made if there are walls left for player in turn to place
            for row in range(8):
                for column in range(8):
                    if (
                        self.nodes[row * 9 + column][0]
                        in self.nodes[row * 9 + column + 9][1]
                        and self.nodes[row * 9 + column + 1][0]
                        in self.nodes[row * 9 + column + 10][1]
                    ):
                        # checks if a horizontal wall can be placed with (row, column) to the left and top
                        # checking if a move from (row, column) to (row + 1, column) AND (row, column + 1)
                        # and (row + 1, column + 1) is allowed
                        # this is only checked for rows 0~7 as row 8 will check for non-existant row 9
                        # and only for columns 0~7 as colum 8 will check for non-existant column 9
                        if (
                            self.nodes[row * 9 + column][0]
                            in self.nodes[row * 9 + column + 1][1]
                            or self.nodes[row * 9 + column + 9][0]
                            in self.nodes[row * 9 + column + 10][1]
                        ):
                            # ensures that there is no vertical wall going through the candidate horizontal row
                            # by checking if a move from (row, column) to (row, column + 1) allowed
                            # and checking if a move from (row + 1, column) to (row + 1, column + 1) is allowed
                            # if both of them are not allowed, there is a vertical wall going through the horizontal wall
                            # NEED A STAR SEARCH ALGORITHM TO VERIFFY EXISTING PATH
                            move = ((row, column), "h")
                            BFS_1 = Greedy_Best_First_Search_Graph(
                                self.nodes, self.p1_pos, 8, move
                            )
                            BFS_2 = Greedy_Best_First_Search_Graph(
                                self.nodes, self.p2_pos, 0, move
                            )
                            if BFS_1 == True and BFS_2 == True:
                                walls_available.append(move)
                    if (
                        self.nodes[row * 9 + column][0]
                        in self.nodes[row * 9 + column + 1][1]
                        and self.nodes[row * 9 + 9 + column][0]
                        in self.nodes[row * 9 + 9 + column + 1][1]
                    ):
                        # checks if a vertical wall can be placed with (row, column) to the left and top
                        # checking if a move from (row, column) to (row, column+1) AND (row+1, column)
                        # and (row + 1, column + 1) is allowed
                        # this is only checked for rows 0~7 as row 8 will check for non-existant row 9
                        # and only for columns 0~7 as colum 8 will check for non-existant column 9
                        if (
                            self.nodes[row * 9 + column][0]
                            in self.nodes[row * 9 + column + 9][1]
                            or self.nodes[row * 9 + column + 1][0]
                            in self.nodes[row * 9 + column + 10]
                        ):
                            # ensures that there is no horizontal wall going through the candidate vertical row
                            # by checking if a move from (row, column) to (row + 1, column) allowed
                            # and checking if a move from (row, column + 1) to (row + 1, column + 1) is allowed
                            # if both of them are not allowed, there is a horizontal wall going through the vertical wall
                            # NEED A STAR SEARCH ALGORITHM TO VERIFFY EXISTING PATH
                            move = ((row, column), "v")
                            BFS_1 = Breadth_First_Search_Graph(
                                self.nodes, self.p1_pos, 8, move
                            )
                            BFS_2 = Breadth_First_Search_Graph(
                                self.nodes, self.p2_pos, 0, move
                            )
                            if BFS_1 and BFS_2:
                                walls_available.append(move)
        algebraic_moves = []
        for move in (
            in_turn_moves + walls_available
        ):  # wrong format to algebraic notation
            if type(move[0]) == tuple:
                if move[1] == "h":
                    algebraic_move = f"{chr(97+move[0][1])}{move[0][0]+1}h"
                elif move[1] == "v":
                    algebraic_move = f"{chr(97+move[0][1])}{move[0][0]+1}v"
            elif type(move[0]) == int:
                algebraic_move = f"{chr(97+move[1])}{move[0]+1}"
            algebraic_moves.append(algebraic_move)
        return algebraic_moves

    def make_move(self, move):
        if len(move) == 2:
            # move is in format (row, column)
            # is a move to row, column
            if self.turn == 0:  # if it's player 1 turn
                self.p1_pos = (
                    int(move[1]) - 1,
                    ord(move[0]) - 97,
                )  # moves player 1 to new position
                if self.p1_pos[0] == 8:
                    # if the new position is on the winning row, game is over
                    self.over = True
                else:
                    self.turn = 1  # change turn to other player

            elif self.turn == 1:  # if it's player 2 turn
                self.p2_pos = (
                    int(move[1]) - 1,
                    ord(move[0]) - 97,
                )  # moves player 2 to new position
                if self.p2_pos[0] == 0:
                    # if the new position is on the winning row, game is over
                    self.over = True
                else:
                    self.turn = 0  # change turn to other player
        elif len(move) == 3:
            # move is in format ((row, column), direction)
            # is a wall place
            pos = (
                int(move[1]) - 1,
                ord(move[0]) - 97,
            )

            # for a wall place, remove B as a neighbour from A and remove A as a neighbour from B and repeat for C and D
            if move[2] == "h":
                self.nodes[pos[0] * 9 + pos[1]][1].remove((pos[0] + 1, pos[1]))
                self.nodes[pos[0] * 9 + pos[1] + 9][1].remove((pos[0], pos[1]))

                self.nodes[pos[0] * 9 + pos[1] + 1][1].remove((pos[0] + 1, pos[1] + 1))
                self.nodes[pos[0] * 9 + pos[1] + 10][1].remove((pos[0], pos[1] + 1))

            elif move[2] == "v":
                self.nodes[pos[0] * 9 + pos[1]][1].remove((pos[0], pos[1] + 1))
                self.nodes[pos[0] * 9 + pos[1] + 1][1].remove((pos[0], pos[1]))

                self.nodes[pos[0] * 9 + pos[1] + 9][1].remove((pos[0] + 1, pos[1] + 1))
                self.nodes[pos[0] * 9 + pos[1] + 10][1].remove((pos[0] + 1, pos[1]))

            # add 1 to number of walls placed
            # and change turn to other player
            if self.turn == 0:
                self.p1_walls_placed += 1
                self.turn = 1
            elif self.turn == 1:
                self.p2_walls_placed += 1
                self.turn = 0

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


# # generate algebraic notations for moves
#             # a-h from left to right and 1-9 from bottom to top
#             # from perspective of player 1 who starts from bottom

#             # player 1 starts at e1
#             # player 2 starts at e9

#             # wall move is formatted((index1, index2), type)
#             # player move is formatted (index1, index2)
#             # where index1 is zero-based indexing from the top
#             # and where index2 is zero-based indexing from the left

#             # index1 of 0 would actually be rank 9 and index1 of 8 would actually be rank 1
#             # index2 of 1 would actually be file a and index2 of 8 would actually be file i
if __name__ == "__main__":
    print("not supposed to be run")
    raise ImportError
