from settings import *

class AllSprites(pygame.sprite.Group):
    def __init__(self, width, height, bg_tile = None):
        super().__init__()
        self.display_surface = pygame.display.get_surface()
        self.offset = vector()
        self.width, self.height = width, height



    def draw(self, target_pos):
        # Starts the camera position at the default x/y values minus half of the width or height of the game window
        self.offset.x = -(target_pos[0] - window_width / 2)
        self.offset.y = -(target_pos[1] - window_height / 2)



        for sprite in sorted(self, key= lambda sprite: sprite.z):
            offset_pos = sprite.rect.topleft + self.offset
            self.display_surface.blit(sprite.image,offset_pos)