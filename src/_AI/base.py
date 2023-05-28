import numpy as np

rng_base = np.random.default_rng(0)


def random_select(moves):
    """Input a boolean array and returns a random index where True"""
    if np.count_nonzero(moves) == 0:
        raise ZeroDivisionError
    return np.random.choice(
        np.arange(0, 140),
        p=np.array(moves, dtype=np.bool8)
        * 1
        / np.count_nonzero(np.array(moves, dtype=np.bool8)),
    )
