from collections import deque
from heapq import heapify, heappush, heappop
from queue import Queue, LifoQueue

GraphShiftDict = {
    128: -9,
    129: 1,
    130: 9,
    131: -1,
    132: -18,
    133: -8,
    134: 2,
    135: 10,
    136: 18,
    137: 8,
    138: -2,
    139: -10,
}
Heuristic_PlayerOne = {
    0: 0,
    1: 0,
    2: 0,
    3: 0,
    4: 0,
    5: 0,
    6: 0,
    7: 0,
    8: 0,
    9: 1,
    10: 1,
    11: 1,
    12: 1,
    13: 1,
    14: 1,
    15: 1,
    16: 1,
    17: 1,
    18: 2,
    19: 2,
    20: 2,
    21: 2,
    22: 2,
    23: 2,
    24: 2,
    25: 2,
    26: 2,
    27: 3,
    28: 3,
    29: 3,
    30: 3,
    31: 3,
    32: 3,
    33: 3,
    34: 3,
    35: 3,
    36: 4,
    37: 4,
    38: 4,
    39: 4,
    40: 4,
    41: 4,
    42: 4,
    43: 4,
    44: 4,
    45: 5,
    46: 5,
    47: 5,
    48: 5,
    49: 5,
    50: 5,
    51: 5,
    52: 5,
    53: 5,
    54: 6,
    55: 6,
    56: 6,
    57: 6,
    58: 6,
    59: 6,
    60: 6,
    61: 6,
    62: 6,
    63: 7,
    64: 7,
    65: 7,
    66: 7,
    67: 7,
    68: 7,
    69: 7,
    70: 7,
    71: 7,
    72: 8,
    73: 8,
    74: 8,
    75: 8,
    76: 8,
    77: 8,
    78: 8,
    79: 8,
    80: 8,
}

Heuristic_PlayerTwo = {
    0: 8,
    1: 8,
    2: 8,
    3: 8,
    4: 8,
    5: 8,
    6: 8,
    7: 8,
    8: 8,
    9: 7,
    10: 7,
    11: 7,
    12: 7,
    13: 7,
    14: 7,
    15: 7,
    16: 7,
    17: 7,
    18: 6,
    19: 6,
    20: 6,
    21: 6,
    22: 6,
    23: 6,
    24: 6,
    25: 6,
    26: 6,
    27: 5,
    28: 5,
    29: 5,
    30: 5,
    31: 5,
    32: 5,
    33: 5,
    34: 5,
    35: 5,
    36: 4,
    37: 4,
    38: 4,
    39: 4,
    40: 4,
    41: 4,
    42: 4,
    43: 4,
    44: 4,
    45: 3,
    46: 3,
    47: 3,
    48: 3,
    49: 3,
    50: 3,
    51: 3,
    52: 3,
    53: 3,
    54: 2,
    55: 2,
    56: 2,
    57: 2,
    58: 2,
    59: 2,
    60: 2,
    61: 2,
    62: 2,
    63: 1,
    64: 1,
    65: 1,
    66: 1,
    67: 1,
    68: 1,
    69: 1,
    70: 1,
    71: 1,
    72: 0,
    73: 0,
    74: 0,
    75: 0,
    76: 0,
    77: 0,
    78: 0,
    79: 0,
    80: 0,
}


def BFS(self, start_pos, player_number):
    node = [start_pos]
    if player_number == 1 and node[-1] <= 8:
        return node
    elif player_number == 2 and node[-1] >= 72:
        return node

    frontier = []
    frontier.append(node)
    explored = set()

    while len(frontier) != 0:
        node = frontier.pop(0)
        pos = node[-1]
        explored.add(pos)

        for direction in range(4):
            new_pos = pos + GraphShiftDict[128 + direction]
            if self.is_direction_valid(pos, direction) and new_pos not in explored:
                if player_number == 1 and new_pos <= 8:
                    return node + [new_pos]
                elif player_number == 2 and new_pos >= 72:
                    return node + [new_pos]
                frontier.append(node + [new_pos])
    return None


def DFS(self, start_pos, player_number):
    node = [start_pos]
    if player_number == 1 and node[-1] <= 8:
        return node
    elif player_number == 2 and node[-1] >= 72:
        return node

    frontier = []
    frontier.append(node)
    explored = set()

    while len(frontier) != 0:
        node = frontier.pop(-1)
        pos = node[-1]
        explored.add(pos)

        for direction in range(4):
            new_pos = pos + GraphShiftDict[128 + direction]
            if self.is_direction_valid(pos, direction) and new_pos not in explored:
                if player_number == 1 and new_pos <= 8:
                    return node + [new_pos]
                elif player_number == 2 and new_pos >= 72:
                    return node + [new_pos]
                frontier.append(node + [new_pos])
    return None


def GBFS(self, start_pos, player_number):
    if player_number == 1:
        node = (Heuristic_PlayerOne[start_pos], [start_pos])
    else:
        node = (Heuristic_PlayerTwo[start_pos], [start_pos])

    if player_number == 1 and node[1][-1] <= 8:
        return node[1]
    elif player_number == 2 and node[1][-1] >= 72:
        return node[1]

    frontier = [node]
    heapify(frontier)
    explored = set()

    while len(frontier) != 0:
        node = heappop(frontier)
        pos = node[1][-1]
        explored.add(pos)

        for direction in range(4):
            new_pos = pos + GraphShiftDict[128 + direction]
            if self.is_direction_valid(pos, direction) and new_pos not in explored:
                if player_number == 1:
                    if new_pos <= 8:
                        return node[1] + [new_pos]
                    frontier.append((Heuristic_PlayerOne[new_pos], node[1] + [new_pos]))

                elif player_number == 2:
                    if new_pos >= 72:
                        return node[1] + [new_pos]
                    frontier.append((Heuristic_PlayerTwo[new_pos], node[1] + [new_pos]))

    return None


def Astar(self, start_pos, player_number):
    if player_number == 1:
        node = (Heuristic_PlayerOne[start_pos], 0, [start_pos])
    else:
        node = (Heuristic_PlayerTwo[start_pos], 0, [start_pos])

    if player_number == 1 and node[2][-1] <= 8:
        return node[2]
    elif player_number == 2 and node[2][-1] >= 72:
        return node[2]

    frontier = [node]
    heapify(frontier)
    explored = set()

    while len(frontier) != 0:
        node = heappop(frontier)
        pos = node[2][-1]
        explored.add(pos)

        for direction in range(4):
            new_pos = pos + GraphShiftDict[128 + direction]
            if self.is_direction_valid(pos, direction) and new_pos not in explored:
                if player_number == 1:
                    if new_pos <= 8:
                        return node[2] + [new_pos]
                    frontier.append(
                        (
                            Heuristic_PlayerOne[new_pos] + node[1] + 1,
                            node[1] + 1,
                            node[2] + [new_pos],
                        )
                    )

                elif player_number == 2:
                    if new_pos >= 72:
                        return node[1] + [new_pos]
                    frontier.append(
                        (
                            Heuristic_PlayerTwo[new_pos] + node[1] + 1,
                            node[1] + 1,
                            node[2] + [new_pos],
                        )
                    )

    return None
