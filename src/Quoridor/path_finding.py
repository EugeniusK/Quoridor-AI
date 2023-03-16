import copy


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
        nodes_visited.append(nodes_to_be_visited.pop(0))
        if nodes_to_be_visited == []:
            valid = False
            break
    return valid


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
        nodes_to_be_visited.sort(key=lambda x: abs(x[0] - destination_row))
        nodes_visited.append(nodes_to_be_visited.pop(0))
        if nodes_to_be_visited == []:
            valid = False
            break
    return valid


def A_Star_Search_Graph(nodes, pos_player, destination_row, move):
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
        nodes_to_be_visited.sort(
            key=lambda x: abs(x[0] - destination_row)
            + abs(x[0] - pos[0])
            + abs(x[1] - pos[1])
        )
        nodes_visited.append(nodes_to_be_visited.pop(0))
        if nodes_to_be_visited == []:
            valid = False
            break
    return valid
