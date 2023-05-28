import numpy as np
from numba import njit, int8, boolean


@njit(cache=True)
def roll_numba(
    arr,
    num,
):
    result = np.empty_like(arr)
    if num > 0:
        result[:num] = arr[-num:]
        result[num:] = arr[:-num]
    elif num < 0:
        result[num:] = arr[:-num]
        result[:num] = arr[-num:]
    else:
        result[:] = arr
    return result


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

    # Create new initial state nodes where move has been made
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

    # Starting position of the player
    node = np.copy(pos)

    # If player is at destination_row, return True
    if node[0] == destination_row:
        return True

    # frontier ← array that holds a maximum of 81 positions possible on 9x9 board
    frontier = np.full((81, 2), 127, dtype=np.int8)

    # Add initial position to the frontier
    frontier[0] = node
    frontier_length = 1

    # explored ← an empty 9x9 array of boolean
    explored = np.zeros((9, 9), dtype=np.bool8)

    while True:
        # If the frontier is empty, return False
        if frontier_length == 0:
            return False
        # node ← pop from frontier at index 0 (like accessing FIFO queue)
        node = np.copy(frontier[0])
        frontier[0] = [127, 127]
        frontier = roll_numba(frontier, -1)
        frontier_length -= 1

        # Add position to explored
        explored[node[0], node[1]] = True

        # Iterate through move in all 4 possible directions
        for direction in range(0, 4):
            if direction == 2:  # South move
                idx1 = node[0] - 1
                idx2 = node[1]
            elif direction == 1:  # East move
                idx1 = node[0]
                idx2 = node[1] + 1
            elif direction == 0:  # North move
                idx1 = node[0] + 1
                idx2 = node[1]
            elif direction == 3:  # West move
                idx1 = node[0]
                idx2 = node[1] - 1

            # If the move in the given direction is valid
            if nodes[node[0], node[1], direction]:
                # Iterates through frontier and sees if move is in frontier
                in_frontier = False
                for idx in range(81):
                    if frontier[idx, 0] == idx1 and frontier[idx, 1] == idx2:
                        in_frontier = True
                        break
                    elif frontier[idx, 0] == 127:
                        break
                # If not in frontier and not explored
                if not in_frontier and explored[idx1, idx2] == False:
                    # If move reaches destination_row, return True
                    if idx1 == destination_row:
                        return True
                    # Add move to frontier
                    frontier[frontier_length] = [idx1, idx2]
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

    # Create new initial state nodes where move has been made
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

    # Starting position of the player
    node = np.copy(pos)

    # If player is at destination_row, return True
    if node[0] == destination_row:
        return True

    # frontier ← array that holds a maximum of 81 positions possible on 9x9 board
    frontier = np.full((81, 2), 127, dtype=np.int8)

    # Add initial position to the frontier
    frontier[0] = node
    frontier_length = 1

    # explored ← an empty 9x9 array of boolean
    explored = np.zeros((9, 9), dtype=np.bool8)

    while True:
        # If the frontier is empty, return False
        if frontier_length == 0:
            return False

        # node ← pop from frontier from end (like accessing LIFO queue)
        node = np.copy(frontier[frontier_length - 1])
        frontier[frontier_length - 1] = [127, 127]
        frontier_length -= 1

        explored[node[0], node[1]] = True

        # Iterate through move in all 4 possible directions
        for direction in range(0, 4):
            if direction == 2:  # South move
                idx1 = node[0] - 1
                idx2 = node[1]
            elif direction == 1:  # East move
                idx1 = node[0]
                idx2 = node[1] + 1
            elif direction == 0:  # North move
                idx1 = node[0] + 1
                idx2 = node[1]
            elif direction == 3:  # West move
                idx1 = node[0]
                idx2 = node[1] - 1

            # If the move in the given direction is valid
            if nodes[node[0], node[1], direction]:
                # Iterates through frontier and sees if move is in frontier
                in_frontier = False
                for idx in range(81):
                    if frontier[idx, 0] == idx1 and frontier[idx, 1] == idx2:
                        in_frontier = True
                        break
                    elif frontier[idx, 0] == 127:
                        break
                # If not in frontier and not explored
                if not in_frontier and explored[idx1, idx2] == False:
                    # If move reaches destination_row, return True
                    if idx1 == destination_row:
                        return True
                    # Add move to frontier
                    frontier[frontier_length] = [idx1, idx2]
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

    # Create new initial state nodes where move has been made
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

    # Starting position of the player
    node = np.copy(pos)

    # If player is at destination_row, return True
    if node[0] == destination_row:
        return True

    # frontier ← array that holds a maximum of 81 positions possible on 9x9 board
    frontier = np.full((81, 2), 127, dtype=np.int8)

    # Add initial position to the frontier
    frontier[0] = node
    frontier_length = 1

    frontier_manhatten_distance = np.full((81), 127, dtype=np.int8)
    frontier_manhatten_distance[0] = np.abs(destination_row - node[0])

    # explored ← an empty 9x9 array of boolean
    explored = np.zeros((9, 9), dtype=np.bool8)
    while True:
        # If the frontier is empty, return False
        if frontier_length == 0:
            return False

        # node ← pop from frontier with the lowest manhatten distance
        min_idx = np.argmin(frontier_manhatten_distance)
        node = np.copy(frontier[min_idx])
        frontier_length -= 1

        # Add position to explored
        explored[node[0], node[1]] = True

        # Iterate through move in all 4 possible directions
        for direction in range(0, 4):
            if direction == 2:  # South move
                idx1 = node[0] - 1
                idx2 = node[1]
            elif direction == 1:  # East move
                idx1 = node[0]
                idx2 = node[1] + 1
            elif direction == 0:  # North move
                idx1 = node[0] + 1
                idx2 = node[1]
            elif direction == 3:  # West move
                idx1 = node[0]
                idx2 = node[1] - 1
            # If the move in the given direction is valid
            if nodes[node[0], node[1], direction]:
                in_frontier = False
                for idx in range(81):
                    if frontier[idx, 0] == idx1 and frontier[idx, 1] == idx2:
                        in_frontier = True
                        break
                    elif frontier[idx, 0] == 127:
                        break
                if not in_frontier and explored[idx1, idx2] == False:
                    if idx1 == destination_row:
                        return True
                    max_idx = np.argmax(frontier_manhatten_distance)
                    frontier[max_idx] = [idx1, idx2]
                    frontier_manhatten_distance[max_idx] = np.abs(
                        destination_row - idx1
                    )
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


# @njit(cache=True)  # UCT with sort
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

        for direction in range(0, 4):
            if direction == 2:  # South move
                idx1 = node[0] - 1
                idx2 = node[1]
            elif direction == 1:  # East move
                idx1 = node[0]
                idx2 = node[1] + 1
            elif direction == 0:  # North move
                idx1 = node[0] + 1
                idx2 = node[1]
            elif direction == 3:  # West move
                idx1 = node[0]
                idx2 = node[1] - 1

            if nodes[node[0], node[1], direction]:
                # Sees if the south move is in the frontier
                in_frontier = False
                frontier_idx = 0
                for idx in range(81):
                    if frontier[idx, 0] == idx1 and frontier[idx, 1] == idx2:
                        in_frontier = True
                        frontier_idx = idx
                        break
                    elif frontier[idx, 0] == 127:
                        break
                # If not in frontier and not explored
                if not in_frontier and explored[idx1, idx2] == False:
                    # If south move reaches destination_row, return True
                    if idx1 == destination_row:
                        return True
                    # Add move to frontier with path cost
                    frontier[frontier_length] = [idx1, idx2, node[2] + 1]
                    frontier_length += 1
                # If in frontier but with higher path_cost
                elif in_frontier and frontier[frontier_idx, 2] > node[2] + 1:
                    # Update path cost to be lowest possible
                    frontier[frontier_idx, 2] = node[2] + 1
        frontier = frontier[frontier[:, 2].argsort()]


@njit(cache=True)  # UCT with argmin for minimum path cost from root to query node
def Uniform_Cost_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
    # Psuedocode from Artifical Intelligence: A modern approach
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

    # Create new initial state NODES where move has been made
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

    # Starting position of the player
    node = np.copy(pos)

    # If player is at destination_row, return True
    if node[0] == destination_row:
        return True

    # frontier ← array that holds a maximum of 81 positions possible on 9x9 board
    frontier = np.full((81, 2), 127, dtype=np.int8)
    # Add initial position to the frontier
    frontier[0] = node
    frontier_length = 1

    # frontier_path_cost ← array that holds the path cost of corresponding positions in frontier
    frontier_path_cost = np.full((81), 127, dtype=np.int8)
    frontier_path_cost[0] = 0

    # explored ← an empty 9x9 array of boolean
    explored = np.zeros((9, 9), dtype=np.bool8)
    while True:
        # If the frontier is empty, return False
        if frontier_length == 0:
            return False

        # min_idx ← index of the lowest path cost
        min_idx = np.argmin(frontier_path_cost)

        # node ← access corresponding index in frontier that has lowest path cost
        # (equivalent to popping from priortiy queue ordered by path cost)
        node = np.copy(frontier[min_idx])
        frontier_length -= 1

        # Add position to explored
        explored[node[0], node[1]] = True

        # Iterate through move in all 4 possible directions
        for direction in range(0, 4):
            # Calculate idx1 and idx2 of move based on direction
            if direction == 2:  # South move
                idx1 = node[0] - 1
                idx2 = node[1]
            elif direction == 1:  # East move
                idx1 = node[0]
                idx2 = node[1] + 1
            elif direction == 0:  # North move
                idx1 = node[0] + 1
                idx2 = node[1]
            elif direction == 3:  # West move
                idx1 = node[0]
                idx2 = node[1] - 1

            # Direction 0: North, 1: East, 2: South, 3: West
            # If the move in the given direction is valid
            if nodes[node[0], node[1], direction]:
                # Iterates through frontier and sees if move is in frontier
                in_frontier = False
                frontier_idx = 300
                for idx in range(81):
                    if frontier[idx, 0] == idx1 and frontier[idx, 1] == idx2:
                        in_frontier = True
                        frontier_idx = idx
                        break
                    # elif frontier[idx, 0] == 127:
                    #     break
                # If not in frontier and not explored
                if not in_frontier and explored[idx1, idx2] == False:
                    # If move reaches destination_row, return True
                    if idx1 == destination_row:
                        return True
                    # Gets the unused index in frontier_path_cost (first index where 127 - default init state)
                    max_idx = np.argmax(frontier_path_cost)
                    # Add move to frontier and new path cost to frontier_path_cost
                    frontier[max_idx] = [idx1, idx2]
                    frontier_path_cost[max_idx] = frontier_path_cost[min_idx] + 1
                    frontier_length += 1
                # If in frontier but with higher path_cost
                elif (
                    in_frontier
                    and frontier_path_cost[frontier_idx]
                    > frontier_path_cost[min_idx] + 1
                ):
                    # Update path cost to be lowest possible
                    frontier_path_cost[frontier_idx] = frontier_path_cost[min_idx] + 1
        frontier[min_idx] = [127, 127]
        frontier_path_cost[min_idx] = 127


@njit(cache=True)  # A* with argmin for f(n) / estimated cost of path through query node
def A_Star_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
    # Psuedocode from Artifical Intelligence: A modern approach
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

    # Create new initial state NODES where move has been made
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

    # Starting position of the player
    node = np.copy(pos)

    # If player is at destination_row, return True
    if node[0] == destination_row:
        return True

    # frontier ← array that holds a maximum of 81 positions possible on 9x9 board
    frontier = np.full((81, 2), 127, dtype=np.int8)
    # Add initial position to the frontier
    frontier[0] = node
    frontier_length = 1

    # frontier_estimate_cost ← array that holds the estimated cost of corresponding positions in frontier
    frontier_estimate_cost = np.full((81), 127, dtype=np.int8)
    frontier_estimate_cost[0] = 0 + np.abs(destination_row - node[0])

    # explored ← an empty 9x9 array of boolean
    explored = np.zeros((9, 9), dtype=np.bool8)
    while True:
        # If the frontier is empty, return False
        if frontier_length == 0:
            return False

        # min_idx ← index of the lowest estimate cost
        min_idx = np.argmin(frontier_estimate_cost)

        # node ← access corresponding index in frontier that has lowest estimate cost
        # (equivalent to popping from priortiy queue ordered by estimate cost)
        node = np.copy(frontier[min_idx])
        frontier_length -= 1

        # Add position to explored
        explored[node[0], node[1]] = True

        # Iterate through move in all 4 possible directions
        for direction in range(0, 4):
            # Calculate idx1 and idx2 of move based on direction
            if direction == 2:  # South move
                idx1 = node[0] - 1
                idx2 = node[1]
            elif direction == 1:  # East move
                idx1 = node[0]
                idx2 = node[1] + 1
            elif direction == 0:  # North move
                idx1 = node[0] + 1
                idx2 = node[1]
            elif direction == 3:  # West move
                idx1 = node[0]
                idx2 = node[1] - 1

            # Direction 0: North, 1: East, 2: South, 3: West
            # If the move in the given direction is valid
            if nodes[node[0], node[1], direction]:
                # Iterates through frontier and sees if move is in frontier
                in_frontier = False
                frontier_idx = 300
                for idx in range(81):
                    if frontier[idx, 0] == idx1 and frontier[idx, 1] == idx2:
                        in_frontier = True
                        frontier_idx = idx
                        break
                    elif frontier[idx, 0] == 127:
                        break
                # If not in frontier and not explored
                if not in_frontier and explored[idx1, idx2] == False:
                    # If move reaches destination_row, return True
                    if idx1 == destination_row:
                        return True
                    # Gets the unused index in frontier_path_cost (first index where 127 - default init state)
                    max_idx = np.argmax(frontier_estimate_cost)
                    # Add move to frontier and new path cost to frontier_path_cost
                    frontier[max_idx] = [idx1, idx2]
                    frontier_estimate_cost[max_idx] = (
                        frontier_estimate_cost[min_idx]
                        - np.abs(destination_row - node[0])
                        + 1
                        + np.abs(destination_row - idx1)
                    )
                    frontier_length += 1
                # If in frontier but with higher estimated cost
                elif (
                    in_frontier
                    and frontier_estimate_cost[frontier_idx]
                    > frontier_estimate_cost[min_idx]
                    - np.abs(destination_row - node[0])
                    + 1
                    + np.abs(destination_row - idx1),
                ):
                    # Update estimate cost to be lowest possible
                    frontier_estimate_cost[frontier_idx] = (
                        frontier_estimate_cost[min_idx]
                        - np.abs(destination_row - node[0])
                        + 1
                        + np.abs(destination_row - idx1)
                    )
        frontier[min_idx] = [127, 127]
        frontier_estimate_cost[min_idx] = 127
