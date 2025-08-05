import pygame
import random
import os

from Classes.menu import *
from Classes.spritesheet import *

class Game():
    def __init__(self, player, spritesheet, map, clock):
        pygame.init()

        # Objects
        self.player = player
        self.spritesheet = spritesheet
        self.map = map
        self.clock = clock

        # Delta-time
        self.TARGET_FPS = 60

        # Music
        self.MUSIC_FOLDER = 'Music'
        self.music_files = [file for file in os.listdir(self.MUSIC_FOLDER) if file.endswith(('.mp3', '.ogg', '.wav'))]
        self.SONG_END = pygame.USEREVENT + 1
        self.current_song_index = 0

        # Booleans
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False
        
        # Display
        self.DISPLAY_W, self.DISPLAY_H = 512, 384
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        
        # GUI
        self.font_name = 'Fonts/8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        
        # Menus
        self.main_menu = MainMenu(self)
        self.options_menu = OptionsMenu(self)
        self.credits_menu = CreditsMenu(self)
        self.current_menu = self.main_menu

    def game_loop(self):
        while self.playing:
            self.check_events()

            if self.START_KEY:
                self.playing = False
            elif self.BACK_KEY:
                self.playing = False
                self.current_menu = self.main_menu
                break

            self.display.fill(self.WHITE)

            # Delta-time coefficient
            dt = self.clock.tick(60) * 0.001 * self.TARGET_FPS
                        
            # Resets player if out of bounds
            if self.player.rect.y > 384:
                self.player.reset_position()

            # Update player
            self.player.update(dt, self.map.tiles)

            # Update map
            self.map.draw_map(self.display)
            self.player.draw(self.display)

            self.window.blit(self.display, (0, 0))
            pygame.display.flip()
            self.clock.tick(60)

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False,

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit
                self.running, self.playing = False, False
                self.current_menu.run_display = False

            # Starts new song
            elif event.type == self.SONG_END:
                self.current_song_index += 1
                if self.current_song_index < len(self.music_files):
                    pygame.mixer.music.load(os.path.join(self.MUSIC_FOLDER, self.music_files[self.current_song_index]))
                    pygame.mixer.music.play()
                else: # Loops
                    self.current_song_index = 0
                    random.shuffle(self.music_files)
                    pygame.mixer.music.load(os.path.join(self.MUSIC_FOLDER, self.music_files[self.current_song_index]))
                    pygame.mixer.music.play()

            elif self.playing: # game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.player.image = Spritesheet('sprite_sheet.png').parse_sprite('player_left.png')
                        self.player.LEFT_KEY = True
                    elif event.key == pygame.K_d:
                        self.player.image = Spritesheet('sprite_sheet.png').parse_sprite('player_right.png')
                        self.player.RIGHT_KEY = True
                    elif event.key == pygame.K_w:
                        self.player.jump(7)
                    elif event.key == pygame.K_BACKSPACE:
                        self.BACK_KEY = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.player.LEFT_KEY = False
                    elif event.key == pygame.K_d:
                        self.player.RIGHT_KEY = False
                    elif event.key == pygame.K_w:
                        if self.player.is_jumping:
                            # player.velocity.y *= 0.25
                            self.player.is_jumping = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.BACK_KEY = False
            else: # menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.UP_KEY = True
                    elif event.key == pygame.K_s:
                        self.DOWN_KEY = True
                    elif event.key == pygame.K_RETURN:
                        self.START_KEY = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.BACK_KEY = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_w:
                        self.UP_KEY = False
                    elif event.key == pygame.K_s:
                        self.DOWN_KEY = False
                    elif event.key == pygame.K_RETURN:
                        self.START_KEY = False
                    elif event.key == pygame.K_BACKSPACE:
                        self.BACK_KEY = False
    
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)

    def music_mixer(self):
        # Initialize mixer
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(self.SONG_END)

        # Shuffle music
        random.shuffle(self.music_files)

        # Music state
        pygame.mixer.music.load(os.path.join(self.MUSIC_FOLDER, self.music_files[self.current_song_index]))
        pygame.mixer.music.play()
    
