from Quoridor.game import Game


def action_to_algebra(action_number):
    if action_number < 64:
        return f"{chr(97+action_number%8)}{action_number//8+1}h"
    elif action_number < 128:
        return f"{chr(97+action_number%8)}{(action_number%64)//8+1}v"
    elif action_number < 140:
        return ["N", "E", "S", "W", "NN", "NE", "EE", "SE", "SS", "SW", "WW", "NW"][
            action_number % 128
        ]


def test(
    representation,
    path_finding_mode,
    moves,
    mode,
    output,
    note="NONE",
    display=False,
):
    board = Game(
        representation=representation,
        path_finding_mode=path_finding_mode,
    )
    for move in moves:
        board.take_action(move)

    available_moves = board.available_actions()

    if display:
        board.display()
    if mode == "all":
        algebraic_available = [
            action_to_algebra(x) for x in range(140) if available_moves[x]
        ]
        if set(algebraic_available) == set(output):
            print("PASS", note)
        else:
            print(
                "FAIL",
                note,
                "MISSING",
                [m for m in output if m not in algebraic_available],
                "EXTRA",
                [m for m in algebraic_available if m not in output],
                "TURN",
                board.board.turn,
            )
    elif mode == "walls":
        algebraic_available = [
            action_to_algebra(x) for x in range(128) if available_moves[x]
        ]
        if set(algebraic_available) == set(output):
            print("PASS", note)
        else:
            print(
                "FAIL",
                note,
                "MISSING",
                [m for m in output if m not in algebraic_available],
                "EXTRA",
                [m for m in algebraic_available if m not in output],
                "TURN",
                board.board.turn,
            )
    elif mode == "moves":
        algebraic_available = [
            action_to_algebra(128 + x) for x in range(12) if available_moves[128 + x]
        ]
        if set(algebraic_available) == set(output):
            print("PASS", note)
        else:
            print(
                "FAIL",
                note,
                "MISSING",
                [m for m in output if m not in algebraic_available],
                "EXTRA",
                [m for m in algebraic_available if m not in output],
                "TURN",
                board.board.turn,
                available_moves[128:],
            )


def test_suite(representation, path_finding_mode):
    print(representation, path_finding_mode)
    test(
        representation,
        path_finding_mode,
        [128, 130, 128, 130],
        "moves",
        ["N", "E", "S", "W"],
        "1 basic movement",
    )
    test(
        representation,
        path_finding_mode,
        [129, 130, 129, 130, 129, 130, 129, 130],
        "moves",
        ["N", "W"],
        "1 bottom right corner movement",
    )
    test(
        representation,
        path_finding_mode,
        [131, 130, 131, 130, 131, 130, 131, 130],
        "moves",
        ["N", "E"],
        "1 bottom left corner movement",
    )

    test(
        representation,
        path_finding_mode,
        [131, 130, 131, 130, 131, 130, 131, 130, 128, 1],
        "moves",
        ["N", "E", "S"],
        "1 west side extreme",
    )
    test(
        representation,
        path_finding_mode,
        [131, 130, 131, 130, 131, 130, 131, 130, 128, 130, 128, 1],
        "moves",
        ["N", "E", "S"],
        "1 west side extreme",
    )

    test(
        representation,
        path_finding_mode,
        [131, 130, 131, 130, 131, 130, 131, 130, 128, 130, 128, 130, 128, 1],
        "moves",
        ["N", "E", "S"],
        "1 west side extreme",
    )

    test(
        representation,
        path_finding_mode,
        [129, 130, 129, 130, 129, 130, 129, 130, 128, 1],
        "moves",
        ["N", "W", "S"],
        "1 east side extreme",
    )
    test(
        representation,
        path_finding_mode,
        [129, 130, 129, 130, 129, 130, 129, 130, 128, 130, 128, 1],
        "moves",
        ["N", "W", "S"],
        "1 east side extreme",
    )

    test(
        representation,
        path_finding_mode,
        [129, 130, 129, 130, 129, 130, 129, 130, 128, 130, 128, 130, 128, 1],
        "moves",
        ["N", "W", "S"],
        "1 east side extreme",
    )
    test(
        representation,
        path_finding_mode,
        [129, 131, 129, 131, 129, 131, 129, 131, 1],
        "moves",
        ["E", "S"],
        "2 west side extreme",
    )
    test(
        representation,
        path_finding_mode,
        [129, 131, 129, 131, 129, 131, 129, 131, 128, 130, 1],
        "moves",
        ["E", "S", "N"],
        "2 west side extreme",
    )
    test(
        representation,
        path_finding_mode,
        [129, 131, 129, 131, 129, 131, 129, 131, 128, 130, 128, 130, 1],
        "moves",
        ["E", "S", "N"],
        "2 west side extreme",
    )
    test(
        representation,
        path_finding_mode,
        [129, 131, 129, 131, 129, 131, 129, 131, 128, 130, 128, 130, 128, 130, 1],
        "moves",
        ["E", "S", "N"],
        "2 west side extreme",
    )
    test(
        representation,
        path_finding_mode,
        [128, 130, 128, 130, 128, 130, 128],
        "moves",
        ["N", "E", "W", "SS"],
        "2 adjacent to 1 movement",
    )
    test(
        representation,
        path_finding_mode,
        [128, 130, 128, 130, 128, 130, 128, 1],
        "moves",
        ["E", "S", "W", "NN"],
        "1 adjacent to 2 movement",
    )

    test(
        representation,
        path_finding_mode,
        [128, 130, 128, 130, 128, 130, 128, 43],
        "moves",
        ["E", "S", "W", "NW", "NE"],
        "1 adjacent to 2 with wall North of player 2",
    )
    test(
        representation,
        path_finding_mode,
        [128, 130, 128, 130, 128, 130, 128, 43, 100, 1],
        "moves",
        ["S", "W", "NW"],
        "1 adjacent to 2 with wall North and East of player 2",
    )
    test(
        representation,
        path_finding_mode,
        [0, 9, 12, 14, 17, 32, 40, 123, 125],
        "walls",
        [
            "c1h",
            "d1h",
            "e1h",
            "f1h",
            "g1h",
            "h1h",
            "d3h",
            "e3h",
            "f3h",
            "g3h",
            "h3h",
            "a4h",
            "b4h",
            "c4h",
            "d4h",
            "e4h",
            "f4h",
            "g4h",
            "h4h",
            "c5h",
            "d5h",
            "e5h",
            "f5h",
            "g5h",
            "h5h",
            "c6h",
            "d6h",
            "e6h",
            "f6h",
            "g6h",
            "h6h",
            "a7h",
            "b7h",
            "c7h",
            "d7h",
            "f7h",
            "g7h",
            "h7h",
            "a8h",
            "b8h",
            "c8h",
            "g8h",
            "h8h",
            "b1v",
            "c1v",
            "d1v",
            "e1v",
            "f1v",
            "g1v",
            "h1v",
            "a2v",
            "c2v",
            "d2v",
            "f2v",
            "h2v",
            "a3v",
            "c3v",
            "d3v",
            "e3v",
            "f3v",
            "g3v",
            "h3v",
            "a4v",
            "b4v",
            "c4v",
            "d4v",
            "e4v",
            "f4v",
            "g4v",
            "h4v",
            "b5v",
            "c5v",
            "d5v",
            "e5v",
            "f5v",
            "g5v",
            "h5v",
            "b6v",
            "c6v",
            "d6v",
            "e6v",
            "f6v",
            "g6v",
            "h6v",
            "a7v",
            "b7v",
            "c7v",
            "e7v",
            "g7v",
            "h7v",
            "a8v",
            "b8v",
            "c8v",
            "e8v",
            "g8v",
            "h8v",
        ],
        "1 adjacent to 2 with wall North and East of player 2",
    )
    test(
        representation,
        path_finding_mode,
        [0, 2, 4, 6, 79, 80],
        "all",
        [
            "E",
            "W",
            "a2h",
            "b2h",
            "c2h",
            "d2h",
            "e2h",
            "f2h",
            "g2h",
            "b3h",
            "c3h",
            "d3h",
            "e3h",
            "f3h",
            "g3h",
            "a4h",
            "b4h",
            "c4h",
            "d4h",
            "e4h",
            "f4h",
            "g4h",
            "h4h",
            "a5h",
            "b5h",
            "c5h",
            "d5h",
            "e5h",
            "f5h",
            "g5h",
            "h5h",
            "a6h",
            "b6h",
            "c6h",
            "d6h",
            "e6h",
            "f6h",
            "g6h",
            "h6h",
            "a7h",
            "b7h",
            "c7h",
            "d7h",
            "e7h",
            "f7h",
            "g7h",
            "h7h",
            "a8h",
            "b8h",
            "c8h",
            "d8h",
            "e8h",
            "f8h",
            "g8h",
            "h8h",
            "b1v",
            "d1v",
            "b2v",
            "c2v",
            "d2v",
            "e2v",
            "f2v",
            "g2v",
            "b3v",
            "c3v",
            "d3v",
            "e3v",
            "f3v",
            "g3v",
            "b4v",
            "c4v",
            "d4v",
            "e4v",
            "f4v",
            "g4v",
            "h4v",
            "a5v",
            "b5v",
            "c5v",
            "d5v",
            "e5v",
            "f5v",
            "g5v",
            "h5v",
            "a6v",
            "b6v",
            "c6v",
            "d6v",
            "e6v",
            "f6v",
            "g6v",
            "h6v",
            "a7v",
            "b7v",
            "c7v",
            "d7v",
            "e7v",
            "f7v",
            "g7v",
            "h7v",
            "a8v",
            "b8v",
            "c8v",
            "d8v",
            "e8v",
            "f8v",
            "g8v",
            "h8v",
        ],
        "Wall block only path",
    )

    test(
        representation,
        path_finding_mode,
        [5, 12, 15, 16, 27, 30, 54, 61, 68, 74, 78, 83, 100, 107, 109, 123, 120],
        "walls",
        [
            "a1h",
            "b1h",
            "c1h",
            "d1h",
            "h1h",
            "a2h",
            "b2h",
            "e3h",
            "f3h",
            "g3h",
            "h3h",
            "a4h",
            "b4h",
            "a5h",
            "b5h",
            "c5h",
            "f5h",
            "g5h",
            "h5h",
            "a6h",
            "b6h",
            "c6h",
            "g6h",
            "h6h",
            "a7h",
            "b7h",
            "c7h",
            "d7h",
            "e7h",
            "b8h",
            "c8h",
            "h8h",
            "a1v",
            "b1v",
            "h1v",
            "a2v",
            "b2v",
            "f2v",
            "b3v",
            "e3v",
            "f3v",
            "h3v",
            "a4v",
            "b4v",
            "c4v",
            "f4v",
            "h4v",
            "a5v",
            "b5v",
            "c5v",
            "g5v",
            "h5v",
            "a6v",
            "b6v",
            "c6v",
            "g6v",
            "h6v",
            "b7v",
            "c7v",
            "e7v",
            "h7v",
            "b8v",
            "c8v",
            "e8v",
            "g8v",
            "h8v",
        ],
        "Complex",
        # True,
    )


test_suite("bitboard", "BFS")
test_suite("bitboard", "DFS")
test_suite("bitboard", "GBFS")
test_suite("bitboard", "UCT")
test_suite("bitboard", "Astar")
test_suite("graph", "BFS")
test_suite("graph", "DFS")
test_suite("graph", "GBFS")
test_suite("graph", "UCT")
test_suite("graph", "Astar")
test_suite("bitboard_optim", "BFS")
test_suite("bitboard_optim", "DFS")
test_suite("bitboard_optim", "GBFS")
test_suite("bitboard_optim", "UCT")
test_suite("bitboard_optim", "Astar")
test_suite("graph_optim", "BFS")
test_suite("graph_optim", "DFS")
test_suite("graph_optim", "GBFS")
test_suite("graph_optim", "UCT")
test_suite("graph_optim", "Astar")
# test_suite("graph")
# test_suite("bitboard")
# test_suite("graph_optim")
