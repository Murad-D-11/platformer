import pygame
from Classes.menu import *

class Game():
    def __init__(self):
        pygame.init()
        self.running, self.playing = True, False
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False
        self.DISPLAY_W, self.DISPLAY_H = 512, 384
        self.display = pygame.Surface((self.DISPLAY_W, self.DISPLAY_H))
        self.window = pygame.display.set_mode((self.DISPLAY_W, self.DISPLAY_H))
        self.font_name = 'Fonts/8-BIT WONDER.TTF'
        self.BLACK, self.WHITE = (0, 0, 0), (255, 255, 255)
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

            self.display.fill(self.BLACK)
            
            # ----------------------------- Game ----------------------------- #

            # # Remove trail
            # screen.fill(WHITE)

            # # Delta-time coefficient
            # dt = clock.tick(60) * 0.001 * TARGET_FPS

            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         running = False

            #     # Keyboard event listener
            #     if event.type == pygame.KEYDOWN:
            #         if event.key == pygame.K_a:
            #             player.image = Spritesheet('sprite_sheet.png').parse_sprite('player_left.png')
            #             player.LEFT_KEY = True
            #         elif event.key == pygame.K_d:
            #             player.image = Spritesheet('sprite_sheet.png').parse_sprite('player_right.png')
            #             player.RIGHT_KEY = True
            #         elif event.key == pygame.K_w:
            #             player.jump(7)

            #     if event.type == pygame.KEYUP:
            #         if event.key == pygame.K_a:
            #             player.LEFT_KEY = False
            #         elif event.key == pygame.K_d:
            #             player.RIGHT_KEY = False
            #         elif event.key == pygame.K_w:
            #             if player.is_jumping:
            #                 # player.velocity.y *= 0.25
            #                 player.is_jumping = False

            #     # Starts new song
            #     elif event.type == SONG_END:
            #         current_song_index += 1
            #         if current_song_index < len(music_files):
            #             pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[current_song_index]))
            #             pygame.mixer.music.play()
            #         else: # Loops
            #             current_song_index = 0
            #             random.shuffle(music_files)
            #             pygame.mixer.music.load(os.path.join(MUSIC_FOLDER, music_files[current_song_index]))
            #             pygame.mixer.music.play()


            # # Resets player if out of bounds
            # if player.rect.y > 384:
            #     player.reset_position()

            # # Update player
            # player.update(dt, map.tiles)

            # # Update map
            # map.draw_map(screen)
            # player.draw(screen)

            # pygame.display.flip()
            # clock.tick(60)

            # ---------------------------------------------------------------- #

            self.window.blit(self.display, (0, 0))
            pygame.display.update()

    def reset_keys(self):
        self.UP_KEY, self.DOWN_KEY, self.LEFT_KEY, self.RIGHT_KEY, self.START_KEY, self.BACK_KEY = False, False, False, False, False, False

    def check_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # quit
                self.running, self.playing = False, False
                self.current_menu.run_display = False

            if self.playing: # game
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_a:
                        self.LEFT_KEY = True
                    elif event.key == pygame.K_d:
                        self.RIGHT_KEY = True
                    elif event.key == pygame.K_w:
                        self.UP_KEY = True
                    elif event.key == pygame.K_BACKSPACE:
                        self.BACK_KEY = True

                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_a:
                        self.LEFT_KEY = False
                    elif event.key == pygame.K_d:
                        self.RIGHT_KEY = False
                    elif event.key == pygame.K_w:
                        self.UP_KEY = False
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
                        self.START_KEY == False
                    elif event.key == pygame.K_BACKSPACE:
                        self.BACK_KEY = False
    
    def draw_text(self, text, size, x, y):
        font = pygame.font.Font(self.font_name, size)
        text_surface = font.render(text, True, self.WHITE)
        text_rect = text_surface.get_rect()
        text_rect.center = (x, y)
        self.display.blit(text_surface, text_rect)
    