from settings import *
from timers import Timer
from sprites import Player


class Game:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Space Shooter")
        self.load_assets()

        self.player = Player(
            self.assets["player"], Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2)
        )

    def load_assets(self):
        self.assets = {
            "player": load_texture(join("images", "spaceship.png")),
            "star": load_texture(join("images", "star.png")),
        }

        self.star_data = [
            (
                Vector2(
                    randint(0, WINDOW_WIDTH), randint(0, WINDOW_HEIGHT)
                ),  # POSITION.
                uniform(0.5, 1.6),  # SIZE.
            )
            for _ in range(30)
        ]

    def draw_stars(self):
        for star in self.star_data:
            draw_texture_ex(self.assets["star"], star[0], 0, star[1], WHITE)

    def update(self):
        dt = get_frame_time()
        self.player.update(dt)

    def draw(self):
        begin_drawing()
        clear_background(BG_COLOR)
        self.draw_stars()
        self.player.draw()
        end_drawing()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()
        close_window()


if __name__ == "__main__":
    Game().run()
