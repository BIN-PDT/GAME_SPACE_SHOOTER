from settings import *
from timers import Timer
from sprites import Player, Laser


class Game:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Space Shooter")
        self.load_assets()

        self.group_laser = []
        self.player = Player(
            self.assets["player"],
            Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            self.shoot_laser,
        )

    def load_assets(self):
        self.assets = {
            "player": load_texture(join("images", "spaceship.png")),
            "star": load_texture(join("images", "star.png")),
            "laser": load_texture(join("images", "laser.png")),
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

    def shoot_laser(self, pos):
        self.group_laser.append(Laser(self.assets["laser"], pos))

    def discard_sprites(self):
        self.group_laser = [laser for laser in self.group_laser if not laser.discard]

    def update(self):
        dt = get_frame_time()
        self.player.update(dt)
        self.discard_sprites()
        for laser in self.group_laser:
            laser.update(dt)

    def draw(self):
        begin_drawing()
        clear_background(BG_COLOR)
        self.draw_stars()
        self.player.draw()
        for laser in self.group_laser:
            laser.draw()
        end_drawing()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()
        close_window()


if __name__ == "__main__":
    Game().run()
