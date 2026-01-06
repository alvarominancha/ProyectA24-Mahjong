"""
Tile Module.

This module contains the definition of the Tile class, which represents
the fundamental unit (the game piece) in Mahjong Solitaire.
"""

class Tile:
    """
    Represents a single Mahjong tile and its state.

    Attributes:
        suit (str): The suit of the tile (e.g., Bamboo, Dots, Winds).
        value (str | int): The specific value (1-9, North, Red, etc.).
        id (int): A unique identifier for the tile.
        x (int): The logical X coordinate on the board grid.
        y (int): The logical Y coordinate on the board grid.
        z (int): The Z coordinate (layer/stack height) on the board.
        is_visible (bool): Indicates if the tile should be rendered.
        is_selected (bool): Indicates if the tile is currently selected by the user.
    """

    def __init__(self, suit, value, tile_id):
        """
        Initializes a new Tile instance.

        Args:
            suit (str): The suit/family of the tile.
            value (str | int): The specific value of the tile.
            tile_id (int): The unique ID assigned by the deck generator.
        """
        self.id = tile_id
        self.suit = suit
        self.value = value
        
        # Initial coordinates (set later by the layout loader)
        self.x = 0
        self.y = 0
        self.z = 0
        
        self.is_visible = True
        self.is_selected = False  # <--- NUEVO ATRIBUTO

    def set_position(self, x, y, z):
        """
        Sets the tile's position in the 3D board space.

        Args:
            x (int): The horizontal position.
            y (int): The vertical position.
            z (int): The layer or stack height.
        """
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        """
        Returns a formal string representation of the tile.
        Useful for debugging and logging.

        Returns:
            str: A readable description of the tile and its position.
        """
        return f"[{self.suit}-{self.value} (ID:{self.id}) at ({self.x},{self.y},{self.z})]"