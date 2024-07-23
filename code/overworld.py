from settings import *
from sprites import Sprite, AnimatedSprite, Node, Icon
from groups import WorldSprites
from random import randint

class Overworld:
    def __init__(self, tmx_map, data, overworld_frames):
        self.display_surface = pygame.display.get_surface()
        self.data = data

        # groups
        self.all_sprites = WorldSprites(data)
        self.node_sprites = pygame.sprite.Group()

        self.setup(tmx_map, overworld_frames)

        self.create_path_sprites()

        self.current_node = [node for node in self.node_sprites if node.level == 0][0]

    def setup(self, tmx_map, overworld_frames):
        # tiles
        for layer in ['main', 'top']:
            for x, y, surf in tmx_map.get_layer_by_name(layer).tiles():
                Sprite((x * tile_size,y * tile_size), surf, self.all_sprites, z_layers['bg tiles'])

        # water
        for col in range(tmx_map.width):
            for row in range(tmx_map.height):
                AnimatedSprite((col * tile_size,row * tile_size), overworld_frames['water'], self.all_sprites, z_layers['bg'])

        # objects
        for obj in tmx_map.get_layer_by_name('Objects'):
            if obj.name == 'palm':
                AnimatedSprite((obj.x, obj.y), overworld_frames['palms'], self.all_sprites, z_layers['main'], randint(4,6))
            else:
                z = z_layers[f'{'bg details' if obj.name == 'grass' else 'bg tiles'}']
                Sprite((obj.x, obj.y), obj.image, self.all_sprites, z)

        # pathing
        self.paths = {}
        for obj in tmx_map.get_layer_by_name('Paths'):
            pos = [(int(p.x + tile_size / 2), int(p.y + tile_size / 2)) for p in obj.points]
            start = obj.properties['start']
            end = obj.properties['end']
            self.paths[end] = {'pos': pos, 'start': start}
        

        # nodes and the player
        for obj in tmx_map.get_layer_by_name('Nodes'):

            # overworld player image
            if obj.name == 'Node' and obj.properties['stage'] == self.data.current_level:
                self.icon = Icon((obj.x + tile_size / 2, obj.y + tile_size / 2), self.all_sprites, overworld_frames['icon'])

            # nodes
            if obj.name == 'Node':
                available_paths = {k:v for k,v in obj.properties.items() if k in ('left', 'right', 'up', 'down')}
                Node(
                    pos = (obj.x, obj.y), 
                    surf = overworld_frames['path']['node'], 
                    groups = (self.all_sprites, self.node_sprites),
                    level = obj.properties['stage'],
                    data = self.data,
                    paths = available_paths)

    def create_path_sprites(self):

        # get tiles from path
        nodes = {node.level: vector(node.grid_pos) for node in self.node_sprites}
        path_tiles = {}

        for path_id, data in self.paths.items():
            path = data['pos']
            start_node, end_node = nodes[data['start']], nodes[path_id]
            path_tiles[path_id] = [start_node]

            for index, points in enumerate(path): # goes through all the points in the path and grabbing the index
                if index < len(path) -1: 
                    start, end = vector(points), vector(path[index + 1]) # stores the current(vectorpoints) and the next point (vectorpathindex + 1)
                    path_dir = (end - start) / tile_size
                    start_tile = vector(int(start[0] / tile_size), int(start[1]/ tile_size)) # the tile the player starts at

                if path_dir.y:
                    dir_y = 1 if path_dir.y > 0 else -1 # checks if player is going up or down
                    for y in range(dir_y, int(path_dir.y) + dir_y): # starts at 1 and counts upwards until 3, without including it
                        path_tiles[path_id].append(start_tile + vector(0, y)) # specifies the direction to move, down in this case

                if path_dir.x: # same as above, but checks the horizontal movement
                    dir_x = 1 if path_dir.x > 0 else -1
                    for x in range(dir_x, int(path_dir.x) + dir_x):
                        path_tiles[path_id].append(start_tile + vector(x, 0))

            path_tiles[path_id].append(end_node)

    def input(self):
        keys = pygame.key.get_pressed()
        if self.current_node and not self.icon.path:
            if keys[pygame.K_s] and self.current_node.can_move('down'):
                self.move('down')
            if keys[pygame.K_a] and self.current_node.can_move('left'):
                self.move('left')
            if keys[pygame.K_d] and self.current_node.can_move('right'):
                self.move('right')
            if keys[pygame.K_w] and self.current_node.can_move('up'):
                self.move('up')
    
    def move(self, direction):
        path_key = int(self.current_node.paths[direction][0])
        path_reverse = True if self.current_node.paths[direction][-1] == 'r' else False
        # Gets all of the position points within the dictionary if you can't reverse, if you want to reverse then we'd reverse the list
        path = self.paths[path_key]['pos'][:] if not path_reverse else self.paths[path_key]['pos'][::-1]
        self.icon.start_move(path)

    def get_current_node(self):
        nodes = pygame.sprite.spritecollide(self.icon, self.node_sprites, False)
        if nodes:
            self.current_node = nodes[0]

    def run(self, dt):
        self.input()
        self.get_current_node()
        self.all_sprites.update(dt)
        self.all_sprites.draw(self.icon.rect.center)