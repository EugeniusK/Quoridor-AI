import numpy as np
import random
import sys


class QuoridorGraphicalBoard:
    def __init__(self):
        self.nodes = []  # all 81 positions possible
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
                            walls_available.append(((row, column), "h"))
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
                            walls_available.append(((row, column), "v"))
        return in_turn_moves + walls_available

    def make_move(self, move):
        if type(move[0]) == int:
            # move is in format (row, column)
            # is a move to row, column
            if self.turn == 0:  # if it's player 1 turn
                self.p1_pos = move  # moves player 1 to new position
                if self.p1_pos[0] == 8:
                    # if the new position is on the winning row, game is over
                    self.over = True
                else:
                    self.turn = 1  # change turn to other player

            elif self.turn == 1:  # if it's player 2 turn
                self.p2_pos = move  # moves player 2 to new position
                if self.p2_pos[0] == 0:
                    # if the new position is on the winning row, game is over
                    self.over = True
                else:
                    self.turn = 0  # change turn to other player
        elif type(move[0]) == tuple:
            # move is in format ((row, column), direction)
            # is a wall place
            pos = move[0]

            # for a wall place, remove B as a neighbour from A and remove A as a neighbour from B and repeat for C and D
            if move[1] == "h":
                self.nodes[pos[0] * 9 + pos[1]][1].remove((pos[0] + 1, pos[1]))
                self.nodes[pos[0] * 9 + pos[1] + 9][1].remove((pos[0], pos[1]))

                self.nodes[pos[0] * 9 + pos[1] + 1][1].remove((pos[0] + 1, pos[1] + 1))
                self.nodes[pos[0] * 9 + pos[1] + 10][1].remove((pos[0], pos[1] + 1))

            elif move[1] == "v":
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

    def display(self):
        # older version of display function
        print()
        print(f"Turn is {self.turn + 1}")
        print(f"Player 1 has {10 - self.p1_walls_placed} walls left")
        print(f"Player 2 has {10 - self.p2_walls_placed} walls left")

        for row in range(9):
            line = []
            line_below = []
            for column in range(9):
                # print "w" for wall
                # print "1" for player 1
                # print "2" for player 2
                # print " " for nothing
                if (row, column) == self.p1_pos:
                    line.append("1")
                elif (row, column) == self.p2_pos:
                    line.append("2")
                else:
                    line.append("_")
                if (row, column + 1) in self.nodes[row * 9 + column][1]:
                    line.append(" ")
                else:
                    if column != 8:
                        line.append("w")
                    else:
                        line.append(" ")

                if (row + 1, column) in self.nodes[row * 9 + column][1]:
                    line_below.append(" ")
                else:
                    if row != 8:
                        line_below.append("w")

            print(" ".join(line))
            print("   ".join(line_below))

    def display_beautiful(self):
        for row in range(9):
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
                            north = True
                        if (row, column + 1) not in self.nodes[row * 9 + column + 10][
                            1
                        ]:
                            # wall between X2 and X4
                            east = True
                        if (row + 1, column) not in self.nodes[row * 9 + column + 10][
                            1
                        ]:
                            # wall between X3 and X4
                            south = True
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
            print("".join(line))
            print("".join(line_below))

    def is_over(self):
        # returns if the game is over
        # if the game is over, return the player who won
        if self.over == True:
            return (True, self.turn)
        else:
            return (False, self.turn)
