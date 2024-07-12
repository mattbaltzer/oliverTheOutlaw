import pygame, sys

window_width, window_height = 1280, 720
tile_size = 64
animation_speed = 6 

# layers
z_layers = {
    'bg': 0,
    'clouds': 1,
    'bg tiles': 2, 
    'path': 3,
    'bg details': 4,
    'main': 5,
    'water': 6,
    'fg': 7
}