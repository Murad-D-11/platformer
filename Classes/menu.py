import pygame, colorsys

class Menu():
    def __init__(self, game):
        self.game = game
        self.mid_w, self.mid_h = self.game.DISPLAY_W / 2, self.game.DISPLAY_H / 2
        self.run_display = True
        self.cursor_rect = pygame.Rect(0, 0, 20, 20)
        self.offset = -100

    def draw_cursor(self):
        self.game.draw_text("*", 15, self.cursor_rect.x, self.cursor_rect.y)

    def blit_screen(self): # updates screen
        self.game.window.blit(self.game.display, (0, 0))
        pygame.display.update()
        self.game.reset_keys()
    
class MainMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.state = 'Levels'
        
        self.levelsx, self.levelsy = self.mid_w, self.mid_h + 30
        self.volumex, self.volumey = self.mid_w, self.mid_h + 50
        self.creditsx, self.creditsy = self.mid_w, self.mid_h + 70
        self.cursor_rect.midtop = (self.levelsx + self.offset, self.levelsy)

        self.icon = pygame.image.load('Images/icon.png')
        self.tab = pygame.image.load('Images/tab.png')

        # Title flash timer
        self.title_colour_timer = 0
        self.title_colour_state = True # True = colour1, False = colour2

        # Colors (you can change these)
        self.colour1 = (40, 86, 17) # Dark Grey
        self.colour2 = (40, 40, 40) # Grey

    def display_menu(self):
        self.run_display = True
        clock = pygame.time.Clock()

        while self.run_display:
            self.game.check_events()
            self.check_input()

            # Update timer
            self.title_colour_timer += clock.get_time()
            if self.title_colour_timer > 500: # Switch every 0.5s
                self.title_colour_state = not self.title_colour_state
                self.title_colour_timer = 0

            # 8 Bit Chambers colour
            chambers_colour = self.colour1 if self.title_colour_state else self.colour2

            # Robo Trials opposite colour
            robo_colour = self.colour2 if self.title_colour_state else self.colour1

            self.game.display.fill(self.game.BLACK)
            self.game.display.blit(self.tab, (self.mid_w - 144, self.mid_h - 170))
            self.game.display.blit(self.icon, (45, 30))

            # Draw titles with alternating colours
            self.game.draw_text("Robo Trials", 20, self.mid_w, self.mid_h - 130, robo_colour)
            self.game.draw_text("8 Bit Chambers", 20, self.mid_w, self.mid_h - 110, chambers_colour)

            # Rest of menu
            self.game.draw_text("Main Menu", 20, 512 / 2, 384 / 2 - 20)
            self.game.draw_text("Levels", 20, self.levelsx, self.levelsy)
            self.game.draw_text("Volume", 20, self.volumex, self.volumey)
            self.game.draw_text("Credits", 20, self.creditsx, self.creditsy)

            self.draw_cursor()
            self.blit_screen()
            clock.tick(60)

    def move_cursor(self):
        if self.game.DOWN_KEY: # down
            if self.state == 'Levels':
                self.cursor_rect.midtop = ((self.volumex + self.offset), self.volumey)
                self.state = 'Volume'
            elif self.state == 'Volume':
                self.cursor_rect.midtop = ((self.creditsx + self.offset), self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = ((self.levelsx + self.offset), self.levelsy)
                self.state = 'Levels'
        elif self.game.UP_KEY: # up
            if self.state == 'Levels':
                self.cursor_rect.midtop = ((self.creditsx + self.offset), self.creditsy)
                self.state = 'Credits'
            elif self.state == 'Volume':
                self.cursor_rect.midtop = ((self.levelsx + self.offset), self.levelsy)
                self.state = 'Levels'
            elif self.state == 'Credits':
                self.cursor_rect.midtop = ((self.volumex + self.offset), self.volumey)
                self.state = 'Volume'

    def check_input(self):
        self.move_cursor()

        if self.game.START_KEY:
            if self.state == 'Levels':
                self.game.current_menu = self.game.levels_menu
            elif self.state == 'Volume':
                self.game.current_menu = self.game.volume_menu
            elif self.state == 'Credits':
                self.game.current_menu = self.game.credits_menu

            self.run_display = False

class LevelsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Level 1'
        self.lvl1x, self.lvl1y = self.mid_w, self.mid_h + 20
        self.lvl2x, self.lvl2y = self.mid_w, self.mid_h + 40
        self.lvl3x, self.lvl3y = self.mid_w, self.mid_h + 60
        self.lvl4x, self.lvl4y = self.mid_w, self.mid_h + 80
        self.lvl5x, self.lvl5y = self.mid_w, self.mid_h + 100
        self.cursor_rect.midtop = (self.lvl1x + self.offset, self.lvl1y)

    def display_menu(self):
        self.run_display = True
        while self.run_display:
            self.game.check_events()
            self.check_input()
            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Levels', 20, self.mid_w, self.mid_h - 20)
            self.game.draw_text('Level 1', 15, self.lvl1x, self.lvl1y)
            self.game.draw_text('Level 2', 15, self.lvl2x, self.lvl2y)
            self.game.draw_text('Level 3', 15, self.lvl3x, self.lvl3y)
            self.game.draw_text('Level 4', 15, self.lvl4x, self.lvl4y)
            self.game.draw_text('Level 5', 15, self.lvl5x, self.lvl5y)
            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.current_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY:
            if self.state == 'Level 1':
                self.state = 'Level 2'
                self.cursor_rect.midtop = (self.lvl2x + self.offset, self.lvl2y)
            elif self.state == 'Level 2':
                self.state = 'Level 3'
                self.cursor_rect.midtop = (self.lvl3x + self.offset, self.lvl3y)
            elif self.state == 'Level 3':
                self.state = 'Level 4'
                self.cursor_rect.midtop = (self.lvl4x + self.offset, self.lvl4y)
            elif self.state == 'Level 4':
                self.state = 'Level 5'
                self.cursor_rect.midtop = (self.lvl5x + self.offset, self.lvl5y)
            elif self.state == 'Level 5':
                self.state = 'Level 1'
                self.cursor_rect.midtop = (self.lvl1x + self.offset, self.lvl1y)

        elif self.game.UP_KEY:
            if self.state == 'Level 1':
                self.state = 'Level 5'
                self.cursor_rect.midtop = (self.lvl5x + self.offset, self.lvl5y)
            elif self.state == 'Level 2':
                self.state = 'Level 1'
                self.cursor_rect.midtop = (self.lvl1x + self.offset, self.lvl1y)
            elif self.state == 'Level 3':
                self.state = 'Level 2'
                self.cursor_rect.midtop = (self.lvl2x + self.offset, self.lvl2y)
            elif self.state == 'Level 4':
                self.state = 'Level 3'
                self.cursor_rect.midtop = (self.lvl3x + self.offset, self.lvl3y)
            elif self.state == 'Level 5':
                self.state = 'Level 4'
                self.cursor_rect.midtop = (self.lvl4x + self.offset, self.lvl4y)

        elif self.game.START_KEY:
            self.game.playing = True
            self.game.current_level = int(self.state.split()[-1])
            self.run_display = False


class VolumeMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)
        self.state = 'Music'

        self.volumex, self.volumey = self.mid_w, self.mid_h - 60
        self.musicx, self.musicy = self.mid_w - 100, self.mid_h + 20
        self.soundx, self.soundy = self.mid_w - 100, self.mid_h + 60

        self.cursor_rect.midtop = (self.musicx + self.offset, self.musicy)

        self.sliders = [
            Slider(game, (self.musicx + 170, self.musicy), (150, 15), 0.5, 0, 100),
            Slider(game, (self.soundx + 170, self.soundy), (150, 15), 0.5, 0, 100)
        ]

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()

            self.game.display.fill(self.game.BLACK)

            mouse_pos = pygame.mouse.get_pos()
            mouse = pygame.mouse.get_pressed()

            # Draw title & labels
            self.game.draw_text('Volume', 20, self.volumex, self.volumey)
            self.game.draw_text('Music', 15, self.musicx, self.musicy)
            self.game.draw_text('Sound', 15, self.soundx, self.soundy)

            # Update sliders
            for i, slider in enumerate(self.sliders):
                if slider.container_rect.collidepoint(mouse_pos) and mouse[0]:
                    slider.move_slider(mouse_pos)
                    val = slider.get_value() / 100 # 0.0 to 1.0

                    if i == 0:  # Music slider
                        pygame.mixer.music.set_volume(val)
                        self.game.music_volume = val
                    elif i == 1:  # Sound slider
                        for sfx in self.game.sound_effects:
                            sfx.set_volume(val)
                        self.game.sound_volume = val

                slider.render()

            # Back key returns to main menu
            if self.game.BACK_KEY:
                self.game.current_menu = self.game.main_menu
                self.run_display = False

            self.blit_screen()

    # def check_input(self):
    #     if self.game.BACK_KEY:
    #         self.game.current_menu = self.game.main_menu
    #         self.run_display = False
    #     elif self.game.UP_KEY or self.game.DOWN_KEY:
    #         if self.state == 'Music':
    #             self.state = 'Sound'
    #             self.cursor_rect.midtop = (self.soundx + self.offset, self.soundy)
    #         elif self.state == 'Sound':
    #             self.state = 'Music'
    #             self.cursor_rect.midtop = (self.musicx + self.offset, self.musicy)
    #     elif self.game.START_KEY:
    #         pass

class CreditsMenu(Menu):
    def __init__(self, game):
        Menu.__init__(self, game)

        self.creditsx, self.creditsy = self.mid_w, self.mid_h - 20
        self.muradx, self.murady = self.mid_w, self.mid_h + 10
        self.masasukex, self.masasukey = self.mid_w, self.mid_h + 30
        self.timmyx, self.timmyy = self.mid_w, self.mid_h + 50

    def display_menu(self):
        self.run_display = True

        while self.run_display:
            self.game.check_events()

            if self.game.START_KEY or self.game.BACK_KEY:
                self.game.current_menu = self.game.main_menu
                self.run_display = False

            self.game.display.fill(self.game.BLACK)
            self.game.draw_text('Credits', 20, self.creditsx, self.creditsy)
            self.game.draw_text('Gameplay and Graphics by Murad D', 15, self.muradx, self.murady)
            self.game.draw_text('Song 1 by Masasuke M', 15, self.masasukex, self.masasukey)
            self.game.draw_text('Song 2 by Timmy Ong', 15, self.timmyx, self.timmyy)
            self.blit_screen()

class Slider:
    def __init__(self, game, pos: tuple, size: tuple, init_val: float, min: int, max: int):
        self.game = game
        
        self.pos = pos
        self.size = size

        self.slider_left_pos = self.pos[0] - (size[0] // 2)
        self.slider_right_pos = self.pos[0] + (size[0] // 2)
        self.slider_top_pos = self.pos[1] - (size[1] // 2)

        self.min = min
        self.max = max
        self.init_val = (self.slider_right_pos - self.slider_left_pos) * init_val # <-- in percentage

        self.container_rect = pygame.Rect(self.slider_left_pos, self.slider_top_pos, self.size[0], self.size[1])
        self.button_rect = pygame.Rect(self.slider_left_pos + self.init_val - 5, self.slider_top_pos, 10, self.size[1])

    def move_slider(self, mouse_pos):
        self.button_rect.centerx = mouse_pos[0]

    def render(self):
        pygame.draw.rect(self.game.display, (96, 96, 96), self.container_rect)
        pygame.draw.rect(self.game.display, self.game.WHITE, self.button_rect)

    def get_value(self):
        val_range = self.slider_right_pos- self.slider_left_pos - 1
        button_val = self.button_rect.centerx - self.slider_left_pos

        return (button_val / val_range) * (self.max - self.min) + self.min # returns volume value
    
class VictoryMenu(Menu):
    def __init__(self, game):
        super().__init__(game)
        self.state = 'Main Menu'

        self.winx, self.winy = self.mid_w, self.mid_h - 70
        self.thxx, self.thxy = self.mid_w, self.mid_h - 30
        self.menux, self.menuy = self.mid_w, self.mid_h + 50
        self.exitx, self.exity = self.mid_w, self.mid_h + 70

        self.cursor_rect.midtop = (self.menux + self.offset, self.menuy)
        self.rainbow_hue = 0

    def display_menu(self):
        self.run_display = True
        self.game.victory_sfx.play()

        while self.run_display:
            self.game.check_events()
            self.check_input()

            self.game.display.fill(self.game.BLACK)

            # Cycle hue for rainbow
            self.rainbow_hue = (self.rainbow_hue + 0.005) % 1.0
            r, g, b = colorsys.hsv_to_rgb(self.rainbow_hue, 1, 1)
            rainbow_colour = (int(r * 255), int(g * 255), int(b * 255))

            # Draw rainbow "YOU WIN"
            self.game.draw_text("YOU WIN", 20, self.winx, self.winy, rainbow_colour)

            # Draw other static text
            self.game.draw_text("THANKS FOR PLAYING", 20, self.thxx, self.thxy)
            self.game.draw_text("Main Menu", 20, self.menux, self.menuy)
            self.game.draw_text("Exit", 20, self.exitx, self.exity)

            self.draw_cursor()
            self.blit_screen()

    def check_input(self):
        if self.game.BACK_KEY:
            self.game.current_menu = self.game.main_menu
            self.run_display = False
        elif self.game.DOWN_KEY or self.game.UP_KEY:
            if self.state == 'Main Menu':
                self.state = 'Exit'
                self.cursor_rect.midtop = (self.exitx + self.offset, self.exity)
            elif self.state == 'Exit':
                self.state = 'Main Menu'
                self.cursor_rect.midtop = (self.menux + self.offset, self.menuy)
        elif self.game.START_KEY:
            if self.state == 'Main Menu':
                self.game.current_menu = self.game.main_menu
                self.run_display = False
            elif self.state == 'Exit':
                self.game.running, self.game.playing = False, False
                self.game.current_menu.run_display = False
