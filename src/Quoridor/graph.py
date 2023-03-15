import numpy as np
import random
import sys


class QuoridorGraphicalBoard:
    def __init__(self):
        self.nodes = []
        self.p1_pos = (0, 4)
        self.p2_pos = (8, 4)

        self.p1_walls_placed = 0
        self.p2_walls_placed = 0

        self.turn = 0  # False if player 1 turn, True if player 2 turn

        self.over = False
        for row in range(0, 9):
            for column in range(0, 9):

                position = (row, column)
                neighbours = [
                    (row - 1, column),
                    (row, column + 1),
                    (row + 1, column),
                    (row, column - 1),
                ]

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
        # places that the piece can move to
        # in_turn_moves stores the moves of the player in turn
        # out_turn_moves stores the moves of the player not in turn
        # in_turn_pos stores the location of the player in turn
        # out_turn_pos stores the location of the player out of turn

        walls_left = True
        if self.turn == 0:
            # Case 1 : It's player 1's turn
            in_turn_moves = self.nodes[self.p1_pos[0] * 9 + self.p1_pos[1]][1][:]
            out_turn_moves = self.nodes[self.p2_pos[0] * 9 + self.p2_pos[1]][1][:]

            in_turn_pos = self.p1_pos
            out_turn_pos = self.p2_pos

            if self.p1_walls_placed == 10:
                walls_left = False
        elif self.turn == 1:
            # Case 2 : It's the player 2's turn
            in_turn_moves = self.nodes[self.p2_pos[0] * 9 + self.p2_pos[1]][1][:]
            out_turn_moves = self.nodes[self.p1_pos[0] * 9 + self.p1_pos[1]][1][:]

            in_turn_pos = self.p2_pos
            out_turn_pos = self.p1_pos

            if self.p2_walls_placed == 10:
                walls_left = False
        if out_turn_pos in in_turn_moves:
            # removes any moves for player in turn that goes to the out of turn player's position
            # FOLLOWS THE RULE
            in_turn_moves.remove(out_turn_pos)

            relative_pos = (
                out_turn_pos[0] - in_turn_pos[0],
                out_turn_pos[1] - in_turn_pos[1],
            )  # calculates relative position of out of turn player from in turn player
            # print(self.turn, relative_pos, in_turn_pos, out_turn_pos)

            # IF the move that jumps over out of turn player is available, add the move
            # OTHERWISE, add the moves adjacent to the out of turn player
            # by adding the moves available from out_turn_pos - knowing that the move that jumps over is unavailable
            # and remove the in turn position as it will be in out of turns possible moves

            if relative_pos == (-1, 0):  # N
                if (in_turn_pos[0] - 2, in_turn_pos[1]) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0] - 2, in_turn_pos[1]))
                else:
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)
            elif relative_pos == (0, 1):  # E
                if (in_turn_pos[0], in_turn_pos[1] + 2) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0], in_turn_pos[1] + 2))
                else:
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)
            elif relative_pos == (1, 0):  # S
                if (in_turn_pos[0] + 2, in_turn_pos[1]) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0] + 2, in_turn_pos[1]))
                else:
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)
            elif relative_pos == (0, -1):  # W
                if (in_turn_pos[0], in_turn_pos[1] - 2) in out_turn_moves:
                    in_turn_moves.append((in_turn_pos[0], in_turn_pos[1] - 2))
                else:
                    in_turn_moves.extend(out_turn_moves)
                    in_turn_moves.remove(in_turn_pos)

        for row in range(9):
            line = ["_", "_", "_", "_", "_", "_", "_", "_", "_"]
            if self.p1_pos[0] == row:
                line[self.p1_pos[1]] = "1"
            if self.p2_pos[0] == row:
                line[self.p2_pos[1]] = "2"

            for move in in_turn_moves:
                if move[0] == row:
                    line[move[1]] = "x"

        # walls that players can place
        walls_available = []
        if walls_left == True:
            for row in range(8):
                for column in range(8):
                    if (
                        self.nodes[row * 9 + column][0]
                        in self.nodes[row * 9 + column + 9][1]
                        and self.nodes[row * 9 + column + 1][0]
                        in self.nodes[row * 9 + column + 10][1]
                    ):
                        # horizontal wall check
                        if (
                            self.nodes[row * 9 + column][0]
                            in self.nodes[row * 9 + column + 1][1]
                            or self.nodes[row * 9 + column + 9][0]
                            in self.nodes[row * 9 + column + 10][1]
                        ):
                            # ensures that there is no vertical wall going through the candidate horizontal row
                            # NEED A STAR SEARCH ALGORITHM TO VERIFFY EXISTING PATH
                            walls_available.append(((row, column), "h"))
                    if (
                        self.nodes[row * 9 + column][0]
                        in self.nodes[row * 9 + column + 1][1]
                        and self.nodes[row * 9 + 9 + column][0]
                        in self.nodes[row * 9 + 9 + column + 1][1]
                    ):
                        # vertical wall checks
                        if (
                            self.nodes[row * 9 + column][0]
                            in self.nodes[row * 9 + column + 9][1]
                            or self.nodes[row * 9 + column + 1][0]
                            in self.nodes[row * 9 + column + 10]
                        ):
                            # ensures that there is no vertical wall going through the candidate horizontal row
                            # NEED A STAR SEARCH ALGORITHM TO VERIFFY EXISTING PATH
                            walls_available.append(((row, column), "h"))
        return in_turn_moves + walls_available

    def make_move(self, move):
        if type(move[0]) == int:  # is a move to row, column
            if self.turn == 0:
                self.p1_pos = move
                if self.p1_pos[0] == 8:
                    self.over = True
                else:
                    self.turn = 1

            elif self.turn == 1:
                self.p2_pos = move
                if self.p2_pos[0] == 0:
                    self.over = True
                else:
                    self.turn = 0
        elif type(move[0]) == tuple:  # is a wall place
            pos = move[0]
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

            if self.turn == 0:
                self.turn = 1
                self.p1_walls_placed += 1
            elif self.turn == 1:
                self.turn = 0
                self.p2_walls_placed += 1

    def display(self):
        print()
        print(f"Turn is {self.turn + 1}")
        print(f"Player 1 has {10 - self.p1_walls_placed} walls left")
        print(f"Player 2 has {10 - self.p2_walls_placed} walls left")
        for row in range(9):
            line = []
            line_below = []
            for column in range(9):
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
                    # adds the intersections
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
            return (True, self.turn)
        else:
            return (False, self.turn)
