from tkinter import *

import random

import Tetris

##########################################################
# please test my game by checking if:
# 1. Blocks don't run into each other/ run into "walls"
# 2. Upon a row is fully stacked, the full row goes away
# 3. And you will get points from #2
# 4. You can pause or restart the game
# 5. You are having fun playing !
##########################################################

assert (Tetris.playTetris()[0] == 250)
assert (Tetris.playTetris()[1] == 350)
assert (str(type(Tetris.playTetris())) == "<class 'tuple'>")

