"""
Main game engine for Mahjong Solitaire.
Manages game state, input handling, and game flow.
"""

import pygame
import time
from board import Board
from tileset import TileSet
from renderer import GameRenderer


class MahjongGame:
    """Main game class that manages the Mahjong game."""
    
    # Game states
    STATE_MENU = "menu"
    STATE_PLAYING = "playing"
    STATE_PAUSED = "paused"
    STATE_WON = "won"
    STATE_LOST = "lost"
    
    def __init__(self):
        """Initialize the game."""
        self.renderer = GameRenderer()
        self.board = Board()
        self.tileset = TileSet()
        
        self.state = self.STATE_MENU
        self.selected_tiles = []
        self.moves = 0
        self.start_time = None
        self.elapsed_time = 0
        
        self.running = True
        
    def new_game(self):
        """Start a new game."""
        # Reset board
        self.board.clear_board()
        
        # Create and shuffle tileset
        self.tileset = TileSet()
        self.tileset.shuffle()
        
        # Setup board
        self.board.setup_board(self.tileset)
        
        # Reset game state
        self.selected_tiles = []
        self.renderer.selected_tiles = []
        self.renderer.hint_tiles = []
        self.moves = 0
        self.start_time = time.time()
        self.elapsed_time = 0
        self.state = self.STATE_PLAYING
    
    def handle_tile_click(self, tile):
        """
        Handle clicking on a tile.
        
        Args:
            tile: The clicked Tile object
        """
        if self.state != self.STATE_PLAYING:
            return
        
        # Check if tile is free
        if not tile.is_free(self.board):
            return
        
        # If tile already selected, deselect it
        if tile in self.selected_tiles:
            self.selected_tiles.remove(tile)
            self.renderer.selected_tiles.remove(tile)
            return
        
        # If we already have 2 tiles selected, deselect all
        if len(self.selected_tiles) >= 2:
            self.selected_tiles.clear()
            self.renderer.selected_tiles.clear()
        
        # Select the tile
        self.selected_tiles.append(tile)
        self.renderer.selected_tiles.append(tile)
        
        # If we have 2 tiles selected, try to match them
        if len(self.selected_tiles) == 2:
            tile1, tile2 = self.selected_tiles
            
            if self.board.remove_tiles(tile1, tile2):
                # Successful match
                self.moves += 1
                self.selected_tiles.clear()
                self.renderer.selected_tiles.clear()
                self.renderer.hint_tiles.clear()
                
                # Check win/loss conditions
                if self.board.is_game_won():
                    self.state = self.STATE_WON
                elif self.board.is_game_lost():
                    self.state = self.STATE_LOST
            else:
                # Invalid match - tiles don't match
                # Keep them selected so player sees why
                pass
    
    def handle_button_click(self, button_id):
        """
        Handle clicking on a button.
        
        Args:
            button_id: ID of the clicked button
        """
        if button_id == 'new_game':
            self.new_game()
        elif button_id == 'undo':
            if self.board.undo_last_move():
                self.moves = max(0, self.moves - 1)
                self.selected_tiles.clear()
                self.renderer.selected_tiles.clear()
                self.renderer.hint_tiles.clear()
        elif button_id == 'hint':
            hint = self.board.get_hint()
            if hint:
                self.renderer.hint_tiles = list(hint)
            else:
                self.renderer.hint_tiles = []
        elif button_id == 'quit':
            self.running = False
    
    def handle_events(self):
        """Handle pygame events."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    mouse_pos = pygame.mouse.get_pos()
                    
                    # Check if a button was clicked
                    button_id = self.renderer.get_button_at_mouse(mouse_pos)
                    if button_id:
                        self.handle_button_click(button_id)
                        continue
                    
                    # Check if a tile was clicked
                    tile = self.renderer.get_tile_at_mouse(self.board, mouse_pos)
                    if tile:
                        self.handle_tile_click(tile)
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_n:
                    self.new_game()
                elif event.key == pygame.K_u:
                    self.handle_button_click('undo')
                elif event.key == pygame.K_h:
                    self.handle_button_click('hint')
    
    def update(self):
        """Update game state."""
        if self.state == self.STATE_PLAYING and self.start_time:
            self.elapsed_time = int(time.time() - self.start_time)
    
    def render(self):
        """Render the game."""
        # Render board
        self.renderer.render_board(self.board)
        
        # Render UI
        game_state = {
            'tiles_remaining': self.board.count_tiles(),
            'moves': self.moves,
            'time': self.elapsed_time,
        }
        self.renderer.render_ui(game_state)
        
        # Render game over messages
        if self.state == self.STATE_WON:
            self.render_message("You Won!", "Press N for New Game")
        elif self.state == self.STATE_LOST:
            self.render_message("No More Moves!", "Press N for New Game or U to Undo")
        elif self.state == self.STATE_MENU:
            self.render_message("Mahjong Solitaire", "Press N to Start New Game")
        
        self.renderer.update_display()
    
    def render_message(self, title, subtitle):
        """
        Render a centered message on screen.
        
        Args:
            title: Main message text
            subtitle: Secondary message text
        """
        # Semi-transparent overlay
        overlay = pygame.Surface((self.renderer.WINDOW_WIDTH, self.renderer.WINDOW_HEIGHT))
        overlay.set_alpha(128)
        overlay.fill((0, 0, 0))
        self.renderer.screen.blit(overlay, (0, 0))
        
        # Title text
        font = pygame.font.Font(None, 72)
        title_text = font.render(title, True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(self.renderer.WINDOW_WIDTH // 2, 
                                                  self.renderer.WINDOW_HEIGHT // 2 - 40))
        self.renderer.screen.blit(title_text, title_rect)
        
        # Subtitle text
        small_font = pygame.font.Font(None, 36)
        subtitle_text = small_font.render(subtitle, True, (255, 255, 255))
        subtitle_rect = subtitle_text.get_rect(center=(self.renderer.WINDOW_WIDTH // 2, 
                                                        self.renderer.WINDOW_HEIGHT // 2 + 40))
        self.renderer.screen.blit(subtitle_text, subtitle_rect)
    
    def run(self):
        """Main game loop."""
        while self.running:
            self.handle_events()
            self.update()
            self.render()
        
        self.renderer.quit()


def main():
    """Main entry point."""
    game = MahjongGame()
    game.run()


if __name__ == "__main__":
    main()
