def board_to_string(board):
    output = []
    for row in range(9):
        line = []
        line_below = []
        for col in range(9):
            pos = row * 9 + col
            if pos == board.p1_pos:
                line.append(" 1 ")
            elif row * 9 + col == board.p2_pos:
                line.append(" 2 ")
            else:
                line.append("   ")

            if col != 8:
                if board.is_direction_valid(row * 9 + col, 1):
                    # can move East from pos so add thin wall
                    line.append("\u2502")
                else:
                    # cannot move East from pos so add thick wall
                    line.append("\u2503")
            if row != 8:
                if board.is_direction_valid(row * 9 + col, 2):
                    line_below.append("\u2500\u2500\u2500")
                else:
                    line_below.append("\u2501\u2501\u2501")

                if col != 8:
                    north = not board.is_direction_valid(row * 9 + col, 1)
                    east = not board.is_direction_valid(row * 9 + col + 1, 2)
                    south = not board.is_direction_valid(row * 9 + col + 9, 1)
                    west = not board.is_direction_valid(row * 9 + col, 2)

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
        output.append("".join(line))
        output.append("".join(line_below))
    return "\n".join(output)


def output_to_cli(board):
    print(board_to_string(board))
