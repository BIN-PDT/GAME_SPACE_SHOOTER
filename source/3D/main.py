from settings import *


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

    def update(self):
        dt = get_frame_time()

    def draw(self):
        clear_background(BG_COLOR)
        begin_drawing()
        begin_mode_3d(self.camera)
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
