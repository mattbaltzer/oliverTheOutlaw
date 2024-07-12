from settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites):
        super().__init__(groups)
        self.image = pygame.Surface((48, 56))
        self.image.fill('red')

        # rectangles
        self.rect = self.image.get_frect(topleft = pos)
        self.old_rect = self.rect.copy()

        # movement
        self.direction = vector()
        self.speed = 200
        self.gravity = 1000

        # collision
        self.collision_sprites = collision_sprites


    def input(self):
        keys = pygame.key.get_pressed()
        input_vector = vector()

        if keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_SPACE]:
            input_vector.y += 1

        self.direction.x = input_vector.normalize().x if input_vector else 0

    def move(self, dt):
        # horizontal
        self.rect.x += self.direction.x * self.speed * dt
        self.collision('horizontal')

        # vertical
        self.direction.y += self.gravity / 2 * dt
        self.rect.y += self.direction.y * dt
        # The double is used to calculate the average downward velocity
        self.direction.y += self.gravity / 2 * dt
        self.collision('vertical')
        


    def collision(self, axis):
        for sprite in self.collision_sprites:
            # checks the rectangle of a sprite against the rectangle of the player
            if sprite.rect.colliderect(self.rect):
                if axis == 'horizontal':
                    # left side
                    if self.rect.left <= sprite.rect.right and self.old_rect.left >= sprite.old_rect.right:
                        self.rect.left = sprite.rect.right 
                    # right side
                    if self.rect.right >= sprite.rect.left and self.old_rect.right <= sprite.old_rect.left:
                        self.rect.right = sprite.rect.left
                else:
                    # top 
                    if self.rect.top <= sprite.rect.bottom and self.old_rect.top >= sprite.old_rect.bottom:
                        self.rect.top = sprite.rect.bottom
                    # bottom
                    if self.rect.bottom >= sprite.rect.top and self.old_rect.bottom <= sprite.old_rect.top:
                        self.rect.bottom = sprite.rect.top
                    self.direction.y = 0


    def update(self, dt):
        self.old_rect = self.rect.copy()
        self.input()
        self.move(dt)