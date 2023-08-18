import numpy as np
from numba import njit, uint64, int8

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


def bitboard_get_index(bitboard):
    if bitboard[4] == 2147483648:
        return 0
    elif bitboard[4] == 8589934592:
        return 1
    elif bitboard[4] == 34359738368:
        return 2
    elif bitboard[4] == 137438953472:
        return 3
    elif bitboard[4] == 549755813888:
        return 4
    elif bitboard[4] == 2199023255552:
        return 5
    elif bitboard[4] == 8796093022208:
        return 6
    elif bitboard[4] == 35184372088832:
        return 7
    elif bitboard[4] == 140737488355328:
        return 8
    elif bitboard[3] == 2:
        return 9
    elif bitboard[3] == 8:
        return 10
    elif bitboard[3] == 32:
        return 11
    elif bitboard[3] == 128:
        return 12
    elif bitboard[3] == 512:
        return 13
    elif bitboard[3] == 2048:
        return 14
    elif bitboard[3] == 8192:
        return 15
    elif bitboard[3] == 32768:
        return 16
    elif bitboard[3] == 131072:
        return 17
    elif bitboard[3] == 34359738368:
        return 18
    elif bitboard[3] == 137438953472:
        return 19
    elif bitboard[3] == 549755813888:
        return 20
    elif bitboard[3] == 2199023255552:
        return 21
    elif bitboard[3] == 8796093022208:
        return 22
    elif bitboard[3] == 35184372088832:
        return 23
    elif bitboard[3] == 140737488355328:
        return 24
    elif bitboard[3] == 562949953421312:
        return 25
    elif bitboard[3] == 2251799813685248:
        return 26
    elif bitboard[2] == 32:
        return 27
    elif bitboard[2] == 128:
        return 28
    elif bitboard[2] == 512:
        return 29
    elif bitboard[2] == 2048:
        return 30
    elif bitboard[2] == 8192:
        return 31
    elif bitboard[2] == 32768:
        return 32
    elif bitboard[2] == 131072:
        return 33
    elif bitboard[2] == 524288:
        return 34
    elif bitboard[2] == 2097152:
        return 35
    elif bitboard[2] == 549755813888:
        return 36
    elif bitboard[2] == 2199023255552:
        return 37
    elif bitboard[2] == 8796093022208:
        return 38
    elif bitboard[2] == 35184372088832:
        return 39
    elif bitboard[2] == 140737488355328:
        return 40
    elif bitboard[2] == 562949953421312:
        return 41
    elif bitboard[2] == 2251799813685248:
        return 42
    elif bitboard[2] == 9007199254740992:
        return 43
    elif bitboard[2] == 36028797018963968:
        return 44
    elif bitboard[1] == 512:
        return 45
    elif bitboard[1] == 2048:
        return 46
    elif bitboard[1] == 8192:
        return 47
    elif bitboard[1] == 32768:
        return 48
    elif bitboard[1] == 131072:
        return 49
    elif bitboard[1] == 524288:
        return 50
    elif bitboard[1] == 2097152:
        return 51
    elif bitboard[1] == 8388608:
        return 52
    elif bitboard[1] == 33554432:
        return 53
    elif bitboard[1] == 8796093022208:
        return 54
    elif bitboard[1] == 35184372088832:
        return 55
    elif bitboard[1] == 140737488355328:
        return 56
    elif bitboard[1] == 562949953421312:
        return 57
    elif bitboard[1] == 2251799813685248:
        return 58
    elif bitboard[1] == 9007199254740992:
        return 59
    elif bitboard[1] == 36028797018963968:
        return 60
    elif bitboard[1] == 144115188075855872:
        return 61
    elif bitboard[1] == 576460752303423488:
        return 62
    elif bitboard[0] == 8192:
        return 63
    elif bitboard[0] == 32768:
        return 64
    elif bitboard[0] == 131072:
        return 65
    elif bitboard[0] == 524288:
        return 66
    elif bitboard[0] == 2097152:
        return 67
    elif bitboard[0] == 8388608:
        return 68
    elif bitboard[0] == 33554432:
        return 69
    elif bitboard[0] == 134217728:
        return 70
    elif bitboard[0] == 536870912:
        return 71
    elif bitboard[0] == 140737488355328:
        return 72
    elif bitboard[0] == 562949953421312:
        return 73
    elif bitboard[0] == 2251799813685248:
        return 74
    elif bitboard[0] == 9007199254740992:
        return 75
    elif bitboard[0] == 36028797018963968:
        return 76
    elif bitboard[0] == 144115188075855872:
        return 77
    elif bitboard[0] == 576460752303423488:
        return 78
    elif bitboard[0] == 2305843009213693952:
        return 79
    elif bitboard[0] == 9223372036854775808:
        return 80


@njit(cache=True)
def bitboard_get_row_col(bitboard, row, col):
    idx = row * 17 + col
    if 0 <= idx <= 32:
        return bitboard[4] & np.uint64(2 ** (idx + 31)) != 0
    elif 33 <= idx <= 96:
        return bitboard[3] & np.uint64(2 ** (idx - 33)) != 0
    elif 97 <= idx <= 160:
        return bitboard[2] & np.uint64(2 ** (idx - 97)) != 0
    elif 161 <= idx <= 224:
        return bitboard[1] & np.uint64(2 ** (idx - 161)) != 0
    elif 225 <= idx <= 288:
        return bitboard[0] & np.uint64(2 ** (idx - 225)) != 0


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


shift_bitboard_mask_arr = np.array(
    [
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446744073709551615,
        18446744071562067968,
    ],
    dtype=np.uint64,
)


@njit(uint64[:](uint64[:], int8), cache=True)
def shift_bitboard(bitboard, shift):
    # right is positive shift EAST
    """
    Shift the bitboard by shift
    while ensuring that bits outside of the 17x17 are not set
    """
    arr = np.zeros(5, dtype=np.uint64)
    rolled_bitboard = np.zeros(5, dtype=np.uint64)
    if shift < 64 and shift > 0:
        rolled_bitboard[1:5] = bitboard[0:4]
        arr = (bitboard >> np.uint64(shift)) + (
            rolled_bitboard << np.uint64(64 - shift)
        ) & shift_bitboard_mask_arr
    elif shift < 0 and shift > -64:
        rolled_bitboard[0:4] = bitboard[1:5]
        arr = (bitboard << np.uint64(-shift)) + (
            rolled_bitboard >> np.uint64(64 + shift)
        )
    return arr


@njit(cache=True)
def shift_bitboard_check_wall(player_bitboard, wall_bitboard, shift, mask):
    """
    Shift the bitboard right by shift
    Then bitwise AND with wall bitboard and compare to blank bitboard
    to ensure that the player doesn't go through a wal
    Then AND with full bitboard to ensure the player is on the board
    """
    rolled_bitboard = np.zeros(5, dtype=np.uint64)
    if shift > 0 and shift < 64:
        rolled_bitboard[1:5] = player_bitboard[0:4]
        rolled_bitboard = (player_bitboard >> np.uint64(shift)) + (
            rolled_bitboard << np.uint64(64 - shift)
        ) & shift_bitboard_mask_arr
    elif shift < 0 and shift > -64:
        rolled_bitboard[0:4] = player_bitboard[1:5]
        rolled_bitboard = (player_bitboard << np.uint64(-shift)) + (
            rolled_bitboard >> np.uint64(64 + shift)
        )
    return np.array_equal(rolled_bitboard & wall_bitboard, blank) and ~np.array_equal(
        rolled_bitboard & mask, blank
    )


def display(bitboard):
    line = "".join([np.binary_repr(x, 64) for x in bitboard])
    for i in range(0, 17):
        print(line[i * 17 : i * 17 + 17])
    print()


@njit(cache=True)
def manhatten_distance(bitboard_player, player_number=1):
    found_idx = -1
    if bitboard_player[4] != 0:
        if bitboard_player[4] == 2147483648:
            found_idx = 0
        elif bitboard_player[4] == 8589934592:
            found_idx = 2
        elif bitboard_player[4] == 34359738368:
            found_idx = 4
        elif bitboard_player[4] == 137438953472:
            found_idx = 6
        elif bitboard_player[4] == 549755813888:
            found_idx = 8
        elif bitboard_player[4] == 2199023255552:
            found_idx = 10
        elif bitboard_player[4] == 8796093022208:
            found_idx = 12
        elif bitboard_player[4] == 35184372088832:
            found_idx = 14
        elif bitboard_player[4] == 140737488355328:
            found_idx = 16
    elif bitboard_player[3] != 0:
        if bitboard_player[3] == 2:
            found_idx = 34
        elif bitboard_player[3] == 8:
            found_idx = 36
        elif bitboard_player[3] == 32:
            found_idx = 38
        elif bitboard_player[3] == 128:
            found_idx = 40
        elif bitboard_player[3] == 512:
            found_idx = 42
        elif bitboard_player[3] == 2048:
            found_idx = 44
        elif bitboard_player[3] == 8192:
            found_idx = 46
        elif bitboard_player[3] == 32768:
            found_idx = 48
        elif bitboard_player[3] == 131072:
            found_idx = 50
        elif bitboard_player[3] == 34359738368:
            found_idx = 68
        elif bitboard_player[3] == 137438953472:
            found_idx = 70
        elif bitboard_player[3] == 549755813888:
            found_idx = 72
        elif bitboard_player[3] == 2199023255552:
            found_idx = 74
        elif bitboard_player[3] == 8796093022208:
            found_idx = 76
        elif bitboard_player[3] == 35184372088832:
            found_idx = 78
        elif bitboard_player[3] == 140737488355328:
            found_idx = 80
        elif bitboard_player[3] == 562949953421312:
            found_idx = 82
        elif bitboard_player[3] == 2251799813685248:
            found_idx = 84
    elif bitboard_player[2] != 0:
        if bitboard_player[2] == 32:
            found_idx = 102
        elif bitboard_player[2] == 128:
            found_idx = 104
        elif bitboard_player[2] == 512:
            found_idx = 106
        elif bitboard_player[2] == 2048:
            found_idx = 108
        elif bitboard_player[2] == 8192:
            found_idx = 110
        elif bitboard_player[2] == 32768:
            found_idx = 112
        elif bitboard_player[2] == 131072:
            found_idx = 114
        elif bitboard_player[2] == 524288:
            found_idx = 116
        elif bitboard_player[2] == 2097152:
            found_idx = 118
        elif bitboard_player[2] == 549755813888:
            found_idx = 136
        elif bitboard_player[2] == 2199023255552:
            found_idx = 138
        elif bitboard_player[2] == 8796093022208:
            found_idx = 140
        elif bitboard_player[2] == 35184372088832:
            found_idx = 142
        elif bitboard_player[2] == 140737488355328:
            found_idx = 144
        elif bitboard_player[2] == 562949953421312:
            found_idx = 146
        elif bitboard_player[2] == 2251799813685248:
            found_idx = 148
        elif bitboard_player[2] == 9007199254740992:
            found_idx = 150
        elif bitboard_player[2] == 36028797018963968:
            found_idx = 152
    elif bitboard_player[1] != 0:
        if bitboard_player[1] == 512:
            found_idx = 170
        elif bitboard_player[1] == 2048:
            found_idx = 172
        elif bitboard_player[1] == 8192:
            found_idx = 174
        elif bitboard_player[1] == 32768:
            found_idx = 176
        elif bitboard_player[1] == 131072:
            found_idx = 178
        elif bitboard_player[1] == 524288:
            found_idx = 180
        elif bitboard_player[1] == 2097152:
            found_idx = 182
        elif bitboard_player[1] == 8388608:
            found_idx = 184
        elif bitboard_player[1] == 33554432:
            found_idx = 186
        elif bitboard_player[1] == 8796093022208:
            found_idx = 204
        elif bitboard_player[1] == 35184372088832:
            found_idx = 206
        elif bitboard_player[1] == 140737488355328:
            found_idx = 208
        elif bitboard_player[1] == 562949953421312:
            found_idx = 210
        elif bitboard_player[1] == 2251799813685248:
            found_idx = 212
        elif bitboard_player[1] == 9007199254740992:
            found_idx = 214
        elif bitboard_player[1] == 36028797018963968:
            found_idx = 216
        elif bitboard_player[1] == 144115188075855872:
            found_idx = 218
        elif bitboard_player[1] == 576460752303423488:
            found_idx = 220
    else:
        if bitboard_player[0] == 8192:
            found_idx = 238
        elif bitboard_player[0] == 32768:
            found_idx = 240
        elif bitboard_player[0] == 131072:
            found_idx = 242
        elif bitboard_player[0] == 524288:
            found_idx = 244
        elif bitboard_player[0] == 2097152:
            found_idx = 246
        elif bitboard_player[0] == 8388608:
            found_idx = 248
        elif bitboard_player[0] == 33554432:
            found_idx = 250
        elif bitboard_player[0] == 134217728:
            found_idx = 252
        elif bitboard_player[0] == 536870912:
            found_idx = 254
        elif bitboard_player[0] == 140737488355328:
            found_idx = 272
        elif bitboard_player[0] == 562949953421312:
            found_idx = 274
        elif bitboard_player[0] == 2251799813685248:
            found_idx = 276
        elif bitboard_player[0] == 9007199254740992:
            found_idx = 278
        elif bitboard_player[0] == 36028797018963968:
            found_idx = 280
        elif bitboard_player[0] == 144115188075855872:
            found_idx = 282
        elif bitboard_player[0] == 576460752303423488:
            found_idx = 284
        elif bitboard_player[0] == 2305843009213693952:
            found_idx = 286
        elif bitboard_player[0] == 9223372036854775808:
            found_idx = 288
    if player_number == 1:
        return 8 - found_idx // 34
    else:
        return found_idx // 34


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


# @njit(cache=True)
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

    path = np.zeros(5, dtype=np.uint64)

    path_cost = np.full((9, 9), -1, dtype=np.int8)
    start_idx = bitboard_get_index(start_pos)
    path_cost[8 - start_idx // 9, 8 - start_idx % 9] = 0
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
        prev_index = bitboard_get_index(node)
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
                if (
                    not in_frontier
                    and np.array_equal(shifted_bitboard & explored, blank)
                    and not np.array_equal(shifted_bitboard, blank)
                ):
                    if (
                        player_number == 1 and shifted_bitboard[0] >= 140737488355328
                    ) or (  # 2^47
                        player_number == 2
                        and np.uint64(2147483648)
                        <= shifted_bitboard[4]
                        <= np.uint64(140737488355328)
                    ):  # 2^47
                        shifted_index = bitboard_get_index(shifted_bitboard)
                        path_cost[8 - shifted_index // 9, 8 - shifted_index % 9] = (
                            path_cost[8 - prev_index // 9, 8 - prev_index % 9] + 1
                        )
                        path += shifted_bitboard
                        current_index = shifted_index
                        current_value = 8
                        while True:
                            if current_index < 72:
                                if (
                                    path_cost[
                                        8 - (current_index + 9) // 9,
                                        8 - (current_index + 9) % 9,
                                    ]
                                    == current_value - 1
                                ):
                                    path += shift_bitboard(shifted_bitboard, -17)
                                    shifted_bitboard = shift_bitboard(
                                        shifted_bitboard, -34
                                    )
                                    path += shifted_bitboard
                            if current_index % 9 > 0:
                                if (
                                    path_cost[
                                        8 - (current_index - 1) // 9,
                                        8 - (current_index - 1) % 9,
                                    ]
                                    == current_value - 1
                                ):
                                    path += shift_bitboard(shifted_bitboard, 1)
                                    shifted_bitboard = shift_bitboard(
                                        shifted_bitboard, 2
                                    )
                                    path += shifted_bitboard
                            if current_index > 8:
                                if (
                                    path_cost[
                                        8 - (current_index - 9) // 9,
                                        8 - (current_index - 9) % 9,
                                    ]
                                    == current_value - 1
                                ):
                                    path += shift_bitboard(shifted_bitboard, 17)
                                    shifted_bitboard = shift_bitboard(
                                        shifted_bitboard, 34
                                    )
                                    path += shifted_bitboard
                            if current_index % 9 < 8:
                                if (
                                    path_cost[
                                        8 - (current_index + 1) // 9,
                                        8 - (current_index + 1) % 9,
                                    ]
                                    == current_value - 1
                                ):
                                    path += shift_bitboard(shifted_bitboard, -1)
                                    shifted_bitboard = shift_bitboard(
                                        shifted_bitboard, -2
                                    )
                                    path += shifted_bitboard

                            current_value -= 1
                            current_index = bitboard_get_index(shifted_bitboard)
                            if current_value == 0:
                                break
                        print(wall_number)
                        display(path)
                        return True

                    frontier[frontier_length] = shifted_bitboard

                    shifted_index = bitboard_get_index(shifted_bitboard)

                    if (
                        path_cost[8 - shifted_index // 9, 8 - shifted_index % 9]
                        < path_cost[8 - prev_index // 9, 8 - prev_index % 9] + 1
                    ):
                        path_cost[8 - shifted_index // 9, 8 - shifted_index % 9] = (
                            path_cost[8 - prev_index // 9, 8 - prev_index % 9] + 1
                        )

                    frontier_length += 1


# @njit(cache=True)
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


# @njit(cache=True)
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
        frontier[min_idx] = full
        frontier_manhatten_distance[min_idx] = 127
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


# @njit(cache=True)
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
        frontier[min_idx] = full
        frontier_path_cost[min_idx] = 127
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


# @njit(cache=True)
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
        frontier[min_idx] = full
        frontier_costs[min_idx] = [127, 127, 127]
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


bitboard = np.array([0, 0, 0, 0, 2**39], dtype=np.uint64)
BreadthFirstSearch_Bitboard(bitboard, 1, np.zeros(5, dtype=np.uint64), 0)
