import pygame

class EndLevelPopup:
    """Popup showing level completion stats"""
    
    def __init__(self):
        self.width = 500
        self.height = 400
        self.bg_color = (40, 40, 60)
        self.border_color = (255, 200, 0)
        self.title_font = pygame.font.Font("Tiny5-Regular.ttf", 48)
        self.text_font = pygame.font.Font("Tiny5-Regular.ttf", 25)
        
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
        if rank =="S":
            rank_text = self.title_font.render(f"Rank: {rank}  ", True, rank_color)
            line1 = self.title_font.render("money spent mostly ", True, rank_color)
            line2 = self.title_font.render("on essentials!", True, rank_color)
            surface.blit(rank_text, (x + 170, y + 90))
            surface.blit(line1, (x + 20, y + 130))
            surface.blit(line2, (x + 40, y + 170))

        elif rank =="A":
            rank_text = self.title_font.render(f"Rank: {rank}  ", True, rank_color)
            line1 = self.text_font.render("Great job! But remember to spend ", True, rank_color)
            line2 = self.text_font.render("money on essentials.", True, rank_color)
            surface.blit(rank_text, (x + 170, y + 90))
            surface.blit(line1, (x + 30, y + 130))
            surface.blit(line2, (x + 80, y + 170))
        elif rank =="B":
            rank_text = self.title_font.render(f"Rank: {rank} ", True, rank_color)
            line1 = self.text_font.render("Good! But", True, rank_color)
            line2 = self.text_font.render("you can do better", True, rank_color)
            surface.blit(rank_text, (x + 90, y + 90))
        if rank =="C":
            rank_text = self.title_font.render(f"Rank: {rank} ", True, rank_color)
            line1 = self.text_font.render("Focus more on essentials. ", True, rank_color)
            surface.blit(rank_text, (x + 90, y + 90))
            surface.blit(line1, (x + 90, y + 130))
        elif rank =="D":
            rank_text = self.title_font.render(f"Rank: {rank}  ", True, rank_color)
            line1 = self.text_font.render("You spent your money poorly.", True, rank_color)
            line2 = self.text_font.render("You must focus on on essentials", True, rank_color)
            surface.blit(rank_text, (x + 170, y + 90))
            surface.blit(line1, (x + 80, y + 130))
            surface.blit(line2, (x + 40, y + 170))
        
        # Stats
        stats_y = y + 240
        stats = []
        if distractors:
            stats.append("Distractors:")
            for item in distractors:
                stats.append(f"  - {item}")
        if scams:
            stats.append("Scams:")
            for item in scams:
                stats.append(f"  - {item}")
        
        for i, stat in enumerate(stats):
            text = self.text_font.render(stat, True, (255, 255, 255))
            if stat.endswith(":"):  # Heading
                text_x = x + (self.width - text.get_width()) // 2
            else:  # Item
                text_x = x + 20
            surface.blit(text, (text_x, stats_y + i * 25))
        
        # Continue prompt
        prompt = self.text_font.render("Press SPACE to continue", True, (255, 255, 0))
        surface.blit(prompt, (x + 90, y + 330))