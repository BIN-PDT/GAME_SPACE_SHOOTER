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
