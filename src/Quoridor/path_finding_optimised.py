import numpy as np
from numba import njit, int8, boolean
from .functions import roll_numba


@njit(cache=True)
def Breadth_First_Search_Graph_More_Optim(og_nodes, pos, destination_row, move):
    """
    function BREADTH-FIRST-SEARCH(problem) returns a solution, or failure
        node ← a node with STATE = problem.INITIAL-STATE, PATH-COST = 0
        if problem.GOAL-TEST(node.STATE) then return SOLUTION(node)
        frontier ← a FIFO queue with node as the only element
        explored ← an empty set
        loop do
            if EMPTY?(frontier) then return failure
            node←POP(frontier)
            add node.STATE to explored
            for each action in problem.ACTIONS(node.STATE) do
                child ←CHILD-NODE(problem,node,action)
                if child.STATE is not in explored or frontier then
                        if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
                        frontier ←INSERT(child,frontier)
    """
    nodes = np.copy(og_nodes)
    if move[2] == 0:  # horizontal wall move
        if nodes[pos[0], pos[1], 0]:
            nodes[pos[0], pos[1], 0] = False
        if pos[1] + 1 < 9:
            if nodes[pos[0], pos[1] + 1, 0]:
                nodes[pos[0], pos[1] + 1, 0] = False
        if pos[0] + 1 < 9:
            if nodes[pos[0] + 1, pos[1], 2]:
                nodes[pos[0] + 1, pos[1], 2] = False
        if pos[0] + 1 < 9 and pos[1] + 1 < 9:
            if nodes[pos[0] + 1, pos[1] + 1, 2]:
                nodes[pos[0] + 1, pos[1] + 1, 2] = False
    elif move[2] == 0:
        if nodes[pos[0], pos[1], 1]:
            nodes[pos[0], pos[1], 1] = False
        if pos[1] + 1 < 9:
            if nodes[pos[0], pos[1] + 1, 3]:
                nodes[pos[0], pos[1] + 1, 3] = False
        if pos[0] + 1 < 9:
            if nodes[pos[0] + 1, pos[1], 1]:
                nodes[pos[0] + 1, pos[1], 1] = False
        if pos[0] + 1 < 9 and pos[1] + 1 < 9:
            if nodes[pos[0] + 1, pos[1] + 1, 3]:
                nodes[pos[0] + 1, pos[1] + 1, 3] = False
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
                if node[1] == destination_row:
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
                if node[1] == destination_row:
                    return True
                frontier[frontier_length] = [node[0], node[1] - 1]
                frontier_length += 1
