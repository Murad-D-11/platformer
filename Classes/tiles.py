import pygame, csv, os

class Tile(pygame.sprite.Sprite):
    def __init__(self, image, x, y, spritesheet):
        pygame.sprite.Sprite.__init__(self)
        self.image = spritesheet.parse_sprite(image)
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = x, y

    def draw(self, surface):
        surface.blit(self.image, (self.rect.x, self.rect.y))
        # pygame.draw.rect(surface, (255, 0, 0), self.rect, 1) # hitbox

class TileMap():
    def __init__(self, filename, spritesheet):
        self.tile_size = 32
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
        for entry in self.tiles:
            entry.get('data').draw(self.map_surface)

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
                if tile == '0': # Batoude
                    tiles.append({'data': Tile('batoude.png', x * self.tile_size, y * self.tile_size, self.spritesheet), 'id': 0})
                elif tile == '1': # Brick layer
                    tiles.append({'data': Tile('brick.png', x * self.tile_size, y * self.tile_size, self.spritesheet), 'id': 1})
                elif tile == '2': # Chain
                    tiles.append({'data': Tile('chain.png', x * self.tile_size, y * self.tile_size, self.spritesheet), 'id': 2})
                elif tile == '3': # Fin
                    tiles.append({'data': Tile('fin.png', x * self.tile_size, y * self.tile_size, self.spritesheet), 'id': 3})
                elif tile == '4': # Jump orb
                    tiles.append({'data': Tile('jump_orb.png', x * self.tile_size, y * self.tile_size, self.spritesheet), 'id': 4})
                elif tile == '6': # Surface
                    tiles.append({'data': Tile('pebbles.png', x * self.tile_size, y * self.tile_size, self.spritesheet), 'id': 6})
                elif tile == '7': # Floating platform
                    tiles.append({'data': Tile('platform.png', x * self.tile_size, y * self.tile_size, self.spritesheet), 'id': 7})
                elif tile == '9': # Player (facing right)
                    self.start_x, self.start_y = x * self.tile_size, y * self.tile_size
                elif tile == '10': # Spike
                    tiles.append({'data': Tile('spike.png', x * self.tile_size, y * self.tile_size, self.spritesheet), 'id': 10})
                x += 1
            y += 1

        self.map_w, self.map_h = x * self.tile_size, y * self.tile_size
        return tiles
