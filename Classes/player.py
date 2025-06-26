import pygame
from Classes.spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('sprite_sheet.png').parse_sprite('player_right.png')
        self.rect = self.image.get_rect()
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground = False, False
        self.gravity, self.friction =  0.35, -0.15
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt):
        self.horizontal_movement(dt)
        self.vertical_movement(dt)

    def horizontal_movement(self, dt):
        self.acceleration.x = 0

        # Acceleration
        if self.LEFT_KEY:
            self.acceleration.x -= 1
        elif self.RIGHT_KEY:
            self.acceleration.x += 1

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * dt
        self.limit_velocity(5)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 7: self.velocity.y = 7 # Limits vertical velocity
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)

        # Always lands on y = 128
        if self.position.y > 128:
            self.on_ground = True
            self.velocity.y = 0
            self.position.y = 128

        self.rect.bottom = self.position.y

    # Limits horizontal velocity
    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.is_jumping = True
            self.velocity.y -= 8 # Starting velocity
            self.on_ground = False
