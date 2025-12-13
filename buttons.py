import pygame

class Button:
    """A simple button class template for pygame"""
    
    def __init__(self, x, y, width, height, text, color, hover_color=None):
        """
        Initialize a button
        
        Args:
            x, y: Position of the button
            width, height: Dimensions of the button
            text: Text to display on button
            color: Button color (RGB tuple)
            hover_color: Color when hovered (optional, defaults to slightly brighter)
        """
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color if hover_color else self.brighten_color(color)
        self.is_hovered = False
        self.font = pygame.font.Font(None, 36)
    
    def brighten_color(self, color):
        """Make a color slightly brighter"""
        return tuple(min(c + 30, 255) for c in color)
    
    def draw(self, surface):
        """Draw the button on the surface"""
        current_color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, current_color, self.rect)
        
        # Draw text
        text_surface = pygame.font.Font("CSO-game-\\Tiny5-Regular.ttf", 36).render(self.text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def check_hover(self, mouse_pos):
        """Check if mouse is hovering over button"""
        self.is_hovered = self.rect.collidepoint(mouse_pos)
    
    def is_clicked(self, mouse_pos):
        """Check if button was clicked"""
        return self.rect.collidepoint(mouse_pos)