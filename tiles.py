import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 16
        self.start_x, self.start_y = 0, 0
        self.spritesheet = spritesheet
        self.tiles = self.load_tiles(filename)
        self.map_surface = pygame.Surface((self.map_w, self.map_h))
        self.map_surface.set_colorkey((0, 0, 0))
        self.load_map()

    # Draws the map onto the screen
    def draw_map(self, surface):
        surface.blit(self.map_surface, (0, 0))

    # Loads map as one big surface
    def load_map(self):
        for tile in self.tiles:
            tile.draw(self.map_surface)

    # Converts the .csv file into a list of rows
    def read_csv(self, filename):
        map = []
        
        with open(os.path.join(filename)) as data:
            data = csv.reader(data, delimiter=',')
            for row in data:
                map.append(list(row))
        
        return map
    
    def load_tiles(self, filename):
        tiles = []
        map = self.read_csv(filename)
        x, y = 0, 0
        
        # Iterates through all tiles in the map
        for row in map:
            x = 0
            for tile in row:
                if tile == '0': # Brick layer
                    tiles.append(Tile('brick.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '1': # Surface
                    tiles.append(Tile('pebbles.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '2': # Floating platform
                    tiles.append(Tile('platform.png', x * self.tile_size, y * self.tile_size, self.spritesheet))
                elif tile == '3': # Player
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                x += 1
            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
