"""
Game Constants Module.

This module defines global constants used throughout the Mahjong project,
including tile dimensions, suit identifiers, and GUI configuration.
"""

# --- LOGIC CONSTANTS (PHASE 1) ---

# Tile Suits
SUIT_DOTS = "Dots"
SUIT_BAMBOO = "Bamboo"
SUIT_CHARACTERS = "Characters"
SUIT_WINDS = "Winds"
SUIT_DRAGONS = "Dragones"
SUIT_FLOWERS = "Flowers"
SUIT_SEASONS = "Seasons"

# Logical Tile Dimensions (for collision math)
TILE_WIDTH = 2
TILE_HEIGHT = 2

# --- GUI CONFIGURATION (PHASE 2) ---

# Colors (R, G, B)
COLOR_BACKGROUND = (0, 100, 0)      # Dark Green (Table)
COLOR_TILE_FACE = (255, 250, 240)   # Cream/White (Bone color)
COLOR_TILE_SIDE = (200, 190, 160)   # Darker Cream (3D depth)
COLOR_TEXT = (0, 0, 0)              # Black
COLOR_HIGHLIGHT = (255, 215, 0)     # Gold (Selected tile)
COLOR_BORDER = (50, 50, 50)         # Dark Grey (Tile border)
COLOR_HINT = (0, 255, 255)          # Cyan (Pista/Ayuda) <--- NUEVO
COLOR_BUTTON = (50, 50, 200)        # Azul oscuro para el botón

# Screen Dimensions
SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
FPS = 60

# Visual Tile Size (Pixels)
# Logic size is 2x2, but visual size needs to be bigger.
# Multiplier to convert Logic Coords -> Screen Pixels.
TILE_SIZE_SCALE = 24 

# Actual drawing size of a tile in pixels
VISUAL_WIDTH = 2 * TILE_SIZE_SCALE    # 48 pixels wide
VISUAL_HEIGHT = 2.6 * TILE_SIZE_SCALE # Slightly taller for 3D look (approx 62px)

# ... (Resto del archivo igual) ...

# 3D Depth offset
# Cambiamos esto para desplazar las capas superiores hacia la DERECHA y ARRIBA
# Esto suele ayudar a ver mejor los laterales libres.
LAYER_SHIFT_X = 5
LAYER_SHIFT_Y = -5