"""
Constants Module

This module defines global configuration variables for the Spanish Mahjong game.
It includes settings for colors, screen dimensions, tile geometry, and gameplay constants.
"""

# --- COLOR PALETTE (RGB) ---
COLOR_BACKGROUND = (0, 100, 0)      # Dark Green (Felt table look)
COLOR_TILE_FACE = (250, 240, 230)   # Off-white / Bone color
COLOR_TILE_SIDE = (80, 40, 0)       # Dark Brown (Wood effect for 3D depth)
COLOR_BORDER = (0, 0, 0)            # Black
COLOR_HIGHLIGHT = (255, 215, 0)     # Gold (Selected tile)
COLOR_HINT = (0, 255, 255)          # Cyan (Hint)
COLOR_TEXT = (0, 0, 0)
COLOR_BUTTON = (50, 50, 200)

# --- SCREEN SETTINGS ---
SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 800
FPS = 60

# --- TILE GEOMETRY & RENDERING ---

# Logical dimensions (Grid units)
TILE_WIDTH = 2
TILE_HEIGHT = 2

# Visual dimensions (Pixels)
VISUAL_WIDTH = 54     
VISUAL_HEIGHT = 76    

# --- ISOMETRIC SCALING ---
# Controls the spacing between tiles to create the pseudo-3D layout.

# Horizontal Spacing:
# Compact value to keep tiles close side-by-side.
TILE_SCALE_X = 26 

# Vertical Spacing:
# Larger value to minimize vertical overlap and improve visibility of stacked tiles.
TILE_SCALE_Y = 36

# --- 3D DEPTH EFFECT ---
# Offsets for drawing the "side" of the tile to create volume.
LAYER_SHIFT_X = -3
LAYER_SHIFT_Y = -3
TILE_THICKNESS = 4    # Thickness of the tile edge (pixels)

# --- GAMEPLAY IDENTIFIERS ---
SUIT_COINS = "Coins"
SUIT_CUPS = "Cups"
SUIT_SWORDS = "Swords"
SUIT_CLUBS = "Clubs"

TYPE_KNIGHT = "Knight"
TYPE_JOKER = "Joker"
TYPE_JACK = "Jack"
TYPE_KING = "King"