import numpy as np
from numba import njit, int8, boolean
from .functions import roll_numba


@njit(cache=True)
def Breadth_First_Search_Graph_Optim(nodes, pos, destination_row, move):
    # Psuedocode from Artifical Intelligence: A modern approach
    # -------------------------------------------------------------------------------
    # function BREADTH-FIRST-SEARCH(problem) returns a solution, or failure
    #     node ← a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    #     if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    #     frontier ← a FIFO queue with node as the only element
    #     explored ← an empty set
    #     loop do
    #         if EMPTY?(frontier) then return failure
    #         node←POP(frontier) /*choosestheshallowestnodeinfrontier */
    #         add node.STATE to explored
    #         for each action in problem.ACTIONS(node.STATE) do
    #             child ←CHILD-NODE(problem,node,action)
    #             if child.STATE is not in explored or frontier then
    #                 if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
    #                 frontier ←INSERT(child,frontier)
    # -------------------------------------------------------------------------------
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

    node = np.copy(pos)

    if node[0] == destination_row:
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

    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = node
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

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
            if child_node[0] != -1 and child_node[1] != -1:
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

                if not in_frontier and explored[child_node[0], child_node[1]] == False:
                    if node[0] == destination_row:
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
    # Psuedocide from Artifical INtelligence: A modern approach
    # Adapted from Uniform Cost Search based on
    # "tries to expand the node that is closest to the goal" - pg 92
    # "it evaluates nodes by using just the heuristic function; that is, f (n) = h(n)" - pg 92
    # -------------------------------------------------------------------------------
    # function GREEDY-BEST-FIRST-SEARCH(problem) returns a solution, or failure
    # node ← a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    # frontier ← a priority queue ordered by h(n), with node as the only element
    # explored ← an empty set
    # loop do
    #       if EMPTY?(frontier) then return failure
    #       node←POP(frontier) /*choosesthelowest-costnodeinfrontier */
    #       if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    #       add node.STATE to explored
    #       for each action in problem.ACTIONS(node.STATE) do
    #           child ←CHILD-NODE(problem,node,action)
    #           if child.STATE is not in explored or frontier then
    #               frontier ←INSERT(child,frontier)
    # ------------------------------------------------------------------------------
    # h(n) would be the minimum number of moves to reach the destination row - assuming no walls
    # "h(n) = estimated cost of the cheapest path from the state at node n to a goal state."
    # The heuristic above can never overestimate the cost as there is no shorter length path possible
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

    node = np.copy(pos)

    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = pos
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

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

        if node[0] == destination_row:
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

        explored[node[0], node[1]] = True

        for child_node_idx in range(1, 5):
            child_node = nodes[node[0], node[1], child_node_idx]
            if child_node[0] != -1 and child_node[1] != -1:
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

                if not in_frontier and explored[child_node[0], child_node[1]] == False:
                    frontier[frontier_length] = child_node
                    frontier_length += 1


@njit(cache=True)
def Depth_First_Search_Graph_Optim(nodes, pos, destination_row, move):
    # Psuedocode from Artifical Intelligence: A modern approach
    # Adapted from Breadth First Search based on
    # "whereas breadth-first-search uses a FIFO queue, depth-first search uses a LIFO queue" - pg 85
    # -------------------------------------------------------------------------------
    # function DEPTH-FIRST-SEARCH(problem) returns a solution, or failure
    #     node ← a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    #     if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    #     frontier ← a LIFO queue with node as the only element
    #     explored ← an empty set
    #     loop do
    #         if EMPTY?(frontier) then return failure
    #         node←POP(frontier) /*choosestheshallowestnodeinfrontier */
    #         add node.STATE to explored
    #         for each action in problem.ACTIONS(node.STATE) do
    #             child ←CHILD-NODE(problem,node,action)
    #             if child.STATE is not in explored or frontier then
    #                 if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
    #                 frontier ←INSERT(child,frontier)
    # -------------------------------------------------------------------------------
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

    node = np.copy(pos)

    if node[0] == destination_row:
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

    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = node
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

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
        frontier[frontier_length - 1] = [127, 127]
        frontier_length -= 1

        explored[node[0], node[1]] = True

        for child_node_idx in range(1, 5):
            child_node = nodes[node[0], node[1], child_node_idx]
            if child_node[0] != -1 and child_node[1] != -1:
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

                if not in_frontier and explored[child_node[0], child_node[1]] == False:
                    if node[0] == destination_row:
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
def Uniform_Cost_Search_Graph_Optim(nodes, pos, destination_row, move):
    # Psuedocide from Artifical INtelligence: A modern approach
    # -------------------------------------------------------------------------------
    # function UNIFORM-COST-SEARCH(problem) returns a solution, or failure
    # node ← a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    # frontier ← a priority queue ordered by PATH-COST, with node as the only element
    # explored ← an empty set
    # loop do
    #       if EMPTY?(frontier) then return failure
    #       node←POP(frontier) /*choosesthelowest-costnodeinfrontier */
    #       if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    #       add node.STATE to explored
    #       for each action in problem.ACTIONS(node.STATE) do
    #           child ←CHILD-NODE(problem,node,action)
    #           if child.STATE is not in explored or frontier then
    #               frontier ←INSERT(child,frontier)
    #           else if child.STATE is in frontier with higher PATH-COST then
    #               replace that frontier node with child
    # ------------------------------------------------------------------------------
    # PATH-COST can be interpreted as g(n) or "the cost to reach the node" - pg 93
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

    node = np.copy(pos)

    frontier = np.full((81, 3), 127, dtype=np.int8)
    frontier[0, 0:2] = node
    frontier[0, 2] = 0
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

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
        frontier[0] = [127, 127, 127]
        frontier = roll_numba(frontier, -1)
        frontier_length -= 1

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
                if not in_frontier and explored[child_node[0], child_node[1]] == False:
                    frontier[frontier_length, 0:2] = child_node
                    frontier[frontier_length, 2] = node[2] + 1
                    frontier = frontier[frontier[:, 2].argsort()]
                elif in_frontier and frontier[in_frontier_index, 2] > node[2] + 1:
                    frontier[in_frontier_index, 2] = node[2] + 1


@njit(cache=True)
def A_Star_Search_Graph_Optim(nodes, pos, destination_row, move):
    # Psuedocide from Artifical INtelligence: A modern approach
    # Adapted from Uniform Cost Search based on
    # "It evaluates nodes by combining g(n), the cost to reach the node,
    #   and h(n), the cost to get from the node to the goal" - pg 92
    # "f(n) = g(n) + h(n)
    #   f(n) = estimated cost of the cheapest solution through n" - pg 92
    # "The algorithm is identical to UNIFORM-COST-SEARCH except that A∗ uses g + h instead of g." - pg 92
    # -------------------------------------------------------------------------------
    # function A-STAR-SEARCH(problem) returns a solution, or failure
    # node ← a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
    # frontier ← a priority queue ordered by f(n), with node as the only element
    # explored ← an empty set
    # loop do
    #       if EMPTY?(frontier) then return failure
    #       node←POP(frontier) /*choosesthelowest-costnodeinfrontier */
    #       if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
    #       add node.STATE to explored
    #       for each action in problem.ACTIONS(node.STATE) do
    #           child ←CHILD-NODE(problem,node,action)
    #           if child.STATE is not in explored or frontier then
    #               frontier ←INSERT(child,frontier)
    #           else if child.STATE is in frontier with higher PATH-COST then
    #               replace that frontier node with child
    # ------------------------------------------------------------------------------
    # h(n) would be the minimum number of moves to reach the destination row - assuming no walls
    # "h(n) = estimated cost of the cheapest path from the state at node n to a goal state."
    # The heuristic above can never overestimate the cost as there is no shorter length path possible
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

    node = np.copy(pos)

    frontier = np.full((81, 4), 127, dtype=np.int8)
    frontier[0, 0:2] = node
    frontier[0, 2] = 0
    frontier[0, 3] = np.abs(destination_row - node[0])
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

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
                if not in_frontier and explored[child_node[0], child_node[1]] == False:
                    frontier[frontier_length, 0:2] = child_node
                    frontier[frontier_length, 2] = node[2] + 1
                    frontier[frontier_length, 3] = np.abs(destination_row - node[0])
                    frontier = frontier[np.sum(frontier[:, 2:], axis=1).argsort()]
                elif in_frontier and frontier[in_frontier_index, 2] > node[2] + 1:
                    frontier[in_frontier_index, 2] = node[2] + 1


@njit(cache=True)
def Breadth_First_Search_Graph_More_Optim(nodes, pos, destination_row, move):
    change_idx = np.zeros(4, dtype=np.bool8)
    if move[2] == 0:  # horizontal wall move
        if nodes[pos[0], pos[1], 0]:
            nodes[pos[0], pos[1], 0] = False
            change_idx[0] = True
        if pos[1] + 1 < 9:
            if nodes[pos[0], pos[1] + 1, 0]:
                nodes[pos[0], pos[1] + 1, 0] = False
                change_idx[1] = True
        if pos[0] + 1 < 9:
            if nodes[pos[0] + 1, pos[1], 2]:
                nodes[pos[0] + 1, pos[1], 2] = False
                change_idx[2] = True
        if pos[0] + 1 < 9 and pos[1] + 1 < 9:
            if nodes[pos[0] + 1, pos[1] + 1, 2]:
                nodes[pos[0] + 1, pos[1] + 1, 2] = False
                change_idx[3] = True
    elif move[2] == 0:
        if nodes[pos[0], pos[1], 1]:
            nodes[pos[0], pos[1], 1] = False
            change_idx[0] = True
        if pos[1] + 1 < 9:
            if nodes[pos[0], pos[1] + 1, 3]:
                nodes[pos[0], pos[1] + 1, 3] = False
                change_idx[1] = True
        if pos[0] + 1 < 9:
            if nodes[pos[0] + 1, pos[1], 1]:
                nodes[pos[0] + 1, pos[1], 1] = False
                change_idx[2] = True
        if pos[0] + 1 < 9 and pos[1] + 1 < 9:
            if nodes[pos[0] + 1, pos[1] + 1, 3]:
                nodes[pos[0] + 1, pos[1] + 1, 3] = False
                change_idx[3] = True

    node = np.copy(pos)
    if node[0] == destination_row:
        if move[2] == 0:  # horizontal wall move
            if change_idx[0]:
                nodes[pos[0], pos[1], 0] = True
            if change_idx[1]:
                nodes[pos[0], pos[1] + 1, 0] = True
            if change_idx[2]:
                nodes[pos[0] + 1, pos[1], 2] = True
            if change_idx[3]:
                nodes[pos[0] + 1, pos[1] + 1, 2] = True
        elif move[2] == 1:
            if change_idx[0]:
                nodes[pos[0], pos[1], 1] = True
            if change_idx[1]:
                nodes[pos[0], pos[1] + 1, 3] = True
            if change_idx[2]:
                nodes[pos[0] + 1, pos[1], 1] = True
            if change_idx[3]:
                nodes[pos[0] + 1, pos[1] + 1, 3] = True
        return True
    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = node
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

    while True:
        if frontier_length == 0:
            if move[2] == 0:  # horizontal wall move
                if change_idx[0]:
                    nodes[pos[0], pos[1], 0] = True
                if change_idx[1]:
                    nodes[pos[0], pos[1] + 1, 0] = True
                if change_idx[2]:
                    nodes[pos[0] + 1, pos[1], 2] = True
                if change_idx[3]:
                    nodes[pos[0] + 1, pos[1] + 1, 2] = True
            elif move[2] == 1:
                if change_idx[0]:
                    nodes[pos[0], pos[1], 1] = True
                if change_idx[1]:
                    nodes[pos[0], pos[1] + 1, 3] = True
                if change_idx[2]:
                    nodes[pos[0] + 1, pos[1], 1] = True
                if change_idx[3]:
                    nodes[pos[0] + 1, pos[1] + 1, 3] = True
            return False

        node = np.copy(frontier[0])
        frontier[0] = [127, 127]
        frontier = roll_numba(frontier, -1)
        frontier_length -= 1

        explored[node[0], node[1]] = True

        # South move possible
        if nodes[node[0], node[1], 2]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx][0] == node[0] - 1 and frontier[idx][1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
                    break
            if not in_frontier and explored[node[0] - 1, node[1]] == False:
                if node[0] - 1 == destination_row:
                    if move[2] == 0:  # horizontal wall move
                        if change_idx[0]:
                            nodes[pos[0], pos[1], 0] = True
                        if change_idx[1]:
                            nodes[pos[0], pos[1] + 1, 0] = True
                        if change_idx[2]:
                            nodes[pos[0] + 1, pos[1], 2] = True
                        if change_idx[3]:
                            nodes[pos[0] + 1, pos[1] + 1, 2] = True
                    elif move[2] == 1:
                        if change_idx[0]:
                            nodes[pos[0], pos[1], 1] = True
                        if change_idx[1]:
                            nodes[pos[0], pos[1] + 1, 3] = True
                        if change_idx[2]:
                            nodes[pos[0] + 1, pos[1], 1] = True
                        if change_idx[3]:
                            nodes[pos[0] + 1, pos[1] + 1, 3] = True
                    return True
                frontier[frontier_length] = [node[0] - 1, node[1]]
                frontier_length += 1
        # East move
        if nodes[node[0], node[1], 1]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx][0] == node[0] and frontier[idx][1] == node[1] + 1:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] + 1] == False:
                if node[1] == destination_row:
                    if move[2] == 0:  # horizontal wall move
                        if change_idx[0]:
                            nodes[pos[0], pos[1], 0] = True
                        if change_idx[1]:
                            nodes[pos[0], pos[1] + 1, 0] = True
                        if change_idx[2]:
                            nodes[pos[0] + 1, pos[1], 2] = True
                        if change_idx[3]:
                            nodes[pos[0] + 1, pos[1] + 1, 2] = True
                    elif move[2] == 1:
                        if change_idx[0]:
                            nodes[pos[0], pos[1], 1] = True
                        if change_idx[1]:
                            nodes[pos[0], pos[1] + 1, 3] = True
                        if change_idx[2]:
                            nodes[pos[0] + 1, pos[1], 1] = True
                        if change_idx[3]:
                            nodes[pos[0] + 1, pos[1] + 1, 3] = True
                    return True
                frontier[frontier_length] = [node[0], node[1] + 1]
                frontier_length += 1
        # North move
        if nodes[node[0], node[1], 0]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx][0] == node[0] + 1 and frontier[idx][1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
                    break
            if not in_frontier and explored[node[0] + 1, node[1]] == False:
                if node[0] + 1 == destination_row:
                    if move[2] == 0:  # horizontal wall move
                        if change_idx[0]:
                            nodes[pos[0], pos[1], 0] = True
                        if change_idx[1]:
                            nodes[pos[0], pos[1] + 1, 0] = True
                        if change_idx[2]:
                            nodes[pos[0] + 1, pos[1], 2] = True
                        if change_idx[3]:
                            nodes[pos[0] + 1, pos[1] + 1, 2] = True
                    elif move[2] == 1:
                        if change_idx[0]:
                            nodes[pos[0], pos[1], 1] = True
                        if change_idx[1]:
                            nodes[pos[0], pos[1] + 1, 3] = True
                        if change_idx[2]:
                            nodes[pos[0] + 1, pos[1], 1] = True
                        if change_idx[3]:
                            nodes[pos[0] + 1, pos[1] + 1, 3] = True
                    return True
                frontier[frontier_length] = [node[0] + 1, node[1]]
                frontier_length += 1
        # West move
        if nodes[node[0], node[1], 3]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx][0] == node[0] and frontier[idx][1] == node[1] - 1:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] - 1] == False:
                if node[1] == destination_row:
                    if move[2] == 0:  # horizontal wall move
                        if change_idx[0]:
                            nodes[pos[0], pos[1], 0] = True
                        if change_idx[1]:
                            nodes[pos[0], pos[1] + 1, 0] = True
                        if change_idx[2]:
                            nodes[pos[0] + 1, pos[1], 2] = True
                        if change_idx[3]:
                            nodes[pos[0] + 1, pos[1] + 1, 2] = True
                    elif move[2] == 1:
                        if change_idx[0]:
                            nodes[pos[0], pos[1], 1] = True
                        if change_idx[1]:
                            nodes[pos[0], pos[1] + 1, 3] = True
                        if change_idx[2]:
                            nodes[pos[0] + 1, pos[1], 1] = True
                        if change_idx[3]:
                            nodes[pos[0] + 1, pos[1] + 1, 3] = True
                    return True
                frontier[frontier_length] = [node[0], node[1] - 1]
                frontier_length += 1
