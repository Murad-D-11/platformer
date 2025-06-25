import pygame
from Classes.player import Player

# Variables and Constants
running = True
movement = None
WHITE = (255, 255, 255)
x = 1152 / 2
y = 864 / 2

# Screen Setup
pygame.init()
screen = pygame.display.set_mode(size=(1152, 864), vsync=1)

# Other Objects Setup
clock = pygame.time.Clock()
player = Player(screen, WHITE, x, y, 20, 20)

# Screen remains open
while running:
    screen.fill((0, 0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                movement = "left"
            if event.key == pygame.K_d:
                movement = "right"
            if event.key == pygame.K_w:
                movement = "up"

        elif event.type == pygame.KEYUP:
            if event.key in [pygame.K_a, pygame.K_d, pygame.K_w]:
                movement = None

    if movement == "left":
        x -= 1
    if movement == "right":
        x += 1
    if movement == "up":
        y -= 1

    player.move(x, y)

    pygame.display.flip()
    clock.tick(144)

pygame.quit()
