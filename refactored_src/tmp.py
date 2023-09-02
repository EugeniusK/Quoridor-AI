# for i in range(204, 204 + 18, 2):
#     print(2 ** (255 - i), "=> ", i, ",")
# for i in range(238, 238 + 18, 2):
#     print(2 ** (255 - i), "=> ", i, ",")


def output(i):
    for i in range(i, i + 17, 2):
        print(
            2 ** ((i // 64 + 1) * 64 - 1 - i),
            "=> ",
            "return",
            i // 2 - 8 * (i // 34),
            ",",
        )


for i in range(0, 288, 34):
    output(i)
