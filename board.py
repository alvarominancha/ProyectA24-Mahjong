"""
Board Module.

This module manages the game board logic, including tile generation, 
layout positioning, collision detection, and matching rules.
"""

import random
import constants as c
import layouts
from tile import Tile

class Board:
    """
    Represents the Mahjong board state.
    Handles the deck generation, layout assignment, and move validation.
    """

    def __init__(self, layout_mode, difficulty):
        """
        Initializes the board with a specific layout and difficulty.
        
        Args:
            layout_mode (str): The shape of the map (TURTLE, BUTTERFLY, COLOSSEUM).
            difficulty (str): The complexity of the deck (EASY, MEDIUM, HARD).
        """
        self.tiles = []
        
        # --- 1. LOAD LAYOUT POSITIONS ---
        if layout_mode == "BUTTERFLY":
            self.positions = layouts.get_butterfly_layout()
        elif layout_mode == "COLOSSEUM":
            self.positions = layouts.get_colosseum_layout()
        else:
            self.positions = layouts.get_turtle_layout()
            
        # --- 2. GENERATE DECK & ASSIGN POSITIONS ---
        self._generate_custom_deck(len(self.positions), difficulty)
        self._assign_positions()

    def _generate_custom_deck(self, total_needed, difficulty):
        """
        Generates a balanced deck of tiles based on the requested difficulty.
        Ensures matching pairs are available.
        """
        self.tiles = []
        available_types = []
        
        # Base Configuration
        suits = [c.SUIT_COINS, c.SUIT_CUPS, c.SUIT_SWORDS]
        values = list(range(1, 10)) 
        
        # Special Sets definitions
        special_sets = [
            (c.TYPE_KNIGHT, ["Coins", "Cups", "Swords", "Clubs"]),
            (c.TYPE_JACK, ["Coins", "Cups", "Swords", "Clubs"]),
            (c.TYPE_KING, ["Coins", "Cups", "Swords", "Clubs"]),
            (c.TYPE_JOKER, ["Red", "Green", "Blue"])
        ]
        
        # --- DIFFICULTY ADJUSTMENT ---
        if difficulty == "MEDIUM":
            # Remove Kings and Jokers
            special_sets = [
                (c.TYPE_KNIGHT, ["Coins", "Cups", "Swords", "Clubs"]),
                (c.TYPE_JACK, ["Coins", "Cups", "Swords", "Clubs"])
            ]
            
        elif difficulty == "EASY":
            # Simplified deck: Coins and Cups only, values 1-7
            suits = [c.SUIT_COINS, c.SUIT_CUPS]
            values = list(range(1, 8))
            special_sets = []

        # Build pool of types
        for s in suits:
            for v in values:
                available_types.append((s, v))
        
        for type_name, subtypes in special_sets:
            for sub in subtypes:
                available_types.append((type_name, sub))

        # --- FILL DECK WITH PAIRS ---
        tile_id = 0
        current_deck = []
        
        while len(current_deck) < total_needed:
            stype = random.choice(available_types)
            # Add pairs to ensure solvability
            for _ in range(2):
                if len(current_deck) < total_needed:
                    current_deck.append(Tile(stype[0], stype[1], tile_id))
                    tile_id += 1
        
        random.shuffle(current_deck)
        self.tiles = current_deck

    def _assign_positions(self):
        """Maps the logical 3D coordinates to the tile objects."""
        limit = min(len(self.tiles), len(self.positions))
        for i in range(limit):
            x, y, z = self.positions[i]
            self.tiles[i].set_position(x, y, z)

    # --- GAMEPLAY LOGIC ---

    def can_move(self, tile):
        """
        Determines if a tile is 'free' to be selected.
        Rule: A tile is free if no tile is on top AND (left is free OR right is free).
        """
        left, right = tile.x, tile.x + c.TILE_WIDTH
        top, bottom = tile.y, tile.y + c.TILE_HEIGHT
        layer = tile.z
        
        blocked_above = False
        blocked_left = False
        blocked_right = False
        
        for other in self.tiles:
            if other.id == tile.id or not other.is_visible: continue
            
            # Check blocking tile above (Z+1)
            if other.z == layer + 1:
                # Collision detection (Axis-Aligned Bounding Box)
                if (other.x < right and other.x + c.TILE_WIDTH > left and 
                    other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    blocked_above = True
            
            # Check neighbors (Same Z)
            if other.z == layer:
                # Left neighbor
                if (other.x + c.TILE_WIDTH == left and 
                    other.y < bottom and other.y + c.TILE_HEIGHT > top): 
                    blocked_left = True
                # Right neighbor
                if (other.x == right and 
                    other.y < bottom and other.y + c.TILE_HEIGHT > top): 
                    blocked_right = True
                    
        # Returns True only if top is free AND at least one side is free
        return not blocked_above and not (blocked_left and blocked_right)

    def is_match(self, t1, t2):
        """
        Checks if two tiles are a valid match according to game rules.
        Includes special wildcard logic for Jacks and Kings.
        """
        # Special Bonus Rules (Wildcards)
        if t1.suit == c.TYPE_JACK and t2.suit == c.TYPE_JACK: return True
        if t1.suit == c.TYPE_KING and t2.suit == c.TYPE_KING: return True
        
        # Standard Rules (Exact Match)
        if t1.suit == t2.suit and t1.value == t2.value: return True
        
        return False
        
    def has_valid_moves(self):
        """Checks if there is at least one valid pair available to play."""
        visible_tiles = [t for t in self.tiles if t.is_visible and self.can_move(t)]
        
        for i in range(len(visible_tiles)):
            for j in range(i + 1, len(visible_tiles)):
                if self.is_match(visible_tiles[i], visible_tiles[j]): 
                    return True
        return False

    def get_hint_pair(self):
        """Finds and returns a valid matching pair for the hint system."""
        visible_tiles = [t for t in self.tiles if t.is_visible and self.can_move(t)]
        
        for i in range(len(visible_tiles)):
            for j in range(i + 1, len(visible_tiles)):
                if self.is_match(visible_tiles[i], visible_tiles[j]): 
                    return (visible_tiles[i], visible_tiles[j])
        return None

    def shuffle_remaining(self):
        """Rearranges the suits and values of the visible tiles, keeping positions."""
        vis = [t for t in self.tiles if t.is_visible]
        content = [(t.suit, t.value) for t in vis]
        random.shuffle(content)
        
        for i, t in enumerate(vis):
            t.suit, t.value = content[i]
            t.is_selected = False

    # --- PERSISTENCE ---

    def get_state(self): 
        """Serializes the board state for saving."""
        return [t.to_dict() for t in self.tiles]

    def set_state(self, tiles_data):
        """Restores the board state from saved data."""
        self.tiles = []
        for t_data in tiles_data:
            self.tiles.append(Tile.from_dict(t_data))