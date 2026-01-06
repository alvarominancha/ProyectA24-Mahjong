"""
Tile class for Mahjong game.
Represents a single Mahjong tile with its properties.
"""

class Tile:
    """Represents a single Mahjong tile."""
    
    # Tile suits/types
    BAMBOO = "bamboo"
    CHARACTER = "character"
    DOT = "dot"
    WIND = "wind"
    DRAGON = "dragon"
    FLOWER = "flower"
    SEASON = "season"
    
    # Wind tiles
    EAST = "east"
    SOUTH = "south"
    WEST = "west"
    NORTH = "north"
    
    # Dragon tiles
    RED = "red"
    GREEN = "green"
    WHITE = "white"
    
    def __init__(self, suit, rank=None, unique_id=None):
        """
        Initialize a Mahjong tile.
        
        Args:
            suit: The suit/type of the tile (bamboo, character, dot, wind, dragon, flower, season)
            rank: The rank/number of the tile (1-9 for suited, specific values for honors)
            unique_id: Unique identifier for this specific tile instance
        """
        self.suit = suit
        self.rank = rank
        self.unique_id = unique_id
        self.x = 0  # Board position x
        self.y = 0  # Board position y
        self.z = 0  # Board layer
        self.selectable = True  # Whether this tile can be selected
        
    def matches(self, other):
        """
        Check if this tile matches another tile for removal.
        
        Args:
            other: Another Tile object
            
        Returns:
            bool: True if tiles match, False otherwise
        """
        if not isinstance(other, Tile):
            return False
            
        # Flowers and seasons match any within their own suit
        if self.suit in (self.FLOWER, self.SEASON):
            return self.suit == other.suit
            
        # All other tiles must match exactly on suit and rank
        return self.suit == other.suit and self.rank == other.rank
    
    def is_free(self, board):
        """
        Check if this tile is free to be selected (not blocked).
        
        A tile is free if:
        - No tile is on top of it (higher z-level at same x,y)
        - At least one side (left or right) is not blocked by adjacent tiles
        
        Args:
            board: The Board object containing all tiles
            
        Returns:
            bool: True if tile is free, False otherwise
        """
        if not self.selectable:
            return False
            
        # Check if any tile is on top of this tile
        for tile in board.tiles:
            if tile.z == self.z + 1:
                # Check if the tile above overlaps with this tile
                if (abs(tile.x - self.x) < 1.0 and abs(tile.y - self.y) < 1.0):
                    return False
        
        # Check if at least one side is free
        left_blocked = False
        right_blocked = False
        
        for tile in board.tiles:
            if tile.z == self.z and tile != self:
                # Check left side
                if tile.x == self.x - 1 and abs(tile.y - self.y) < 1.0:
                    left_blocked = True
                # Check right side
                elif tile.x == self.x + 1 and abs(tile.y - self.y) < 1.0:
                    right_blocked = True
        
        # At least one side must be free
        return not (left_blocked and right_blocked)
    
    def __str__(self):
        """String representation of the tile."""
        if self.rank is not None:
            return f"{self.suit}-{self.rank}"
        return f"{self.suit}"
    
    def __repr__(self):
        """Detailed representation of the tile."""
        return f"Tile({self.suit}, {self.rank}, pos=({self.x},{self.y},{self.z}))"
    
    def __eq__(self, other):
        """Check equality based on unique_id if available, otherwise by properties."""
        if not isinstance(other, Tile):
            return False
        if self.unique_id is not None and other.unique_id is not None:
            return self.unique_id == other.unique_id
        return self.suit == other.suit and self.rank == other.rank
    
    def __hash__(self):
        """Make tile hashable for use in sets/dicts."""
        if self.unique_id is not None:
            return hash(self.unique_id)
        return hash((self.suit, self.rank))
