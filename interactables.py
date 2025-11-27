import pygame

class Interactable:
    """Base class for objects the player can interact with"""
    
    def __init__(self, x, y, width, height, name, interaction_text, image_path=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.name = name
        self.interaction_text = interaction_text
        self.is_near_player = False
        
        # Colors (used only if no image)
        self.color = (100, 200, 100)
        self.hover_color = (150, 255, 150)

        # Load image if provided
        self.image = None
        if image_path is not None:
            self.load_image(image_path, width, height)

    def load_image(self, path, width, height):
        """Loads and scales the interactable's image."""
        try:
            img = pygame.image.load(path).convert_alpha()
            self.image = pygame.transform.scale(img, (width, height))
        except:
            print(f"⚠️ Failed to load image: {path}")
            self.image = None

    def check_near_player(self, player_rect, distance=50):
        """Check if player is close enough to interact"""
        interaction_area = player_rect.inflate(distance * 2, distance * 2)
        self.is_near_player = interaction_area.colliderect(self.rect)
        return self.is_near_player
    
    def interact(self):
        print(f"Interacting with {self.name}: {self.interaction_text}")
    
    def draw(self, surface):
        """Draw image if present, otherwise draw rectangle"""
        
        if self.image:
            # Draw the image
            surface.blit(self.image, self.rect)
        else:
            # Fallback rectangle
            color = self.hover_color if self.is_near_player else self.color
            pygame.draw.rect(surface, color, self.rect)
        
        # Draw name label
        font = pygame.font.Font(None, 24)
        text = font.render(self.name, True, (255, 255, 255))
        text_rect = text.get_rect(center=(self.rect.centerx, self.rect.top - 10))
        surface.blit(text, text_rect)
        
        # Interaction prompt
        if self.is_near_player:
            prompt = font.render("[E] to interact", True, (255, 255, 0))
            prompt_rect = prompt.get_rect(center=(self.rect.centerx, self.rect.bottom + 15))
            surface.blit(prompt, prompt_rect)
