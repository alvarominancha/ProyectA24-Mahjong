"""
Tile renderer for creating simple tile graphics.
"""

import os


def create_simple_tile_images():
    """
    Create simple colored tile images using pygame.
    This is a placeholder - in a production game, you'd use proper tile artwork.
    """
    try:
        import pygame
    except ImportError:
        print("Pygame not installed. Run: pip install pygame")
        return False
    
    pygame.init()
    
    # Tile dimensions
    TILE_WIDTH = 60
    TILE_HEIGHT = 80
    
    # Ensure assets directory exists
    os.makedirs("assets/tiles", exist_ok=True)
    
    # Color schemes for different tile types
    colors = {
        'bamboo': (0, 150, 0),      # Green
        'character': (200, 0, 0),    # Red
        'dot': (0, 0, 200),          # Blue
        'wind': (150, 150, 0),       # Yellow
        'dragon': (150, 0, 150),     # Purple
        'flower': (255, 100, 150),   # Pink
        'season': (255, 150, 0),     # Orange
    }
    
    # Create tiles for suited tiles (1-9)
    for suit in ['bamboo', 'character', 'dot']:
        for rank in range(1, 10):
            surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
            surface.fill((240, 240, 220))  # Cream background
            
            # Draw border
            pygame.draw.rect(surface, (100, 100, 80), (0, 0, TILE_WIDTH, TILE_HEIGHT), 3)
            
            # Draw suit indicator
            pygame.draw.circle(surface, colors[suit], (TILE_WIDTH // 2, 20), 10)
            
            # Draw rank text
            font = pygame.font.Font(None, 48)
            text = font.render(str(rank), True, (0, 0, 0))
            text_rect = text.get_rect(center=(TILE_WIDTH // 2, TILE_HEIGHT // 2))
            surface.blit(text, text_rect)
            
            # Save
            filename = f"assets/tiles/{suit}_{rank}.png"
            pygame.image.save(surface, filename)
    
    # Create wind tiles
    winds = ['east', 'south', 'west', 'north']
    wind_chars = ['E', 'S', 'W', 'N']
    for wind, char in zip(winds, wind_chars):
        surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        surface.fill((240, 240, 220))
        pygame.draw.rect(surface, (100, 100, 80), (0, 0, TILE_WIDTH, TILE_HEIGHT), 3)
        pygame.draw.circle(surface, colors['wind'], (TILE_WIDTH // 2, 20), 10)
        
        font = pygame.font.Font(None, 48)
        text = font.render(char, True, (0, 0, 0))
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, TILE_HEIGHT // 2))
        surface.blit(text, text_rect)
        
        filename = f"assets/tiles/wind_{wind}.png"
        pygame.image.save(surface, filename)
    
    # Create dragon tiles
    dragons = ['red', 'green', 'white']
    dragon_chars = ['R', 'G', 'W']
    for dragon, char in zip(dragons, dragon_chars):
        surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        surface.fill((240, 240, 220))
        pygame.draw.rect(surface, (100, 100, 80), (0, 0, TILE_WIDTH, TILE_HEIGHT), 3)
        pygame.draw.circle(surface, colors['dragon'], (TILE_WIDTH // 2, 20), 10)
        
        font = pygame.font.Font(None, 48)
        text = font.render(char, True, (0, 0, 0))
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, TILE_HEIGHT // 2))
        surface.blit(text, text_rect)
        
        filename = f"assets/tiles/dragon_{dragon}.png"
        pygame.image.save(surface, filename)
    
    # Create flower tiles
    for flower_num in range(1, 5):
        surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        surface.fill((240, 240, 220))
        pygame.draw.rect(surface, (100, 100, 80), (0, 0, TILE_WIDTH, TILE_HEIGHT), 3)
        pygame.draw.circle(surface, colors['flower'], (TILE_WIDTH // 2, 20), 10)
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"F{flower_num}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, TILE_HEIGHT // 2))
        surface.blit(text, text_rect)
        
        filename = f"assets/tiles/flower_{flower_num}.png"
        pygame.image.save(surface, filename)
    
    # Create season tiles
    for season_num in range(1, 5):
        surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
        surface.fill((240, 240, 220))
        pygame.draw.rect(surface, (100, 100, 80), (0, 0, TILE_WIDTH, TILE_HEIGHT), 3)
        pygame.draw.circle(surface, colors['season'], (TILE_WIDTH // 2, 20), 10)
        
        font = pygame.font.Font(None, 36)
        text = font.render(f"S{season_num}", True, (0, 0, 0))
        text_rect = text.get_rect(center=(TILE_WIDTH // 2, TILE_HEIGHT // 2))
        surface.blit(text, text_rect)
        
        filename = f"assets/tiles/season_{season_num}.png"
        pygame.image.save(surface, filename)
    
    # Create blank/back tile
    surface = pygame.Surface((TILE_WIDTH, TILE_HEIGHT))
    surface.fill((100, 100, 80))
    pygame.draw.rect(surface, (50, 50, 40), (0, 0, TILE_WIDTH, TILE_HEIGHT), 3)
    filename = "assets/tiles/blank.png"
    pygame.image.save(surface, filename)
    
    pygame.quit()
    print("Tile images created successfully!")
    return True


if __name__ == "__main__":
    create_simple_tile_images()
