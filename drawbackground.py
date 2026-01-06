import pygame


def draw_background(screen, background, cam_rect, world_width, world_height):
    """
    Draw a non-repeating background using the camera viewport rect.

    cam_rect: a pygame.Rect in world coordinates representing the
    viewport (x, y, width, height). This handles zoom by using the
    viewport size rather than assuming screen size equals world-region.
    """
    screen_width, screen_height = screen.get_size()

    # Viewport size in world coordinates
    cam_w = int(cam_rect.width)
    cam_h = int(cam_rect.height)

    # Top-left of viewport in world coords
    left = int(cam_rect.x)
    top = int(cam_rect.y)

    # Clamp to world bounds
    left = max(0, min(left, max(0, world_width - cam_w)))
    top = max(0, min(top, max(0, world_height - cam_h)))

    # Rect of the background to sample
    bg_rect = pygame.Rect(left, top, cam_w, cam_h)

    # Extract the portion and scale to the screen if viewport != screen
    portion = background.subsurface(bg_rect).copy()
    if (cam_w, cam_h) != (screen_width, screen_height):
        portion = pygame.transform.scale(portion, (screen_width, screen_height))

    screen.blit(portion, (0, 0))
