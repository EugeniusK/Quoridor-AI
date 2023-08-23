import math
import random
import numpy as np
from numba import njit
from Quoridor.b_optim import QuoridorBitboardOptim
import sys

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

    # generate a random successor instead of generating all - based on https://gist.github.com/qpwo/c538c6f73727e254fdc7fab81024f6e1
    while True:
        if node.is_over():
            return 1 if node.winner() == start else 0

        available = False
        while not available:
            action = random.randint(0, 139)
            if node.is_action_available(action):
                node.take_action(action)
                available = True


def backpropagate(path, reward):
    """Backpropagation: Use the result of the playout to update information in the nodes on the path from C to R."""
    for node in reversed(path):
        node.games_won += reward
        node.games_played += 1
        reward = 1 - reward


def roll_out(root):
    path = select(root)
    leaf = path[-1]
    child = expand(leaf)
    reward = simulate(child.state, child.state.turn)
    backpropagate(path + [child], reward)


def choose(root):
    if root.state.is_over():
        raise RuntimeError("Game is over already")

    def score(node):
        if node.games_played == 0:
            return float("-inf")
        return node.games_won / node.games_played

    return root.children.index(max(root.children, key=score))


class MCTS_NODE:
    def __init__(self, state):
        self.state = state
        self.games_won = 0
        self.games_played = 0
        self.children = []

    def __sizeof__(self):
        return (
            object.__sizeof__(self)
            + sum(sys.getsizeof(v) for v in self.__dict__.values())
            + sum(sys.getsizeof(item) for item in self.children)
        )


if __name__ == "__main__":
    pass
