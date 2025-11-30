import pygame

class Camera:
    def __init__(self, world_width, world_height, screen_width, screen_height):
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)

    def apply(self, rect):
        return rect.move(-self.camera.x, -self.camera.y)
    
    def update(self, targetx, targety):
        x = targetx - self.screen_width // 2
        y = targety - self.screen_height // 2

        # limit scrolling to map size
        x = min(0, x)  # left
        y = min(0, y)  # top
        x = max(0, min(x, self.camera.width - self.screen_width))
        y = max(0, min(y, self.camera.height - self.screen_height))

        self.camera.topleft = (x, y)
        self.camera = pygame.Rect(x, y, self.screen_width, self.screen_height)