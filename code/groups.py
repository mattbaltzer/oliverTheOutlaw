from settings import *
from sprites import Sprite

class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, clouds, horizon_line, bg_tile = None, top_limit = 0):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.width, self.height = width * tile_size, height * tile_size
        self.borders = {
            'left': 0,
            'right': -self.width + window_width,
            'bottom': -self.height + window_height,
            'top': top_limit,}
        self.sky = not bg_tile
        self.horizon_line = horizon_line

        if bg_tile:
            for col in range(width):
                for row in range(-int(top_limit / tile_size) - 1, height):
                    x, y = col * tile_size, row * tile_size
                    Sprite((x, y), bg_tile, self, -1)
        else:
            #sky
            self.large_cloud = clouds['large'],
            self.small_clouds = clouds['small']

    def camera_constraint(self):
        self.offset.x = self.offset.x if self.offset.x < self.borders['left'] else self.borders['left']
        self.offset.x = self.offset.x if self.offset.x > self.borders['right'] else self.borders['right']
        self.offset.y = self.offset.y if self.offset.y > self.borders['bottom'] else self.borders['bottom']
        self.offset.y = self.offset.y if self.offset.y < self.borders['top'] else self.borders['top']

    def draw_sky(self):
        self.display_surface.fill('#ddc6a1')
        horizon_pos = self.horizon_line + self.offset.y

        sea_rect = pygame.FRect(0, horizon_pos, window_width, window_height - horizon_pos)
        pygame.draw.rect(self.display_surface, '#92a9ce', sea_rect)

        # Sets up the horizon line
        pygame.draw.line(self.display_surface, '#f5f1de', (0, horizon_pos), (window_width, horizon_pos), 4)

    def draw(self, target_pos):
        # Starts the camera position at the default x/y values minus half of the width or height of the game window
        self.offset.x = -(target_pos[0] - window_width / 2)
        self.offset.y = -(target_pos[1] - window_height / 2)
        self.camera_constraint()

        if self.sky:
            self.draw_sky()

        for sprite in sorted(self, key= lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image,offset_pos)