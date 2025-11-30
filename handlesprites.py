import pygame
import os 
import sys

sys.dont_write_bytecode = True
class Character:

    def load_animation(self, filename, num_frames):
            """Load animation frames from horizontal sprite sheet"""
            sheet = pygame.image.load(filename).convert_alpha()
            sheet_w, sheet_h = sheet.get_size()
            
            frame_w = sheet_w // num_frames
            frame_h = sheet_h
            
            # print(f"\n{filename}:")
            # print(f"  Sheet size: {sheet_w}x{sheet_h}")
            # print(f"  Frame size: {frame_w}x{frame_h}")
            # print(f"  Num frames: {num_frames}")
            
            frames = []
            for i in range(num_frames):
                # Create new surface
                frame_surf = pygame.Surface((frame_w, frame_h), pygame.SRCALPHA, 32)
                frame_surf.fill((0, 0, 0, 0))  # Clear to transparent
                
                # Copy frame area
                source_rect = pygame.Rect(i * frame_w, 0, frame_w, frame_h)
                frame_surf.blit(sheet, (0, 0), source_rect)
                
                frames.append(frame_surf)
                print(f"  Frame {i}: {frame_surf.get_size()}")
            
            return frames
            
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animations = {
            'walkleft': self.load_animation('farmer_frames\\walk_left.png', 4),
            'walkright': self.load_animation('farmer_frames\\walk_right.png', 4),
            'walkup': self.load_animation('farmer_frames\\walk_up.png', 4),
            'walkdown': self.load_animation('farmer_frames\\walk_down.png', 4),
        }
        self.current_animation = 'walkdown'
        self.last_direction = self.current_animation[4:]
    
        self.current_frame = 0
        self.frame_counter = 0
        self.animation_speed = 10
        self.is_idle = False  # ADD THIS LINE
        
        # Scale all frames to 128px height
        # Scale all frames to SAME WIDTH + HEIGHT
        target_h = 128

        # Determine the maximum width of all frames
        max_width = 0
        for key in self.animations:
            for frame in self.animations[key]:
                w, h = frame.get_size()
                new_w = int(w * (target_h / h))
                max_width = max(max_width, new_w)

        # Now rescale frames to max_width
        for key in self.animations:
            uniform_frames = []
            for frame in self.animations[key]:
                w, h = frame.get_size()
                new_w = int(w * (target_h / h))

                # Create a CLEAN uniform-sized frame
                final = pygame.Surface((max_width, target_h), pygame.SRCALPHA)
                final.fill((0, 0, 0, 0))

                # Scale original to new_w
                scaled = pygame.transform.scale(frame, (new_w, target_h))

                # Center it (optional)
                final.blit(scaled, ((max_width - new_w) // 2, 0))

                uniform_frames.append(final)

            self.animations[key] = uniform_frames

            
    def update(self):
        """Update animation frame"""
        if self.is_idle:  # ADD THIS CHECK
            return  # Don't animate when idle
            
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            frames = self.animations[self.current_animation]
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.frame_counter = 0
    
    def draw(self, surface):
        """Draw current frame"""
        frame = self.animations[self.current_animation][self.current_frame]
        surface.blit(frame, (self.x, self.y))
        
    def set_animation(self, animation_name):
        """Change animation"""
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame = 0
            self.frame_counter = 0
            if "walk" in animation_name:
                self.last_direction = animation_name.replace("walk", "")
        self.is_idle = False  # ADD THIS LINE
    
    def set_idle(self):
        """Set idle pose (first frame of last direction)"""
        idle_animation = f'walk{self.last_direction}'
        if self.current_animation != idle_animation or self.current_frame != 0:
            self.current_animation = idle_animation
            self.current_frame = 0
            self.frame_counter = 0
        self.is_idle = True  # ADD THIS LINE

    def get_rect(self):
        """Get collision rectangle for the character"""
        frame = self.animations[self.current_animation][self.current_frame]
        w, h = frame.get_size()
        return pygame.Rect(self.x, self.y, w, h)