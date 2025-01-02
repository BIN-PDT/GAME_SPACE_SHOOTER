from settings import *
from timers import Timer


class Game:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Space Shooter")

    def run(self):
        while not window_should_close():
            begin_drawing()
            end_drawing()
        close_window()


if __name__ == "__main__":
    Game().run()
