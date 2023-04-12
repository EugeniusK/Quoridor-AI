import numpy as np
from numba import njit, int8, boolean
from .functions import roll_numba


@njit(cache=True)  # @njit(boolean(int8[:, :, :, :], int8[:, :], int8, int8[:]))
def Breadth_First_Search_Graph_Optim(nodes, pos, destination_row, move):
    wall_idx = np.zeros(4, dtype=np.int8)
    if move[2] == 0:  # horizontal wall move
        for i in range(1, 5):
            if (
                nodes[move[0] + 1, move[1], i, 0] == nodes[move[0], move[1], 0, 0]
                and nodes[move[0] + 1, move[1], i, 1] == nodes[move[0], move[1], 0, 1]
            ):
                nodes[move[0] + 1, move[1], i] = [-1, -1]
                wall_idx[0] = i
            if (
                nodes[move[0], move[1], i, 0] == nodes[move[0] + 1, move[1], 0, 0]
                and nodes[move[0], move[1], i, 1] == nodes[move[0] + 1, move[1], 0, 1]
            ):
                nodes[move[0], move[1], i] = [-1, -1]
                wall_idx[1] = i
            if (
                nodes[move[0] + 1, move[1] + 1, i, 0]
                == nodes[move[0], move[1] + 1, 0, 0]
                and nodes[move[0] + 1, move[1] + 1, i, 1]
                == nodes[move[0], move[1] + 1, 0, 1]
            ):
                nodes[move[0] + 1, move[1] + 1, i] = [-1, -1]
                wall_idx[2] = i
            if (
                nodes[move[0], move[1] + 1, i, 0]
                == nodes[move[0] + 1, move[1] + 1, 0, 0]
                and nodes[move[0], move[1] + 1, i, 1]
                == nodes[move[0] + 1, move[1] + 1, 0, 1]
            ):
                nodes[move[0], move[1] + 1, i] = [-1, -1]
                wall_idx[3] = i
    elif move[2] == 1:  # vertical wall move
        for i in range(5):
            if (
                nodes[move[0], move[1] + 1, i, 0] == nodes[move[0], move[1], 0, 0]
                and nodes[move[0], move[1] + 1, i, 1] == nodes[move[0], move[1], 0, 1]
            ):
                nodes[move[0], move[1] + 1, i] = [-1, -1]
                wall_idx[0] = i
            if (
                nodes[move[0], move[1], i, 0] == nodes[move[0], move[1] + 1, 0, 0]
                and nodes[move[0], move[1], i, 1] == nodes[move[0], move[1] + 1, 0, 1]
            ):
                nodes[move[0], move[1], i] = [-1, -1]
                wall_idx[1] = i
            if (
                nodes[move[0] + 1, move[1] + 1, i, 0]
                == nodes[move[0] + 1, move[1], 0, 0]
                and nodes[move[0] + 1, move[1] + 1, i, 1]
                == nodes[move[0] + 1, move[1], 0, 1]
            ):
                nodes[move[0] + 1, move[1] + 1, i] = [-1, -1]
                wall_idx[2] = i
            if (
                nodes[move[0] + 1, move[1], i, 0]
                == nodes[move[0] + 1, move[1] + 1, 0, 0]
                and nodes[move[0] + 1, move[1], i, 1]
                == nodes[move[0] + 1, move[1] + 1, 0, 1]
            ):
                nodes[move[0] + 1, move[1], i] = [-1, -1]
                wall_idx[3] = i
    else:
        return True

    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = pos
    frontier_length = 1
    explored = np.zeros((9, 9), dtype=np.bool8)
    explored[pos[0], pos[1]] = np.bool8(True)
    while True:
        if frontier_length == 0:
            if move[2] == 0:
                nodes[move[0] + 1, move[1], wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0], move[1] + 1]

                nodes[move[0], move[1] + 1, wall_idx[3]] = [move[0] + 1, move[1] + 1]
            if move[2] == 1:
                nodes[move[0], move[1] + 1, wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0], move[1] + 1]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1], wall_idx[3]] = [move[0] + 1, move[1] + 1]
            return False
        node = np.copy(frontier[0])
        frontier[0] = [127, 127]
        frontier = roll_numba(frontier, -1)
        frontier_length -= 1
        explored[node[0], node[1]] = True
        for child_node_idx in range(1, 5):
            child_node = nodes[node[0], node[1], child_node_idx]
            if (
                explored[child_node[0], child_node[1]] == False
                and child_node[0] != -1
                and child_node[1] != -1
            ):
                in_frontier = False
                for frontier_node_idx in range(81):
                    if (
                        child_node[0] == frontier[frontier_node_idx, 0]
                        and child_node[1] == frontier[frontier_node_idx, 1]
                    ):
                        in_frontier = True
                        break
                    elif frontier[frontier_node_idx, 0] == 127:
                        break

                if not in_frontier:
                    if child_node[0] == destination_row:
                        if move[2] == 0:
                            nodes[move[0] + 1, move[1], wall_idx[0]] = [
                                move[0],
                                move[1],
                            ]

                            nodes[move[0], move[1], wall_idx[1]] = [
                                move[0] + 1,
                                move[1],
                            ]

                            nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [
                                move[0],
                                move[1] + 1,
                            ]

                            nodes[move[0], move[1] + 1, wall_idx[3]] = [
                                move[0] + 1,
                                move[1] + 1,
                            ]
                        if move[2] == 1:
                            nodes[move[0], move[1] + 1, wall_idx[0]] = [
                                move[0],
                                move[1],
                            ]

                            nodes[move[0], move[1], wall_idx[1]] = [
                                move[0],
                                move[1] + 1,
                            ]

                            nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [
                                move[0] + 1,
                                move[1],
                            ]

                            nodes[move[0] + 1, move[1], wall_idx[3]] = [
                                move[0] + 1,
                                move[1] + 1,
                            ]
                        return True
                    frontier[frontier_length] = child_node
                    frontier_length += 1


@njit(cache=True)
def Greedy_Best_First_Search_Graph_Optim(nodes, pos, destination_row, move):
    wall_idx = np.zeros(4, dtype=np.int8)
    if move[2] == 0:  # horizontal wall move
        for i in range(1, 5):
            if (
                nodes[move[0] + 1, move[1], i, 0] == nodes[move[0], move[1], 0, 0]
                and nodes[move[0] + 1, move[1], i, 1] == nodes[move[0], move[1], 0, 1]
            ):
                nodes[move[0] + 1, move[1], i] = [-1, -1]
                wall_idx[0] = i
            if (
                nodes[move[0], move[1], i, 0] == nodes[move[0] + 1, move[1], 0, 0]
                and nodes[move[0], move[1], i, 1] == nodes[move[0] + 1, move[1], 0, 1]
            ):
                nodes[move[0], move[1], i] = [-1, -1]
                wall_idx[1] = i
            if (
                nodes[move[0] + 1, move[1] + 1, i, 0]
                == nodes[move[0], move[1] + 1, 0, 0]
                and nodes[move[0] + 1, move[1] + 1, i, 1]
                == nodes[move[0], move[1] + 1, 0, 1]
            ):
                nodes[move[0] + 1, move[1] + 1, i] = [-1, -1]
                wall_idx[2] = i
            if (
                nodes[move[0], move[1] + 1, i, 0]
                == nodes[move[0] + 1, move[1] + 1, 0, 0]
                and nodes[move[0], move[1] + 1, i, 1]
                == nodes[move[0] + 1, move[1] + 1, 0, 1]
            ):
                nodes[move[0], move[1] + 1, i] = [-1, -1]
                wall_idx[3] = i
    elif move[2] == 1:  # vertical wall move
        for i in range(5):
            if (
                nodes[move[0], move[1] + 1, i, 0] == nodes[move[0], move[1], 0, 0]
                and nodes[move[0], move[1] + 1, i, 1] == nodes[move[0], move[1], 0, 1]
            ):
                nodes[move[0], move[1] + 1, i] = [-1, -1]
                wall_idx[0] = i
            if (
                nodes[move[0], move[1], i, 0] == nodes[move[0], move[1] + 1, 0, 0]
                and nodes[move[0], move[1], i, 1] == nodes[move[0], move[1] + 1, 0, 1]
            ):
                nodes[move[0], move[1], i] = [-1, -1]
                wall_idx[1] = i
            if (
                nodes[move[0] + 1, move[1] + 1, i, 0]
                == nodes[move[0] + 1, move[1], 0, 0]
                and nodes[move[0] + 1, move[1] + 1, i, 1]
                == nodes[move[0] + 1, move[1], 0, 1]
            ):
                nodes[move[0] + 1, move[1] + 1, i] = [-1, -1]
                wall_idx[2] = i
            if (
                nodes[move[0] + 1, move[1], i, 0]
                == nodes[move[0] + 1, move[1] + 1, 0, 0]
                and nodes[move[0] + 1, move[1], i, 1]
                == nodes[move[0] + 1, move[1] + 1, 0, 1]
            ):
                nodes[move[0] + 1, move[1], i] = [-1, -1]
                wall_idx[3] = i
    else:
        return True
    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = pos
    frontier_length = 1
    explored = np.zeros((9, 9), dtype=np.bool8)
    explored[pos[0], pos[1]] = np.bool8(True)
    while True:
        if frontier_length == 0:
            if move[2] == 0:
                nodes[move[0] + 1, move[1], wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0], move[1] + 1]

                nodes[move[0], move[1] + 1, wall_idx[3]] = [move[0] + 1, move[1] + 1]
            if move[2] == 1:
                nodes[move[0], move[1] + 1, wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0], move[1] + 1]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1], wall_idx[3]] = [move[0] + 1, move[1] + 1]
            return False
        node = np.copy(frontier[frontier_length - 1])
        frontier[frontier_length] = [127, 127]
        frontier_length -= 1
        explored[node[0], node[1]] = True
        for child_node_idx in range(1, 5):
            child_node = nodes[node[0], node[1], child_node_idx]
            if (
                explored[child_node[0], child_node[1]] == False
                and child_node[0] != -1
                and child_node[1] != -1
            ):
                in_frontier = False
                for frontier_node_idx in range(81):
                    if (
                        child_node[0] == frontier[frontier_node_idx, 0]
                        and child_node[1] == frontier[frontier_node_idx, 1]
                    ):
                        in_frontier = True
                        break
                    elif frontier[frontier_node_idx, 0] == 127:
                        break

                if not in_frontier:
                    if child_node[0] == destination_row:
                        if move[2] == 0:
                            nodes[move[0] + 1, move[1], wall_idx[0]] = [
                                move[0],
                                move[1],
                            ]

                            nodes[move[0], move[1], wall_idx[1]] = [
                                move[0] + 1,
                                move[1],
                            ]

                            nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [
                                move[0],
                                move[1] + 1,
                            ]

                            nodes[move[0], move[1] + 1, wall_idx[3]] = [
                                move[0] + 1,
                                move[1] + 1,
                            ]
                        if move[2] == 1:
                            nodes[move[0], move[1] + 1, wall_idx[0]] = [
                                move[0],
                                move[1],
                            ]

                            nodes[move[0], move[1], wall_idx[1]] = [
                                move[0],
                                move[1] + 1,
                            ]

                            nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [
                                move[0] + 1,
                                move[1],
                            ]

                            nodes[move[0] + 1, move[1], wall_idx[3]] = [
                                move[0] + 1,
                                move[1] + 1,
                            ]
                        return True
                    frontier[frontier_length] = child_node
                    frontier_length += 1


@njit(cache=True)
def Depth_First_Search_Graph_Optim(nodes, pos, destination_row, move):
    wall_idx = np.zeros(4, dtype=np.int8)
    if move[2] == 0:  # horizontal wall move
        for i in range(1, 5):
            if (
                nodes[move[0] + 1, move[1], i, 0] == nodes[move[0], move[1], 0, 0]
                and nodes[move[0] + 1, move[1], i, 1] == nodes[move[0], move[1], 0, 1]
            ):
                nodes[move[0] + 1, move[1], i] = [-1, -1]
                wall_idx[0] = i
            if (
                nodes[move[0], move[1], i, 0] == nodes[move[0] + 1, move[1], 0, 0]
                and nodes[move[0], move[1], i, 1] == nodes[move[0] + 1, move[1], 0, 1]
            ):
                nodes[move[0], move[1], i] = [-1, -1]
                wall_idx[1] = i
            if (
                nodes[move[0] + 1, move[1] + 1, i, 0]
                == nodes[move[0], move[1] + 1, 0, 0]
                and nodes[move[0] + 1, move[1] + 1, i, 1]
                == nodes[move[0], move[1] + 1, 0, 1]
            ):
                nodes[move[0] + 1, move[1] + 1, i] = [-1, -1]
                wall_idx[2] = i
            if (
                nodes[move[0], move[1] + 1, i, 0]
                == nodes[move[0] + 1, move[1] + 1, 0, 0]
                and nodes[move[0], move[1] + 1, i, 1]
                == nodes[move[0] + 1, move[1] + 1, 0, 1]
            ):
                nodes[move[0], move[1] + 1, i] = [-1, -1]
                wall_idx[3] = i
    elif move[2] == 1:  # vertical wall move
        for i in range(5):
            if (
                nodes[move[0], move[1] + 1, i, 0] == nodes[move[0], move[1], 0, 0]
                and nodes[move[0], move[1] + 1, i, 1] == nodes[move[0], move[1], 0, 1]
            ):
                nodes[move[0], move[1] + 1, i] = [-1, -1]
                wall_idx[0] = i
            if (
                nodes[move[0], move[1], i, 0] == nodes[move[0], move[1] + 1, 0, 0]
                and nodes[move[0], move[1], i, 1] == nodes[move[0], move[1] + 1, 0, 1]
            ):
                nodes[move[0], move[1], i] = [-1, -1]
                wall_idx[1] = i
            if (
                nodes[move[0] + 1, move[1] + 1, i, 0]
                == nodes[move[0] + 1, move[1], 0, 0]
                and nodes[move[0] + 1, move[1] + 1, i, 1]
                == nodes[move[0] + 1, move[1], 0, 1]
            ):
                nodes[move[0] + 1, move[1] + 1, i] = [-1, -1]
                wall_idx[2] = i
            if (
                nodes[move[0] + 1, move[1], i, 0]
                == nodes[move[0] + 1, move[1] + 1, 0, 0]
                and nodes[move[0] + 1, move[1], i, 1]
                == nodes[move[0] + 1, move[1] + 1, 0, 1]
            ):
                nodes[move[0] + 1, move[1], i] = [-1, -1]
                wall_idx[3] = i
    else:
        return True
    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = pos
    frontier_length = 1
    explored = np.zeros((9, 9), dtype=np.bool8)
    explored[pos[0], pos[1]] = np.bool8(True)
    while True:
        if frontier_length == 0:
            if move[2] == 0:
                nodes[move[0] + 1, move[1], wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0], move[1] + 1]

                nodes[move[0], move[1] + 1, wall_idx[3]] = [move[0] + 1, move[1] + 1]
            if move[2] == 1:
                nodes[move[0], move[1] + 1, wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0], move[1] + 1]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1], wall_idx[3]] = [move[0] + 1, move[1] + 1]
            return False
        node = np.copy(frontier[0])
        frontier[0] = [127, 127]
        frontier_length -= 1
        frontier = roll_numba(frontier, -1)
        explored[node[0], node[1]] = True
        for child_node_idx in range(1, 5):
            child_node = nodes[node[0], node[1], child_node_idx]
            if (
                explored[child_node[0], child_node[1]] == False
                and child_node[0] != -1
                and child_node[1] != -1
            ):
                in_frontier = False
                for frontier_node_idx in range(81):
                    if (
                        child_node[0] == frontier[frontier_node_idx, 0]
                        and child_node[1] == frontier[frontier_node_idx, 1]
                    ):
                        in_frontier = True
                        break
                    elif frontier[frontier_node_idx, 0] == 127:
                        break

                if not in_frontier:
                    if child_node[0] == destination_row:
                        if move[2] == 0:
                            nodes[move[0] + 1, move[1], wall_idx[0]] = [
                                move[0],
                                move[1],
                            ]

                            nodes[move[0], move[1], wall_idx[1]] = [
                                move[0] + 1,
                                move[1],
                            ]

                            nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [
                                move[0],
                                move[1] + 1,
                            ]

                            nodes[move[0], move[1] + 1, wall_idx[3]] = [
                                move[0] + 1,
                                move[1] + 1,
                            ]
                        if move[2] == 1:
                            nodes[move[0], move[1] + 1, wall_idx[0]] = [
                                move[0],
                                move[1],
                            ]

                            nodes[move[0], move[1], wall_idx[1]] = [
                                move[0],
                                move[1] + 1,
                            ]

                            nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [
                                move[0] + 1,
                                move[1],
                            ]

                            nodes[move[0] + 1, move[1], wall_idx[3]] = [
                                move[0] + 1,
                                move[1] + 1,
                            ]
                        return True
                    frontier[frontier_length] = child_node
                    frontier_length += 1
                    frontier_sort = np.abs(
                        frontier - np.full((81, 2), destination_row, dtype=np.int8)
                    )
                    frontier = frontier[frontier_sort[:, 0].argsort()]


@njit(cache=True)
def Uniform_Cost_Search_Graph_Optim(nodes, pos, destination_row, move):
    wall_idx = np.zeros(4, dtype=np.int8)
    if move[2] == 0:  # horizontal wall move
        for i in range(1, 5):
            if (
                nodes[move[0] + 1, move[1], i, 0] == nodes[move[0], move[1], 0, 0]
                and nodes[move[0] + 1, move[1], i, 1] == nodes[move[0], move[1], 0, 1]
            ):
                nodes[move[0] + 1, move[1], i] = [-1, -1]
                wall_idx[0] = i
            if (
                nodes[move[0], move[1], i, 0] == nodes[move[0] + 1, move[1], 0, 0]
                and nodes[move[0], move[1], i, 1] == nodes[move[0] + 1, move[1], 0, 1]
            ):
                nodes[move[0], move[1], i] = [-1, -1]
                wall_idx[1] = i
            if (
                nodes[move[0] + 1, move[1] + 1, i, 0]
                == nodes[move[0], move[1] + 1, 0, 0]
                and nodes[move[0] + 1, move[1] + 1, i, 1]
                == nodes[move[0], move[1] + 1, 0, 1]
            ):
                nodes[move[0] + 1, move[1] + 1, i] = [-1, -1]
                wall_idx[2] = i
            if (
                nodes[move[0], move[1] + 1, i, 0]
                == nodes[move[0] + 1, move[1] + 1, 0, 0]
                and nodes[move[0], move[1] + 1, i, 1]
                == nodes[move[0] + 1, move[1] + 1, 0, 1]
            ):
                nodes[move[0], move[1] + 1, i] = [-1, -1]
                wall_idx[3] = i
    elif move[2] == 1:  # vertical wall move
        for i in range(5):
            if (
                nodes[move[0], move[1] + 1, i, 0] == nodes[move[0], move[1], 0, 0]
                and nodes[move[0], move[1] + 1, i, 1] == nodes[move[0], move[1], 0, 1]
            ):
                nodes[move[0], move[1] + 1, i] = [-1, -1]
                wall_idx[0] = i
            if (
                nodes[move[0], move[1], i, 0] == nodes[move[0], move[1] + 1, 0, 0]
                and nodes[move[0], move[1], i, 1] == nodes[move[0], move[1] + 1, 0, 1]
            ):
                nodes[move[0], move[1], i] = [-1, -1]
                wall_idx[1] = i
            if (
                nodes[move[0] + 1, move[1] + 1, i, 0]
                == nodes[move[0] + 1, move[1], 0, 0]
                and nodes[move[0] + 1, move[1] + 1, i, 1]
                == nodes[move[0] + 1, move[1], 0, 1]
            ):
                nodes[move[0] + 1, move[1] + 1, i] = [-1, -1]
                wall_idx[2] = i
            if (
                nodes[move[0] + 1, move[1], i, 0]
                == nodes[move[0] + 1, move[1] + 1, 0, 0]
                and nodes[move[0] + 1, move[1], i, 1]
                == nodes[move[0] + 1, move[1] + 1, 0, 1]
            ):
                nodes[move[0] + 1, move[1], i] = [-1, -1]
                wall_idx[3] = i
    else:
        return True
    frontier = np.full((81, 3), 127, dtype=np.int8)
    frontier[0, 0:2] = pos
    frontier[0, 2] = 0
    frontier_length = 1
    explored = np.zeros((9, 9), dtype=np.bool8)
    explored[pos[0], pos[1]] = True
    while True:
        if frontier_length == 0:
            if move[2] == 0:
                nodes[move[0] + 1, move[1], wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0], move[1] + 1]

                nodes[move[0], move[1] + 1, wall_idx[3]] = [move[0] + 1, move[1] + 1]
            elif move[2] == 1:
                nodes[move[0], move[1] + 1, wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0], move[1] + 1]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1], wall_idx[3]] = [move[0] + 1, move[1] + 1]
            return False
        node = np.copy(frontier[0])
        frontier_length -= 1
        frontier = roll_numba(frontier, -1)
        if node[0] == destination_row:
            if move[2] == 0:
                nodes[move[0] + 1, move[1], wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0], move[1] + 1]

                nodes[move[0], move[1] + 1, wall_idx[3]] = [move[0] + 1, move[1] + 1]
            if move[2] == 1:
                nodes[move[0], move[1] + 1, wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0], move[1] + 1]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1], wall_idx[3]] = [move[0] + 1, move[1] + 1]
            return True

        explored[node[0], node[1]] = True
        for child_node_idx in range(1, 5):
            child_node = nodes[node[0], node[1], child_node_idx]
            if child_node[0] != -1 and child_node[1] != -1:
                in_frontier = False
                in_frontier_index = -1
                for frontier_node_idx in range(81):
                    if (
                        child_node[0] == frontier[frontier_node_idx, 0]
                        and child_node[1] == frontier[frontier_node_idx, 1]
                    ):
                        in_frontier = True
                        in_frontier_index = frontier_node_idx
                        break
                    elif frontier[frontier_node_idx, 0] == 127:
                        break
                if not in_frontier and explored[child_node[0], child_node[1]] == False:
                    frontier[frontier_length, 0:2] = child_node
                    frontier[frontier_length, 2] = node[2] + 1
                    frontier = frontier[frontier[:, 2].argsort()]
                elif in_frontier and frontier[in_frontier_index, 2] > node[2] + 1:
                    frontier[in_frontier_index, 2] = node[2] + 1


@njit(cache=True)
def A_Star_Search_Graph_Optim(nodes, pos, destination_row, move):
    wall_idx = np.zeros(4, dtype=np.int8)
    if move[2] == 0:  # horizontal wall move
        for i in range(1, 5):
            if (
                nodes[move[0] + 1, move[1], i, 0] == nodes[move[0], move[1], 0, 0]
                and nodes[move[0] + 1, move[1], i, 1] == nodes[move[0], move[1], 0, 1]
            ):
                nodes[move[0] + 1, move[1], i] = [-1, -1]
                wall_idx[0] = i
            if (
                nodes[move[0], move[1], i, 0] == nodes[move[0] + 1, move[1], 0, 0]
                and nodes[move[0], move[1], i, 1] == nodes[move[0] + 1, move[1], 0, 1]
            ):
                nodes[move[0], move[1], i] = [-1, -1]
                wall_idx[1] = i
            if (
                nodes[move[0] + 1, move[1] + 1, i, 0]
                == nodes[move[0], move[1] + 1, 0, 0]
                and nodes[move[0] + 1, move[1] + 1, i, 1]
                == nodes[move[0], move[1] + 1, 0, 1]
            ):
                nodes[move[0] + 1, move[1] + 1, i] = [-1, -1]
                wall_idx[2] = i
            if (
                nodes[move[0], move[1] + 1, i, 0]
                == nodes[move[0] + 1, move[1] + 1, 0, 0]
                and nodes[move[0], move[1] + 1, i, 1]
                == nodes[move[0] + 1, move[1] + 1, 0, 1]
            ):
                nodes[move[0], move[1] + 1, i] = [-1, -1]
                wall_idx[3] = i
    elif move[2] == 1:  # vertical wall move
        for i in range(5):
            if (
                nodes[move[0], move[1] + 1, i, 0] == nodes[move[0], move[1], 0, 0]
                and nodes[move[0], move[1] + 1, i, 1] == nodes[move[0], move[1], 0, 1]
            ):
                nodes[move[0], move[1] + 1, i] = [-1, -1]
                wall_idx[0] = i
            if (
                nodes[move[0], move[1], i, 0] == nodes[move[0], move[1] + 1, 0, 0]
                and nodes[move[0], move[1], i, 1] == nodes[move[0], move[1] + 1, 0, 1]
            ):
                nodes[move[0], move[1], i] = [-1, -1]
                wall_idx[1] = i
            if (
                nodes[move[0] + 1, move[1] + 1, i, 0]
                == nodes[move[0] + 1, move[1], 0, 0]
                and nodes[move[0] + 1, move[1] + 1, i, 1]
                == nodes[move[0] + 1, move[1], 0, 1]
            ):
                nodes[move[0] + 1, move[1] + 1, i] = [-1, -1]
                wall_idx[2] = i
            if (
                nodes[move[0] + 1, move[1], i, 0]
                == nodes[move[0] + 1, move[1] + 1, 0, 0]
                and nodes[move[0] + 1, move[1], i, 1]
                == nodes[move[0] + 1, move[1] + 1, 0, 1]
            ):
                nodes[move[0] + 1, move[1], i] = [-1, -1]
                wall_idx[3] = i
    else:
        return True
    frontier = np.full((81, 4), 127, dtype=np.int8)
    frontier[0, 0:2] = pos
    frontier[0, 2:] = [0, abs(pos[0] - destination_row)]
    frontier_length = 1
    explored = np.zeros((9, 9), dtype=np.bool8)
    explored[pos[0], pos[1]] = True
    while True:
        if frontier_length == 0:
            if move[2] == 0:
                nodes[move[0] + 1, move[1], wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0], move[1] + 1]

                nodes[move[0], move[1] + 1, wall_idx[3]] = [move[0] + 1, move[1] + 1]
            elif move[2] == 1:
                nodes[move[0], move[1] + 1, wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0], move[1] + 1]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1], wall_idx[3]] = [move[0] + 1, move[1] + 1]
            return False
        node = np.copy(frontier[0])
        frontier_length -= 1
        frontier = roll_numba(frontier, -1)
        if node[0] == destination_row:
            if move[2] == 0:
                nodes[move[0] + 1, move[1], wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0], move[1] + 1]

                nodes[move[0], move[1] + 1, wall_idx[3]] = [move[0] + 1, move[1] + 1]
            if move[2] == 1:
                nodes[move[0], move[1] + 1, wall_idx[0]] = [move[0], move[1]]

                nodes[move[0], move[1], wall_idx[1]] = [move[0], move[1] + 1]

                nodes[move[0] + 1, move[1] + 1, wall_idx[2]] = [move[0] + 1, move[1]]

                nodes[move[0] + 1, move[1], wall_idx[3]] = [move[0] + 1, move[1] + 1]
            return True

        explored[node[0], node[1]] = True
        for child_node_idx in range(1, 5):
            child_node = nodes[node[0], node[1], child_node_idx]
            if child_node[0] != -1 and child_node[1] != -1:
                in_frontier = False
                in_frontier_index = -1
                for frontier_node_idx in range(81):
                    if (
                        child_node[0] == frontier[frontier_node_idx, 0]
                        and child_node[1] == frontier[frontier_node_idx, 1]
                    ):
                        in_frontier = True
                        in_frontier_index = frontier_node_idx
                        break
                    elif frontier[frontier_node_idx, 0] == 127:
                        break
                if not in_frontier and explored[child_node[0], child_node[1]] == False:
                    frontier[frontier_length, 0:2] = child_node
                    frontier[frontier_length, 2] = node[2] + 1
                    frontier[frontier_length, 3] = abs(destination_row - node[0])
                    frontier = frontier[np.sum(frontier[:, 2:], axis=1).argsort()]
                elif in_frontier and frontier[in_frontier_index, 2] > node[2] + 1:
                    frontier[in_frontier_index, 2] = node[2] + 1


# # print(timeit.timeit("shift5_numba(test_arr, 2)", setup=setup))
# # print(timeit.timeit("np.roll(test_arr, 2)", setup=setup))
# pos = np.array([0, 4], dtype=np.int8)
# move = np.array([0, 4, 0], dtype=np.int8)
# Breadth_First_Search_Graph_Optim(nodes, pos, 8, move)
