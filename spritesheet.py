import pygame
import json

class Spritesheet:
    def __init__(self, filename):
        self.filename = filename
        self.sprite_sheet = pygame.image.load(filename).convert()
        self.meta_data = self.filename.replace('png', 'json')

        # Reads .json file
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

        # Appends all values of key "fileName"
        self.sprite_lookup = {sprite["fileName"]: sprite for sprite in self.data["sprites"]}

    # Gets a hold of the chosen sprite
    def get_sprite(self, x, y, w, h):
        sprite = pygame.Surface((w, h))
        sprite.set_colorkey((0, 0, 0))
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, w, h))
        return sprite
    
    def parse_sprite(self, name):
        if name not in self.sprite_lookup:
            raise ValueError(f"Sprite with name '{name}' not found.")
    
        # Collects the dimensions of the chosen sprite
        sprite = self.sprite_lookup[name]
        x, y, w, h = sprite["x"], sprite["y"], sprite["width"], sprite["height"]

        # Returns the chosen sprite
        image = self.get_sprite(x, y, w, h)
        return image
