import pygame
from camera import Camera
from drawbackground import draw_background

pygame.init()
# Create a screen surface (no display window needed)
screen = pygame.Surface((1170, 720))
# Background sized to world
background = pygame.Surface((2000, 1500))
world_width, world_height = 2000, 1500

# Create camera with same params as game
camera = Camera(world_width, world_height, 1170, 720, zoom=1.4)
# Center camera somewhere near an edge to test clamping
camera.update(1900, 1400)

# Call draw_background with camera viewport
try:
    draw_background(screen, background, camera.camera, world_width, world_height)
    print("draw_background executed successfully")
except Exception as e:
    print("draw_background raised:", repr(e))
