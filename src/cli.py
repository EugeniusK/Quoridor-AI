from Quoridor.game import Game

while True:
    game = Game(player_one="human", player_two="random", representation="graph_optim")
    while True:
        game.display()

        move_valid = False
        moves_available = game.available_actions()
        while not move_valid:
            move_input = input()
            if move_input.isnumeric():
                if 0 <= int(move_input) <= 140:
                    if moves_available[int(move_input)]:
                        move_valid = True

        game.take_action(int(move_input))
        if game.is_over():
            print("GAME OVER YOU WIN")
            break
        game.display()
        game.take_action(game.select(game.available_actions()))
        if game.is_over():
            print("GAME OVER YOU LOSE")
            break
