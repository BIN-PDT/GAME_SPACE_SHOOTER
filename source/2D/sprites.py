from settings import *


class Sprite:
    def __init__(self, texture, pos, direction, speed):
        self.texture = texture
        self.size = Vector2(texture.width, texture.height)
        self.pos = pos
        self.direction = direction
        self.SPEED = speed

    def move(self, dt):
        self.pos.x += self.direction.x * self.SPEED * dt
        self.pos.y += self.direction.y * self.SPEED * dt

    def update(self, dt):
        pass

    def draw(self):
        draw_texture_v(self.texture, self.pos, WHITE)


class Player(Sprite):
    def __init__(self, texture, pos):
        super().__init__(texture, pos, Vector2(), PLAYER_SPEED)

    def input(self):
        self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        self.direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))
        self.direction = Vector2Normalize(self.direction)

        if is_key_pressed(KEY_SPACE):
            print("Laser")

    def constraint(self):
        self.pos.x = max(0, min(self.pos.x, WINDOW_WIDTH - self.size.x))
        self.pos.y = max(0, min(self.pos.y, WINDOW_HEIGHT - self.size.y))

    def update(self, dt):
        self.input()
        self.move(dt)
        self.constraint()
