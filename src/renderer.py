"""
Game renderer for Mahjong using pygame.
Handles all visual rendering and display.
"""

import pygame
import os
from tile import Tile


class GameRenderer:
    """Handles rendering of the game board and UI."""
    
    # Display settings
    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 768
    TILE_WIDTH = 60
    TILE_HEIGHT = 80
    TILE_SPACING = 5
    
    # Colors
    BG_COLOR = (34, 139, 34)  # Forest green
    UI_BG_COLOR = (50, 50, 50)
    TEXT_COLOR = (255, 255, 255)
    SELECTED_COLOR = (255, 255, 0)
    HINT_COLOR = (0, 255, 255)
    BUTTON_COLOR = (70, 70, 70)
    BUTTON_HOVER_COLOR = (100, 100, 100)
    
    def __init__(self):
        """Initialize the renderer."""
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("Mahjong Solitaire")
        
        self.clock = pygame.time.Clock()
        self.tile_images = {}
        self.load_tile_images()
        
        # UI elements
        self.buttons = {}
        self.hovered_tile = None
        self.selected_tiles = []
        self.hint_tiles = []
        
    def load_tile_images(self):
        """Load all tile images from assets folder."""
        assets_dir = "assets/tiles"
        
        # Check if images exist, if not create them
        if not os.path.exists(assets_dir) or len(os.listdir(assets_dir)) == 0:
            from create_tiles import create_simple_tile_images
            create_simple_tile_images()
        
        # Load suited tiles
        for suit in ['bamboo', 'character', 'dot']:
            for rank in range(1, 10):
                filename = f"{assets_dir}/{suit}_{rank}.png"
                if os.path.exists(filename):
                    self.tile_images[f"{suit}-{rank}"] = pygame.image.load(filename)
        
        # Load wind tiles
        for wind in ['east', 'south', 'west', 'north']:
            filename = f"{assets_dir}/wind_{wind}.png"
            if os.path.exists(filename):
                self.tile_images[f"wind-{wind}"] = pygame.image.load(filename)
        
        # Load dragon tiles
        for dragon in ['red', 'green', 'white']:
            filename = f"{assets_dir}/dragon_{dragon}.png"
            if os.path.exists(filename):
                self.tile_images[f"dragon-{dragon}"] = pygame.image.load(filename)
        
        # Load flower tiles
        for flower_num in range(1, 5):
            filename = f"{assets_dir}/flower_{flower_num}.png"
            if os.path.exists(filename):
                self.tile_images[f"flower-{flower_num}"] = pygame.image.load(filename)
        
        # Load season tiles
        for season_num in range(1, 5):
            filename = f"{assets_dir}/season_{season_num}.png"
            if os.path.exists(filename):
                self.tile_images[f"season-{season_num}"] = pygame.image.load(filename)
    
    def get_tile_image_key(self, tile):
        """Get the image key for a tile."""
        return str(tile)
    
    def get_tile_screen_pos(self, tile):
        """
        Convert tile board position to screen coordinates.
        
        Args:
            tile: Tile object
            
        Returns:
            tuple: (screen_x, screen_y) coordinates
        """
        # Offset based on layer for 3D effect
        layer_offset_x = tile.z * 3
        layer_offset_y = tile.z * 3
        
        # Base position centered in screen
        base_x = 200
        base_y = 100
        
        screen_x = base_x + (tile.x * (self.TILE_WIDTH + self.TILE_SPACING)) + layer_offset_x
        screen_y = base_y + (tile.y * (self.TILE_HEIGHT + self.TILE_SPACING)) + layer_offset_y
        
        return int(screen_x), int(screen_y)
    
    def render_tile(self, tile, highlight=False, hint=False):
        """
        Render a single tile.
        
        Args:
            tile: Tile object to render
            highlight: Whether to highlight the tile (selected)
            hint: Whether to show as a hint
        """
        screen_x, screen_y = self.get_tile_screen_pos(tile)
        
        # Get tile image
        image_key = self.get_tile_image_key(tile)
        if image_key in self.tile_images:
            image = self.tile_images[image_key]
            self.screen.blit(image, (screen_x, screen_y))
        else:
            # Fallback: draw a rectangle
            pygame.draw.rect(self.screen, (200, 200, 200),
                           (screen_x, screen_y, self.TILE_WIDTH, self.TILE_HEIGHT))
        
        # Draw highlight border if selected
        if highlight:
            pygame.draw.rect(self.screen, self.SELECTED_COLOR,
                           (screen_x - 2, screen_y - 2, 
                            self.TILE_WIDTH + 4, self.TILE_HEIGHT + 4), 3)
        
        # Draw hint border
        if hint:
            pygame.draw.rect(self.screen, self.HINT_COLOR,
                           (screen_x - 2, screen_y - 2, 
                            self.TILE_WIDTH + 4, self.TILE_HEIGHT + 4), 2)
    
    def render_board(self, board):
        """
        Render the entire game board.
        
        Args:
            board: Board object to render
        """
        # Clear screen
        self.screen.fill(self.BG_COLOR)
        
        # Sort tiles by layer (render bottom layers first)
        sorted_tiles = sorted(board.tiles, key=lambda t: (t.z, t.y, t.x))
        
        # Render each tile
        for tile in sorted_tiles:
            is_selected = tile in self.selected_tiles
            is_hint = tile in self.hint_tiles
            self.render_tile(tile, highlight=is_selected, hint=is_hint)
    
    def render_ui(self, game_state):
        """
        Render UI elements (buttons, text, etc).
        
        Args:
            game_state: Dictionary containing game state information
        """
        font = pygame.font.Font(None, 36)
        small_font = pygame.font.Font(None, 24)
        
        # Render tile count
        tiles_text = font.render(f"Tiles: {game_state.get('tiles_remaining', 0)}", 
                                 True, self.TEXT_COLOR)
        self.screen.blit(tiles_text, (10, 10))
        
        # Render moves
        moves_text = font.render(f"Moves: {game_state.get('moves', 0)}", 
                                True, self.TEXT_COLOR)
        self.screen.blit(moves_text, (10, 50))
        
        # Render time
        time_text = font.render(f"Time: {game_state.get('time', 0)}s", 
                               True, self.TEXT_COLOR)
        self.screen.blit(time_text, (10, 90))
        
        # Render buttons
        button_y = self.WINDOW_HEIGHT - 60
        button_spacing = 120
        
        buttons_config = [
            ('new_game', 'New Game', 10),
            ('undo', 'Undo', 130),
            ('hint', 'Hint', 250),
            ('quit', 'Quit', 370),
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        
        for btn_id, btn_text, btn_x in buttons_config:
            btn_rect = pygame.Rect(btn_x, button_y, 110, 40)
            self.buttons[btn_id] = btn_rect
            
            # Check if mouse is hovering
            is_hover = btn_rect.collidepoint(mouse_pos)
            btn_color = self.BUTTON_HOVER_COLOR if is_hover else self.BUTTON_COLOR
            
            pygame.draw.rect(self.screen, btn_color, btn_rect, border_radius=5)
            pygame.draw.rect(self.screen, self.TEXT_COLOR, btn_rect, 2, border_radius=5)
            
            text = small_font.render(btn_text, True, self.TEXT_COLOR)
            text_rect = text.get_rect(center=btn_rect.center)
            self.screen.blit(text, text_rect)
    
    def get_tile_at_mouse(self, board, mouse_pos):
        """
        Get the topmost tile at the mouse position.
        
        Args:
            board: Board object
            mouse_pos: (x, y) mouse coordinates
            
        Returns:
            Tile object or None
        """
        # Sort tiles by layer (highest first) to get topmost tile
        sorted_tiles = sorted(board.tiles, key=lambda t: -t.z)
        
        for tile in sorted_tiles:
            screen_x, screen_y = self.get_tile_screen_pos(tile)
            tile_rect = pygame.Rect(screen_x, screen_y, self.TILE_WIDTH, self.TILE_HEIGHT)
            
            if tile_rect.collidepoint(mouse_pos):
                return tile
        
        return None
    
    def get_button_at_mouse(self, mouse_pos):
        """
        Get the button ID at the mouse position.
        
        Args:
            mouse_pos: (x, y) mouse coordinates
            
        Returns:
            str: Button ID or None
        """
        for btn_id, btn_rect in self.buttons.items():
            if btn_rect.collidepoint(mouse_pos):
                return btn_id
        return None
    
    def update_display(self):
        """Update the display."""
        pygame.display.flip()
        self.clock.tick(60)  # 60 FPS
    
    def quit(self):
        """Clean up and quit pygame."""
        pygame.quit()
