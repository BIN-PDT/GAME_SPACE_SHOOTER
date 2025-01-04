from math import sin
from settings import *


class Model:
    def __init__(self, model, pos, speed, direction=Vector3()):
        self.model = model
        self.pos = pos
        self.SPEED = speed
        self.direction = direction

    def move(self, dt):
        self.pos.x += self.direction.x * self.SPEED * dt
        self.pos.y += self.direction.y * self.SPEED * dt
        self.pos.z += self.direction.z * self.SPEED * dt

    def update(self, dt):
        self.move(dt)

    def draw(self):
        draw_model(self.model, self.pos, 1, WHITE)


class Floor(Model):
    def __init__(self, texture):
        mesh = gen_mesh_cube(32, 1, 32)
        model = load_model_from_mesh(mesh)
        set_material_texture(model.materials[0], MATERIAL_MAP_ALBEDO, texture)
        super().__init__(model, Vector3(6.5, -2, -8), 0)


class Player(Model):
    def __init__(self, model, shoot_laser):
        super().__init__(model, Vector3(), PLAYER_SPEED)
        self.shoot_laser = shoot_laser
        self.angle = 0

    def input(self):
        self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        if is_key_pressed(KEY_SPACE):
            self.shoot_laser(self.pos)

    def constraint(self):
        self.pos.x = max(-6, min(7, self.pos.x))
        self.angle = max(-15, min(15, self.angle))

    def update(self, dt):
        self.angle -= self.direction.x * 10 * dt
        self.pos.y += sin(get_time() * 5) * 0.1 * dt
        self.input()
        super().update(dt)
        self.constraint()

    def draw(self):
        draw_model_ex(
            self.model, self.pos, Vector3(0, 0, 1), self.angle, Vector3(1, 1, 1), WHITE
        )
