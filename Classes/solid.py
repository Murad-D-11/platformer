# TO-DO: create a separate hitbox for every solid created

import pygame

class Solid:
    def __init__(self, surface, colour, h, v, width, height):
        self.surface = surface
        self.colour = colour
        self.width = width
        self.height = height
