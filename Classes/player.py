import pygame
from Classes.spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.image = Spritesheet('sprite_sheet.png').parse_sprite('player_right.png')
        self.rect = self.image.get_rect()
        self.rect.width -= 4
        self.rect.height -= 4
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground, self.can_midair_jump = False, False, False
        self.last_jump_orb = None
        self.gravity, self.friction =  0.35, -0.15
        self.position, self.velocity = pygame.math.Vector2(0, 0), pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)
        self.start_x = 0
        self.start_y = 0

    def set_start_position(self, x, y):
        self.start_x = x
        self.start_y = y
        self.position.x = x
        self.position.y = y
        self.rect.x = x
        self.rect.bottom = y

    def reset_position(self):
        self.position.x = self.start_x
        self.position.y = self.start_y
        self.velocity = pygame.math.Vector2(0, 0)
        self.rect.x = self.start_x
        self.rect.bottom = self.start_y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt, tiles):
        self.horizontal_movement(dt)
        self.check_collisions_x(tiles)

        self.vertical_movement(dt)
        self.check_collisions_y(tiles)

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
        self.rect.bottom = self.position.y

    # Limits horizontal velocity
    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def jump(self, initial):
        if self.on_ground or self.can_midair_jump:
            self.velocity.y = 0
            self.is_jumping = True
            self.velocity.y -= initial # Starting velocity
            self.on_ground, self.can_midair_jump = False, False

    def get_hits(self, tiles):
        hits = []
        
        for entry in tiles:
            if self.rect.colliderect(entry.get('data')):
                hits.append(entry.get('data'))

        return hits
    
    def check_collisions_x(self, tiles):
        collisions = self.get_hits(tiles)
        
        for tile in collisions:
            for entry in tiles:
                for key, value in entry.items():
                    if value == tile:
                        if entry.get('id') == 1 or entry.get('id') == 6 or entry.get('id') == 7: # Check if solid
                            if self.velocity.x > 0:
                                self.position.x = tile.rect.left - self.rect.w # X position is set to player's left side
                                self.rect.x = self.position.x # Syncs player's position to player's hitbox
                            elif self.velocity.x < 0:
                                self.position.x = tile.rect.right
                                self.rect.x = self.position.x
                        elif entry.get('id') == 0: # Batoude
                            self.jump(10)
                        elif entry.get('id') == 10: # Spike
                            self.reset_position()

        # Player cannot leave the screen's definitive boundaries
        if self.rect.x > (512 - self.rect.width):
            self.position.x = self.rect.x
            self.rect.x = 512 - self.rect.width
            self.velocity.x = 0
        elif self.rect.x < 0:
            self.position.x = self.rect.x
            self.rect.x = 0
            self.velocity.x = 0

    def check_collisions_y(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1 # Move hitbox by one pixel down
        collisions = self.get_hits(tiles)

        # Reset jump orb if player is no longer touching it
        if self.last_jump_orb and self.last_jump_orb not in collisions:
            self.last_jump_orb = None

        for tile in collisions:
            for entry in tiles:
                for key, value in entry.items():
                    if value == tile:
                        if entry.get('id') == 1 or entry.get('id') == 6 or entry.get('id') == 7: # Check if solid
                            if self.velocity.y > 0: # Hit tile from the top
                                self.on_ground = True
                                self.is_jumping = False
                                self.velocity.y = 0
                                self.position.y = tile.rect.top
                                self.rect.bottom = self.position.y

                                # !!! Test-code that works !!!
                                # for entry in tiles:
                                #     for key, value in entry.items():
                                #         if value == tile:
                                #             if entry.get('id') == 1:
                                #                 print("explosion")

                            elif self.velocity.y < 0: # Hit tile from the bottom
                                self.velocity.y = 0
                                self.position.y = tile.rect.bottom + self.rect.h
                                self.rect.bottom = self.position.y
                        elif entry.get('id') == 4:  # Touching Jump Orb
                            if self.last_jump_orb != tile:
                                self.can_midair_jump = True
                                self.last_jump_orb = tile
