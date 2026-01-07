# constants.py

# --- COLORES ---
COLOR_BACKGROUND = (0, 100, 0)      # Tapete Verde
COLOR_TILE_FACE = (250, 240, 230)   # Blanco Hueso (para el fallback de texto)
# CAMBIO: Un marrón más oscuro y profundo para la sombra lateral
COLOR_TILE_SIDE = (100, 50, 10)     
COLOR_BORDER = (0, 0, 0)            # Negro
COLOR_HIGHLIGHT = (255, 215, 0)     # Oro (Selección)
COLOR_HINT = (0, 255, 255)          # Cian (Pista)
COLOR_TEXT = (0, 0, 0)
COLOR_BUTTON = (50, 50, 200)

# --- CONFIGURACIÓN DE PANTALLA ---
# Dejamos el tamaño actual, el tablero grande debería caber bien.
SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 756
FPS = 60

# --- MEDIDAS FICHAS (SUPER-GRANDES & 3D MEJORADO) ---

# 1. DIMENSIONES LÓGICAS (NO TOCAR)
TILE_WIDTH = 2
TILE_HEIGHT = 2

# 2. DIMENSIONES VISUALES (AUMENTADAS UN ~30%)
# Antes 58x82 -> Ahora 74x104
VISUAL_WIDTH = 74     
VISUAL_HEIGHT = 104    

# 3. ESCALA Y RELIEVE
# TILE_SIZE_SCALE = VISUAL_WIDTH / TILE_WIDTH = 74 / 2 = 37
TILE_SIZE_SCALE = 37  
# Altura de capa y desplazamiento aumentados para más efecto 3D
LAYER_SHIFT_X = -8    # Antes -6
LAYER_SHIFT_Y = -8    # Antes -6
TILE_THICKNESS = 10   # Antes 8

# --- PALOS BARAJA ESPAÑOLA ---
SUIT_COINS = "Coins"
SUIT_CUPS = "Cups"
SUIT_SWORDS = "Swords"
SUIT_CLUBS = "Clubs"

TYPE_KNIGHT = "Knight"
TYPE_JOKER = "Joker"
TYPE_JACK = "Jack"
TYPE_KING = "King"