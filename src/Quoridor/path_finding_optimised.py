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
                if frontier[idx][0] == node[0] - 1 and frontier[idx][1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
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
                if frontier[idx][0] == node[0] and frontier[idx][1] == node[1] + 1:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
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
                if frontier[idx][0] == node[0] + 1 and frontier[idx][1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
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
                if frontier[idx][0] == node[0] and frontier[idx][1] == node[1] - 1:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
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
                if frontier[idx][0] == node[0] - 1 and frontier[idx][1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
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
                if frontier[idx][0] == node[0] and frontier[idx][1] == node[1] + 1:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
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
                if frontier[idx][0] == node[0] + 1 and frontier[idx][1] == node[1]:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
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
                if frontier[idx][0] == node[0] and frontier[idx][1] == node[1] - 1:
                    in_frontier = True
                    break
                elif frontier[idx][0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] - 1] == False:
                if node[0] == destination_row:
                    return True
                frontier[frontier_length] = [node[0], node[1] - 1]
                frontier_length += 1


@njit(cache=True)
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
    if move[2] == 1:
        nodes[move[0], move[1], 1] = False
        nodes[move[0], move[1] + 1, 3] = False
        nodes[move[0] + 1, move[1], 1] = False
        nodes[move[0] + 1, move[1] + 1, 3] = False
    node = np.copy(pos)
    if node[0] == destination_row:
        return True
    frontier = np.full((9, 9, 2), 127, dtype=np.int8)
    frontier[destination_row - node[0], 0] = node
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

    while True:
        if frontier_length == 0:
            return False
        for i in range(9):
            if frontier[i, 0, 0] != 127:
                node = np.copy(frontier[i, 0])
        frontier[destination_row - node[0], 0] = [127, 127]
        frontier[destination_row - node[0]] = roll_numba(
            frontier[destination_row - node[0]], -1
        )
        frontier_length -= 1

        explored[node[0], node[1]] = True

        # South move possible
        if nodes[node[0], node[1], 2]:
            in_frontier = False
            for idx in range(9):
                if (
                    frontier[destination_row - node[0], idx][0] == node[0] - 1
                    and frontier[destination_row - node[0], idx][1] == node[1]
                ):
                    in_frontier = True
                    break
                elif frontier[destination_row - node[0], idx][0] == 127:
                    break
            if not in_frontier and explored[node[0] - 1, node[1]] == False:
                if node[0] - 1 == destination_row:
                    return True
                for i in range(9):
                    if frontier[destination_row - node[0], i, 0] != 127:
                        frontier[destination_row - node[0], i] = [node[0] - 1, node[1]]
                        frontier_length += 1
                        break
        # East move
        if nodes[node[0], node[1], 1]:
            in_frontier = False
            for idx in range(9):
                if (
                    frontier[destination_row - node[0], idx][0] == node[0]
                    and frontier[destination_row - node[0], idx][1] == node[1] + 1
                ):
                    in_frontier = True
                    break
                elif frontier[destination_row - node[0], idx][0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] + 1] == False:
                if node[0] == destination_row:
                    return True
                for i in range(9):
                    if frontier[destination_row - node[0], i, 0] != 127:
                        frontier[destination_row - node[0], i] = [node[0], node[1] + 1]
                        frontier_length += 1
                        break
        # North move
        if nodes[node[0], node[1], 0]:
            in_frontier = False
            for idx in range(9):
                if (
                    frontier[destination_row - node[0], idx][0] == node[0] + 1
                    and frontier[destination_row - node[0], idx][1] == node[1]
                ):
                    in_frontier = True
                    break
                elif frontier[destination_row - node[0], idx][0] == 127:
                    break
            if not in_frontier and explored[node[0] + 1, node[1]] == False:
                if node[0] + 1 == destination_row:
                    return True
                for i in range(9):
                    if frontier[destination_row - node[0], i, 0] != 127:
                        frontier[destination_row - node[0], i] = [node[0] + 1, node[1]]
                        frontier_length += 1
                        break
        # West move
        if nodes[node[0], node[1], 3]:
            in_frontier = False
            for idx in range(9):
                if (
                    frontier[destination_row - node[0], idx][0] == node[0]
                    and frontier[destination_row - node[0], idx][1] == node[1] - 1
                ):
                    in_frontier = True
                    break
                elif frontier[destination_row - node[0], idx][0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] - 1] == False:
                if node[0] == destination_row:
                    return True
                for i in range(9):
                    if frontier[destination_row - node[0], i, 0] != 127:
                        frontier[destination_row - node[0], i] = [node[0], node[1] - 1]
                        frontier_length += 1
                        break


def Uniform_Cost_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
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
    frontier = np.full((9, 9, 2), 127, dtype=np.int8)
    frontier[destination_row - node[0], 0] = node
    frontier_length = 1

    explored = np.zeros((9, 9), dtype=np.bool8)

    while True:
        if frontier_length == 0:
            return False
        for i in range(9):
            if frontier[i, 0, 0] != 127:
                node = np.copy(frontier[i, 0])
        frontier[destination_row - node[0], 0] = [127, 127]
        frontier[destination_row - node[0]] = roll_numba(
            frontier[destination_row - node[0]], -1
        )
        frontier_length -= 1

        explored[node[0], node[1]] = True

        # South move possible
        if nodes[node[0], node[1], 2]:
            in_frontier = False
            for idx in range(9):
                if (
                    frontier[destination_row - node[0], idx][0] == node[0] - 1
                    and frontier[destination_row - node[0], idx][1] == node[1]
                ):
                    in_frontier = True
                    break
                elif frontier[destination_row - node[0], idx][0] == 127:
                    break
            if not in_frontier and explored[node[0] - 1, node[1]] == False:
                if node[0] - 1 == destination_row:
                    return True
                for i in range(9):
                    if frontier[destination_row - node[0], i, 0] != 127:
                        frontier[destination_row - node[0], i] = [node[0] - 1, node[1]]
                        frontier_length += 1
                        break
        # East move
        if nodes[node[0], node[1], 1]:
            in_frontier = False
            for idx in range(9):
                if (
                    frontier[destination_row - node[0], idx][0] == node[0]
                    and frontier[destination_row - node[0], idx][1] == node[1] + 1
                ):
                    in_frontier = True
                    break
                elif frontier[destination_row - node[0], idx][0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] + 1] == False:
                if node[0] == destination_row:
                    return True
                for i in range(9):
                    if frontier[destination_row - node[0], i, 0] != 127:
                        frontier[destination_row - node[0], i] = [node[0], node[1] + 1]
                        frontier_length += 1
                        break
        # North move
        if nodes[node[0], node[1], 0]:
            in_frontier = False
            for idx in range(9):
                if (
                    frontier[destination_row - node[0], idx][0] == node[0] + 1
                    and frontier[destination_row - node[0], idx][1] == node[1]
                ):
                    in_frontier = True
                    break
                elif frontier[destination_row - node[0], idx][0] == 127:
                    break
            if not in_frontier and explored[node[0] + 1, node[1]] == False:
                if node[0] + 1 == destination_row:
                    return True
                for i in range(9):
                    if frontier[destination_row - node[0], i, 0] != 127:
                        frontier[destination_row - node[0], i] = [node[0] + 1, node[1]]
                        frontier_length += 1
                        break
        # West move
        if nodes[node[0], node[1], 3]:
            in_frontier = False
            for idx in range(9):
                if (
                    frontier[destination_row - node[0], idx][0] == node[0]
                    and frontier[destination_row - node[0], idx][1] == node[1] - 1
                ):
                    in_frontier = True
                    break
                elif frontier[destination_row - node[0], idx][0] == 127:
                    break
            if not in_frontier and explored[node[0], node[1] - 1] == False:
                if node[0] == destination_row:
                    return True
                for i in range(9):
                    if frontier[destination_row - node[0], i, 0] != 127:
                        frontier[destination_row - node[0], i] = [node[0], node[1] - 1]
                        frontier_length += 1
                        break


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
