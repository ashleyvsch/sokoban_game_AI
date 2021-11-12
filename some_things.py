import sokoban_structures
from global_constants import *

file = 'data/simplegame.txt'
s = sokoban_structures.Sokoban(file)

print(s.board)
print(s.utilities)
print(s.rewards)

print(s.agent)

s.update_agent(UP)

print(s.agent)

print(s.board)