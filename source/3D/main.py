from settings import *
from models import Floor, Player, Laser, Meteor


class Game:
    def __init__(self):
        init_window(WINDOW_WIDTH, WINDOW_HEIGHT, "Space Shooter")
        init_audio_device()
        self.load_assets()
        # CAMERA.
        self.camera = Camera3D()
        self.camera.up = Vector3(0.0, 1.0, 0.0)
        self.camera.fovy = 45.0
        self.camera.target = Vector3(0.0, 0.0, -1.0)
        self.camera.position = Vector3(-4.0, 8.0, 6.0)
        self.camera.projection = CAMERA_PERSPECTIVE
        # GROUP.
        self.group_laser, self.group_meteor = [], []
        # TIMER.
        self.timer_meteor = Timer(METEOR_TIMER_DURATION, True, True, self.create_meteor)
        # SETUP.
        self.floor = Floor(self.dark_texture)
        self.player = Player(self.models["player"], self.shoot_laser)

    def load_assets(self):
        self.models = {
            "player": load_model(join("models", "ship.glb")),
            "laser": load_model(join("models", "laser.glb")),
        }

        self.audio = {
            "laser": load_sound(join("audio", "laser.wav")),
            "explosion": load_sound(join("audio", "explosion.wav")),
            "music": load_music_stream(join("audio", "music.wav")),
        }

        self.textures = [
            load_texture(join("textures", f"{color}.png"))
            for color in ("red", "green", "orange", "purple")
        ]
        self.dark_texture = load_texture(join("textures", "dark.png"))
        self.light_texture = load_texture(join("textures", "light.png"))

        self.font = load_font_ex("Stormfaze.otf", FONT_SIZE, ffi.NULL, 0)

    def shoot_laser(self, pos):
        self.group_laser.append(Laser(self.models["laser"], pos, self.light_texture))

    def create_meteor(self):
        self.group_meteor.append(Meteor(choice(self.textures)))

    def draw_shadows(self):
        # PLAYER.
        player_radius = 0.5 + self.player.pos.y
        player_shadow_pos = Vector3(self.player.pos.x, -1.5, self.player.pos.z)
        draw_cylinder(player_shadow_pos, 0, player_radius, 0.1, 20, SHADOW_COLOR)
        # METEOR.
        for meteor in self.group_meteor:
            meteor_radius = meteor.radius * 0.9
            meteor_shadow_pos = Vector3(meteor.pos.x, -1.5, meteor.pos.z)
            draw_cylinder(meteor_shadow_pos, 0, meteor_radius, 0.1, 20, SHADOW_COLOR)

    def check_discarded(self):
        self.group_laser = [m for m in self.group_laser if not m.discard]
        self.group_meteor = [m for m in self.group_meteor if not m.discard]

    def check_collision(self):
        # PLAYER & METEOR.
        for meteor in self.group_meteor:
            if check_collision_spheres(self.player.pos, 0.8, meteor.pos, meteor.radius):
                close_window()
        # LASER & METEOR.
        for laser in self.group_laser:
            laser_bbox = get_mesh_bounding_box(laser.model.meshes[0])
            laser_collision_bbox = BoundingBox(
                Vector3Add(laser_bbox.min, laser.pos),
                Vector3Add(laser_bbox.max, laser.pos),
            )
            for meteor in self.group_meteor:
                if check_collision_box_sphere(
                    laser_collision_bbox, meteor.pos, meteor.radius
                ):
                    laser.discard = True
                    meteor.timer_destroy.activate()
                    meteor.activate_flash()
                    break

    def update(self):
        dt = get_frame_time()
        self.timer_meteor.update()
        self.player.update(dt)
        for model in self.group_laser + self.group_meteor:
            model.update(dt)
        self.check_collision()
        self.check_discarded()

    def draw(self):
        clear_background(BG_COLOR)
        begin_drawing()
        begin_mode_3d(self.camera)
        self.floor.draw()
        self.draw_shadows()
        self.player.draw()
        for model in self.group_laser + self.group_meteor:
            model.draw()
        end_mode_3d()
        end_drawing()

    def run(self):
        while not window_should_close():
            self.update()
            self.draw()
        close_audio_device()
        close_window()


if __name__ == "__main__":
    Game().run()
