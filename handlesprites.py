import pygame

class Character:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.animations = {
            'walkleft': self._load_animation('farmer_frames\\walk_left.png', 4),
            'walkright': self._load_animation('farmer_frames\\walk_right.png', 4),
            'walkup': self._load_animation('farmer_frames\\walk_up.png', 4),
            'walkdown': self._load_animation('farmer_frames\\walk_down.png', 4),

        }
        self.current_animation = 'walkdown' #default facing down
        self.last_direction = 'down' #tracks direction 
        self.current_frame = 0
        self.frame_counter = 0
        self.animation_speed = 10
        # Upscale all frames to target height of 128px, preserving aspect ratio
        target_h = 128
        for key, frames in self.animations.items():
            new_frames = []
            for f in frames:
                w, h = f.get_size()
                if h != target_h:
                    new_w = max(1, int(w * (target_h / h)))
                    # Use pygame.transform.scale which works with subsurfaces
                    f = pygame.transform.scale(f, (new_w, target_h))
                new_frames.append(f)
            self.animations[key] = new_frames
    
    def _load_animation(self, filename, num_frames):
        """Helper to load animation frames - no scaling, use native size"""
        sprite_sheet = pygame.image.load(filename).convert_alpha()
        sheet_width, sheet_height = sprite_sheet.get_size()
        print(f"Loading {filename}: {sheet_width}x{sheet_height}, expecting {num_frames} frames")
        frames = []
        tile_w = sheet_width // num_frames
        tile_h = sheet_height

        print(f"Loading {filename}: sheet={sheet_width}x{sheet_height}, tile={tile_w}x{tile_h}")
        # If the sheet width divides evenly by num_frames, assume a single row
        # if sheet_width % num_frames == 0:
            
        for i in range(num_frames):
            frame_surface = pygame.Surface((tile_w, tile_h), pygame.SRCALPHA)
            source_rect = pygame.Rect(i * tile_w, 0, tile_w, tile_h)
            frame_surface.blit(sprite_sheet, (0, 0), source_rect)
            frames.append(frame_surface)
        return frames

        # Otherwise try to extract frames from a grid (rows x cols)
        import math
        cols = int(math.ceil(math.sqrt(num_frames)))
        rows = int(math.ceil(num_frames / cols))
        tile_w = sheet_width // cols
        tile_h = sheet_height // rows if rows > 0 else sheet_height

        count = 0
        for r in range(rows):
            for c in range(cols):
                if count >= num_frames:
                    break
                x = c * tile_w
                y = r * tile_h
                try:
                    frame = sprite_sheet.subsurface((x, y, tile_w, tile_h))
                    frames.append(frame)
                except Exception as e:
                    print(f"Error loading grid frame {count} from {filename}: {e}")
                    raise
                count += 1

        return frames
    
    def update(self):
        self.frame_counter += 1
        if self.frame_counter >= self.animation_speed:
            frames = self.animations[self.current_animation]
            self.current_frame = (self.current_frame + 1) % len(frames)
            self.frame_counter = 0
    
    def draw(self, surface):
        frame = self.animations[self.current_animation][self.current_frame]
        surface.blit(frame, (self.x, self.y))
    
    def set_animation(self, animation_name):
        if animation_name != self.current_animation:
            self.current_animation = animation_name
            self.current_frame = 0
            self.frame_counter = 0
            if "walk" in animation_name:
                self.last_direction = animation_name.replace("walk", "")
    def set_idle(self):
        idle_animation = f'walk{self.last_direction}'
        self.current_animation = idle_animation
        self.current_frame = 0
        self.frame_counter = 0
