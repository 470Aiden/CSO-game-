import pygame

class Camera:
    def __init__(self, world_width, world_height, screen_width, screen_height,zoom=1.0):
        self.world_width = world_width
        self.world_height = world_height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.zoom = zoom
        self.camera = pygame.Rect(0, 0, screen_width, screen_height)

    def apply(self, rect):
        """Apply camera offset to a rectangle"""
        return rect.move(-self.camera.x, -self.camera.y)
    
    def apply_pos(self, x, y):
        """Apply camera offset to a position"""
        return (x - self.camera.x, y - self.camera.y)
    
    def update(self, targetx, targety):
        """Update camera to center on target"""
        # Center camera on target
        cam_w = self.screen_width / self.zoom
        cam_h = self.screen_height / self.zoom

        x = targetx - cam_w // 2
        y = targety - cam_h // 2

        # Limit scrolling to world bounds
        x = max(0, min(x, self.world_width - self.screen_width))
        y = max(0, min(y, self.world_height - self.screen_height))

        # Update camera position
        self.camera = pygame.Rect(x, y, self.screen_width, self.screen_height)