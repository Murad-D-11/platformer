# TO-DO List:
# Create multiple levels
# Make the "Fin" tile operational
# Add a bunch of other fun quirks
# Create a menu and other GUI crap

# External imports
import pygame
import random
import os

# Internal class imports
from Classes.game import Game
from Classes.player import Player
from Classes.spritesheet import Spritesheet
from Classes.tiles import *

# ----------------- Variables and Constants ----------------- #

MUSIC_FOLDER = 'Music'
SONG_END = pygame.USEREVENT + 1

TARGET_FPS = 60

# ----------------------------------------------------------- #

g = Game()

# Screen Setup
pygame.init()
screen = pygame.display.set_mode(size=(512, 384), vsync=1)
display = pygame.Surface((512, 384))

# Other Objects Setup
clock = pygame.time.Clock()

# Load player and spritesheet
spritesheet = Spritesheet('sprite_sheet.png')
player = Player()

# Loads and sets up the map
map = TileMap('Maps/level_test.csv', spritesheet)
player.set_start_position(map.start_x, map.start_y)

# Initialize mixer
pygame.mixer.init()
pygame.mixer.music.set_endevent(SONG_END)

# Shuffle music
music_files = [file for file in os.listdir(MUSIC_FOLDER) if file.endswith(('.mp3', '.ogg', '.wav'))]
random.shuffle(music_files)

# Music state
current_song_index = 0
pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[current_song_index]))
pygame.mixer.music.play()

# Screen remains open
while g.running:
    g.current_menu.display_menu()
    g.game_loop()

pygame.quit()
