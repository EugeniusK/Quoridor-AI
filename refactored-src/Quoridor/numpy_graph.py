import numpy as np
from collections import deque

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

ActionStringDict = {
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


class GraphNumpy:
    def __init__(self, pathfinding_mode="BFS"):
        # each index indicates if moves are possible in
        # S, E, N, W in order
        self.nodes = np.array(
            [
                [False, True, True, False],
                [False, True, True, True],
                [False, True, True, True],
                [False, True, True, True],
                [False, True, True, True],
                [False, True, True, True],
                [False, True, True, True],
                [False, True, True, True],
                [False, False, True, True],
                [True, True, True, False],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, False, True, True],
                [True, True, True, False],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, False, True, True],
                [True, True, True, False],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, False, True, True],
                [True, True, True, False],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, False, True, True],
                [True, True, True, False],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, False, True, True],
                [True, True, True, False],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, False, True, True],
                [True, True, True, False],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, True, True, True],
                [True, False, True, True],
                [True, True, False, False],
                [True, True, False, True],
                [True, True, False, True],
                [True, True, False, True],
                [True, True, False, True],
                [True, True, False, True],
                [True, True, False, True],
                [True, True, False, True],
                [True, False, False, True],
            ],
            dtype=np.bool8,
        )

        self.p1_pos = 76
        self.p2_pos = 4

        self.p1_walls_placed = 0
        self.p2_walls_placed = 0

        self.turn = 1

        self.over = False

        self.actions_taken = []
        self.hor_walls_placed = set()
        self.ver_walls_placed = set()

        global ActionStringDict

        self.pathfinding_mode = pathfinding_mode

    def take_action(self, action: int):
        if action < 64:
            self.hor_walls_placed.add(action)
            idx = action % 8 + 9 * (8 - action // 8)
            self.nodes[idx, 0] = False
            self.nodes[idx + 1, 0] = False
            self.nodes[idx - 9, 2] = False
            self.nodes[idx - 8, 2] = False
        elif action < 128:
            self.ver_walls_placed.add(action)
            idx = action % 8 + 9 * (8 - (action - 64) // 8)
            self.nodes[idx, 1] = False
            self.nodes[idx + 1, 3] = False
            self.nodes[idx - 9, 1] = False
            self.nodes[idx - 8, 3] = False
        else:
            if self.turn == 1:
                self.p1_pos += GraphShiftDict[action]
            else:
                self.p2_pos += GraphShiftDict[action]

    def undo_action(self, action: int):
        """
        PROTOTPYE
        """
        if action < 64:
            self.hor_walls_placed.remove(action)
            idx = action % 8 + 9 * (8 - action // 8)
            self.nodes[idx, 0] = True
            self.nodes[idx + 1, 0] = True
            self.nodes[idx - 9, 2] = True
            self.nodes[idx - 8, 2] = True
        elif action < 128:
            self.ver_walls_placed.remove(action)
            idx = action % 8 + 9 * (8 - (action - 64) // 8)
            self.nodes[idx, 1] = True
            self.nodes[idx + 1, 3] = True
            self.nodes[idx - 9, 1] = True
            self.nodes[idx - 8, 3] = True
        else:
            if self.turn == 1:
                self.p1_pos -= GraphShiftDict[action]
            else:
                self.p2_pos -= GraphShiftDict[action]

    def is_direction_valid(self, pos: int, direction: int) -> bool:
        """
        direction: 0, 1, 2, 3 for NESW
        Used only for path-finding algorithms
        """
        return self.nodes[pos, direction]

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
                    and node + GraphShiftDict[128 + direction] not in visited
                ):
                    new_path = list(path)
                    new_path.append(node + GraphShiftDict[128 + direction])
                    queue.append(new_path)
                    visited.add(node + GraphShiftDict[128 + direction])
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
                        new_path.append(node + GraphShiftDict[128 + direction])
                        queue.append(new_path)
        if over:
            return path
        return None

    def search(self, start_pos, player_number):
        if self.pathfinding_mode == "BFS":
            return self.__BFS(start_pos, player_number)
        elif self.pathfinding_mode == "DFS":
            return self.__DFS(start_pos, player_number)

    @profile
    def get_available_actions(self) -> list:
        available_actions = []
        if self.turn == 1:
            in_turn_pos, out_turn_pos = self.p1_pos, self.p2_pos
        else:
            in_turn_pos, out_turn_pos = self.p2_pos, self.p1_pos

        previous_valid_paths = []
        for action_number in range(128):
            # validate walls
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
                if in_turn_pos + GraphShiftDict[action_number] != out_turn_pos:
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
            ActionStringDict[key] for key in sorted(available_actions) if key >= 128
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
                    if self.nodes[pos, 1]:
                        # can move East from pos so add thin wall
                        line.append("\u2502")
                    else:
                        # cannot move East from pos so add thick wall
                        line.append("\u2503")
                if row != 8:
                    if self.nodes[pos, 2] and self.nodes[pos + 9, 0]:
                        line_below.append("\u2500\u2500\u2500")
                    else:
                        line_below.append("\u2501\u2501\u2501")
                    if col != 8:
                        north = ~self.nodes[pos, 1]
                        east = ~self.nodes[pos + 1, 2]
                        south = ~self.nodes[pos + 9, 1]
                        west = ~self.nodes[pos, 2]
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
            print(str(row + 1) + "".join(line))
            print(" " + "".join(line_below))

        print("  a   b   c   d   e   f   g   h   i  ")
