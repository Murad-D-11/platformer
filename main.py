# External imports
import pygame

# Internal class imports
from Classes.player import Player
from Classes.spritesheet import Spritesheet
from Classes.tiles import *

# ----------------- Variables and Constants ----------------- #

# Colours
WHITE = (255, 255, 255)

# Delta-time
TARGET_FPS = 60

# Booleans
running = True

# ----------------------------------------------------------- #

# Screen Setup
pygame.init()
screen = pygame.display.set_mode(size=(512, 384), vsync=1)

# Other Objects Setup
clock = pygame.time.Clock()

# Load player and spritesheet
spritesheet = Spritesheet('sprite_sheet.png')
player = Player()

# Loads and sets up the map
map = TileMap('Maps/level_test.csv', spritesheet)
player.position.x, player.position.y = map.start_x, map.start_y

# Screen remains open
while running:
    screen.fill((0, 0, 0))

    # Delta-time coefficient
    dt = clock.tick(60) * 0.001 * TARGET_FPS

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Keyboard event listener
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                player.image = Spritesheet('sprite_sheet.png').parse_sprite('player_left.png')
                player.LEFT_KEY = True
            elif event.key == pygame.K_d:
                player.image = Spritesheet('sprite_sheet.png').parse_sprite('player_right.png')
                player.RIGHT_KEY = True
            elif event.key == pygame.K_w:
                player.jump()

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.LEFT_KEY = False
            elif event.key == pygame.K_d:
                player.RIGHT_KEY = False
            elif event.key == pygame.K_w:
                if player.is_jumping:
                    # player.velocity.y *= 0.25
                    player.is_jumping = False

    # Update player
    player.update(dt, map.tiles)

    # Update map
    map.draw_map(screen)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
