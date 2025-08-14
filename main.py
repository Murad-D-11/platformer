# External imports
import pygame

# Internal class imports
from Classes.game import Game
from Classes.player import Player
from Classes.spritesheet import Spritesheet
from Classes.tiles import *

pygame.init()

clock = pygame.time.Clock()

icon = pygame.image.load('Images/icon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption("Robo Trial: 8-Bit Chambers!")

g = Game(None, None, None, clock)

# Load player and spritesheet
spritesheet = Spritesheet('sprite_sheet.png')
player = Player(g)

# Maps dictionary for quick access
levels = {
    1: TileMap('Maps/level_1.csv', spritesheet),
    2: TileMap('Maps/level_2.csv', spritesheet),
    3: TileMap('Maps/level_3.csv', spritesheet),
    4: TileMap('Maps/level_4.csv', spritesheet),
    5: TileMap('Maps/level_5.csv', spritesheet),
}

g.player = player
g.levels = levels
g.spritesheet = spritesheet

g.music_mixer()

while g.running:
    g.current_menu.display_menu()

    if g.playing:  # means a level was selected
        selected_map = levels[g.current_level]
        g.map = selected_map
        g.player.set_start_position(selected_map.start_x, selected_map.start_y)

        g.game_loop()

pygame.quit()
