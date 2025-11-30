import pygame

class EndLevelPopup:
    """Popup showing level completion stats"""
    
    def __init__(self):
        self.width = 500
        self.height = 400
        self.bg_color = (40, 40, 60)
        self.border_color = (255, 200, 0)
        self.title_font = pygame.font.Font("Tiny5-Regular.ttf", 48)
        self.text_font = pygame.font.Font("Tiny5-Regular.ttf", 32)
        
    def draw(self, surface, level_num, rank, essentials, distractors, scams):
        """Draw the popup"""
        screen_w, screen_h = surface.get_size()
        
        # Center popup
        x = (screen_w - self.width) // 2
        y = (screen_h - self.height) // 2
        
        # Draw background
        pygame.draw.rect(surface, self.bg_color, (x, y, self.width, self.height))
        pygame.draw.rect(surface, self.border_color, (x, y, self.width, self.height), 5)
        
        # Title
        title = self.title_font.render(f"Level {level_num} Complete!", True, (255, 255, 255))
        surface.blit(title, (x + 80, y + 30))
        
        # Rank
        rank_colors = {"S": (255, 215, 0), "A": (0, 255, 0), "B": (100, 200, 255), 
                      "C": (255, 165, 0), "D": (255, 50, 50)}
        rank_color = rank_colors.get(rank, (255, 255, 255))
        rank_text = self.title_font.render(f"Rank: {rank}", True, rank_color)
        surface.blit(rank_text, (x + 170, y + 90))
        
        # Stats
        stats_y = y + 160
        stats = [
            f"Essential Purchases: {essentials}",
            f"Distractor Purchases: {distractors}",
            f"Scams Fallen For: {scams}"
        ]
        
        for i, stat in enumerate(stats):
            text = self.text_font.render(stat, True, (255, 255, 255))
            surface.blit(text, (x + 60, stats_y + i * 40))
        
        # Continue prompt
        prompt = self.text_font.render("Press SPACE to continue", True, (255, 255, 0))
        surface.blit(prompt, (x + 90, y + 330))