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
from Classes.player import Player
from Classes.spritesheet import Spritesheet
from Classes.tiles import *

# ----------------- Variables and Constants ----------------- #

MUSIC_FOLDER = 'Music'
SONG_END = pygame.USEREVENT + 1
WHITE = (255, 255, 255)
TARGET_FPS = 60

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

# ------------------------ Functions ------------------------ #

# ----------------------------------------------------------- #

# Screen remains open
while running:
    # Remove trail
    screen.fill(WHITE)

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
                player.jump(7)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                player.LEFT_KEY = False
            elif event.key == pygame.K_d:
                player.RIGHT_KEY = False
            elif event.key == pygame.K_w:
                if player.is_jumping:
                    # player.velocity.y *= 0.25
                    player.is_jumping = False

        # Starts new song
        elif event.type == SONG_END:
            current_song_index += 1
            if current_song_index < len(music_files):
                pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[current_song_index]))
                pygame.mixer.music.play()
            else: # Loops
                current_song_index = 0
                random.shuffle(music_files)
                pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[current_song_index]))
                pygame.mixer.music.play()


    # Resets player if out of bounds
    if player.rect.y > 384:
        player.reset_position()

    # Update player
    player.update(dt, map.tiles)

    # Update map
    map.draw_map(screen)
    player.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
