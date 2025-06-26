import pygame

class Player:
    def __init__(self, surface, colour, h, v, width, height):
        self.surface = surface
        self.colour = colour
        self.width = width
        self.height = height

    def move(self, x, y):
        pygame.draw.rect(self.surface, self.colour, (x, y, self.width, self.height))
