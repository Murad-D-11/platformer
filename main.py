# External imports
import pygame

# Internal class imports
from Classes.player import Player
from Classes.solid import Solid
from Classes.spritesheet import Spritesheet
from Classes.tiles import *

# ----------------- Variables and Constants ----------------- #

# Colours
WHITE = (255, 255, 255)

# Jump logic
GRAVITY = 1
JUMP_HEIGHT = 10
Y_VELOCITY = JUMP_HEIGHT

# Booleans
running = True
jumping = False

# Starting coordinates
x, y = (512 / 2), (272 / 2)

# ----------------------------------------------------------- #

# Screen Setup
pygame.init()
screen = pygame.display.set_mode(size=(512, 272), vsync=1)

# Other Objects Setup
clock = pygame.time.Clock()
player = Player(screen, WHITE, x, y, 16, 16)

# Load player and spritesheet
spritesheet = Spritesheet('sprite_sheet.png')
player_img = spritesheet.parse_sprite('player.png')
player_rect = player_img.get_rect()

# Loads and sets up the map
map = TileMap('Maps/level_test.csv', spritesheet)
player_rect.x, player_rect.y = map.start_x, map.start_y

# Screen remains open
while running:
    screen.fill((0, 0, 0))

    # Collision logic
    player_hitbox = pygame.Rect(x, y, 16, 16)
    surface_hitbox = pygame.Rect(256, 176, 300, 20)
    collision = player_hitbox.colliderect(surface_hitbox)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Keyboard event listener
    keys = pygame.key.get_pressed()
    if keys[pygame.K_a]:
        x -= 5
    if keys[pygame.K_d]:
        x += 5
    if keys[pygame.K_w]:
        jumping = True

    # Jumping/falling logic
    if jumping:
        y -= Y_VELOCITY
        Y_VELOCITY -= GRAVITY

        if Y_VELOCITY < -JUMP_HEIGHT:
            jumping = False
            Y_VELOCITY = JUMP_HEIGHT
    elif collision == False:
        y += Y_VELOCITY
        Y_VELOCITY += GRAVITY

    # Update player
    player.move(x, y)
    screen.blit(player_img, (map.start_x, map.start_y))

    # Update map
    map.draw_map(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
