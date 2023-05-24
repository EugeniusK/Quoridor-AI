import numpy as np


def BreadFirstSearch_Bitboard(bitboard_walls, wall_number):
    bitboard = np.copy(bitboard_walls)
    if wall_number < 64:
        idx_wall = (
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
        )
    elif wall_number < 128:
        idx_wall = (
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8),
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 17,
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 34,
        )
    else:
        raise IndexError
    for idx in idx_wall:
        if 0 <= idx <= 32:
            bitboard[4] += 2 ** (idx + 31)
        elif 33 <= idx <= 96:
            bitboard[3] += 2 ** (idx - 33)
        elif 97 <= idx <= 160:
            bitboard[2] += 2 ** (idx - 97)
        elif 161 <= idx <= 224:
            bitboard[1] += 2 ** (idx - 161)
        elif 225 <= idx <= 288:
            bitboard[0] += 2 ** (idx - 225)

    frontier = np.full(81)
    frontier = []  # FIFO queue
    frontier.append(pos_player)
    explored = []  # explored

    while True:
        if frontier == []:
            return False
        node = frontier.pop(0)
        explored.append(node)
        for child_node in board_nodes[node[0] * 9 + node[1]][1]:
            if child_node not in explored and child_node not in frontier:
                if child_node[0] == destination_row:
                    return True
                frontier.append(child_node)


board = np.array([0, 0, 0, 0, 2**39], dtype=np.uint64)
print(id(board))
BreadFirstSearch_Bitboard(board, 5)
print(id(board))
