import copy
import numpy as np

short_north_mask = np.ones((17, 17), dtype=np.bool_)
short_north_mask[16:] = False
short_east_mask = np.rot90(short_north_mask, 3)
short_south_mask = np.rot90(short_north_mask, 2)
short_west_mask = np.rot90(short_north_mask, 1)


def Breadth_First_Search_Graph(nodes, pos_player, destination_row, move):
    board_nodes = copy.deepcopy(nodes)
    pos = move[0]

    if move[1] == "h":
        board_nodes[pos[0] * 9 + pos[1]][1].remove((pos[0] + 1, pos[1]))
        board_nodes[pos[0] * 9 + pos[1] + 9][1].remove((pos[0], pos[1]))

        board_nodes[pos[0] * 9 + pos[1] + 1][1].remove((pos[0] + 1, pos[1] + 1))
        board_nodes[pos[0] * 9 + pos[1] + 10][1].remove((pos[0], pos[1] + 1))

    elif move[1] == "v":
        board_nodes[pos[0] * 9 + pos[1]][1].remove((pos[0], pos[1] + 1))
        board_nodes[pos[0] * 9 + pos[1] + 1][1].remove((pos[0], pos[1]))

        board_nodes[pos[0] * 9 + pos[1] + 9][1].remove((pos[0] + 1, pos[1] + 1))
        board_nodes[pos[0] * 9 + pos[1] + 10][1].remove((pos[0] + 1, pos[1]))

    valid = True
    nodes_visited = []
    nodes_to_be_visited = []
    nodes_to_be_visited.append(pos_player)

    while True:
        for node in board_nodes[
            nodes_to_be_visited[0][0] * 9 + nodes_to_be_visited[0][1]
        ][1]:
            if node not in nodes_to_be_visited and node not in nodes_visited:
                nodes_to_be_visited.append(node)
                if node[0] == destination_row:
                    return True
        nodes_visited.append(nodes_to_be_visited.pop(0))
        if nodes_to_be_visited == []:
            return False


def Greedy_Best_First_Search_Graph(nodes, pos_player, destination_row, move):
    board_nodes = copy.deepcopy(nodes)
    pos = move[0]

    if move[1] == "h":
        board_nodes[pos[0] * 9 + pos[1]][1].remove((pos[0] + 1, pos[1]))
        board_nodes[pos[0] * 9 + pos[1] + 9][1].remove((pos[0], pos[1]))

        board_nodes[pos[0] * 9 + pos[1] + 1][1].remove((pos[0] + 1, pos[1] + 1))
        board_nodes[pos[0] * 9 + pos[1] + 10][1].remove((pos[0], pos[1] + 1))

    elif move[1] == "v":
        board_nodes[pos[0] * 9 + pos[1]][1].remove((pos[0], pos[1] + 1))
        board_nodes[pos[0] * 9 + pos[1] + 1][1].remove((pos[0], pos[1]))

        board_nodes[pos[0] * 9 + pos[1] + 9][1].remove((pos[0] + 1, pos[1] + 1))
        board_nodes[pos[0] * 9 + pos[1] + 10][1].remove((pos[0] + 1, pos[1]))

    valid = True
    nodes_visited = []
    nodes_to_be_visited = []
    nodes_to_be_visited.append(pos_player)

    while True:
        for node in board_nodes[
            nodes_to_be_visited[0][0] * 9 + nodes_to_be_visited[0][1]
        ][1]:
            if node not in nodes_to_be_visited and node not in nodes_visited:
                nodes_to_be_visited.append(node)
                if node[0] == destination_row:
                    return True
        nodes_to_be_visited.sort(key=lambda x: abs(x[0] - destination_row))
        nodes_visited.append(nodes_to_be_visited.pop(0))
        if nodes_to_be_visited == []:
            return False


def Breadth_First_Search_BitBoard(
    player_bitboard: np.ndarray,
    walls_bitboard: np.ndarray,
    destination_row: np.int8,
    move: np.ndarray,
) -> bool:

    walls = walls_bitboard.copy()
    if move[2] == 2 or move[2] == -1:
        return True
    if move[2] == 0:  # horizontal wall
        walls[move[0] * 2 + 1, move[1] * 2 : move[1] * 2 + 3] = True
    elif move[2] == 1:  # vertical wall
        walls[move[0] * 2 : move[0] * 2 + 3, move[1] * 2 + 1] = True
    visited = np.zeros((17, 17), dtype=np.bool_)

    queue = np.full((81, 2), 127, dtype=np.int8)  # indexs of places to visited
    length_queue = np.int8(0)

    queue[0] = np.array(np.where(player_bitboard), dtype=np.int8).T
    queue_bitboard = np.copy(player_bitboard)
    length_queue += 1
    while True:
        # go through neighbours of places
        player_moves = np.zeros((17, 17), dtype=np.bool_)
        tmp_position = np.zeros((17, 17), dtype=np.bool_)
        tmp_position[queue[0][0]][queue[0][1]] = True
        # print(length_queue)
        if True in np.roll(tmp_position, -17) & short_north_mask:
            if True not in np.roll(tmp_position, -17) & walls:
                player_moves += np.roll(tmp_position, -34)
        if True in np.roll(tmp_position, 1) & short_east_mask:
            if True not in np.roll(tmp_position, 1) & walls:
                player_moves += np.roll(tmp_position, 2)
        if True in np.roll(tmp_position, 17) & short_south_mask:
            if True not in np.roll(tmp_position, 17) & walls:
                player_moves += np.roll(tmp_position, 34)
        if True in np.roll(tmp_position, -1) & short_west_mask:
            if True not in np.roll(tmp_position, -1) & walls:
                player_moves += np.roll(tmp_position, -2)
        player_moves_index = np.array(np.where(player_moves), dtype=np.int8).T
        ############## get neighbours
        for index in player_moves_index:
            if (
                queue_bitboard[index[0]][index[1]] == False
                and visited[index[0]][index[1]] == False
            ):

                queue[length_queue] = index
                queue_bitboard[index[0]][index[1]] = True
                length_queue += 1
                if index[0] == destination_row:
                    return True

        visited[queue[0][0]][queue[0][1]] = True
        queue_bitboard[queue[0][0]][queue[0][1]] = False
        queue[0] = [127, 127]
        queue = np.roll(queue, -2)

        length_queue -= 1
        if length_queue == 0:
            return False


def Greedy_Best_First_Search_BitBoard(
    player_bitboard: np.ndarray,
    walls_bitboard: np.ndarray,
    destination_row: np.int8,
    move: np.ndarray,
) -> bool:
    walls = walls_bitboard.copy()
    if move[2] == 2 or move[2] == -1:
        return True
    elif move[2] == 0:  # horizontal wall
        walls[move[0] * 2 + 1, move[1] * 2 : move[1] * 2 + 3] = True
    elif move[2] == 1:  # vertical wall
        walls[move[0] * 2 : move[0] * 2 + 3, move[1] * 2 + 1] = True
    visited = np.zeros((17, 17), dtype=np.bool_)

    queue = np.full((81, 2), 127, dtype=np.int8)  # indexs of places to visited
    length_queue = np.int8(0)

    queue[0] = np.array(np.where(player_bitboard), dtype=np.int8).T
    queue_bitboard = np.copy(player_bitboard)
    length_queue += 1
    while True:
        # go through neighbours of places
        player_moves = np.zeros((17, 17), dtype=np.bool_)
        tmp_position = np.zeros((17, 17), dtype=np.bool_)
        tmp_position[queue[0][0]][queue[0][1]] = True

        if True in np.roll(tmp_position, -17) & short_north_mask:
            if True not in np.roll(tmp_position, -17) & walls:
                player_moves += np.roll(tmp_position, -34)
        if True in np.roll(tmp_position, 1) & short_east_mask:
            if True not in np.roll(tmp_position, 1) & walls:
                player_moves += np.roll(tmp_position, 2)
        if True in np.roll(tmp_position, 17) & short_south_mask:
            if True not in np.roll(tmp_position, 17) & walls:
                player_moves += np.roll(tmp_position, 34)
        if True in np.roll(tmp_position, -1) & short_west_mask:
            if True not in np.roll(tmp_position, -1) & walls:
                player_moves += np.roll(tmp_position, -2)
        player_moves_index = np.array(np.where(player_moves), dtype=np.int8).T

        for index in player_moves_index:
            if (
                queue_bitboard[index[0]][index[1]] == False
                and visited[index[0]][index[1]] == False
            ):

                queue[length_queue] = index
                queue_bitboard[index[0]][index[1]] = True
                length_queue += 1
                if index[0] == destination_row:
                    return True

        visited[queue[0][0]][queue[0][1]] = True
        queue_bitboard[queue[0][0]][queue[0][1]] = False
        queue[0] = [127, 127]
        queue = np.roll(queue, -2)

        queue_sort = np.abs(queue - np.full((81, 2), destination_row, dtype=np.int8))
        queue = queue[queue_sort[:, 0].argsort()]

        length_queue -= 1
        if length_queue == 0:
            return False
