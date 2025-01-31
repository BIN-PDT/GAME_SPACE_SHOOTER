from settings import *


class Sprite:
    def __init__(self, texture, pos, direction, speed):
        self.texture = texture
        self.size = Vector2(texture.width, texture.height)
        # MOVEMENT.
        self.pos = pos
        self.direction = direction
        self.SPEED = speed
        self.discard = False
        # COLLISION.
        self.COLLISION_RADIUS = self.size.y / 2

    def get_center_pos(self):
        return Vector2(self.pos.x + self.size.x / 2, self.pos.y + self.size.y / 2)

    def get_rectangle(self):
        return Rectangle(self.pos.x, self.pos.y, self.size.x, self.size.y)

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


class Meteor(Sprite):
    def __init__(self, texture):
        pos = Vector2(randint(0, WINDOW_WIDTH), randint(-150, -50))
        direction = Vector2(uniform(-0.5, 0.5), 1)
        speed = randint(*METEOR_SPEED_RANGE)
        super().__init__(texture, pos, direction, speed)
        # ROTATION.
        self.rotation = 0
        self.center_pos = Vector2(self.size.x / 2, self.size.y / 2)
        self.source_rect = Rectangle(0, 0, self.size.x, self.size.y)
        self.target_rect = Rectangle(self.pos.x, self.pos.y, self.size.x, self.size.y)

    def rotate(self, dt):
        self.rotation += 60 * dt
        self.target_rect.x = self.pos.x
        self.target_rect.y = self.pos.y

    def get_center_pos(self):
        return self.pos

    def update(self, dt):
        self.move(dt)
        self.rotate(dt)
        self.check_discard()

    def draw(self):
        draw_texture_pro(
            self.texture,
            self.source_rect,
            self.target_rect,
            self.center_pos,
            self.rotation,
            WHITE,
        )


class ExplosionAnimation:
    def __init__(self, textures, pos):
        self.textures = textures
        self.size = Vector2(textures[0].width, textures[1].height)
        self.pos = Vector2(pos.x - self.size.x / 2, pos.y - self.size.y / 2)
        self.discard = False
        self.index = 0

    def update(self, dt):
        if self.index < len(self.textures) - 1:
            self.index += 20 * dt
        else:
            self.discard = True

    def draw(self):
        draw_texture_v(self.textures[int(self.index)], self.pos, WHITE)
