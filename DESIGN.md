-> main.py - what the user should run
- `main()` running during runtime
/Quoridor
-> game.py
- `get_available_action()` returns the list of available actions 
- `get_available_states()` returns the states resulting from all possible actions (for use by AI)

- `take_action()` action of user/agent can be inputed

- `log()` returns a dict with information of the game

-> test.py
- `simulate(**kwargs)` inputs AI version used for both players; board representation; pathfinding mode; set of moves to play (control the moves made)
- `compare(**kwargs)` inputs number of games; board representations; pathfinding modes
______________
-> bitboard.py
-> graph.py
- `get_available_action()` returns the list of available actions as a boolean array with 128+12 values

First 64 values (0~63) represent the horizontal wall placements and whether they are possible or not - a1h, b1h and so on
Next 64 values (64~127) represent the vertical wall placements and whether they are possible or not - a1v, b1v and so on
Next 4 values (128~131) represent the possible moves by the player - in order of N, E, S, W
Next 8 values (132~139) reprsent the possible moves by the player - in order of NN, NE, EE, SE, SS, SW, WW, NW
- `get_available_states()` returns the states resulting from all possible actions (for use by AI)
- `display_beautiful()` outputs the UNICODE representation to terminal
- `take_action()` performs the input move - only called when game isn't over
- `is_over()` returns if the game is over
- `winner()` returns the winner of the game - only called when game is over

______________
