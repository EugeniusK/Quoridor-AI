# 0.0.1

Initial version of graphical board implemented

Better version of board display in terminal that uses Unicode characters instead of ASCII

# 0.0.1.1

Add additional comments describing graph.py

# 0.0.2

Initial version of Breadth First Search, Greedy Best First Search and A* search implemented
Currently using Breadth First Search in graph.py

# 0.0.3

Initial version of bitboards implemented with similar functions to graph.py

# 0.0.4

Initial version of Breadth First Search, Greedy Best First Search implemented for bitboards

Currently using Greedy Best First Search in bitboard.py

Removed A* search from graph.py

# 0.0.4.1

A few small tweaks made to code
Optimised sorting based on distance to destination row in Greedy Best First Search for bitboards

# 0.0.4.2

Added random selection of moves

# 0.0.5

Added method of recording moves in a format inspired by PGN (Portable Game Notation)

# 0.0.5.1

Added comments, tidied up imports
Added simulating n number of games and comparing moves available from the same game state

# 0.0.5.2

Updated filenames to be supported on Windows 10 as well

# 0.0.5.3

Implement multiprocessing to accelerate comparison of moves

# 0.0.5.4

Remove unnecessary code in test.py for non multiprocessed versions

Fix mistakes found in bitboard.py and graph.py found from testing

# 0.0.5.5

Fix further mistakes when multiple rows inline in graphical representation
Passed test with 10000 games with BFS vs BFS

# 0.0.5.6

Implement Uniform Cost Search, Depth First Search and A star search
Implement selection of which search algorithm to be used during testing

# 0.0.5.7

Implement UCT, DFS, A* for bitboard
Fix comparison of search algorithms

# 0.0.6

Initial version of graph representation written with numpy, numba - using adjacency list

Implement BFS for optimised graph

Update test.py and log.py to support optimised graph