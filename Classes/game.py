import pygame, random, os

from Classes.menu import *
from Classes.spritesheet import *

class Game():
    def __init__(self, player, spritesheet, map, clock):
        pygame.init()

        self.current_level = 0
        self.levels = {}

        # Pause
        self.walk_timer = 0
        self.walk_frame_duration = 2500  # milliseconds between frames
        self.current_walk_frame = 0

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

        # Sound
        self.death_sfx = pygame.mixer.Sound('Sounds/death.wav')
        self.jump_sfx = pygame.mixer.Sound('Sounds/jump.wav')
        self.win_sfx = pygame.mixer.Sound('Sounds/win.wav')
        self.scroll_sfx = pygame.mixer.Sound('Sounds/scroll.wav')
        self.select_sfx = pygame.mixer.Sound('Sounds/select.wav')
        self.sound_effects = [self.death_sfx, self.jump_sfx, self.win_sfx, self.scroll_sfx, self.select_sfx]

        # Volume
        self.music_volume = 0.5
        self.sound_volume = 0.5
        pygame.mixer.music.set_volume(self.music_volume)
        for sfx in self.sound_effects:
            sfx.set_volume(self.sound_volume)

        # Booleans
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.START_KEY, self.BACK_KEY= False, False, False, False
        self.facing_right = True
        
        # Display
        self.DISPLAY_W, self.DISPLAY_H = 512, 384
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        
        # GUI
        self.font_name = 'Fonts/8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
        
        # Menus
        self.main_menu = MainMenu(self)
        self.levels_menu = LevelsMenu(self)
        self.volume_menu = VolumeMenu(self)
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

            self.display.fill((0, 76, 153))

            # Delta-time coefficient
            dt = self.clock.tick(60) * 0.001 * self.TARGET_FPS

            # Sprite fliping
            if self.player.velocity.y < 0: 
                if self.facing_right:
                    self.player.image = Spritesheet('sprite_sheet.png').parse_sprite('player_jump.png')
                else:
                    self.player.image = pygame.transform.flip(Spritesheet('sprite_sheet.png').parse_sprite('player_jump.png'), True, False)
            elif self.player.velocity.y > 0:
                if self.facing_right:
                    self.player.image = Spritesheet('sprite_sheet.png').parse_sprite('player_fall.png')
                else:
                    self.player.image = pygame.transform.flip(Spritesheet('sprite_sheet.png').parse_sprite('player_fall.png'), True, False)
            elif self.player.velocity.y == 0:
                if self.player.velocity.x == 0:
                    if self.facing_right:
                        self.player.image = Spritesheet('sprite_sheet.png').parse_sprite('player.png')
                    else:
                        self.player.image = pygame.transform.flip(Spritesheet('sprite_sheet.png').parse_sprite('player.png'), True, False)
                else:
                    if self.facing_right:
                        self.walk_timer += dt * 1000  # convert dt to milliseconds
                        if self.walk_timer >= self.walk_frame_duration:
                            self.walk_timer = 0
                            self.current_walk_frame = (self.current_walk_frame + 1) % 2

                        if self.current_walk_frame == 0:
                            self.player.image = Spritesheet('sprite_sheet.png').parse_sprite('player_walk1.png')
                        else:
                            self.player.image = Spritesheet('sprite_sheet.png').parse_sprite('player_walk2.png')
                    else:
                        self.walk_timer += dt * 1000  # convert dt to milliseconds
                        if self.walk_timer >= self.walk_frame_duration:
                            self.walk_timer = 0
                            self.current_walk_frame = (self.current_walk_frame + 1) % 2

                        if self.current_walk_frame == 0:
                            self.player.image = pygame.transform.flip(Spritesheet('sprite_sheet.png').parse_sprite('player_walk1.png'), True, False)
                        else:
                            self.player.image = pygame.transform.flip(Spritesheet('sprite_sheet.png').parse_sprite('player_walk2.png'), True, False)

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
                        self.facing_right = False
                        self.player.LEFT_KEY = True
                    elif event.key == pygame.K_d:
                        self.facing_right = True
                        self.player.RIGHT_KEY = True
                    elif event.key == pygame.K_w:
                        self.player.jump(7.3)
                    elif event.key == pygame.K_s and self.player.on_ladder: # descending ladder
                        self.player.position.y += 32
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
                        self.select_sfx.play()
                        self.BACK_KEY = False
            else: # menu
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_w:
                        self.scroll_sfx.play()
                        self.UP_KEY = True
                    elif event.key == pygame.K_s:
                        self.scroll_sfx.play()
                        self.DOWN_KEY = True
                    elif event.key == pygame.K_RETURN:
                        self.select_sfx.play()
                        self.START_KEY = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.select_sfx.play()
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

    def handle_level_completion(self):
        if self.current_level < 5:
            self.current_level += 1
            selected_map = self.levels[self.current_level]  # from main.py
            self.map = selected_map
            self.player.set_start_position(selected_map.start_x, selected_map.start_y)
        # else:
        #     self.playing = False
        #     self.current_menu = VictoryMenu(self)  # Placeholder menu

    def music_mixer(self):
        # Initialize mixer
        pygame.mixer.init()
        pygame.mixer.music.set_endevent(self.SONG_END)

        # Shuffle music
        random.shuffle(self.music_files)

        # Music state
        pygame.mixer.music.load(os.path.join(self.MUSIC_FOLDER, self.music_files[self.current_song_index]))
        pygame.mixer.music.play()
    
