"""
TileSet class for Mahjong game.
Manages the complete set of Mahjong tiles.
"""

from tile import Tile
import random


class TileSet:
    """Manages the complete set of 144 Mahjong tiles."""
    
    def __init__(self):
        """Initialize a complete set of Mahjong tiles."""
        self.tiles = []
        self._create_tiles()
    
    def _create_tiles(self):
        """Create all 144 Mahjong tiles according to standard rules."""
        tile_id = 0
        
        # Create suited tiles (bamboo, character, dot)
        # Each suit has ranks 1-9, with 4 copies of each
        for suit in [Tile.BAMBOO, Tile.CHARACTER, Tile.DOT]:
            for rank in range(1, 10):
                for copy in range(4):
                    self.tiles.append(Tile(suit, rank, tile_id))
                    tile_id += 1
        
        # Create wind tiles (4 types, 4 copies each = 16 tiles)
        for wind in [Tile.EAST, Tile.SOUTH, Tile.WEST, Tile.NORTH]:
            for copy in range(4):
                self.tiles.append(Tile(Tile.WIND, wind, tile_id))
                tile_id += 1
        
        # Create dragon tiles (3 types, 4 copies each = 12 tiles)
        for dragon in [Tile.RED, Tile.GREEN, Tile.WHITE]:
            for copy in range(4):
                self.tiles.append(Tile(Tile.DRAGON, dragon, tile_id))
                tile_id += 1
        
        # Create flower tiles (4 unique flowers, 1 copy each = 4 tiles)
        for flower_num in range(1, 5):
            self.tiles.append(Tile(Tile.FLOWER, flower_num, tile_id))
            tile_id += 1
        
        # Create season tiles (4 unique seasons, 1 copy each = 4 tiles)
        for season_num in range(1, 5):
            self.tiles.append(Tile(Tile.SEASON, season_num, tile_id))
            tile_id += 1
    
    def shuffle(self):
        """Shuffle the tiles randomly."""
        random.shuffle(self.tiles)
    
    def get_tiles(self):
        """
        Get all tiles in the set.
        
        Returns:
            list: List of all Tile objects
        """
        return self.tiles.copy()
    
    def count(self):
        """
        Get the total number of tiles.
        
        Returns:
            int: Number of tiles in the set
        """
        return len(self.tiles)
    
    def get_tiles_by_suit(self, suit):
        """
        Get all tiles of a specific suit.
        
        Args:
            suit: The suit to filter by
            
        Returns:
            list: List of tiles matching the suit
        """
        return [tile for tile in self.tiles if tile.suit == suit]
    
    def get_tiles_by_rank(self, rank):
        """
        Get all tiles of a specific rank.
        
        Args:
            rank: The rank to filter by
            
        Returns:
            list: List of tiles matching the rank
        """
        return [tile for tile in self.tiles if tile.rank == rank]
    
    def __len__(self):
        """Return the number of tiles."""
        return len(self.tiles)
    
    def __str__(self):
        """String representation of the tile set."""
        return f"TileSet({len(self.tiles)} tiles)"
