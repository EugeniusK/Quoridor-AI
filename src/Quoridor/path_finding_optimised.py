import numpy as np
from numba import njit, int8, boolean
from .functions import roll_numba


@njit(cache=True)
def Breadth_First_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
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
    nodes = np.copy(og_nodes)
    if move[2] == 0:
        nodes[move[0], move[1], 0] = False
        nodes[move[0] + 1, move[1], 2] = False
        nodes[move[0], move[1] + 1, 0] = False
        nodes[move[0] + 1, move[1] + 1, 2] = False
    if move[2] == 1:
        nodes[move[0], move[1], 1] = False
        nodes[move[0], move[1] + 1, 3] = False
        nodes[move[0] + 1, move[1], 1] = False
        nodes[move[0] + 1, move[1] + 1, 3] = False
    node = np.copy(pos)
    if node[0] == destination_row:
        return True
    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = node
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

    while True:
        if frontier_length == 0:
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
                if frontier[idx, 0] == node[0] - 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] - 1, node[1]] == False:
                if node[0] - 1 == destination_row:
                    return True
                frontier[frontier_length] = [node[0] - 1, node[1]]
                frontier_length += 1
        # East move
        if nodes[node[0], node[1], 1]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] + 1:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] + 1] == False:
                if node[0] == destination_row:
                    return True
                frontier[frontier_length] = [node[0], node[1] + 1]
                frontier_length += 1
        # North move
        if nodes[node[0], node[1], 0]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] + 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] + 1, node[1]] == False:
                if node[0] + 1 == destination_row:
                    return True
                frontier[frontier_length] = [node[0] + 1, node[1]]
                frontier_length += 1
        # West move
        if nodes[node[0], node[1], 3]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] - 1:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] - 1] == False:
                if node[0] == destination_row:
                    return True
                frontier[frontier_length] = [node[0], node[1] - 1]
                frontier_length += 1


@njit(cache=True)
def Depth_First_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
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
    nodes = np.copy(og_nodes)
    if move[2] == 0:
        nodes[move[0], move[1], 0] = False
        nodes[move[0] + 1, move[1], 2] = False
        nodes[move[0], move[1] + 1, 0] = False
        nodes[move[0] + 1, move[1] + 1, 2] = False
    if move[2] == 1:
        nodes[move[0], move[1], 1] = False
        nodes[move[0], move[1] + 1, 3] = False
        nodes[move[0] + 1, move[1], 1] = False
        nodes[move[0] + 1, move[1] + 1, 3] = False
    node = np.copy(pos)
    if node[0] == destination_row:
        return True
    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = node
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

    while True:
        if frontier_length == 0:
            return False

        node = np.copy(frontier[frontier_length - 1])
        frontier[frontier_length - 1] = [127, 127]
        frontier_length -= 1

        explored[node[0], node[1]] = True

        # South move possible
        if nodes[node[0], node[1], 2]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] - 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] - 1, node[1]] == False:
                if node[0] - 1 == destination_row:
                    return True
                frontier[frontier_length] = [node[0] - 1, node[1]]
                frontier_length += 1
        # East move
        if nodes[node[0], node[1], 1]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] + 1:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] + 1] == False:
                if node[0] == destination_row:
                    return True
                frontier[frontier_length] = [node[0], node[1] + 1]
                frontier_length += 1
        # North move
        if nodes[node[0], node[1], 0]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] + 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] + 1, node[1]] == False:
                if node[0] + 1 == destination_row:
                    return True
                frontier[frontier_length] = [node[0] + 1, node[1]]
                frontier_length += 1
        # West move
        if nodes[node[0], node[1], 3]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] - 1:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] - 1] == False:
                if node[0] == destination_row:
                    return True
                frontier[frontier_length] = [node[0], node[1] - 1]
                frontier_length += 1


@njit(cache=True)  # GBFS with argmin for min manhatten distance to query node
def Greedy_Best_First_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
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
    nodes = np.copy(og_nodes)
    if move[2] == 0:
        nodes[move[0], move[1], 0] = False
        nodes[move[0] + 1, move[1], 2] = False
        nodes[move[0], move[1] + 1, 0] = False
        nodes[move[0] + 1, move[1] + 1, 2] = False
    elif move[2] == 1:
        nodes[move[0], move[1], 1] = False
        nodes[move[0], move[1] + 1, 3] = False
        nodes[move[0] + 1, move[1], 1] = False
        nodes[move[0] + 1, move[1] + 1, 3] = False
    node = np.copy(pos)
    if node[0] == destination_row:
        return True
    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = node
    frontier_length = 1

    frontier_manhatten_distance = np.full((81), 127, dtype=np.int8)
    frontier_manhatten_distance[0] = np.abs(destination_row - node[0])
    explored = np.zeros((9, 9), dtype=np.bool8)
    while True:
        if frontier_length == 0:
            return False
        min_idx = np.argmin(frontier_manhatten_distance)
        node = np.copy(frontier[min_idx])

        frontier_length -= 1

        explored[node[0], node[1]] = True

        # South move possible
        if nodes[node[0], node[1], 2]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] - 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] - 1, node[1]] == False:
                if node[0] - 1 == destination_row:
                    return True
                max_idx = np.argmax(frontier_manhatten_distance)
                frontier[max_idx] = [node[0] - 1, node[1]]
                frontier_manhatten_distance[max_idx] = np.abs(
                    destination_row - (node[0] - 1)
                )
                frontier_length += 1

        # East move possible
        if nodes[node[0], node[1], 1]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] + 1:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] + 1] == False:
                if node[0] == destination_row:
                    return True
                max_idx = np.argmax(frontier_manhatten_distance)
                frontier[max_idx] = [node[0], node[1] + 1]
                frontier_manhatten_distance[max_idx] = np.abs(destination_row - node[0])
                frontier_length += 1

        # North move possible
        if nodes[node[0], node[1], 0]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] + 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] + 1, node[1]] == False:
                if node[0] + 1 == destination_row:
                    return True
                max_idx = np.argmax(frontier_manhatten_distance)
                frontier[max_idx] = [node[0] + 1, node[1]]
                frontier_manhatten_distance[max_idx] = np.abs(
                    destination_row - (node[0] + 1)
                )
                frontier_length += 1

        # East move possible
        if nodes[node[0], node[1], 3]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] - 1:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] - 1] == False:
                if node[0] == destination_row:
                    return True
                max_idx = np.argmax(frontier_manhatten_distance)
                frontier[max_idx] = [node[0], node[1] - 1]
                frontier_manhatten_distance[max_idx] = np.abs(destination_row - node[0])
                frontier_length += 1

        frontier[min_idx] = [127, 127]
        frontier_manhatten_distance[min_idx] = 127


@njit(cache=True)  # GBFS with sort
def _Greedy_Best_First_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
    # Psuedocode from Artifical INtelligence: A modern approach
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
    nodes = np.copy(og_nodes)
    if move[2] == 0:
        nodes[move[0], move[1], 0] = False
        nodes[move[0] + 1, move[1], 2] = False
        nodes[move[0], move[1] + 1, 0] = False
        nodes[move[0] + 1, move[1] + 1, 2] = False
    elif move[2] == 1:
        nodes[move[0], move[1], 1] = False
        nodes[move[0], move[1] + 1, 3] = False
        nodes[move[0] + 1, move[1], 1] = False
        nodes[move[0] + 1, move[1] + 1, 3] = False
    node = np.copy(pos)
    if node[0] == destination_row:
        return True
    frontier = np.full((81, 3), 127, dtype=np.int8)
    frontier[0, 0:2] = node
    frontier[0, 2] = np.abs(destination_row - node[0])
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

    while True:
        if frontier_length == 0:
            return False

        node = np.copy(frontier[0])
        frontier[0] = [127, 127, 127]
        frontier = roll_numba(frontier, -1)
        frontier_length -= 1

        explored[node[0], node[1]] = True

        # South move possible
        if nodes[node[0], node[1], 2]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] - 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] - 1, node[1]] == False:
                if node[0] - 1 == destination_row:
                    return True
                frontier[frontier_length] = [
                    node[0] - 1,
                    node[1],
                    np.abs(destination_row - node[0] + 1),
                ]
                frontier_length += 1
        # East move
        if nodes[node[0], node[1], 1]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] + 1:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] + 1] == False:
                if node[0] == destination_row:
                    return True
                frontier[frontier_length] = [
                    node[0],
                    node[1] + 1,
                    np.abs(destination_row - node[0]),
                ]
                frontier_length += 1
        # North move
        if nodes[node[0], node[1], 0]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] + 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] + 1, node[1]] == False:
                if node[0] + 1 == destination_row:
                    return True
                frontier[frontier_length] = [
                    node[0] + 1,
                    node[1],
                    np.abs(destination_row - node[0] - 1),
                ]
                frontier_length += 1
        # West move
        if nodes[node[0], node[1], 3]:
            in_frontier = False
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] - 1:
                    in_frontier = True
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] - 1] == False:
                if node[0] == destination_row:
                    return True
                frontier[frontier_length] = [
                    node[0],
                    node[1] - 1,
                    np.abs(destination_row - node[0]),
                ]
                frontier_length += 1

        frontier = frontier[frontier[:, 2].argsort()]


@njit(cache=True)  # UCT with sort
def _Uniform_Cost_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
    nodes = np.copy(og_nodes)
    if move[2] == 0:
        nodes[move[0], move[1], 0] = False
        nodes[move[0] + 1, move[1], 2] = False
        nodes[move[0], move[1] + 1, 0] = False
        nodes[move[0] + 1, move[1] + 1, 2] = False
    if move[2] == 1:
        nodes[move[0], move[1], 1] = False
        nodes[move[0], move[1] + 1, 3] = False
        nodes[move[0] + 1, move[1], 1] = False
        nodes[move[0] + 1, move[1] + 1, 3] = False
    node = np.copy(pos)
    if node[0] == destination_row:
        return True
    frontier = np.full((81, 3), 127, dtype=np.int8)
    frontier[0, 0:2] = node
    frontier[2] = 0
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

    while True:
        if frontier_length == 0:
            return False

        node = np.copy(frontier[frontier_length - 1])
        frontier[frontier_length - 1] = [127, 127, 127]
        frontier_length -= 1

        explored[node[0], node[1]] = True

        # South move possible
        if nodes[node[0], node[1], 2]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] - 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] - 1, node[1]] == False:
                if node[0] - 1 == destination_row:
                    return True
                frontier[frontier_length] = [node[0] - 1, node[1], node[2] + 1]
                frontier_length += 1
            elif in_frontier and frontier[frontier_idx, 2] > node[2] + 1:
                frontier[frontier_idx, 2] = node[2] + 1
        # East move
        if nodes[node[0], node[1], 1]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] + 1:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] + 1] == False:
                if node[0] == destination_row:
                    return True
                frontier[frontier_length] = [node[0], node[1] + 1, node[2] + 1]
                frontier_length += 1
            elif in_frontier and frontier[frontier_idx, 2] > node[2] + 1:
                frontier[frontier_idx, 2] = node[2] + 1
        # North move
        if nodes[node[0], node[1], 0]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] + 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] + 1, node[1]] == False:
                if node[0] + 1 == destination_row:
                    return True
                frontier[frontier_length] = [node[0] + 1, node[1], node[2] + 1]
                frontier_length += 1
            elif in_frontier and frontier[frontier_idx, 2] > node[2] + 1:
                frontier[frontier_idx, 2] = node[2] + 1
        # West move
        if nodes[node[0], node[1], 3]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] - 1:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] - 1] == False:
                if node[0] == destination_row:
                    return True
                frontier[frontier_length] = [node[0], node[1] - 1, node[2] + 1]
                frontier_length += 1
            elif in_frontier and frontier[frontier_idx, 2] > node[2] + 1:
                frontier[frontier_idx, 2] = node[2] + 1
        frontier = frontier[frontier[:, 2].argsort()]


@njit(cache=True)  # UCT with argmin for minimum path cost from root to query node
def Uniform_Cost_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
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

    nodes = np.copy(og_nodes)
    if move[2] == 0:
        nodes[move[0], move[1], 0] = False
        nodes[move[0] + 1, move[1], 2] = False
        nodes[move[0], move[1] + 1, 0] = False
        nodes[move[0] + 1, move[1] + 1, 2] = False
    elif move[2] == 1:
        nodes[move[0], move[1], 1] = False
        nodes[move[0], move[1] + 1, 3] = False
        nodes[move[0] + 1, move[1], 1] = False
        nodes[move[0] + 1, move[1] + 1, 3] = False
    node = np.copy(pos)
    if node[0] == destination_row:
        return True
    frontier = np.full((81, 2), 127, dtype=np.int8)
    frontier[0] = node
    frontier_length = 1

    frontier_path_cost = np.full((81), 127, dtype=np.int8)
    frontier_path_cost[0] = 0
    explored = np.zeros((9, 9), dtype=np.bool8)
    while True:
        if frontier_length == 0:
            return False
        min_idx = np.argmin(frontier_path_cost)
        node = np.copy(frontier[min_idx])

        frontier_length -= 1

        explored[node[0], node[1]] = True

        # South move possible
        if nodes[node[0], node[1], 2]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] - 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] - 1, node[1]] == False:
                if node[0] - 1 == destination_row:
                    return True
                max_idx = np.argmax(frontier_path_cost)
                frontier[max_idx] = [node[0] - 1, node[1]]
                frontier_path_cost[max_idx] = frontier_path_cost[frontier_idx] + 1
                frontier_length += 1
            elif (
                in_frontier
                and frontier_path_cost[frontier_idx] > frontier_path_cost[min_idx] + 1
            ):
                frontier_path_cost[frontier_idx] = frontier_path_cost[min_idx] + 1

        # East move possible
        if nodes[node[0], node[1], 1]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] + 1:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] + 1] == False:
                if node[0] == destination_row:
                    return True
                max_idx = np.argmax(frontier_path_cost)
                frontier[max_idx] = [node[0], node[1] + 1]
                frontier_path_cost[max_idx] = frontier_path_cost[frontier_idx] + 1
                frontier_length += 1
            elif (
                in_frontier
                and frontier_path_cost[frontier_idx] > frontier_path_cost[min_idx] + 1
            ):
                frontier_path_cost[frontier_idx] = frontier_path_cost[min_idx] + 1

        # North move possible
        if nodes[node[0], node[1], 0]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] + 1 and frontier[idx, 1] == node[1]:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0] + 1, node[1]] == False:
                if node[0] + 1 == destination_row:
                    return True
                max_idx = np.argmax(frontier_path_cost)
                frontier[max_idx] = [node[0] + 1, node[1]]
                frontier_path_cost[max_idx] = frontier_path_cost[frontier_idx] + 1
                frontier_length += 1
            elif (
                in_frontier
                and frontier_path_cost[frontier_idx] > frontier_path_cost[min_idx] + 1
            ):
                frontier_path_cost[frontier_idx] = frontier_path_cost[min_idx] + 1

        # East move possible
        if nodes[node[0], node[1], 3]:
            in_frontier = False
            frontier_idx = 0
            for idx in range(81):
                if frontier[idx, 0] == node[0] and frontier[idx, 1] == node[1] - 1:
                    in_frontier = True
                    frontier_idx = idx
                    break
                elif frontier[idx, 0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] - 1] == False:
                if node[0] == destination_row:
                    return True
                max_idx = np.argmax(frontier_path_cost)
                frontier[max_idx] = [node[0], node[1] - 1]
                frontier_path_cost[max_idx] = frontier_path_cost[frontier_idx] + 1
                frontier_length += 1
            elif (
                in_frontier
                and frontier_path_cost[frontier_idx] > frontier_path_cost[min_idx] + 1
            ):
                frontier_path_cost[frontier_idx] = frontier_path_cost[min_idx] + 1
        frontier[min_idx] = [127, 127]
        frontier_path_cost[min_idx] = 127


@njit(cache=True)  # A* with argmin for f(n) / estimated cost of path through query node
def A_Star_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
    pass
