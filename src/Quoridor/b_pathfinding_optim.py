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
    Shift the bitboard by shift
    while ensuring that bits outside of the 17x17 are not set
    """
    if shift < 64 and shift > 0:
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


@njit(cache=True)
def shift_bitboard_check_wall(player_bitboard, wall_bitboard, shift, mask):
    """
    Shift the bitboard right by shift
    Then bitwise AND with wall bitboard and compare to blank bitboard
    to ensure that the player doesn't go through a wal
    Then AND with full bitboard to ensure the player is on the board
    """
    if shift > 0 and shift < 64:
        rshift = np.uint64(shift)
        lshift = np.uint64(64 - shift)
        copy_bitboard = (player_bitboard >> rshift) + (
            np.roll(player_bitboard, 1) << lshift
        )
        copy_bitboard[4] = copy_bitboard[4] & np.uint64(18446744071562067968)
        if player_bitboard[0] == 0:
            copy_bitboard[0] = 0
    elif shift < 0 and shift > -64:
        rshift = np.uint64(64 + shift)
        lshift = np.uint64(-shift)
        copy_bitboard = (player_bitboard << lshift) + (
            np.roll(player_bitboard, -1) >> rshift
        )
        if player_bitboard[4] == 0:
            copy_bitboard[4] = 0
    return np.array_equal(copy_bitboard & wall_bitboard, blank) and ~np.array_equal(
        copy_bitboard & mask, blank
    )


def display(bitboard):
    line = "".join([np.binary_repr(x, 64) for x in bitboard])
    for i in range(0, 17):
        print(line[i * 17 : i * 17 + 17])
    print()


@njit(cache=True)
def manhatten_distance(bitboard_player, player_number):
    found_idx = 0
    for idx in range(289):
        if 0 <= idx <= 32:
            if bitboard_player[4] == np.uint64(2 ** (idx + 31)):
                found_idx = idx
        elif 33 <= idx <= 96:
            if bitboard_player[3] == np.uint64(2 ** (idx - 33)):
                found_idx = idx
        elif 97 <= idx <= 160:
            if bitboard_player[2] == np.uint64(2 ** (idx - 97)):
                found_idx = idx
        elif 161 <= idx <= 224:
            if bitboard_player[1] == np.uint64(2 ** (idx - 161)):
                found_idx = idx
        elif 225 <= idx <= 288:
            if bitboard_player[0] == np.uint64(2 ** (idx - 225)):
                found_idx = idx

    if player_number == 1:
        return 8 - found_idx // 17
    else:
        return found_idx // 17


short_north_mask = np.array(
    [
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446462598732840960,
    ],
    dtype=np.uint64,
)
short_east_mask = np.array(
    [
        9223301667573723135,
        17870278923326062335,
        18410715001810583535,
        18444492256715866110,
        18446603336221196287,
    ],
    dtype=np.uint64,
)
short_south_mask = np.array(
    [
        140737488355327,
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446744071562067968,
    ],
    dtype=np.uint64,
)
short_west_mask = np.array(
    [
        18446603335147446271,
        17293813772942573055,
        18374685929911615455,
        18442240439722180605,
        18446462594437873664,
    ],
    dtype=np.uint64,
)


@njit(cache=True)
def BreadthFirstSearch_Bitboard(
    bitboard_player, player_number, bitboard_walls, wall_number
):
    # Create new initial state "bitboard" where wall has been placed
    bitboard_walls_placed = np.copy(bitboard_walls)
    if wall_number < 64:
        idx_wall = (
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
        )
    else:
        idx_wall = (
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8),
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 17,
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 34,
        )

    for idx in idx_wall:
        if 0 <= idx <= 32:
            bitboard_walls_placed[4] = bitboard_walls_placed[4] + np.uint64(
                2 ** (idx + 31)
            )

        elif 33 <= idx <= 96:
            bitboard_walls_placed[3] = bitboard_walls_placed[3] + np.uint64(
                2 ** (idx - 33)
            )
        elif 97 <= idx <= 160:
            bitboard_walls_placed[2] = bitboard_walls_placed[2] + np.uint64(
                2 ** (idx - 97)
            )
        elif 161 <= idx <= 224:
            bitboard_walls_placed[1] = bitboard_walls_placed[1] + np.uint64(
                2 ** (idx - 161)
            )
        elif 225 <= idx <= 288:
            bitboard_walls_placed[0] = bitboard_walls_placed[0] + np.uint64(
                2 ** (idx - 225)
            )
    # Starting position of the player
    start_pos = np.copy(bitboard_player)

    # If player is at destination_row, return True
    if (
        player_number == 1
        and start_pos[0] >= np.uint64(140737488355328)
        or player_number == 2
        and np.uint64(2147483648) <= start_pos[4] <= np.uint64(140737488355328)
    ):
        return True

    # frontier ← array that holds a maximum of 81 positions possible on 9x9 board
    frontier = np.full((81, 5), 18446744073709551615, dtype=np.uint64)

    # Add initial start_pos to the frontier
    frontier[0] = start_pos
    frontier_length = 1

    # explored ← an empty bitboard
    explored = np.zeros(5, dtype=np.uint64)
    while True:
        # If the frontier is empty, return False
        if frontier_length == 0:
            return False
        # node ← pop from frontier at index 0 (like accessing FIFO queue)
        node = np.copy(frontier[0])
        frontier[0] = full
        frontier = roll_numba(frontier, -1)
        frontier_length -= 1

        # Add position to explored
        explored += node

        for direction in range(0, 4):
            if direction == 0:  # N
                shift = -17
                mask = short_north_mask
            elif direction == 1:  # E
                shift = 1
                mask = short_east_mask
            elif direction == 2:  # S
                shift = 17
                mask = short_south_mask
            elif direction == 3:  # W
                shift = -1
                mask = short_west_mask

            # If the move in the given direction is valid
            if shift_bitboard_check_wall(node, bitboard_walls_placed, shift, mask):
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
                        and np.uint64(2147483648)
                        <= shifted_bitboard[4]
                        <= np.uint64(140737488355328)  # 2^47
                    ):
                        return True

                    frontier[frontier_length] = shifted_bitboard
                    frontier_length += 1


@njit(cache=True)
def DepthFirstSearch_Bitboard(
    bitboard_player, player_number, bitboard_walls, wall_number
):
    bitboard_walls_placed = np.copy(bitboard_walls)
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

    for idx in idx_wall:
        if 0 <= idx <= 32:
            bitboard_walls_placed[4] = bitboard_walls_placed[4] + np.uint64(
                2 ** (idx + 31)
            )

        elif 33 <= idx <= 96:
            bitboard_walls_placed[3] = bitboard_walls_placed[3] + np.uint64(
                2 ** (idx - 33)
            )
        elif 97 <= idx <= 160:
            bitboard_walls_placed[2] = bitboard_walls_placed[2] + np.uint64(
                2 ** (idx - 97)
            )
        elif 161 <= idx <= 224:
            bitboard_walls_placed[1] = bitboard_walls_placed[1] + np.uint64(
                2 ** (idx - 161)
            )
        elif 225 <= idx <= 288:
            bitboard_walls_placed[0] = bitboard_walls_placed[0] + np.uint64(
                2 ** (idx - 225)
            )

    start_pos = np.copy(bitboard_player)

    # If player is at destination_row, return True
    if (
        player_number == 1
        and start_pos[0] >= np.uint64(140737488355328)
        or player_number == 2
        and np.uint64(2147483648) <= start_pos[4] <= np.uint64(140737488355328)
    ):
        return True

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
                mask = short_north_mask
            elif direction == 1:  # E
                shift = 1
                mask = short_east_mask
            elif direction == 2:  # S
                shift = 17
                mask = short_south_mask
            elif direction == 3:  # W
                shift = -1
                mask = short_west_mask

            if shift_bitboard_check_wall(node, bitboard_walls_placed, shift, mask):
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
                        and np.uint64(2147483648)
                        <= shifted_bitboard[4]
                        <= np.uint64(140737488355328)  # 2^47
                    ):
                        return True

                    frontier[frontier_length] = shifted_bitboard
                    frontier_length += 1


@njit(cache=True)
def GreedyBestFirstSearch_Bitboard(
    bitboard_player, player_number, bitboard_walls, wall_number
):
    bitboard_walls_placed = np.copy(bitboard_walls)
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
            bitboard_walls_placed[4] = bitboard_walls_placed[4] + np.uint64(
                2 ** (idx + 31)
            )

        elif 33 <= idx <= 96:
            bitboard_walls_placed[3] = bitboard_walls_placed[3] + np.uint64(
                2 ** (idx - 33)
            )
        elif 97 <= idx <= 160:
            bitboard_walls_placed[2] = bitboard_walls_placed[2] + np.uint64(
                2 ** (idx - 97)
            )
        elif 161 <= idx <= 224:
            bitboard_walls_placed[1] = bitboard_walls_placed[1] + np.uint64(
                2 ** (idx - 161)
            )
        elif 225 <= idx <= 288:
            bitboard_walls_placed[0] = bitboard_walls_placed[0] + np.uint64(
                2 ** (idx - 225)
            )

    start_pos = np.copy(bitboard_player)

    # If player is at destination_row, return True
    if (
        player_number == 1
        and start_pos[0] >= np.uint64(140737488355328)
        or player_number == 2
        and np.uint64(2147483648) <= start_pos[4] <= np.uint64(140737488355328)
    ):
        return True
    frontier = np.full((81, 5), 18446744073709551615, dtype=np.uint64)
    frontier[0] = start_pos
    frontier_length = 1

    frontier_manhatten_distance = np.full((81), 127, dtype=np.int8)
    frontier_manhatten_distance[0] = manhatten_distance(frontier[0], player_number)
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
                mask = short_north_mask
            elif direction == 1:  # E
                shift = 1
                mask = short_east_mask
            elif direction == 2:  # S
                shift = 17
                mask = short_south_mask
            elif direction == 3:  # W
                shift = -1
                mask = short_west_mask

            if shift_bitboard_check_wall(node, bitboard_walls_placed, shift, mask):
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
                        and np.uint64(2147483648)
                        <= shifted_bitboard[4]
                        <= np.uint64(140737488355328)  # 2^47
                    ):
                        return True
                    max_idx = np.argmax(frontier_manhatten_distance)
                    frontier[max_idx] = shifted_bitboard
                    frontier_manhatten_distance[max_idx] = manhatten_distance(
                        shifted_bitboard, player_number
                    )
                    frontier_length += 1
        frontier[min_idx] = full
        frontier_manhatten_distance[min_idx] = 127


@njit(cache=True)
def UniformCostSearch_Bitboard(
    bitboard_player, player_number, bitboard_walls, wall_number
):
    bitboard_walls_placed = np.copy(bitboard_walls)
    if wall_number < 64:
        idx_wall = (
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
        )
    else:
        idx_wall = (
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8),
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 17,
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 34,
        )

    for idx in idx_wall:
        if 0 <= idx <= 32:
            bitboard_walls_placed[4] = bitboard_walls_placed[4] + np.uint64(
                2 ** (idx + 31)
            )

        elif 33 <= idx <= 96:
            bitboard_walls_placed[3] = bitboard_walls_placed[3] + np.uint64(
                2 ** (idx - 33)
            )
        elif 97 <= idx <= 160:
            bitboard_walls_placed[2] = bitboard_walls_placed[2] + np.uint64(
                2 ** (idx - 97)
            )
        elif 161 <= idx <= 224:
            bitboard_walls_placed[1] = bitboard_walls_placed[1] + np.uint64(
                2 ** (idx - 161)
            )
        elif 225 <= idx <= 288:
            bitboard_walls_placed[0] = bitboard_walls_placed[0] + np.uint64(
                2 ** (idx - 225)
            )

    start_pos = np.copy(bitboard_player)

    # If player is at destination_row, return True
    if (
        player_number == 1
        and start_pos[0] >= np.uint64(140737488355328)
        or player_number == 2
        and np.uint64(2147483648) <= start_pos[4] <= np.uint64(140737488355328)
    ):
        return True
    frontier = np.full((81, 5), 18446744073709551615, dtype=np.uint64)
    frontier[0] = start_pos
    frontier_length = 1

    frontier_path_cost = np.full((81), 127, dtype=np.int8)
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
                mask = short_north_mask
            elif direction == 1:  # E
                shift = 1
                mask = short_east_mask
            elif direction == 2:  # S
                shift = 17
                mask = short_south_mask
            elif direction == 3:  # W
                shift = -1
                mask = short_west_mask

            if shift_bitboard_check_wall(node, bitboard_walls_placed, shift, mask):
                shifted_bitboard = shift_bitboard(node, shift * 2)
                in_frontier = False
                for idx in range(81):
                    if np.array_equal(frontier[idx], shifted_bitboard):
                        in_frontier = True
                        frontier_idx = idx
                        break
                if not in_frontier and np.array_equal(
                    shifted_bitboard & explored, blank
                ):
                    if (
                        player_number == 1
                        and shifted_bitboard[0] >= 140737488355328  # 2^47
                        or player_number == 2
                        and np.uint64(2147483648)
                        <= shifted_bitboard[4]
                        <= np.uint64(140737488355328)  # 2^47
                    ):
                        return True
                    max_idx = np.argmax(frontier_path_cost)
                    frontier[max_idx] = shifted_bitboard
                    frontier_path_cost[max_idx] = frontier_path_cost[min_idx] + 1
                    frontier_length += 1
                elif in_frontier:
                    if (
                        frontier_path_cost[frontier_idx]
                        > frontier_path_cost[min_idx] + 1
                    ):
                        frontier_path_cost[frontier_idx] = (
                            frontier_path_cost[min_idx] + 1
                        )
        frontier[min_idx] = full
        frontier_path_cost[min_idx] = 127


@njit(cache=True)
def AStarSearch_Bitboard(bitboard_player, player_number, bitboard_walls, wall_number):
    bitboard_walls_placed = np.copy(bitboard_walls)
    if wall_number < 64:
        idx_wall = (
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8),
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 1,
            (wall_number // 8 + 1) * 34 - 1 - 2 * (wall_number % 8) - 2,
        )
    else:
        idx_wall = (
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8),
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 17,
            ((wall_number % 64) // 8 + 1) * 34 - 19 - 2 * ((wall_number % 64) % 8) + 34,
        )

    for idx in idx_wall:
        if 0 <= idx <= 32:
            bitboard_walls_placed[4] = bitboard_walls_placed[4] + np.uint64(
                2 ** (idx + 31)
            )

        elif 33 <= idx <= 96:
            bitboard_walls_placed[3] = bitboard_walls_placed[3] + np.uint64(
                2 ** (idx - 33)
            )
        elif 97 <= idx <= 160:
            bitboard_walls_placed[2] = bitboard_walls_placed[2] + np.uint64(
                2 ** (idx - 97)
            )
        elif 161 <= idx <= 224:
            bitboard_walls_placed[1] = bitboard_walls_placed[1] + np.uint64(
                2 ** (idx - 161)
            )
        elif 225 <= idx <= 288:
            bitboard_walls_placed[0] = bitboard_walls_placed[0] + np.uint64(
                2 ** (idx - 225)
            )

    start_pos = np.copy(bitboard_player)

    # If player is at destination_row, return True
    if (
        player_number == 1
        and start_pos[0] >= np.uint64(140737488355328)
        or player_number == 2
        and np.uint64(2147483648) <= start_pos[4] <= np.uint64(140737488355328)
    ):
        return True
    frontier = np.full((81, 5), 18446744073709551615, dtype=np.uint64)
    frontier[0] = start_pos
    frontier_length = 1

    # records path cost, estimated remaining cost, sum
    frontier_costs = np.full((81, 3), 127, dtype=np.int8)

    frontier_costs[0] = [
        0,
        manhatten_distance(bitboard_player, player_number),
        manhatten_distance(bitboard_player, player_number),
    ]
    explored = np.zeros(5, dtype=np.uint64)

    while True:
        if frontier_length == 0:
            return False
        min_idx = np.argmin(frontier_costs[:, 2])
        node = np.copy(frontier[min_idx])
        frontier_length -= 1

        explored += node

        for direction in range(0, 4):
            if direction == 0:  # N
                shift = -17
                mask = short_north_mask
            elif direction == 1:  # E
                shift = 1
                mask = short_east_mask
            elif direction == 2:  # S
                shift = 17
                mask = short_south_mask
            elif direction == 3:  # W
                shift = -1
                mask = short_west_mask

            if shift_bitboard_check_wall(node, bitboard_walls_placed, shift, mask):
                shifted_bitboard = shift_bitboard(node, shift * 2)
                in_frontier = False
                for idx in range(81):
                    if np.array_equal(frontier[idx], shifted_bitboard):
                        in_frontier = True
                        frontier_idx = idx
                        break
                if not in_frontier and np.array_equal(
                    shifted_bitboard & explored, blank
                ):
                    if (
                        player_number == 1
                        and shifted_bitboard[0] >= 140737488355328  # 2^47
                        or player_number == 2
                        and np.uint64(2147483648)
                        <= shifted_bitboard[4]
                        <= np.uint64(140737488355328)  # 2^47
                    ):
                        return True
                    max_idx = np.argmax(frontier_costs[:, 2])
                    frontier[max_idx] = shifted_bitboard
                    frontier_costs[max_idx, 0] = frontier_costs[min_idx, 0] + 1
                    frontier_costs[max_idx, 1] = manhatten_distance(
                        shifted_bitboard, player_number
                    )
                    frontier_costs[max_idx, 2] = np.sum(frontier_costs[max_idx, 0:2])
                    frontier_length += 1
                elif in_frontier:
                    if frontier_costs[frontier_idx, 2] > frontier_costs[
                        min_idx, 0
                    ] + 1 + manhatten_distance(shifted_bitboard, player_number):
                        frontier_costs[frontier_idx, 0] = frontier_costs[min_idx, 0] + 1
                        frontier_costs[frontier_idx, 1] = manhatten_distance(
                            shifted_bitboard, player_number
                        )
                        frontier_costs[frontier_idx, 2] = np.sum(
                            frontier_costs[max_idx, 0:2]
                        )
        frontier[min_idx] = full
        frontier_costs[min_idx] = [127, 127, 127]
