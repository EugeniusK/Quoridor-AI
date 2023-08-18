import heapq
from collections import deque

import numpy as np

"""
Bitboard implemented using NumPy arrays

----2---- (top left is index 0)
---------
---------
---------
---------
---------
---------
---------
----1---- (bottom right is index 288)

Bitboard is made up of five 64-bit integers. The first integer is
from the top left and the fifth integer is ending bottom right.



class QuoridorBoard:
    def __init__(self):
        
    def is_over(self):
        Over: a boolean indicating if the board state is of a game over or not

    def take_action(self, action):
        Action: an integer in the range 0~139

        Actions 0~63 represent horizontal wall placements
        where 0 represents a1h, 1 represents b1h, ..., 63 represents i8h

        Actions 64~127 represent vertical wall placements
        where 0 represents a1v, 1 represents b1v, ..., 63 represents i8v

        Actions 128~139 represent the moves from the player's position
        -  N, E, S, W, NN, NE, EE, SE, SS, SW, WW, NW

        THERE IS NO VALIDATION OF THE ACTION

    def is_direction_valid(self, action):
        returns a boolean indicating if the action is valid
        - will be used by pathfinding algorithm separately

    def display(self):
        outputs the board using CLI or GUI
"""

"""
Graph-board implemented with NumPy array
"""

GraphActionDict = {
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

ActionDict = {
    128: "N",
    129: "E",
    130: "S",
    131: "W",
    132: "NN",
    133: "NE",
    134: "EE",
    135: "SE",
    136: "SS",
    137: "SW",
    138: "WW",
    139: "NW",
}


GraphVanillaAdjList = (
    (False, True, True, False),
    (False, True, True, True),
    (False, True, True, True),
    (False, True, True, True),
    (False, True, True, True),
    (False, True, True, True),
    (False, True, True, True),
    (False, True, True, True),
    (False, False, True, True),
    (True, True, True, False),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, False, True, True),
    (True, True, True, False),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, False, True, True),
    (True, True, True, False),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, False, True, True),
    (True, True, True, False),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, False, True, True),
    (True, True, True, False),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, False, True, True),
    (True, True, True, False),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, False, True, True),
    (True, True, True, False),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, True, True, True),
    (True, False, True, True),
    (True, True, False, False),
    (True, True, False, True),
    (True, True, False, True),
    (True, True, False, True),
    (True, True, False, True),
    (True, True, False, True),
    (True, True, False, True),
    (True, True, False, True),
    (True, False, False, True),
)


class GraphVanilla:
    def __init__(self, pathfinding_mode="BFS"):
        # each index indicates if moves are possible in
        # S, E, N, W in order
        global GraphVanillaAdjList

        self.p1_pos = 76
        self.p2_pos = 4

        self.p1_walls_placed = 0
        self.p2_walls_placed = 0

        self.turn = 1

        self.over = False

        self.actions_taken = []
        self.hor_walls_placed = set()
        self.ver_walls_placed = set()

        global GraphActionDict

        self.pathfinding_mode = pathfinding_mode

    def take_action(self, action: int):
        if action < 64:
            self.hor_walls_placed.add(action)
        elif action < 128:
            self.ver_walls_placed.add(action)
        else:
            if self.turn == 1:
                self.p1_pos += GraphActionDict[action]
            else:
                self.p2_pos += GraphActionDict[action]

    def undo_action(self, action: int):
        if action < 64:
            self.hor_walls_placed.remove(action)
        elif action < 128:
            self.ver_walls_placed.remove(action)
        else:
            if self.turn == 1:
                self.p1_pos -= GraphActionDict[action]
            else:
                self.p2_pos -= GraphActionDict[action]

    def is_direction_valid(self, pos: int, direction: int) -> bool:
        """
        direction: 0, 1, 2, 3 for NESW
        Used only for path-finding algorithms
        """
        if GraphVanillaAdjList[pos][direction]:
            if direction == 0:  # North
                if pos % 9 == 0:
                    return (pos % 9 + 8 * (8 - pos // 9)) not in self.hor_walls_placed
                elif pos % 9 == 8:
                    return (
                        pos % 9 + 8 * (8 - pos // 9) - 1
                    ) not in self.hor_walls_placed
                elif pos % 9 != 0:
                    return (
                        pos % 9 + 8 * (8 - pos // 9) - 1
                    ) not in self.hor_walls_placed and (
                        pos % 9 + 8 * (8 - pos // 9)
                    ) not in self.hor_walls_placed
            elif direction == 1:  # East
                if pos < 9:
                    return (pos % 9 + (15 - pos // 9) * 8) not in self.ver_walls_placed
                elif pos >= 72:
                    return (pos % 9 + (16 - pos // 9) * 8) not in self.ver_walls_placed
                else:
                    return (
                        pos % 9 + (15 - pos // 9) * 8
                    ) not in self.ver_walls_placed and (
                        pos % 9 + (16 - pos // 9) * 8
                    ) not in self.ver_walls_placed
            elif direction == 2:  # South
                if pos % 9 == 0:
                    return (pos % 9 + 8 * (7 - pos // 9)) not in self.hor_walls_placed
                elif pos % 9 == 8:
                    return (
                        pos % 9 + 8 * (7 - pos // 9) - 1
                    ) not in self.hor_walls_placed
                elif pos % 9 != 0:
                    return (
                        pos % 9 + 8 * (7 - pos // 9) - 1
                    ) not in self.hor_walls_placed and (
                        pos % 9 + 8 * (7 - pos // 9)
                    ) not in self.hor_walls_placed
            elif direction == 3:  # West
                if pos < 9:
                    return (
                        pos % 9 + (15 - pos // 9) * 8
                    ) - 1 not in self.ver_walls_placed

                elif pos >= 72:
                    return (
                        pos % 9 + (16 - pos // 9) * 8
                    ) - 1 not in self.ver_walls_placed
                else:
                    return (
                        pos % 9 + (15 - pos // 9) * 8 - 1
                    ) not in self.ver_walls_placed and (
                        pos % 9 + (16 - pos // 9) * 8 - 1
                    ) not in self.ver_walls_placed
        else:
            return False

    def is_wall_valid(self, wall_number: int) -> bool:
        """
        wall_number: integer

        outputs if the wall can be placed or not

        IGNORES PATHFINDING
        """
        if wall_number < 64:
            return (
                (wall_number - 1) not in self.hor_walls_placed
                and wall_number not in self.hor_walls_placed
                and (wall_number + 1) not in self.hor_walls_placed
                and (wall_number + 64) not in self.ver_walls_placed
            )
        else:
            return (
                (wall_number - 8) not in self.ver_walls_placed
                and wall_number not in self.ver_walls_placed
                and (wall_number + 8) not in self.ver_walls_placed
                and (wall_number - 64) not in self.hor_walls_placed
            )

    def __BFS(self, start_pos, player_number):
        queue = deque(maxlen=81)
        queue.append([start_pos])
        visited = set()
        over = False
        while queue:
            path = queue.popleft()
            node = path[-1]
            visited.add(node)
            if player_number == 1 and node <= 8:
                over = True
                break
            elif player_number == 2 and node >= 72:
                over = True
                break

            for direction in range(4):
                if (
                    self.is_direction_valid(node, direction)
                    and node + GraphActionDict[128 + direction] not in visited
                ):
                    new_path = list(path)
                    new_path.append(node + GraphActionDict[128 + direction])
                    queue.append(new_path)
                    visited.add(node + GraphActionDict[128 + direction])
        if over:
            return path
        return None

    def __DFS(self, start_pos, player_number):
        queue = deque(maxlen=81)
        queue.append([start_pos])
        visited = set()
        over = False
        while queue:
            path = queue.pop()
            node = path[-1]
            if player_number == 1 and node <= 8:
                over = True
                break
            elif player_number == 2 and node >= 72:
                over = True
                break
            if node not in visited:
                visited.add(node)
                for direction in range(4):
                    if self.is_direction_valid(node, direction):
                        new_path = list(path)
                        new_path.append(node + GraphActionDict[128 + direction])
                        queue.append(new_path)
        if over:
            return path
        return None

    def search(self, start_pos, player_number):
        if self.pathfinding_mode == "BFS":
            return self.__BFS(start_pos, player_number)
        elif self.pathfinding_mode == "DFS":
            return self.__DFS(start_pos, player_number)

    def get_available_actions_slow(self) -> list:
        available_actions = []
        if self.turn == 1:
            in_turn_pos, out_turn_pos = self.p1_pos, self.p2_pos
        else:
            in_turn_pos, out_turn_pos = self.p2_pos, self.p1_pos

        for action_number in range(128):
            # validate walls
            if self.is_wall_valid(action_number):
                path = self.search(self.p1_pos, 1, action_number)
                if path is not None:
                    available_actions.append(action_number)

        for action_number in range(128, 132):
            if self.is_direction_valid(in_turn_pos, action_number - 128):
                if in_turn_pos + GraphActionDict[action_number] != out_turn_pos:
                    available_actions.append(action_number)
                else:
                    direction = action_number - 128
                    if self.is_direction_valid(out_turn_pos, direction):
                        available_actions.append(132 + 2 * direction)
                    else:
                        if self.is_direction_valid(out_turn_pos, (direction + 1) % 4):
                            available_actions.append(132 + (2 * direction + 1) % 8)
                        if self.is_direction_valid(out_turn_pos, (direction - 1) % 4):
                            available_actions.append(132 + (2 * direction - 1) % 8)

        return sorted(available_actions), [
            ActionDict[key] for key in sorted(available_actions) if key >= 128
        ]

    @profile
    def get_available_actions(self) -> list:
        available_actions = []
        if self.turn == 1:
            in_turn_pos, out_turn_pos = self.p1_pos, self.p2_pos
        else:
            in_turn_pos, out_turn_pos = self.p2_pos, self.p1_pos

        previous_valid_paths = []
        for action_number in range(128):
            if self.is_wall_valid(action_number):
                if len(previous_valid_paths) == 0:
                    path = self.search(self.p1_pos, 1)
                    if path is not None:
                        previous_valid_paths.append(path)
                        available_actions.append(action_number)
                else:
                    self.take_action(action_number)
                    path_traversed = False
                    for path in previous_valid_paths:
                        for idx in range(len(path) - 1):
                            shift = path[idx + 1] - path[idx]
                            if shift == -9 and not self.is_direction_valid(
                                path[idx], 0
                            ):
                                break
                            elif shift == 1 and not self.is_direction_valid(
                                path[idx], 1
                            ):
                                break
                            elif shift == 9 and not self.is_direction_valid(
                                path[idx], 2
                            ):
                                break
                            elif shift == -1 and not self.is_direction_valid(
                                path[idx], 3
                            ):
                                break
                        else:
                            path_traversed = True
                            break
                    if path_traversed:
                        available_actions.append(action_number)
                    else:
                        path = self.search(self.p1_pos, 1)
                        if path is not None:
                            previous_valid_paths.append(path)
                            available_actions.append(action_number)
                    self.undo_action(action_number)

        for action_number in range(128, 132):
            if self.is_direction_valid(in_turn_pos, action_number - 128):
                if in_turn_pos + GraphActionDict[action_number] != out_turn_pos:
                    available_actions.append(action_number)
                else:
                    direction = action_number - 128
                    if self.is_direction_valid(out_turn_pos, direction):
                        available_actions.append(132 + 2 * direction)
                    else:
                        if self.is_direction_valid(out_turn_pos, (direction + 1) % 4):
                            available_actions.append(132 + (2 * direction + 1) % 8)
                        if self.is_direction_valid(out_turn_pos, (direction - 1) % 4):
                            available_actions.append(132 + (2 * direction - 1) % 8)
        return sorted(available_actions), [
            ActionDict[key] for key in sorted(available_actions) if key >= 128
        ]

    def display(self):
        for row in range(9):
            line = []
            line_below = []
            for col in range(9):
                pos = row * 9 + col
                if pos == self.p1_pos:
                    line.append(" 1 ")
                elif row * 9 + col == self.p2_pos:
                    line.append(" 2 ")
                else:
                    line.append("   ")

                if col != 8:
                    if (
                        pos % 9 + (15 - pos // 9) * 8
                    ) not in self.ver_walls_placed and (
                        pos % 9 + (16 - pos // 9) * 8
                    ) not in self.ver_walls_placed:
                        # can move East from pos so add thin wall
                        line.append("\u2502")
                    else:
                        # cannot move East from pos so add thick wall
                        line.append("\u2503")
                if row != 8:
                    if col == 0:
                        if (pos % 9 + 8 * (7 - pos // 9)) not in self.hor_walls_placed:
                            line_below.append("\u2500\u2500\u2500")
                        else:
                            line_below.append("\u2501\u2501\u2501")
                    elif col == 8:
                        if (
                            pos % 9 + 8 * (7 - pos // 9) - 1
                        ) not in self.hor_walls_placed:
                            line_below.append("\u2500\u2500\u2500")
                        else:
                            line_below.append("\u2501\u2501\u2501")
                    else:
                        if (
                            pos % 9 + 8 * (7 - pos // 9) - 1
                        ) not in self.hor_walls_placed and (
                            pos % 9 + 8 * (7 - pos // 9)
                        ) not in self.hor_walls_placed:
                            line_below.append("\u2500\u2500\u2500")
                        else:
                            line_below.append("\u2501\u2501\u2501")

                    if col != 8:
                        if col == 7:
                            north = (
                                pos % 9 + (15 - pos // 9) * 8
                            ) in self.ver_walls_placed or (
                                pos % 9 + (16 - pos // 9) * 8
                            ) in self.ver_walls_placed
                            east = (
                                pos % 9 + 8 * (7 - pos // 9)
                            ) in self.hor_walls_placed
                            south = (
                                pos % 9 + (14 - pos // 9) * 8
                            ) in self.ver_walls_placed or (
                                pos % 9 + (15 - pos // 9) * 8
                            ) in self.ver_walls_placed
                            west = (
                                pos % 9 + 8 * (7 - pos // 9) - 1
                            ) in self.hor_walls_placed or (
                                pos % 9 + 8 * (7 - pos // 9)
                            ) in self.hor_walls_placed
                        elif col == 0:
                            north = (
                                pos % 9 + (15 - pos // 9) * 8
                            ) in self.ver_walls_placed or (
                                pos % 9 + (16 - pos // 9) * 8
                            ) in self.ver_walls_placed
                            east = (
                                pos % 9 + 8 * (7 - pos // 9)
                            ) in self.hor_walls_placed or (
                                pos % 9 + 8 * (7 - pos // 9) + 1
                            ) in self.hor_walls_placed
                            south = (
                                pos % 9 + (14 - pos // 9) * 8
                            ) in self.ver_walls_placed or (
                                pos % 9 + (15 - pos // 9) * 8
                            ) in self.ver_walls_placed
                            west = (
                                pos % 9 + 8 * (7 - pos // 9)
                            ) in self.hor_walls_placed
                        else:
                            north = (
                                pos % 9 + (15 - pos // 9) * 8
                            ) in self.ver_walls_placed or (
                                pos % 9 + (16 - pos // 9) * 8
                            ) in self.ver_walls_placed
                            east = (
                                pos % 9 + 8 * (7 - pos // 9)
                            ) in self.hor_walls_placed or (
                                pos % 9 + 8 * (7 - pos // 9) + 1
                            ) in self.hor_walls_placed
                            south = (
                                pos % 9 + (14 - pos // 9) * 8
                            ) in self.ver_walls_placed or (
                                pos % 9 + (15 - pos // 9) * 8
                            ) in self.ver_walls_placed
                            west = (
                                pos % 9 + 8 * (7 - pos // 9) - 1
                            ) in self.hor_walls_placed or (
                                pos % 9 + 8 * (7 - pos // 9)
                            ) in self.hor_walls_placed
                        if (
                            north == False
                            and east == False
                            and south == False
                            and west == False
                        ):
                            line_below.append("\u253c")
                        elif (
                            north == False
                            and east == False
                            and south == False
                            and west == True
                        ):
                            line_below.append("\u253d")
                        elif (
                            north == False
                            and east == True
                            and south == False
                            and west == False
                        ):
                            line_below.append("\u253e")
                        elif (
                            north == False
                            and east == True
                            and south == False
                            and west == True
                        ):
                            line_below.append("\u253f")
                        elif (
                            north == True
                            and east == False
                            and south == False
                            and west == False
                        ):
                            line_below.append("\u2540")
                        elif (
                            north == False
                            and east == False
                            and south == True
                            and west == False
                        ):
                            line_below.append("\u2541")
                        elif (
                            north == True
                            and east == False
                            and south == True
                            and west == False
                        ):
                            line_below.append("\u2542")
                        elif (
                            north == True
                            and east == False
                            and south == False
                            and west == True
                        ):
                            line_below.append("\u2543")
                        elif (
                            north == True
                            and east == True
                            and south == False
                            and west == False
                        ):
                            line_below.append("\u2544")
                        elif (
                            north == False
                            and east == False
                            and south == True
                            and west == True
                        ):
                            line_below.append("\u2545")
                        elif (
                            north == False
                            and east == True
                            and south == True
                            and west == False
                        ):
                            line_below.append("\u2546")
                        elif (
                            north == True
                            and east == True
                            and south == False
                            and west == True
                        ):
                            line_below.append("\u2547")
                        elif (
                            north == False
                            and east == True
                            and south == True
                            and west == True
                        ):
                            line_below.append("\u2548")
                        elif (
                            north == True
                            and east == False
                            and south == True
                            and west == True
                        ):
                            line_below.append("\u2549")
                        elif (
                            north == True
                            and east == True
                            and south == True
                            and west == False
                        ):
                            line_below.append("\u254A")
                        elif (
                            north == True
                            and east == True
                            and south == True
                            and west == True
                        ):
                            line_below.append("\u254B")
            print("".join(line))
            print("".join(line_below))
