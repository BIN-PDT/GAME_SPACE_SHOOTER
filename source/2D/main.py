from settings import *
from timers import Timer
from sprites import Player, Laser, Meteor, ExplosionAnimation


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
        self.group_meteor = []
        self.timer_meteor = Timer(METEOR_TIMER_DURATION, True, True, self.create_meteor)
        self.group_explosion = []

    def load_assets(self):
        self.assets = {
            "player": load_texture(join("images", "spaceship.png")),
            "star": load_texture(join("images", "star.png")),
            "laser": load_texture(join("images", "laser.png")),
            "meteor": load_texture(join("images", "meteor.png")),
            "explosion": [
                load_texture(join("images", "explosion", f"{i}.png"))
                for i in range(1, 29)
            ],
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

    def create_meteor(self):
        self.group_meteor.append(Meteor(self.assets["meteor"]))

    def discard_sprites(self):
        self.group_laser = [s for s in self.group_laser if not s.discard]
        self.group_meteor = [s for s in self.group_meteor if not s.discard]
        self.group_explosion = [s for s in self.group_explosion if not s.discard]

    def check_collision(self):
        # LASER & METEOR.
        for laser in self.group_laser:
            for meteor in self.group_meteor:
                if check_collision_circle_rec(
                    meteor.get_center_pos(),
                    meteor.COLLISION_RADIUS,
                    laser.get_rectangle(),
                ):
                    laser.discard = meteor.discard = True
                    self.group_explosion.append(
                        ExplosionAnimation(self.assets["explosion"], laser.pos)
                    )
                    break
        # PLAYER & METEOR.
        for meteor in self.group_meteor:
            if check_collision_circles(
                self.player.get_center_pos(),
                self.player.COLLISION_RADIUS,
                meteor.get_center_pos(),
                meteor.COLLISION_RADIUS,
            ):
                close_window()

    def update(self):
        dt = get_frame_time()
        self.timer_meteor.update()
        self.player.update(dt)
        for sprite in self.group_laser + self.group_meteor + self.group_explosion:
            sprite.update(dt)
        self.check_collision()
        self.discard_sprites()

    def draw(self):
        begin_drawing()
        clear_background(BG_COLOR)
        self.draw_stars()
        self.player.draw()
        for sprite in self.group_laser + self.group_meteor + self.group_explosion:
            sprite.draw()
        end_drawing()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()
        close_window()


if __name__ == "__main__":
    Game().run()
