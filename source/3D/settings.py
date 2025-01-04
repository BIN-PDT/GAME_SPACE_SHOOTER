from os.path import join
from random import randint, uniform, choice
from pyray import *
from raylib import *
from timers import Timer


WINDOW_WIDTH, WINDOW_HEIGHT = 1920, 1080
BG_COLOR = BLACK
SHADOW_COLOR = (0, 0, 0, 50)
PLAYER_SPEED = 7
LASER_SPEED = 9
METEOR_SPEED_RANGE = [3, 4]
METEOR_TIMER_DURATION = 0.4
FONT_SIZE = 60
FONT_PADDING = 60
