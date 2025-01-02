from settings import *
from timers import Timer
from sprites import Player, Laser, Meteor, ExplosionAnimation


class Game:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Space Shooter")
        init_audio_device()
        # ASSETS.
        self.load_assets()
        # GROUP.
        self.group_laser = []
        self.group_meteor = []
        self.group_explosion = []
        # TIMER.
        self.timer_meteor = Timer(METEOR_TIMER_DURATION, True, True, self.create_meteor)
        # PLAYER.
        self.player = Player(
            self.assets["player"],
            Vector2(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            self.shoot_laser,
        )
        # MUSIC.
        play_music_stream(self.audios["music"])

    def load_assets(self):
        # FONT & IMAGE.
        self.assets = {
            "font": load_font_ex(join("font", "Stormfaze.otf"), FONT_SIZE, ffi.NULL, 0),
            "player": load_texture(join("images", "spaceship.png")),
            "star": load_texture(join("images", "star.png")),
            "laser": load_texture(join("images", "laser.png")),
            "meteor": load_texture(join("images", "meteor.png")),
            "explosion": [
                load_texture(join("images", "explosion", f"{i}.png"))
                for i in range(1, 29)
            ],
        }
        # MUSIC & SOUND.
        self.audios = {
            "laser": load_sound(join("audio", "laser.wav")),
            "explosion": load_sound(join("audio", "explosion.wav")),
            "music": load_music_stream(join("audio", "music.wav")),
        }
        # INITIAL DATA.
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

    def draw_score(self):
        score_text = str(int(get_time()))
        text_size = measure_text_ex(self.assets["font"], score_text, FONT_SIZE, 0)
        score_pos = WINDOW_WIDTH / 2 - text_size.x, 100
        draw_text_ex(self.assets["font"], score_text, score_pos, FONT_SIZE, 0, WHITE)

    def shoot_laser(self, pos):
        self.group_laser.append(Laser(self.assets["laser"], pos))
        play_sound(self.audios["laser"])

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
                    play_sound(self.audios["explosion"])
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
        update_music_stream(self.audios["music"])
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
        self.draw_score()
        self.player.draw()
        for sprite in self.group_laser + self.group_meteor + self.group_explosion:
            sprite.draw()
        end_drawing()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()
        unload_music_stream(self.audios["music"])
        close_audio_device()
        close_window()


if __name__ == "__main__":
    Game().run()
