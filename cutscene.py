import pygame
import time


def play_farmer_cutscene(screen, clock=None):
    """Play a short cutscene with a background image and animated text.

    - Uses `images/new farm 1.png` if available, falls back to other farm images.
    - Text appears one word at a time. Press SPACE or click to skip once finished.
    """
    if clock is None:
        clock = pygame.time.Clock()

    # Try a few likely image names (project already contains several farm images)
    candidates = [
        "images\\farmer intro.png"
    ]
    bg = None
    for path in candidates:
        try:
            bg = pygame.image.load(path).convert()
            break
        except Exception:
            bg = None

    # If no background found, create a simple placeholder

    # Text to display (word-by-word)
    full_text = (
        "You are a farmer in a rural area. Spend your money wisely "
        "to keep your farm running smoothly."
    )
    words = full_text.split()

   
    try:
        font = pygame.font.Font("Tiny5-Regular.ttf", 28)
    except Exception:
        font = pygame.font.SysFont(None, 28)

    # Text box settings
    box_h = 140
    box_margin = 20
    box_rect = pygame.Rect(
        box_margin,
        screen_h - box_h - box_margin,
        screen_w - box_margin * 2,
        box_h,
    )

    # Animation timing
    word_delay_ms = 150  # moderate speed per word
    last_word_time = pygame.time.get_ticks()
    words_shown = 0
    finished = False
    finish_time = None

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and finished:
                    running = False
                elif event.key == pygame.K_SPACE and not finished:
                    # skip to end immediately
                    words_shown = len(words)
                    finished = True
                    finish_time = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if finished:
                    running = False
                else:
                    words_shown = len(words)
                    finished = True
                    finish_time = pygame.time.get_ticks()

        # Advance words on timer if not finished
        now = pygame.time.get_ticks()
        if not finished and now - last_word_time >= word_delay_ms:
            last_word_time = now
            words_shown = min(words_shown + 1, len(words))
            if words_shown == len(words):
                finished = True
                finish_time = now

        # Draw background
        screen.blit(bg, (0, 0))

        # Draw textbox (semi-transparent)
        s = pygame.Surface((box_rect.w, box_rect.h), pygame.SRCALPHA)
        s.fill((20, 20, 30, 220))
        # border
        screen.blit(s, (box_rect.x, box_rect.y))
        pygame.draw.rect(screen, (200, 180, 40), box_rect, 3)

        # Build the currently visible text
        visible_text = " ".join(words[:words_shown])

        # Wrap text into lines that fit inside the box
        lines = []
        if visible_text:
            words_for_wrap = visible_text.split()
            cur = ""
            for w in words_for_wrap:
                test = (cur + " " + w).strip()
                test_surf = font.render(test, True, (255, 255, 255))
                if test_surf.get_width() <= box_rect.w - 24:
                    cur = test
                else:
                    lines.append(cur)
                    cur = w
            if cur:
                lines.append(cur)

        # Render lines
        text_y = box_rect.y + 16
        for line in lines:
            surf = font.render(line, True, (255, 255, 255))
            screen.blit(surf, (box_rect.x + 12, text_y))
            text_y += surf.get_height() + 6

        # Prompt
        if finished:
            prompt = font.render("Press SPACE or click to continue", True, (255, 220, 0))
            px = box_rect.x + (box_rect.w - prompt.get_width()) // 2
            screen.blit(prompt, (px, box_rect.y + box_rect.h - 34))

        pygame.display.flip()

        # if finished and user doesn't press, auto-close after 2.5s
        if finished and finish_time and pygame.time.get_ticks() - finish_time > 2500:
            running = False


def _play_simple_ending(screen, clock=None, title_text="", body_text="", color=(30, 30, 60), bg_path=None):
    """Generic ending cutscene with placeholder background and animated body text.

    If `bg_path` is provided and the image loads, that image is used as background.
    """
    if clock is None:
        clock = pygame.time.Clock()

    screen_w, screen_h = screen.get_size()
    bg = None
    if bg_path:
        try:
            bg = pygame.image.load(bg_path).convert()
            bg = pygame.transform.scale(bg, (screen_w, screen_h))
        except Exception:
            bg = None

    if bg is None:
        bg = pygame.Surface((screen_w, screen_h))
        bg.fill(color)

    try:
        title_font = pygame.font.Font("Tiny5-Regular.ttf", 48)
        body_font = pygame.font.Font("Tiny5-Regular.ttf", 28)
    except Exception:
        title_font = pygame.font.SysFont(None, 48)
        body_font = pygame.font.SysFont(None, 28)

    # Title centered
    title_surf = title_font.render(title_text, True, (255, 255, 255))

    # Animate body text word-by-word (same logic as farmer cutscene)
    words = body_text.split()
    word_delay_ms = 300
    last_word_time = pygame.time.get_ticks()
    words_shown = 0
    finished = False
    finish_time = None

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                raise SystemExit
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and finished:
                    running = False
                elif event.key == pygame.K_SPACE and not finished:
                    words_shown = len(words)
                    finished = True
                    finish_time = pygame.time.get_ticks()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if finished:
                    running = False
                else:
                    words_shown = len(words)
                    finished = True
                    finish_time = pygame.time.get_ticks()

        now = pygame.time.get_ticks()
        if not finished and now - last_word_time >= word_delay_ms:
            last_word_time = now
            words_shown = min(words_shown + 1, len(words))
            if words_shown == len(words):
                finished = True
                finish_time = now

        screen.blit(bg, (0, 0))
        # draw title
        screen.blit(title_surf, ((screen_w - title_surf.get_width()) // 2, 80))

        # build visible text and wrap
        visible = " ".join(words[:words_shown])
        lines = []
        if visible:
            cur = ""
            for w in visible.split():
                test = (cur + " " + w).strip()
                ts = body_font.render(test, True, (255, 255, 255))
                if ts.get_width() <= screen_w - 120:
                    cur = test
                else:
                    lines.append(cur)
                    cur = w
            if cur:
                lines.append(cur)

        ty = 160
        for line in lines:
            surf = body_font.render(line, True, (255, 255, 255))
            screen.blit(surf, (60, ty))
            ty += surf.get_height() + 8

        if finished:
            prompt = body_font.render("Press SPACE or click to continue", True, (255, 220, 0))
            screen.blit(prompt, ((screen_w - prompt.get_width()) // 2, screen_h - 80))

        pygame.display.flip()

        if finished and finish_time and pygame.time.get_ticks() - finish_time > 3000:
            running = False


def play_good_ending(screen, clock=None):
    title = "Well Done"
    body = (
        "You managed your resources well and kept your farm running. "
        "Your wise choices will ensure a prosperous future for your farm."
    )
    _play_simple_ending(screen, clock, title, body, color=(20, 80, 30), bg_path="images\\farmer good ending.png")


def play_bad_ending(screen, clock=None):
    title = "Tough Times Ahead"
    body = (
        "You struggled to keep the farm afloat. Consider prioritizing essentials "
        "and avoiding costly distractions in future playthroughs."
    )
    _play_simple_ending(screen, clock, title, body, color=(60, 30, 30), bg_path="images\\farmer bad ending (2).png")

