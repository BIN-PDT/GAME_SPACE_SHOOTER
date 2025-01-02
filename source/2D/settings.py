from os.path import join
from random import randint, uniform
from pyray import *
from raylib import *


WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
BG_COLOR = (15, 10, 25, 255)
PLAYER_SPEED = 500
LASER_SPEED = 600
METEOR_SPEED_RANGE = [300, 400]
METEOR_TIMER_DURATION = 0.4
FONT_SIZE = 120
