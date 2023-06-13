from numba import njit
import numpy as np
from timeit import timeit


@njit(cache=True)
def manhatten_distance(bitboard_player, player_number=1):
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
        return 8 - found_idx // 34
    else:
        return found_idx // 34


@njit(cache=True)
def log_manhatten_distance(bitboard_player, player_number=1):
    logged_bitboard = np.log2(bitboard_player)
    found_idx = np.uint8(0)
    if not np.isneginf(logged_bitboard[0]):
        found_idx = logged_bitboard[0] + 225
    elif not np.isneginf(logged_bitboard[1]):
        found_idx = logged_bitboard[1] + 161
    elif not np.isneginf(logged_bitboard[2]):
        found_idx = logged_bitboard[2] + 97
    elif not np.isneginf(logged_bitboard[3]):
        found_idx = logged_bitboard[3] + 33
    elif not np.isneginf(logged_bitboard[4]):
        found_idx = logged_bitboard[4] - 31

    if player_number == 1:
        return 8 - found_idx // 34
    else:
        return found_idx // 34


@njit(cache=True)
def compare_manhatten_distance(bitboard_player, player_number=1):
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


def test(func, input, output):
    if np.array_equal(func(input), output):
        return True, func(input)
    else:
        return False, func(input)


def display(bitboard):
    line = "".join([np.binary_repr(x, 64) for x in bitboard])
    for i in range(0, 17):
        print(line[i * 17 : i * 17 + 17])
    print()


def test_suite(func):
    times_taken = dict()
    inputs = []
    for row in range(9):
        for col in range(9):
            idx = row * 34 + col * 2

            if 0 <= idx <= 32:
                inputs.append(np.array([0, 0, 0, 0, 2 ** (idx + 31)], dtype=np.uint64))
            elif 33 <= idx <= 96:
                inputs.append(np.array([0, 0, 0, 2 ** (idx - 33), 0], dtype=np.uint64))
            elif 97 <= idx <= 160:
                inputs.append(np.array([0, 0, 2 ** (idx - 97), 0, 0], dtype=np.uint64))
            elif 161 <= idx <= 224:
                inputs.append(np.array([0, 2 ** (idx - 161), 0, 0, 0], dtype=np.uint64))
            elif 225 <= idx <= 288:
                inputs.append(np.array([2 ** (idx - 225), 0, 0, 0, 0], dtype=np.uint64))

    outputs = np.concatenate(
        (
            np.full(9, 8),
            np.full(9, 7),
            np.full(9, 6),
            np.full(9, 5),
            np.full(9, 4),
            np.full(9, 3),
            np.full(9, 2),
            np.full(9, 1),
            np.full(9, 0),
        )
    )

    func(inputs[0])
    fail = False
    for io in zip(inputs, outputs):
        time_taken = timeit(
            "test(func, io[0], io[1])",
            globals=globals() | locals(),
            number=10000,
        )
        result = test(func, io[0], io[1])
        if times_taken.get(io[1]) == None:
            times_taken[io[1]] = time_taken
        else:
            times_taken[io[1]] += time_taken
        if result[0] == False:
            fail = True
            print(
                func.__name__,
                False,
                "expect:",
                io[1],
                "result:",
                result[1],
                "time:",
                time_taken,
            )
        else:
            pass
            # print(func.__name__, True, "shift:", io[1], "time:", time_taken)

    if fail == True:
        print(
            func.__name__,
            False,
        )
    else:
        print(func.__name__, True)
    for key, value in times_taken.items():
        print(str(key).rjust(5), str(round(value, 5)).ljust(9))


test_suite(compare_manhatten_distance)

test_suite(log_manhatten_distance)
test_suite(manhatten_distance)
