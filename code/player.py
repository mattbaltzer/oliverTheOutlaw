from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')
        self.rect = self.image.get_frect(topleft = pos)