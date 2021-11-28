import sokoban_structures
from global_constants import *
import helper
import printing

file = 'data/simplegame.txt'
s = sokoban_structures.Sokoban(file)


printing.print_q_table(s)