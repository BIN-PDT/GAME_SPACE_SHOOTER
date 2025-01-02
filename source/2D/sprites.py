from settings import *


class Sprite:
    def __init__(self, texture, pos, direction, speed):
        self.texture = texture
        self.size = Vector2(texture.width, texture.height)
        self.pos = pos
        self.direction = direction
        self.SPEED = speed
        self.discard = False

    def move(self, dt):
        self.pos.x += self.direction.x * self.SPEED * dt
        self.pos.y += self.direction.y * self.SPEED * dt

    def check_discard(self):
        self.discard = not -300 < self.pos.y < WINDOW_HEIGHT + 300

    def update(self, dt):
        pass

    def draw(self):
        draw_texture_v(self.texture, self.pos, WHITE)


class Player(Sprite):
    def __init__(self, texture, pos, shoot_laser):
        super().__init__(texture, pos, Vector2(), PLAYER_SPEED)
        self.shoot_laser = shoot_laser

    def input(self):
        self.direction.x = int(is_key_down(KEY_RIGHT)) - int(is_key_down(KEY_LEFT))
        self.direction.y = int(is_key_down(KEY_DOWN)) - int(is_key_down(KEY_UP))
        self.direction = Vector2Normalize(self.direction)

        if is_key_pressed(KEY_SPACE):
            self.shoot_laser(Vector2(self.pos.x + self.size.x / 2, self.pos.y - 60))

    def constraint(self):
        self.pos.x = max(0, min(self.pos.x, WINDOW_WIDTH - self.size.x))
        self.pos.y = max(0, min(self.pos.y, WINDOW_HEIGHT - self.size.y))

    def update(self, dt):
        self.input()
        self.move(dt)
        self.constraint()


class Laser(Sprite):
    def __init__(self, texture, pos):
        super().__init__(texture, pos, Vector2(0, -1), LASER_SPEED)

    def update(self, dt):
        self.move(dt)
        self.check_discard()
