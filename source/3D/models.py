from math import sin
from settings import *


class Model:
    def __init__(self, model, pos, speed, direction=Vector3()):
        self.model = model
        self.pos = pos
        self.SPEED = speed
        self.direction = direction
        self.discard = False

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
            self.shoot_laser(Vector3Add(self.pos, Vector3(0, 0, -1)))

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


class Laser(Model):
    def __init__(self, model, pos, texture):
        super().__init__(model, pos, LASER_SPEED, Vector3(0, 0, -1))
        set_material_texture(self.model.materials[0], MATERIAL_MAP_ALBEDO, texture)


class Meteor(Model):
    def __init__(self, texture):
        self.radius = uniform(0.6, 1.5)
        self.rotation = Vector3(uniform(-5, 5), uniform(-5, 5), uniform(-5, 5))
        self.ROTATION_SPEED = Vector3(uniform(-1, 1), uniform(-1, 1), uniform(-1, 1))
        # SETUP.
        model = load_model_from_mesh(gen_mesh_sphere(self.radius, 8, 8))
        set_material_texture(model.materials[0], MATERIAL_MAP_ALBEDO, texture)
        pos = Vector3(uniform(-6, 7), 0, -20)
        speed = uniform(*METEOR_SPEED_RANGE)
        direction = Vector3(0, 0, uniform(0.75, 1.25))
        super().__init__(model, pos, speed, direction)
        # COLLISION.
        self.timer_destroy = Timer(0.25, False, False, self.activate_discard)
        # SHADER.
        self.shader = load_shader(ffi.NULL, join("shaders", "flash.fs"))
        model.materials[0].shader = self.shader
        self.flash_loc = get_shader_location(self.shader, "flash")
        self.flash_amount = ffi.new("struct Vector2 *", [1, 0])

    def rotate(self, dt):
        self.rotation.x += self.ROTATION_SPEED.x * dt
        self.rotation.y += self.ROTATION_SPEED.y * dt
        self.rotation.z += self.ROTATION_SPEED.z * dt
        self.model.transform = matrix_rotate_xyz(self.rotation)

    def activate_discard(self):
        self.discard = True

    def activate_flash(self):
        set_shader_value(
            self.shader, self.flash_loc, self.flash_amount, SHADER_UNIFORM_VEC2
        )

    def update(self, dt):
        self.timer_destroy.update()
        if not self.timer_destroy.active:
            self.rotate(dt)
            super().update(dt)
