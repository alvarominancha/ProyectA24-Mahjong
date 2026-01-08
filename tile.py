"""
Tile Module.

This module defines the Tile class, which represents the fundamental 
game piece in Mahjong Solitaire. It handles the state, position, 
and serialization of individual tiles.
"""

class Tile:
    """
    Represents a single Mahjong tile and its current state on the board.

    Attributes:
        suit (str): The suit/family of the tile (e.g., 'Coins', 'Cups').
        value (str | int): The specific value (1-9, King, Jack, etc.).
        id (int): A unique identifier for tracking this specific instance.
        x (int): The logical grid X coordinate.
        y (int): The logical grid Y coordinate.
        z (int): The layer/stack height (Z coordinate).
        is_visible (bool): True if the tile is still in play; False if matched/removed.
        is_selected (bool): True if the user has currently clicked/selected this tile.
    """

    def __init__(self, suit, value, tile_id):
        """
        Initializes a new Tile instance.

        Args:
            suit (str): The suit of the tile.
            value (str | int): The value or rank of the tile.
            tile_id (int): Unique ID assigned during deck generation.
        """
        self.id = tile_id
        self.suit = suit
        self.value = value
        
        # Initial coordinates (defaults to 0, updated by layout loader)
        self.x = 0
        self.y = 0
        self.z = 0
        
        self.is_visible = True
        self.is_selected = False

    def set_position(self, x, y, z):
        """
        Sets the tile's position in the 3D board space.

        Args:
            x (int): The horizontal grid position.
            y (int): The vertical grid position.
            z (int): The layer or stack height.
        """
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """
        Returns a string representation of the tile for debugging.

        Returns:
            str: Format '[Suit-Value (ID) at (x,y,z)]'
        """
        return f"[{self.suit}-{self.value} (ID:{self.id}) at ({self.x},{self.y},{self.z})]"

    def to_dict(self):
        """
        Serializes the tile object into a dictionary.
        Used for saving the game state to a file.

        Returns:
            dict: A dictionary containing all tile attributes.
        """
        return {
            "suit": self.suit,
            "value": self.value,
            "id": self.id,
            "x": self.x,
            "y": self.y,
            "z": self.z,
            "is_visible": self.is_visible,
            "is_selected": self.is_selected
        }

    @staticmethod
    def from_dict(data):
        """
        Factory method to reconstruct a Tile object from a dictionary.
        Used when loading a saved game.

        Args:
            data (dict): The dictionary containing tile data.

        Returns:
            Tile: A fully restored Tile instance.
        """
        # Initialize basic identity
        tile = Tile(data["suit"], data["value"], data["id"])
        
        # Restore position and state
        tile.x = data["x"]
        tile.y = data["y"]
        tile.z = data["z"]
        tile.is_visible = data["is_visible"]
        tile.is_selected = data["is_selected"]
        
        return tile