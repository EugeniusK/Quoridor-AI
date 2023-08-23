from Quoridor.pathfinding import BFS, DFS, GBFS, Astar
from Quoridor.actions import (
    get_available_actions_1,
    get_available_actions_2,
)

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


class VanillaPythonStaticGraph:
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

        self.hor_walls_placed = set()
        self.ver_walls_placed = set()

        global GraphShiftDict

        self.pathfinding_mode = pathfinding_mode

    def take_action(self, action: int):
        if action < 128:
            if action < 64:
                self.hor_walls_placed.add(action)
            else:
                self.ver_walls_placed.add(action)

            if self.turn == 1:
                self.p1_walls_placed += 1
                self.turn = 2
            elif self.turn == 2:
                self.p2_walls_placed += 1
                self.turn = 1
        else:
            if self.turn == 1:
                self.p1_pos += GraphShiftDict[action]
                if self.p1_pos <= 8:
                    self.over = True
                else:
                    self.turn = 2
            else:
                self.p2_pos += GraphShiftDict[action]
                if self.p2_pos >= 72:
                    self.over = True
                else:
                    self.turn = 1

    def undo_action(self, action: int):
        """
        PROTOTPYE
        """
        if action < 128:
            if action < 64:
                self.hor_walls_placed.remove(action)
            else:
                self.ver_walls_placed.remove(action)

            if self.turn == 2:
                self.p1_walls_placed -= 1
                self.turn = 1
            elif self.turn == 1:
                self.p2_walls_placed -= 1
                self.turn = 2
        else:
            raise ValueError("ONLY FOR UNDOING WALLS WITH PATHFINDING")

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
            if wall_number % 8 == 0:
                return (
                    wall_number not in self.hor_walls_placed
                    and (wall_number + 1) not in self.hor_walls_placed
                    and (wall_number + 64) not in self.ver_walls_placed
                )
            elif wall_number % 8 == 7:
                return (
                    (wall_number - 1) not in self.hor_walls_placed
                    and wall_number not in self.hor_walls_placed
                    and (wall_number + 64) not in self.ver_walls_placed
                )
            else:
                return (
                    (wall_number - 1) not in self.hor_walls_placed
                    and wall_number not in self.hor_walls_placed
                    and (wall_number + 1) not in self.hor_walls_placed
                    and (wall_number + 64) not in self.ver_walls_placed
                )
        else:
            if (wall_number - 64) // 8 == 0:
                return (
                    wall_number not in self.ver_walls_placed
                    and (wall_number + 8) not in self.ver_walls_placed
                    and (wall_number - 64) not in self.hor_walls_placed
                )
            elif (wall_number - 64) // 8 == 7:
                return (
                    (wall_number - 8) not in self.ver_walls_placed
                    and wall_number not in self.ver_walls_placed
                    and (wall_number - 64) not in self.hor_walls_placed
                )
            else:
                return (
                    (wall_number - 8) not in self.ver_walls_placed
                    and wall_number not in self.ver_walls_placed
                    and (wall_number + 8) not in self.ver_walls_placed
                    and (wall_number - 64) not in self.hor_walls_placed
                )

    def search(self, start_pos, player_number):
        if self.pathfinding_mode == "BFS":
            return BFS(self, start_pos, player_number)
        elif self.pathfinding_mode == "DFS":
            return DFS(self, start_pos, player_number)
        elif self.pathfinding_mode == "GBFS":
            return GBFS(self, start_pos, player_number)
        elif self.pathfinding_mode == "Astar":
            return Astar(self, start_pos, player_number)

    def get_available_actions(self, version=1):
        if version is None or version == 1:
            return get_available_actions_1(self)
        else:
            return get_available_actions_2(self)

    def is_over(self):
        return self.over


class VanillaPythonDynamicGraph:
    def __init__(self, pathfinding_mode="BFS"):
        # each index indicates if moves are possible in
        # S, E, N, W in order
        self.nodes = [
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
        ]

        self.p1_pos = 76
        self.p2_pos = 4

        self.p1_walls_placed = 0
        self.p2_walls_placed = 0

        self.turn = 1

        self.over = False

        self.hor_walls_placed = set()
        self.ver_walls_placed = set()

        self.pathfinding_mode = pathfinding_mode

    def take_action(self, action: int):
        if action < 128:
            if action < 64:
                self.hor_walls_placed.add(action)
                idx = action % 8 + 9 * (8 - action // 8)
                self.nodes[idx][0] = False
                self.nodes[idx + 1][0] = False
                self.nodes[idx - 9][2] = False
                self.nodes[idx - 8][2] = False
            else:
                self.ver_walls_placed.add(action)
                idx = action % 8 + 9 * (8 - (action - 64) // 8)
                self.nodes[idx][1] = False
                self.nodes[idx + 1][3] = False
                self.nodes[idx - 9][1] = False
                self.nodes[idx - 8][3] = False

            if self.turn == 1:
                self.p1_walls_placed += 1
                self.turn = 2
            elif self.turn == 2:
                self.p2_walls_placed += 1
                self.turn = 1
        else:
            if self.turn == 1:
                self.p1_pos += GraphShiftDict[action]
                if self.p1_pos <= 8:
                    self.over = True
                else:
                    self.turn = 2
            else:
                self.p2_pos += GraphShiftDict[action]
                if self.p2_pos >= 72:
                    self.over = True
                else:
                    self.turn = 1

    def undo_action(self, action: int):
        """
        PROTOTPYE
        """
        if action < 128:
            if action < 64:
                self.hor_walls_placed.remove(action)
                idx = action % 8 + 9 * (8 - action // 8)
                self.nodes[idx][0] = True
                self.nodes[idx + 1][0] = True
                self.nodes[idx - 9][2] = True
                self.nodes[idx - 8][2] = True
            else:
                self.ver_walls_placed.remove(action)
                idx = action % 8 + 9 * (8 - (action - 64) // 8)
                self.nodes[idx][1] = True
                self.nodes[idx + 1][3] = True
                self.nodes[idx - 9][1] = True
                self.nodes[idx - 8][3] = True

            if self.turn == 2:
                self.p1_walls_placed -= 1
                self.turn = 1
            elif self.turn == 1:
                self.p2_walls_placed -= 1
                self.turn = 2
        else:
            raise ValueError("ONLY FOR UNDOING WALLS WITH PATHFINDING")

    def is_direction_valid(self, pos: int, direction: int) -> bool:
        """
        direction: 0, 1, 2, 3 for NESW
        Used only for path-finding algorithms
        """
        return self.nodes[pos][direction]

    def is_wall_valid(self, wall_number: int) -> bool:
        """
        wall_number: integer

        outputs if the wall can be placed or not

        IGNORES PATHFINDING
        """
        if wall_number < 64:
            if wall_number % 8 == 0:
                return (
                    wall_number not in self.hor_walls_placed
                    and (wall_number + 1) not in self.hor_walls_placed
                    and (wall_number + 64) not in self.ver_walls_placed
                )
            elif wall_number % 8 == 7:
                return (
                    (wall_number - 1) not in self.hor_walls_placed
                    and wall_number not in self.hor_walls_placed
                    and (wall_number + 64) not in self.ver_walls_placed
                )
            else:
                return (
                    (wall_number - 1) not in self.hor_walls_placed
                    and wall_number not in self.hor_walls_placed
                    and (wall_number + 1) not in self.hor_walls_placed
                    and (wall_number + 64) not in self.ver_walls_placed
                )
        else:
            if (wall_number - 64) // 8 == 0:
                return (
                    wall_number not in self.ver_walls_placed
                    and (wall_number + 8) not in self.ver_walls_placed
                    and (wall_number - 64) not in self.hor_walls_placed
                )
            elif (wall_number - 64) // 8 == 7:
                return (
                    (wall_number - 8) not in self.ver_walls_placed
                    and wall_number not in self.ver_walls_placed
                    and (wall_number - 64) not in self.hor_walls_placed
                )
            else:
                return (
                    (wall_number - 8) not in self.ver_walls_placed
                    and wall_number not in self.ver_walls_placed
                    and (wall_number + 8) not in self.ver_walls_placed
                    and (wall_number - 64) not in self.hor_walls_placed
                )

    def search(self, start_pos, player_number):
        if self.pathfinding_mode == "BFS":
            return BFS(self, start_pos, player_number)
        elif self.pathfinding_mode == "DFS":
            return DFS(self, start_pos, player_number)
        elif self.pathfinding_mode == "GBFS":
            return GBFS(self, start_pos, player_number)
        elif self.pathfinding_mode == "Astar":
            return Astar(self, start_pos, player_number)

    def get_available_actions(self, version=1):
        if version is None or version == 1:
            return get_available_actions_1(self)
        else:
            return get_available_actions_2(self)

    def is_over(self):
        return self.over
