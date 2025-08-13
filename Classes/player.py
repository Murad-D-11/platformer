import pygame
from Classes.spritesheet import Spritesheet

class Player(pygame.sprite.Sprite):
    def __init__(self, game):
        pygame.sprite.Sprite.__init__(self)

        self.game = game

        # Sound
        self.death_sfx = self.game.death_sfx
        self.jump_sfx = self.game.jump_sfx
        self.win_sfx = self.game.win_sfx

        self.image = Spritesheet('sprite_sheet.png').parse_sprite('player.png')
        self.rect = self.image.get_rect()
        self.rect.width -= 4
        self.rect.height -= 4
        self.LEFT_KEY, self.RIGHT_KEY, self.FACING_LEFT = False, False, False
        self.is_jumping, self.on_ground, self.can_midair_jump = False, False, False
        self.last_jump_orb = None
        self.on_ladder = False
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
        self.death_sfx.play()

        self.position.x = self.start_x
        self.position.y = self.start_y
        self.velocity = pygame.math.Vector2(0, 0)
        self.rect.x = self.start_x
        self.rect.bottom = self.start_y

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

    def update(self, dt, tiles):
        self.on_ladder = False

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
        self.limit_velocity(4)
        self.position.x += self.velocity.x * dt + (self.acceleration.x * 0.5) * (dt * dt)
        self.rect.x = self.position.x

    def vertical_movement(self, dt):
        self.velocity.y += self.acceleration.y * dt
        if self.velocity.y > 12: self.velocity.y = 12 # Limits vertical velocity
        self.position.y += self.velocity.y * dt + (self.acceleration.y * 0.5) * (dt * dt)
        self.rect.bottom = self.position.y

    # Limits horizontal velocity
    def limit_velocity(self, max_vel):
        self.velocity.x = max(-max_vel, min(self.velocity.x, max_vel))
        if abs(self.velocity.x) < .01: self.velocity.x = 0

    def jump(self, initial):
        if self.on_ground or self.can_midair_jump:
            self.jump_sfx.play()

            self.velocity.y = 0
            self.is_jumping = True
            self.velocity.y -= initial # Starting velocity
            self.on_ground, self.can_midair_jump = False, False

    # Register any contact with any object
    def get_hits(self, tiles):
        hits = []
        
        for entry in tiles:
            tile = entry.get('data')
            tile_id = entry.get('id')

            if tile_id == 10:  # Special case: spike
                if hasattr(tile, 'hitbox') and self.rect.colliderect(tile.hitbox):
                    hits.append(tile)
            else: # Any other solid tile
                if self.rect.colliderect(tile.rect):
                    hits.append(tile)

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
                        elif entry.get('id') == 3:  # Fin tile
                            self.win_sfx.play()
                            self.game.handle_level_completion()
                        elif entry.get('id') == 5: # Ladder
                            self.on_ladder = True
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
                        elif entry.get('id') == 5: # Ladder
                            self.on_ladder = True

                            if self.velocity.y > 0:
                                # Standing on top of ladder tile (existing check)
                                if self.rect.bottom <= tile.rect.top + 10:
                                    self.on_ground = True
                                    self.is_jumping = False
                                    self.velocity.y = 0
                                    self.position.y = tile.rect.top
                                    self.rect.bottom = self.position.y

                                # NEW: Standing on bottom of ladder tile
                                elif abs(self.rect.bottom - tile.rect.bottom) <= 10:
                                    self.on_ground = True
                                    self.is_jumping = False
                                    self.velocity.y = 0
                                    self.position.y = tile.rect.bottom
                                    self.rect.bottom = self.position.y
