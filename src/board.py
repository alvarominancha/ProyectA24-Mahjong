"""
Board class for Mahjong game.
Manages the game board layout and tile positions.
"""

from tileset import TileSet


class Board:
    """Manages the Mahjong game board and tile layout."""
    
    # Standard turtle/pyramid layout pattern
    TURTLE_LAYOUT = [
        # Layer 0 (bottom)
        [
            "  XXXX  ",
            " XXXXXX ",
            "XXXXXXXX",
            " XXXXXX ",
            "  XXXX  "
        ],
        # Layer 1
        [
            "   XX   ",
            "  XXXX  ",
            "  XXXX  ",
            "  XXXX  ",
            "   XX   "
        ],
        # Layer 2
        [
            "        ",
            "   XX   ",
            "   XX   ",
            "   XX   ",
            "        "
        ],
        # Layer 3
        [
            "        ",
            "    X   ",
            "        ",
            "        ",
            "        "
        ],
        # Layer 4 (top)
        [
            "        ",
            "   X    ",
            "        ",
            "        ",
            "        "
        ]
    ]
    
    def __init__(self, layout=None):
        """
        Initialize the game board.
        
        Args:
            layout: Optional custom layout pattern (list of layers)
        """
        self.tiles = []
        self.layout = layout if layout else self.TURTLE_LAYOUT
        self.removed_tiles = []
        self.move_history = []
        
    def setup_board(self, tileset):
        """
        Set up the board with tiles from a tileset.
        
        Args:
            tileset: TileSet object containing shuffled tiles
        """
        tiles = tileset.get_tiles()
        tile_index = 0
        
        # Place tiles according to the layout
        for z, layer in enumerate(self.layout):
            for y, row in enumerate(layer):
                for x, cell in enumerate(row):
                    if cell == 'X' and tile_index < len(tiles):
                        tile = tiles[tile_index]
                        tile.x = x
                        tile.y = y
                        tile.z = z
                        tile.selectable = True
                        self.tiles.append(tile)
                        tile_index += 1
        
    def get_tile_at(self, x, y, z):
        """
        Get the tile at specific coordinates.
        
        Args:
            x: X coordinate
            y: Y coordinate
            z: Z coordinate (layer)
            
        Returns:
            Tile object or None if no tile at that position
        """
        for tile in self.tiles:
            if tile.x == x and tile.y == y and tile.z == z:
                return tile
        return None
    
    def get_free_tiles(self):
        """
        Get all tiles that are currently free to select.
        
        Returns:
            list: List of free Tile objects
        """
        return [tile for tile in self.tiles if tile.is_free(self)]
    
    def get_matching_pairs(self):
        """
        Get all valid matching pairs of free tiles.
        
        Returns:
            list: List of tuples (tile1, tile2) representing valid pairs
        """
        pairs = []
        free_tiles = self.get_free_tiles()
        
        for i, tile1 in enumerate(free_tiles):
            for tile2 in free_tiles[i+1:]:
                if tile1.matches(tile2):
                    pairs.append((tile1, tile2))
        
        return pairs
    
    def remove_tiles(self, tile1, tile2):
        """
        Remove a matching pair of tiles from the board.
        
        Args:
            tile1: First tile to remove
            tile2: Second tile to remove
            
        Returns:
            bool: True if tiles were removed, False otherwise
        """
        # Validate the move
        if tile1 not in self.tiles or tile2 not in self.tiles:
            return False
        
        if not tile1.is_free(self) or not tile2.is_free(self):
            return False
        
        if not tile1.matches(tile2):
            return False
        
        # Remove the tiles
        self.tiles.remove(tile1)
        self.tiles.remove(tile2)
        
        # Store in history for undo
        self.move_history.append((tile1, tile2))
        self.removed_tiles.extend([tile1, tile2])
        
        return True
    
    def undo_last_move(self):
        """
        Undo the last tile removal.
        
        Returns:
            bool: True if undo was successful, False if no moves to undo
        """
        if not self.move_history:
            return False
        
        tile1, tile2 = self.move_history.pop()
        self.tiles.append(tile1)
        self.tiles.append(tile2)
        self.removed_tiles.remove(tile1)
        self.removed_tiles.remove(tile2)
        
        return True
    
    def is_game_won(self):
        """
        Check if the game is won (all tiles removed).
        
        Returns:
            bool: True if all tiles are removed
        """
        return len(self.tiles) == 0
    
    def is_game_lost(self):
        """
        Check if the game is lost (no valid moves remaining).
        
        Returns:
            bool: True if no valid moves remain and tiles still on board
        """
        if len(self.tiles) == 0:
            return False
        
        return len(self.get_matching_pairs()) == 0
    
    def get_hint(self):
        """
        Get a hint for the next valid move.
        
        Returns:
            tuple: (tile1, tile2) or None if no valid moves
        """
        pairs = self.get_matching_pairs()
        if pairs:
            return pairs[0]
        return None
    
    def count_tiles(self):
        """
        Get the number of tiles remaining on the board.
        
        Returns:
            int: Number of tiles on board
        """
        return len(self.tiles)
    
    def clear_board(self):
        """Remove all tiles from the board."""
        self.tiles.clear()
        self.removed_tiles.clear()
        self.move_history.clear()
    
    def __str__(self):
        """String representation of the board."""
        return f"Board({len(self.tiles)} tiles remaining)"
