import pygame
import random
from events import FinancialEvent
from state import GameState


game_state = GameState()
class Level:
    """Represents a single level with specific difficulty"""
    
    def __init__(self, level_num, duration, essential_events, distractor_events, scam_events=None):
        self.level_num = level_num
        self.duration = duration  # seconds
        self.essential_events = essential_events  # [(name, cost, time_limit), ...]
        self.distractor_events = distractor_events
        self.scam_events = scam_events if scam_events else []
        self.start_time = None
        self.completed = False
        
    def is_finished(self):
        """Check if level time is up"""
        if self.start_time is None:
            return False
        import time
        return time.time() - self.start_time >= self.duration
    
    def start(self):
        """Start the level timer"""
        import time
        self.start_time = time.time()
    
    def get_remaining_time(self):
        """Get seconds remaining in level"""
        if self.start_time is None:
            return self.duration
        import time
        elapsed = time.time() - self.start_time
        return max(0, self.duration - elapsed)


class LevelManager:
    """Manages level progression and difficulty"""
    
    def __init__(self):
        self.current_level = 0
        self.levels = self.create_levels()
        self.event_images = self.load_event_images()
        
        # Stats tracking
        self.essentials_completed = 0
        self.distractors_bought = 0
        self.scams_fell_for = 0
        
    def load_event_images(self):
        """Load and scale event icons"""
        images = {
            "Rent Due": pygame.image.load("images\rent due.png").convert_alpha(),
            "Light Bill": pygame.image.load("images\\light bill icon.png").convert_alpha(),
            "fertilizer": pygame.image.load("images\\fertilizer.png").convert_alpha(),
            "Water Bill": pygame.image.load("images\\water bill.png").convert_alpha(),
            "Buy Shoes": pygame.image.load("images\\shoe.png").convert_alpha(),
            "Buy Video Game": pygame.image.load("mr placeholder.jpg").convert_alpha(),
            "Expensive Phone": pygame.image.load("mr placeholder.jpg").convert_alpha(),
            "Lottery Ticket": pygame.image.load("images\\lottery ticket.png").convert_alpha(),
            "Crypto Investment": pygame.image.load("images\\crypto.png").convert_alpha(),
        }
        
        for k in images:
            images[k] = pygame.transform.scale(images[k], (64, 64))
        
        return images
    
    def create_levels(self):
        """Create all levels with increasing difficulty"""
        return [
            # Level 1: Easy - 60 seconds, few events
            Level(1, 6, 
                  [("Rent Due", 100, 20), ("Light Bill", 50, 15), ("Manure", 30, 10), ("Fertilizer", 20, 15)],
                  [("Buy Shoes", 40, 20)]),
            
            # Level 2: Medium - 90 seconds, more events
            Level(2, 90,
                  [("Rent Due", 100, 18), ("Light Bill", 50, 15), ("Water Bill", 30, 12), ("Fertilizer", 20, 15)],
                  [("Buy Video Game", 60, 15), ("Buy Shoes", 40, 18)]),
            
            # Level 3: Hard - 120 seconds, shorter time limits, scams
            Level(3, 120,
                  [("Rent Due", 120, 15), ("Light Bill", 60, 12), ("Water Bill", 40, 10)],
                  [("Expensive Phone", 200, 20), ("Buy Video Game", 60, 12), ("Buy Shoes", 40, 15)],
                  [("Lottery Ticket", 20, 25), ("Crypto Investment", 100, 20)]),
            
            # Level 4: Very Hard - 150 seconds, many events
            Level(4, 150,
                  [("Rent Due", 150, 12), ("Light Bill", 70, 10), ("Water Bill", 50, 8)],
                  [("Expensive Phone", 250, 15), ("Buy Video Game", 80, 10), ("Buy Shoes", 50, 12)],
                  [("Lottery Ticket", 30, 20), ("Fake Investment", 150, 18)]),
        ]
    
    def get_current_level(self):
        """Get the current level object"""
        if self.current_level < len(self.levels):
            return self.levels[self.current_level]
        return None
    
    def next_level(self):
        """Move to next level"""
        self.current_level += 1
        
        self.essentials_completed = 0
        self.distractors_bought = 0
        self.scams_fell_for = 0
    
    def spawn_event_for_level(self, level, game_state):
        """Spawn a random event from the current level"""
        # Combine all possible events
        all_events = []
        
        for name, cost, time_limit in level.essential_events:
            all_events.append(("essential", name, cost, time_limit))
        
        for name, cost, time_limit in level.distractor_events:
            all_events.append(("distractor", name, cost, time_limit))
        
        for name, cost, time_limit in level.scam_events:
            all_events.append(("scam", name, cost, time_limit))
        
        if not all_events:
            return
        
        # Pick random event
        event_type, name, cost, time_limit = random.choice(all_events)
        
        # Random position
        x = random.randint(400, 800)
        y = random.randint(300, 800)
        
        # Get image
        img = self.event_images.get(name, self.event_images["Rent Due"])
        
        # Create event with type tag
        event = FinancialEvent(x, y, 64, 64, name, cost, time_limit, image=img)
        event.event_type = event_type  # Tag it as essential/distractor/scam
        
        game_state.events.append(event)
    
    def calculate_rank(self):
        """Calculate performance rank based on stats"""
        score = 0
        
        # Reward essentials completed
        score += self.essentials_completed * 10
        
        # Penalize distractors
        score -= self.distractors_bought * 5
        
        # Heavy penalty for scams
        score -= self.scams_fell_for * 15
        
        # Determine rank
        if score >= 40:
            return "S"
        elif score >= 30:
            return "A"
        elif score >= 20:
            return "B"
        elif score >= 10:
            return "C"
        else:
            return "D"