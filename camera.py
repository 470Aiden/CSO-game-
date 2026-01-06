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

        # Compute desired top-left so the camera is centered on the target
        x = targetx - cam_w // 2
        y = targety - cam_h // 2

        # Clamp using the viewport size (cam_w/cam_h). This prevents
        # the camera from getting stuck when the world bounds are smaller
        # or when zoom is not 1.0.
        max_x = max(0, self.world_width - cam_w)
        max_y = max(0, self.world_height - cam_h)

        x = max(0, min(x, max_x))
        y = max(0, min(y, max_y))

        # Store integer rect for camera (viewport in world coordinates)
        self.camera = pygame.Rect(int(x), int(y), int(cam_w), int(cam_h))