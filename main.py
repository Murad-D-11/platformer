import pygame

from Classes.player import Player
from Classes.solid import Solid

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
x, y = (1152 / 2), (864 / 2)

# ----------------------------------------------------------- #

# Screen Setup
pygame.init()
screen = pygame.display.set_mode(size=(1152, 864), vsync=1)

# Other Objects Setup
clock = pygame.time.Clock()
player = Player(screen, WHITE, x, y, 20, 20)

# Screen remains open
while running:
    screen.fill((0, 0, 0))

    playerHitbox = pygame.Rect(x, y, 20, 20)
    surfaceHitbox = pygame.Rect(426, 452, 300, 20)
    
    collision = playerHitbox.colliderect(surfaceHitbox)

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

    player.move(x, y)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
