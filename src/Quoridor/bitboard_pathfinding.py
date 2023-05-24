import numpy as np
from numba import njit

blank = np.zeros(5, dtype=np.uint64)
full = np.array(
    [
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
    ],
    dtype=np.uint64,
)


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
def shift_bitboard(bitboard, shift):
    # right is positive shift EAST
    """
    0001 0000 0000 --> 0000 1000 0000 = everything >> 1 and add 0000 1000 0000
    0000 1000 0000 is equal to roll init (0000 0001 0000) and << 4-1
    BUT IF 0000 0001 >> 1 = 0000 0000
    using above, 0000 0001 >> 1 ??= 0000 0000 + 1000 0000

    """
    if shift > 0 and shift < 64:
        rshift = np.uint64(shift)
        lshift = np.uint64(64 - shift)
        copy_bitboard = (bitboard >> rshift) + (np.roll(bitboard, 1) << lshift)
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        if bitboard[0] == 0:
            copy_bitboard[0] = 0
    elif shift < 0 and shift > -64:
        rshift = np.uint64(64 + shift)
        lshift = np.uint64(-shift)
        copy_bitboard = (bitboard << lshift) + (np.roll(bitboard, -1) >> rshift)
        if bitboard[4] == 0:
            copy_bitboard[4] = 0
    return copy_bitboard


def display(bitboard):
    line = "".join([np.binary_repr(x, 64) for x in bitboard])
    for i in range(0, 17):
        print(line[i * 17 : i * 17 + 17])
    print()


@njit(cache=True)
def manhatten_distance(bitboard_player, player_number):
    if player_number == 1:
        shift = -34
    elif player_number == 2:
        shift = 34
    for i in range(8):
        bitboard_player = shift_bitboard(bitboard_player, shift)
        if np.array_equal(shift_bitboard(bitboard_player, shift), blank):
            return np.int8(i + 1)


# print(manhatten_distance(np.array([0, 0, 0, 0, 2**39], dtype=np.uint64), 1))


@njit(cache=True)
def BreadthFirstSearch_Bitboard(
    bitboard_player, player_number, bitboard_walls, wall_number
):
    bitboard = np.copy(bitboard_walls)
    if wall_number < 64:
        idx_wall = (
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
        )
    elif wall_number < 128:
        idx_wall = (
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8),
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 17,
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 34,
        )
    else:
        raise IndexError

    for idx in idx_wall:
        if 0 <= idx <= 32:
            bitboard[4] += 2 ** (idx + 31)
        elif 33 <= idx <= 96:
            bitboard[3] += 2 ** (idx - 33)
        elif 97 <= idx <= 160:
            bitboard[2] += 2 ** (idx - 97)
        elif 161 <= idx <= 224:
            bitboard[1] += 2 ** (idx - 161)
        elif 225 <= idx <= 288:
            bitboard[0] += 2 ** (idx - 225)

    start_pos = np.copy(bitboard_player)

    frontier = np.full((81, 5), 18446744073709551615, dtype=np.uint64)
    frontier[0] = start_pos
    frontier_length = 1

    explored = np.zeros(5, dtype=np.uint64)
    while True:
        if frontier_length == 0:
            return False
        node = np.copy(frontier[0])
        frontier[0] = full
        frontier = roll_numba(frontier, -1)
        frontier_length -= 1

        explored += node

        for direction in range(0, 4):
            if direction == 0:  # N
                shift = -17
            elif direction == 1:  # E
                shift = 1
            elif direction == 2:  # S
                shift = 17
            elif direction == 3:  # W
                shift = -1

            if np.array_equal(shift_bitboard(node, shift) & bitboard_walls, blank):
                shifted_bitboard = shift_bitboard(node, shift * 2)
                in_frontier = False
                for idx in range(81):
                    if np.array_equal(frontier[idx], shifted_bitboard):
                        in_frontier = True
                        break
                    elif np.array_equal(frontier[idx], full):
                        break
                if not in_frontier and np.array_equal(
                    shifted_bitboard & explored, blank
                ):
                    if (
                        player_number == 1
                        and shifted_bitboard[0] >= 140737488355328  # 2^47
                        or player_number == 2
                        and shifted_bitboard[4] <= 140737488355328  # 2^47
                    ):
                        return True

                    frontier[frontier_length] = shifted_bitboard
                    frontier_length += 1


@njit(cache=True)
def DepthFirstSearch_Bitboard(
    bitboard_player, player_number, bitboard_walls, wall_number
):
    blank = np.zeros(5, dtype=np.uint64)
    full = np.array(
        [
            18446744073709551615,
            18446744073709551615,
            18446744073709551615,
            18446744073709551615,
            18446744073709551615,
        ],
        dtype=np.uint64,
    )
    bitboard = np.copy(bitboard_walls)
    if wall_number < 64:
        idx_wall = (
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
        )
    elif wall_number < 128:
        idx_wall = (
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8),
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 17,
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 34,
        )
    else:
        raise IndexError
    for idx in idx_wall:
        if 0 <= idx <= 32:
            bitboard[4] += 2 ** (idx + 31)
        elif 33 <= idx <= 96:
            bitboard[3] += 2 ** (idx - 33)
        elif 97 <= idx <= 160:
            bitboard[2] += 2 ** (idx - 97)
        elif 161 <= idx <= 224:
            bitboard[1] += 2 ** (idx - 161)
        elif 225 <= idx <= 288:
            bitboard[0] += 2 ** (idx - 225)

    start_pos = np.copy(bitboard_player)

    frontier = np.full((81, 5), 18446744073709551615, dtype=np.uint64)
    frontier[0] = start_pos
    frontier_length = 1

    explored = np.zeros(5, dtype=np.uint64)
    while True:
        if frontier_length == 0:
            return False
        node = np.copy(frontier[frontier_length - 1])
        frontier[frontier_length - 1] = full
        frontier_length -= 1

        explored += node

        for direction in range(0, 4):
            if direction == 0:  # N
                shift = -17
            elif direction == 1:  # E
                shift = 1
            elif direction == 2:  # S
                shift = 17
            elif direction == 3:  # W
                shift = -1

            if np.array_equal(shift_bitboard(node, shift) & bitboard_walls, blank):
                shifted_bitboard = shift_bitboard(node, shift * 2)
                in_frontier = False
                for idx in range(81):
                    if np.array_equal(frontier[idx], shifted_bitboard):
                        in_frontier = True
                        break
                    elif np.array_equal(frontier[idx], full):
                        break
                if not in_frontier and np.array_equal(
                    shifted_bitboard & explored, blank
                ):
                    if (
                        player_number == 1
                        and shifted_bitboard[0] >= 140737488355328  # 2^47
                        or player_number == 2
                        and shifted_bitboard[4] <= 140737488355328  # 2^47
                    ):
                        return True

                    frontier[frontier_length] = shifted_bitboard
                    frontier_length += 1


@njit(cache=True)
def GreedyBestFirstSearch_Bitboard(
    bitboard_player, player_number, bitboard_walls, wall_number
):
    bitboard = np.copy(bitboard_walls)
    if wall_number < 64:
        idx_wall = (
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
        )
    elif wall_number < 128:
        idx_wall = (
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8),
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 17,
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 34,
        )
    else:
        raise IndexError
    for idx in idx_wall:
        if 0 <= idx <= 32:
            bitboard[4] += 2 ** (idx + 31)
        elif 33 <= idx <= 96:
            bitboard[3] += 2 ** (idx - 33)
        elif 97 <= idx <= 160:
            bitboard[2] += 2 ** (idx - 97)
        elif 161 <= idx <= 224:
            bitboard[1] += 2 ** (idx - 161)
        elif 225 <= idx <= 288:
            bitboard[0] += 2 ** (idx - 225)

    start_pos = np.copy(bitboard_player)

    frontier = np.full((81, 5), 18446744073709551615, dtype=np.uint64)
    frontier[0] = start_pos
    frontier_length = 1

    frontier_manhatten_distance = np.full(81, 127, dtpye=np.int8)
    frontier_manhatten_distance[0] = manhatten_distance[frontier[0]]
    explored = np.zeros(5, dtype=np.uint64)
    while True:
        if frontier_length == 0:
            return False

        min_idx = np.argmin(frontier_manhatten_distance)
        node = np.copy(frontier[min_idx])
        frontier_length -= 1

        explored += node

        for direction in range(0, 4):
            if direction == 0:  # N
                shift = -17
            elif direction == 1:  # E
                shift = 1
            elif direction == 2:  # S
                shift = 17
            elif direction == 3:  # W
                shift = -1

            if np.array_equal(shift_bitboard(node, shift) & bitboard_walls, blank):
                shifted_bitboard = shift_bitboard(node, shift * 2)
                in_frontier = False
                for idx in range(81):
                    if np.array_equal(frontier[idx], shifted_bitboard):
                        in_frontier = True
                        break
                    elif np.array_equal(frontier[idx], full):
                        break
                if not in_frontier and np.array_equal(
                    shifted_bitboard & explored, blank
                ):
                    if (
                        player_number == 1
                        and shifted_bitboard[0] >= 140737488355328  # 2^47
                        or player_number == 2
                        and shifted_bitboard[4] <= 140737488355328  # 2^47
                    ):
                        return True
                    max_idx = np.argmax(frontier_manhatten_distance)
                    frontier[max_idx] = shifted_bitboard
                    frontier_length += 1
        frontier[min_idx] = full
        frontier_manhatten_distance[min_idx] = 127


@njit(cache=True)
def UniformCostSearch_Bitboard(
    bitboard_player, player_number, bitboard_walls, wall_number
):
    bitboard = np.copy(bitboard_walls)
    if wall_number < 64:
        idx_wall = (
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
        )
    elif wall_number < 128:
        idx_wall = (
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8),
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 17,
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 34,
        )
    else:
        raise IndexError
    for idx in idx_wall:
        if 0 <= idx <= 32:
            bitboard[4] += 2 ** (idx + 31)
        elif 33 <= idx <= 96:
            bitboard[3] += 2 ** (idx - 33)
        elif 97 <= idx <= 160:
            bitboard[2] += 2 ** (idx - 97)
        elif 161 <= idx <= 224:
            bitboard[1] += 2 ** (idx - 161)
        elif 225 <= idx <= 288:
            bitboard[0] += 2 ** (idx - 225)

    start_pos = np.copy(bitboard_player)

    frontier = np.full((81, 5), 18446744073709551615, dtype=np.uint64)
    frontier[0] = start_pos
    frontier_length = 1

    frontier_path_cost = np.full(81, 127, dtpye=np.int8)
    frontier_path_cost[0] = 0
    explored = np.zeros(5, dtype=np.uint64)
    while True:
        if frontier_length == 0:
            return False

        min_idx = np.argmin(frontier_path_cost)
        node = np.copy(frontier[min_idx])
        frontier_length -= 1

        explored += node

        for direction in range(0, 4):
            if direction == 0:  # N
                shift = -17
            elif direction == 1:  # E
                shift = 1
            elif direction == 2:  # S
                shift = 17
            elif direction == 3:  # W
                shift = -1

            if np.array_equal(shift_bitboard(node, shift) & bitboard_walls, blank):
                shifted_bitboard = shift_bitboard(node, shift * 2)
                in_frontier = False
                frontier_idx = 255
                for idx in range(81):
                    if np.array_equal(frontier[idx], shifted_bitboard):
                        in_frontier = True
                        frontier_idx = idx
                        break
                    elif np.array_equal(frontier[idx], full):
                        break
                if not in_frontier and np.array_equal(
                    shifted_bitboard & explored, blank
                ):
                    if (
                        player_number == 1
                        and shifted_bitboard[0] >= 140737488355328  # 2^47
                        or player_number == 2
                        and shifted_bitboard[4] <= 140737488355328  # 2^47
                    ):
                        return True
                    max_idx = np.argmax(frontier_path_cost)
                    frontier[max_idx] = shifted_bitboard
                    frontier_path_cost[max_idx] = frontier_path_cost[min_idx] + 1
                    frontier_length += 1
                elif (
                    in_frontier
                    and frontier_path_cost[frontier_idx]
                    > frontier_path_cost[min_idx] + 1
                ):
                    frontier_path_cost[frontier_idx] = frontier_path_cost[min_idx] + 1
        frontier[min_idx] = full
        frontier_path_cost[min_idx] = 127


@njit(cache=True)
def AStarSearch_Bitboard(bitboard_player, player_number, bitboard_walls, wall_number):
    bitboard = np.copy(bitboard_walls)
    if wall_number < 64:
        idx_wall = (
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
        )
    elif wall_number < 128:
        idx_wall = (
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8),
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 17,
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 34,
        )
    else:
        raise IndexError
    for idx in idx_wall:
        if 0 <= idx <= 32:
            bitboard[4] += 2 ** (idx + 31)
        elif 33 <= idx <= 96:
            bitboard[3] += 2 ** (idx - 33)
        elif 97 <= idx <= 160:
            bitboard[2] += 2 ** (idx - 97)
        elif 161 <= idx <= 224:
            bitboard[1] += 2 ** (idx - 161)
        elif 225 <= idx <= 288:
            bitboard[0] += 2 ** (idx - 225)

    start_pos = np.copy(bitboard_player)

    frontier = np.full((81, 5), 18446744073709551615, dtype=np.uint64)
    frontier[0] = start_pos
    frontier_length = 1

    # records path cost from start to current,
    # estimated path cost from current to destination and sum
    frontier_estimate_cost = np.full((81, 3), 127, dtype=np.int8)

    frontier_estimate_cost[0] = [
        0,
        manhatten_distance(bitboard_player, player_number),
        manhatten_distance(bitboard_player, player_number),
    ]
    explored = np.zeros(5, dtype=np.uint64)
    while True:
        if frontier_length == 0:
            return False

        min_idx = np.argmin(frontier_estimate_cost[:, 2])
        node = np.copy(frontier[min_idx])
        frontier_length -= 1

        explored += node

        for direction in range(0, 4):
            if direction == 0:  # N
                shift = -17
            elif direction == 1:  # E
                shift = 1
            elif direction == 2:  # S
                shift = 17
            elif direction == 3:  # W
                shift = -1

            if np.array_equal(shift_bitboard(node, shift) & bitboard_walls, blank):
                shifted_bitboard = shift_bitboard(node, shift * 2)
                in_frontier = False
                frontier_idx = 255
                for idx in range(81):
                    if np.array_equal(frontier[idx], shifted_bitboard):
                        in_frontier = True
                        frontier_idx = idx
                        break
                    elif np.array_equal(frontier[idx], full):
                        break
                if not in_frontier and np.array_equal(
                    shifted_bitboard & explored, blank
                ):
                    if (
                        player_number == 1
                        and shifted_bitboard[0] >= 140737488355328  # 2^47
                        or player_number == 2
                        and shifted_bitboard[4] <= 140737488355328  # 2^47
                    ):
                        return True
                    max_idx = np.argmax(frontier_estimate_cost)
                    frontier[max_idx] = shifted_bitboard
                    frontier_estimate_cost[max_idx] = np.array(
                        [
                            frontier_estimate_cost[min_idx] + 1,
                            manhatten_distance(shifted_bitboard, player_number),
                            frontier_estimate_cost[min_idx]
                            + 1
                            + manhatten_distance(shifted_bitboard, player_number),
                        ],
                        dtype=np.int8,
                    )
                    frontier_length += 1
                elif (
                    in_frontier
                    and frontier_estimate_cost[frontier_idx, 2]
                    > frontier_estimate_cost[min_idx] + 1,
                    manhatten_distance(shifted_bitboard, player_number),
                ):
                    frontier_estimate_cost[frontier_idx] = [
                        frontier_estimate_cost[min_idx] + 1,
                        manhatten_distance(shifted_bitboard, player_number),
                        frontier_estimate_cost[min_idx]
                        + 1
                        + manhatten_distance(shifted_bitboard, player_number),
                    ]
        frontier[min_idx] = full
        frontier_estimate_cost[min_idx] = 127


board = np.array([0, 0, 0, 0, 2**39], dtype=np.uint64)


testing = '''

import timeit

print(
    timeit.timeit(
        """shift_bitboard(np.array(
            [
                0b0000000000000000011111111111111111000000000000000000000000000000,
                0,
                0,
                0,
                0,
            ],
            dtype=np.uint64,
        ), 5)""",
        globals=globals(),
        number=10_000_000,
    )
    / 1e7
)
print(
    timeit.timeit(
        """shift_bitboard_original(np.array(
            [
                0b0000000000000000011111111111111111000000000000000000000000000000,
                0,
                0,
                0,
                0,
            ],
            dtype=np.uint64,
        ), 5)""",
        globals=globals(),
        number=10_000_000,
    )
    / 1e7
)

'''
