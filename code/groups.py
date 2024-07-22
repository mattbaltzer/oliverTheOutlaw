from settings import *
from sprites import Sprite, Cloud
from random import choice, randint
from timer import Timer

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
            # sky
            self.large_cloud = clouds['large']
            self.small_clouds = clouds['small']
            self.cloud_direction = -1

            # large cloud
            self.large_cloud_speed = 50
            self.large_cloud_x = 0
            self.large_cloud_tiles = int(self.width / self.large_cloud.get_width()) + 2
            self.large_cloud_width, self.large_cloud_height  = self.large_cloud.get_size()

            # small clouds
            # timer - > creates a cloud every 2.5 seconds, random speed and always moving left
            # lots of clouds to start with
            self.cloud_timer = Timer(2000, self.create_cloud, True)
            self.cloud_timer.activate
            for cloud in range(20):
                pos = (randint(0, self.width), randint(self.borders['top'], self.horizon_line))
                surf = choice(self.small_clouds)
                Cloud(pos, surf, self)

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

    def draw_large_cloud(self, dt):
        self.large_cloud_x += self.cloud_direction * self.large_cloud_speed * dt
        if self.large_cloud_x <= -self.large_cloud_width:
            self.large_cloud_x = 0
        for cloud in range(self.large_cloud_tiles):
            left = self.large_cloud_x + self.large_cloud_width * cloud + self.offset.x
            top = self.horizon_line - self.large_cloud_height + self.offset.y
            self.display_surface.blit(self.large_cloud, (left, top))

    def create_cloud(self):
        pos = (randint(self.width + 500, self.width + 600), randint(self.borders['top'], self.horizon_line))
        surf = choice(self.small_clouds)
        Cloud(pos, surf, self)

    def draw(self, target_pos, dt):
        # Starts the camera position at the default x/y values minus half of the width or height of the game window
        self.offset.x = -(target_pos[0] - window_width / 2)
        self.offset.y = -(target_pos[1] - window_height / 2)
        self.camera_constraint()

        if self.sky:
            self.cloud_timer.update()
            self.draw_sky()
            self.draw_large_cloud(dt)

        for sprite in sorted(self, key= lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image,offset_pos)