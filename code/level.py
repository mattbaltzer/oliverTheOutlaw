from settings import *
from sprites import Sprite, AnimatedSprite, MovingSprite, Spike
from player import Player
from groups import AllSprites
from enemies import Tooth, Shell

class Level:
    def __init__(self, tmx_map, level_frames):
        self.display_surface = pygame.display.get_surface()

        # groups
        self.all_sprites = AllSprites()
        self.collision_sprites = pygame.sprite.Group()
        self.semicollidable_sprites = pygame.sprite.Group()
        self.damage_sprites = pygame.sprite.Group()
        self.tooth_sprites = pygame.sprite.Group()

        self.setup(tmx_map, level_frames)
    
    def setup(self, tmx_map, level_frames):
        # tiles
        for layer in ['BG', 'Terrain', 'FG', 'Platforms']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                groups = [self.all_sprites]
                if layer == 'Terrain': groups.append(self.collision_sprites)
                if layer == 'Platforms': groups.append(self.semicollidable_sprites)
                match layer:
                    case 'BG': z = z_layers['bg tiles']
                    case 'FG': z = z_layers['bg tiles']
                    case _: z = z_layers['main']
                Sprite((x * tile_size,y * tile_size),surf,groups, z)
        
        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'player':
                self.player = Player(
                    pos = (obj.x,obj.y),
                    groups = self.all_sprites, 
                    collision_sprites = self.collision_sprites, 
                    semicollidable_sprites = self.semicollidable_sprites,
                    frames = level_frames['player'])
            else:
                if obj.name in ('barrel', 'crate'):
                    Sprite((obj.x, obj.y), obj.image, (self.all_sprites, self.collision_sprites))
                else:
                    if 'palm' not in obj.name:
                        frames = level_frames[obj.name]
                        AnimatedSprite((obj.x, obj.y), frames, self.all_sprites, z, animation_speed)

        # moving objects
        for obj in tmx_map.get_layer_by_name('Moving Objects'):
            if obj.name == 'spike':
                Spike(
                    pos = (obj.x + obj.width / 2, obj.y + obj.height / 2 ),
                    surf = level_frames['spike'],
                    radius = obj.properties['radius'],
                    speed = obj.properties['speed'],
                    start_angle = obj.properties['start_angle'],
                    end_angle = obj.properties['end_angle'],
                    groups = (self.all_sprites, self.damage_sprites)
                )
                for radius in range(0, obj.properties['radius'], 20):
                    Spike(
                    pos = (obj.x + obj.width / 2, obj.y + obj.height / 2),
                    surf = level_frames['spike_chain'],
                    radius = radius,
                    speed = obj.properties['speed'],
                    start_angle = obj.properties['start_angle'],
                    end_angle = obj.properties['end_angle'],
                    groups = self.all_sprites,
                    z = z_layers['bg details'],
                )
            else:
                frames = level_frames[obj.name]
                groups =  (self.all_sprites, self.semicollidable_sprites) if obj.properties['platform'] else (self.all_sprites, self.damage_sprites)
                if obj.width > obj.height: # horizontal movement
                    move_dir = 'x'
                    start_pos = (obj.x, obj.y + obj.height / 2)
                    end_pos = (obj.x + obj.width, obj.y + obj.height / 2)
                else: # vertical movement
                    move_dir = 'y'
                    start_pos = (obj.x + obj.width / 2, obj.y)
                    end_pos = (obj.x + obj.width / 2, obj.y + obj.height)
                speed = obj.properties['speed']
                MovingSprite(frames, groups, start_pos, end_pos, move_dir, speed, obj.properties['flip'])

                if obj.name == 'saw':
                    if move_dir == 'x':
                        y = start_pos[1] - level_frames['saw_chain'].get_height() / 2
                        left, right = int(start_pos[0]), int(end_pos[0])
                        for x in range(left, right, 20):
                            Sprite((x,y), level_frames['saw_chain'], self.all_sprites, z = z_layers['bg details'])
                    else:
                        x = start_pos[0] - level_frames['saw_chain'].get_width() / 2
                        top, bottom = int(start_pos[1]), int(end_pos[1])
                        for y in range(top, bottom, 20):
                            Sprite((x,y), level_frames['saw_chain'], self.all_sprites, z = z_layers['bg details'])
                
        # enemies
        for obj in tmx_map.get_layer_by_name('Enemies'):
            if obj.name == 'tooth':
                Tooth((obj.x, obj.y), level_frames['tooth'], (self.all_sprites, self.damage_sprites, self.tooth_sprites), self.collision_sprites)
            if obj.name =='shell':
                Shell((obj.x, obj.y), level_frames['shell'], (self.all_sprites, self.collision_sprites), obj.properties['reverse'], self.player)

    def run(self, dt):
        self.display_surface.fill('black')
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.player.hitbox_rect.center)