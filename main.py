# TO-DO List:
# Make the "Fin" tile operational
# Add a bunch of other fun quirks
# Create a menu and other GUI crap

# External imports
import pygame

# Internal class imports
from Classes.game import Game
from Classes.player import Player
from Classes.spritesheet import Spritesheet
from Classes.tiles import *

pygame.init()

# Other Objects Setup
clock = pygame.time.Clock()

g = Game(None, None, None, clock)

# Load player and spritesheet
spritesheet = Spritesheet('sprite_sheet.png')
player = Player()

# Loads and sets up the map (for debugging purposes)
map = TileMap('Maps/level_test.csv', spritesheet)
player.set_start_position(map.start_x, map.start_y)

g.player = player
g.spritesheet = spritesheet
g.map = map

g.music_mixer()

while g.running:
    g.current_menu.display_menu()
    g.game_loop()

pygame.quit()
