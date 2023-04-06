import random

import numpy as np

random.seed(0)
rng_base = np.random.default_rng(0)


def random_select(moves):
    if type(moves) == list:
        return random.choice(moves)
    elif type(moves) == np.ndarray:
        number_valid = np.unique(np.where(moves != [-1, -1, -1])[0]).size
        return np.delete(moves, np.unique(np.where(moves == [-1, -1, -1])[0]), 0)[
            rng_base.integers(0, number_valid - 1, dtype=np.uint8)
        ]
