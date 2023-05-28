import math
import random
import numpy as np
from numba import njit
import copy

UCT_CONST = 2
"""
    Notes taken after from https://vgarciasc.github.io/mcts-viz/

    Start from current state (root)
    Leaf - get random child node if root has no children
         - get child node with MAXIMUM UCT

    Randomly simulate from the leaf until the state is terminal
    Backpropagate values

    ALWAYS maximimse UCT during selection

    If it is the machine's turn,

    the root node has most recently made the human's move
    - the children are indicative of the moves that the machine can play
"""


def select(root):
    """Selection: Start from root and select sucessive child nodes until a leaf is reached.
    The root is the game state that Monte-Carlo Tree Search will run from.
    The leaf is the node that has no games played yet - effectively infinite UCT score.

    Input:
    root -> MCTS_NODE

    Ouput:
    path -> list

    Function returns a path from the root to the leaf.
    """

    """Description from Wikipedia - Selection: Start from root R and select successive child nodes until a leaf node L is reached.
    The root is the current game state and a leaf is any node that has a potential child from
    which no simulation (playout) has yet been initiated."""

    def uct(node, parent_node, exploration_const):
        if (
            node.games_played == 0
        ):  # prevent division by zero errors when node hasn't been visited
            return float("inf")
        return node.games_won / node.games_played + exploration_const * math.sqrt(
            math.log(parent_node.games_played) / node.games_played
        )

    path = [root]
    last_node = path[-1]
    while True:
        if len(last_node.children) == 0:
            return path
        else:
            last_node = max(
                last_node.children, key=lambda child: uct(child, last_node, UCT_CONST)
            )
            path.append(last_node)


def expand(node):
    """Expansion: Unless L ends the game decisively (e.g. win/loss/draw) for either player, create one (or more)
    child nodes and choose node C from one of them. Child nodes are any valid moves from the game position defined by L.
    """
    if node.children != []:
        raise AttributeError(
            "This function should be called on a leaf node with no children"
        )
    node.children = [MCTS_NODE(child) for child in node.state.get_available_states()]
    return random.choice(node.children)


def simulate(node, start):
    """Simulation: Complete one random playout from node C. This step is sometimes also called playout or rollout.
    A playout may be as simple as choosing uniform random moves until the game is decided (for example in chess,
    the game is won, lost, or drawn)."""
    while True:
        if node.is_over():
            # print("winner", node.winner())
            return 1 if node.winner() == start else 0
        node = random.choice(node.get_available_states())


def backpropagate(path, reward):
    """Backpropagation: Use the result of the playout to update information in the nodes on the path from C to R."""
    for node in reversed(path):
        # node.state.display_beautiful()

        node.games_won += reward
        node.games_played += 1
        # print(
        #     "turn",
        #     node.state.turn,
        #     "init_won",
        #     node.games_won - reward,
        #     "new_won",
        #     node.games_won,
        #     node.games_played,
        # )
        reward = 1 - reward


class QuoridorGraphicalBoardMoreOptimB:
    def __init__(self, path_finding_mode="BFS", **kwargs):
        # Adjaceny list stores valid edges as boolean instead of representing 2D index
        # 9x9x4 size as each position has 4 possible - North, East, South, West
        # Each node has [1, 2, 3, 4] whichrepresents valid in North, East, South, West <-- in this order
        if (
            kwargs.get("nodes") == None
            and kwargs.get("p1_pos") == None
            and kwargs.get("p2_pos") == None
            and kwargs.get("p1_walls_placed") == None
            and kwargs.get("p2_walls_placed") == None
            and kwargs.get("turn") == None
            and kwargs.get("over") == None
        ):
            self.nodes = np.array(
                [
                    [
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
                    [
                        [True, True, True, False],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, False, True, True],
                    ],
                    [
                        [True, True, True, False],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, False, True, True],
                    ],
                    [
                        [True, True, True, False],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, False, True, True],
                    ],
                    [
                        [True, True, True, False],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, False, True, True],
                    ],
                    [
                        [True, True, True, False],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, False, True, True],
                    ],
                    [
                        [True, True, True, False],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, False, True, True],
                    ],
                    [
                        [True, True, True, False],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, True, True, True],
                        [True, False, True, True],
                    ],
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
                    ],
                ],
                dtype=np.bool8,
            )

            # Position of both players represented as [row, col]
            # From perspective of player 1, [0,0] is a1 and [8,8] is h9
            self.p1_pos = np.array([0, 4], dtype=np.int8)
            self.p2_pos = np.array([8, 4], dtype=np.int8)

            # Number of walls that each player has placed
            self.p1_walls_placed = np.int8(0)
            self.p2_walls_placed = np.int8(0)

            # Player who is in turn
            self.turn = 1

            # If the game is over or not
            self.over = np.bool8(False)
        else:
            self.nodes = kwargs["nodes"]
            self.p1_pos = kwargs["p1_pos"]
            self.p2_pos = kwargs["p2_pos"]
            self.p1_walls_placed = kwargs["p1_walls_placed"]
            self.p2_walls_placed = kwargs["p2_walls_placed"]
            self.turn = kwargs["turn"]
            self.over = kwargs["over"]
        # Search mode to be used
        self.path_finding_mode = path_finding_mode

    def get_available_actions(self):
        walls_left = True
        if self.turn == 1:
            in_turn_pos = self.p1_pos
            out_turn_pos = self.p2_pos
            if self.p1_walls_placed == 10:
                walls_left = False
        else:
            in_turn_pos = self.p2_pos
            out_turn_pos = self.p1_pos
            if self.p2_walls_placed == 10:
                walls_left = False

        # Boolean array indicating if S,E,N,W moves are possible
        if in_turn_pos[0] > 8 or in_turn_pos[1] > 8:
            self.display_beautiful()
            raise IndexError
        in_turn_moves = np.copy(self.nodes[in_turn_pos[0], in_turn_pos[1]])

        actions = np.zeros(144, dtype=np.bool8)

        adjacent = False

        NORTH_MOVE = in_turn_pos + np.array([1, 0], dtype=np.int8)
        EAST_MOVE = in_turn_pos + np.array([0, 1], dtype=np.int8)
        SOUTH_MOVE = in_turn_pos + np.array([-1, 0], dtype=np.int8)
        WEST_MOVE = in_turn_pos + np.array([0, -1], dtype=np.int8)

        # Code below follows this structure:
        # If the move in a direction is valid
        # --> If the move causes the player in turn
        #     to land on player out of turn
        #         Record that players are adjacent
        #     Otherwise, add the move to actions array
        if in_turn_moves[0]:
            if np.array_equal(NORTH_MOVE, out_turn_pos):
                adjacent = True
            else:
                actions[131] = True

        if in_turn_moves[1]:
            if np.array_equal(EAST_MOVE, out_turn_pos):
                adjacent = True
            else:
                actions[135] = True

        if in_turn_moves[2]:
            if np.array_equal(SOUTH_MOVE, out_turn_pos):
                adjacent = True
            else:
                actions[139] = True

        if in_turn_moves[3]:
            if np.array_equal(WEST_MOVE, out_turn_pos):
                adjacent = True
            else:
                actions[143] = True

        # If the 2 players are adjacent,
        # Determine if the player in turn can jump over the other player
        # or if there are moves available to the side
        if adjacent:
            relative_pos = out_turn_pos - in_turn_pos
            # player in turn is North of player out of turn
            if relative_pos[0] == np.int8(1) and relative_pos[1] == np.int8(0):
                # If double North move is possible, add
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:
                    actions[129] = True

                else:
                    # Otherwise add North East, North West moves
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:
                        actions[130] = True

                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:
                        actions[128] = True

            # player in turn is East of player out of turn
            elif relative_pos[0] == np.int8(0) and relative_pos[1] == np.int8(1):
                # If double East move is possible, add
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:
                    actions[133] = True

                else:
                    # Otherwise add South East, North East moves
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:
                        actions[134] = True

                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:
                        actions[132] = True

            # player in turn is South of player out of turn
            elif relative_pos[0] == np.int8(-1) and relative_pos[1] == np.int8(0):
                # If double South move is possible, add
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:
                    actions[137] = True

                else:
                    # Otherwise add South East, South West moves
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][1]:
                        actions[136] = True

                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:
                        actions[138] = True

            # player in turn is West of player out of turn
            elif relative_pos[0] == np.int8(0) and relative_pos[1] == np.int8(-1):
                # If double West move is possible, add
                if self.nodes[out_turn_pos[0], out_turn_pos[1]][3]:
                    actions[141] = True

                else:
                    # Otherwise add South West, North West moves
                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][2]:
                        actions[140] = True

                    if self.nodes[out_turn_pos[0], out_turn_pos[1]][0]:
                        actions[142] = True

        if walls_left:
            if self.path_finding_mode == "BFS":
                search = Breadth_First_Search_Graph_More_Optim
            elif self.path_finding_mode == "DFS":
                search = Depth_First_Search_Graph_More_Optim
            elif self.path_finding_mode == "GBFS":
                search = Greedy_Best_First_Search_Graph_More_Optim
            elif self.path_finding_mode == "UCT":
                search = Uniform_Cost_Search_Graph_More_Optim
            elif self.path_finding_mode == "Astar":
                search = A_Star_Search_Graph_More_Optim
            for row in range(8):
                for col in range(8):
                    # Checks if horizontal wall position is empty
                    # - can move North from both places
                    if self.nodes[row, col, 0] and self.nodes[row, col + 1, 0]:
                        if (
                            (self.nodes[row, col, 1] or self.nodes[row + 1, col, 1])
                            or (
                                (row == 1 or row == 6)
                                and ~self.nodes[row - 1, col, 1]
                                and ~self.nodes[row, col, 1]
                                and ~self.nodes[row + 1, col, 1]
                                and ~self.nodes[row + 2, col, 1]
                            )
                            or (
                                row > 1
                                and row < 6
                                and (
                                    self.nodes[row - 2, col, 1]
                                    or self.nodes[row + 3, col, 1]
                                )
                                and ~self.nodes[row - 1, col, 1]
                                and ~self.nodes[row, col, 1]
                                and ~self.nodes[row + 1, col, 1]
                                and ~self.nodes[row + 2, col, 1]
                            )
                            or (
                                (row == 3 or row == 4)
                                and ~self.nodes[row - 3, col, 1]
                                and ~self.nodes[row - 2, col, 1]
                                and ~self.nodes[row - 1, col, 1]
                                and ~self.nodes[row, col, 1]
                                and ~self.nodes[row + 1, col, 1]
                                and ~self.nodes[row + 2, col, 1]
                                and ~self.nodes[row + 3, col, 1]
                                and ~self.nodes[row + 4, col, 1]
                            )
                        ):
                            if search(
                                self.nodes,
                                self.p1_pos,
                                8,
                                np.array([row, col, 0], dtype=np.int8),
                            ) and search(
                                self.nodes,
                                self.p2_pos,
                                0,
                                np.array([row, col, 0], dtype=np.int8),
                            ):
                                actions[row * 8 + col] = True

                    if self.nodes[row, col, 1] and self.nodes[row + 1, col, 1]:
                        if (
                            (self.nodes[row, col, 0] or self.nodes[row, col + 1, 0])
                            or (
                                (col == 1 or col == 6)
                                and ~self.nodes[row, col - 1, 0]
                                and ~self.nodes[row, col, 0]
                                and ~self.nodes[row, col + 1, 0]
                                and ~self.nodes[row, col + 2, 0]
                            )
                            or (
                                col > 1
                                and col < 6
                                and (
                                    self.nodes[row, col - 2, 0]
                                    or self.nodes[row, col + 3, 0]
                                )
                                and ~self.nodes[row, col - 1, 0]
                                and ~self.nodes[row, col, 0]
                                and ~self.nodes[row, col + 1, 0]
                                and ~self.nodes[row, col + 2, 0]
                            )
                            or (
                                (col == 3 or col == 4)
                                and ~self.nodes[row, col - 3, 0]
                                and ~self.nodes[row, col - 2, 0]
                                and ~self.nodes[row, col - 1, 0]
                                and ~self.nodes[row, col, 0]
                                and ~self.nodes[row, col + 1, 0]
                                and ~self.nodes[row, col + 2, 0]
                                and ~self.nodes[row, col + 3, 0]
                                and ~self.nodes[row, col + 4, 0]
                            )
                        ):
                            # Validate vertical wall allows a path to end
                            if search(
                                self.nodes,
                                self.p1_pos,
                                8,
                                np.array([row, col, 1], dtype=np.int8),
                            ) and search(
                                self.nodes,
                                self.p2_pos,
                                0,
                                np.array([row, col, 1], dtype=np.int8),
                            ):
                                actions[64 + row * 8 + col] = True
        return actions

    def take_action(self, action):
        # action is a number ranging from 0 to 143
        """
        128 - North, west 1,-1
        129 - D north 2,0
        130 - North, east 1,1
        131 - Basic north 1,0
        135 - Basic east 0,1
        139 - Basic south -1,0
        143 - Basic west 0,-1

        """
        rel_move = np.array(
            [
                [1, -1],
                [2, 0],
                [1, 1],
                [1, 0],
                [1, 1],
                [0, 2],
                [-1, 1],
                [0, 1],
                [-1, 1],
                [-2, 0],
                [-1, -1],
                [-1, 0],
                [-1, -1],
                [0, -2],
                [1, -1],
                [0, -1],
            ]
        )

        if action < 128:
            if action < 64:  # horizontal
                self.nodes[action // 8, action % 8, 0] = False
                self.nodes[action // 8 + 1, action % 8, 2] = False
                self.nodes[action // 8, action % 8 + 1, 0] = False
                self.nodes[action // 8 + 1, action % 8 + 1, 2] = False
            else:  # vertical
                self.nodes[(action % 64) // 8, (action % 64) % 8, 1] = False
                self.nodes[(action % 64) // 8, (action % 64) % 8 + 1, 3] = False
                self.nodes[(action % 64) // 8 + 1, (action % 64) % 8, 1] = False
                self.nodes[(action % 64) // 8 + 1, (action % 64) % 8 + 1, 3] = False
            if self.turn == 1:
                self.p1_walls_placed += 1
                self.turn = 2
            else:
                self.p2_walls_placed += 1
                self.turn = 1

        elif action < 144:
            if self.turn == 1:
                self.p1_pos += rel_move[action % 128]
                if self.p1_pos[0] == 8:
                    self.over = True
                else:
                    self.turn = 2
            elif self.turn == 2:
                self.p2_pos += rel_move[action % 128]
                if self.p2_pos[0] == 0:
                    self.over = True
                else:
                    self.turn = 1

    def display_beautiful(self):
        for row in range(8, -1, -1):
            line = []
            line_below = []
            for column in range(9):
                if np.array_equal(self.p1_pos, [row, column]):
                    line.append(" 1 ")
                elif np.array_equal(self.p2_pos, [row, column]):
                    line.append(" 2 ")
                else:
                    line.append("   ")

                if self.nodes[row, column, 1] and self.nodes[row, column + 1, 3]:
                    line.append("\u2502")
                else:
                    if column != 8:
                        line.append("\u2503")
                if row != 8:
                    # if no horizontal wall below (row, column) place thin lines
                    # otherwise, place thick lines to show a wall
                    if self.nodes[row, column, 0] and self.nodes[row + 1, column, 2]:
                        line_below.append("\u2500\u2500\u2500")
                    else:
                        line_below.append("\u2501\u2501\u2501")
                    if column != 8:
                        # variables describing if there is part of a wall above the intersection
                        north = ~self.nodes[row + 1, column, 1]
                        east = ~self.nodes[row, column + 1, 0]
                        south = ~self.nodes[row, column, 1]
                        west = ~self.nodes[row, column, 0]

                        """
                        If row = 0, column = 0
                        X1 X2
                          I
                        X3 X4
                        looking at intersection I
                        """

                        # wall between X1 and X3

                        # add Unicode characters based on what combination of walls are around the intersection
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
            print(" " + "".join(line_below))
            print(str(row + 1) + "".join(line))
        print("  a   b   c   d   e   f   g   h   i  ")

    def is_over(self):
        return self.over

    def winner(self):
        return self.turn

    def get_available_states(self):
        states = []
        actions = self.get_available_actions()
        for action_idx in range(144):
            if actions[action_idx]:
                result = copy.deepcopy(self)
                result.take_action(action_idx)
                states.append(result)
        return states

    def get_random_child(self):
        return random.choice(self.get_available_states())

    def reward(self):
        if self.is_over():
            if self.turn == 1:
                return 1
            else:
                return 0


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


class MCTS_NODE:
    def __init__(self, state):
        self.state = state
        self.games_won = 0
        self.games_played = 0
        self.children = []

    def generate_children(self):
        self.children = [
            MCTS_NODE(child) for child in self.state.get_available_states()
        ]

    def __sizeof__(self):
        return (
            object.__sizeof__(self)
            + sum(sys.getsizeof(v) for v in self.__dict__.values())
            + sum(sys.getsizeof(item) for item in self.children)
        )

    # def __repr__(self):
    #     return f"{self.games_won}/{self.games_played}"


board = QuoridorGraphicalBoardMoreOptimB()


root = MCTS_NODE(board)

import sys


def roll_out(root):
    path = select(root)
    leaf = path[-1]
    child = expand(leaf)
    reward = simulate(child.state, child.state.turn)
    backpropagate(path + [child], reward)
    print(sys.getsizeof(root) / 1e6, "MB")


for i in range(500):
    roll_out(root)
print(
    [
        (c.games_won, c.games_played)
        for c in sorted(root.children, key=lambda x: x.games_played)
    ]
)
# for i in range(500):
#     print(i + 1, "th rollout")
#     roll_out(root)


# def display_mcts(root, depth=1):
#     if root.children == []:
#         return
#     print(f"{root.games_won}/{root.games_played}")
#     children_games = [
#         f"{c.games_won}/{c.games_played}" for c in root.children if c.games_played != 0
#     ]
#     if children_games == []:
#         pass
#     else:
#         print(children_games)


# print(display_mcts(root))


# print(
#     [
#         (c.games_played, id(c))
#         for c in sorted(root.children, key=lambda x: id(x))
#         if c.games_played != 0
#     ]
# )


'''


def select(root):
    """Selection: Start from root R and select successive child nodes until a leaf node L is reached.
    The root is the current game state and a leaf is any node that has a potential child from
    which no simulation (playout) has yet been initiated."""
    """Input the starting board game state, return a child that hasn't had any playout from yet.
    """

    def uct(node, parent_node, exploration_const):
        return node.games_won / node.games_played + exploration_const * math.sqrt(
            math.log(parent_node.games_played) / node.games_played
        )

    path = [root]
    while True:
        node = path[-1]
        if min(node.children, key=lambda child: child.games_played).games_played == 0:
            path.append(
                random.choice(
                    [child for child in node.children if child.games_played == 0]
                )
            )
            return path
        else:
            node = max(node.children, key=lambda child: uct(child, node))


def expand(node):
    """Expansion: Unless L ends the game decisively (e.g. win/loss/draw) for either player, create one (or more)
    child nodes and choose node C from one of them. Child nodes are any valid moves from the game position defined by L.
    """
    node.children = [MCTS_NODE(child) for child in node.state.get_available_states()]


def simulate(node, start):
    """Simulation: Complete one random playout from node C. This step is sometimes also called playout or rollout.
    A playout may be as simple as choosing uniform random moves until the game is decided (for example in chess,
    the game is won, lost, or drawn)."""
    while True:
        if node.is_over():
            print("winner", node.winner())
            return 1 if node.winner() == start else 0
        node = node.get_random_child()


def backpropagate(path, reward):
    """Backpropagation: Use the result of the playout to update information in the nodes on the path from C to R."""
    for node in reversed(path):
        node.state.display_beautiful()

        node.games_won += reward
        node.games_played += 1
        print(
            "turn",
            node.state.turn,
            "init_won",
            node.games_won - reward,
            "new_won",
            node.games_won,
        )
        reward = 1 - reward


def roll_out(root):
    path = select(root)
    leaf = path[-1]
    expand(leaf)
    reward = simulate(leaf)

board = QuoridorGraphicalBoardMoreOptimB()


root = MCTS_NODE(board)
expand(root)
path = select(root)

score = simulate(path[-1].state, path[-1].state.turn)
print("start", path[-1].state.turn, "score", score)
backpropagate(path, score)
for p in path:
    print(p.state.turn, p.games_won)
# print(root.games_won)
# print([c.games_won for c in root.children])
'''
