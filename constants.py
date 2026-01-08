# constants.py

# --- COLORES ---
COLOR_BACKGROUND = (0, 100, 0)
COLOR_TILE_FACE = (250, 240, 230)
COLOR_TILE_SIDE = (80, 40, 0)       # <--- CAMBIO: Marrón más oscuro (Más contraste 3D)
COLOR_BORDER = (0, 0, 0)            # Negro puro
COLOR_HIGHLIGHT = (255, 215, 0)
COLOR_HINT = (0, 255, 255)
COLOR_TEXT = (0, 0, 0)
COLOR_BUTTON = (50, 50, 200)

# --- PANTALLA ---
SCREEN_WIDTH = 1450
SCREEN_HEIGHT = 800
FPS = 60

# --- MEDIDAS FICHAS (OPTIMIZADAS PARA CLARIDAD) ---
# --- MEDIDAS FICHAS (PERFIL BAJO Y COMPACTO) ---
TILE_WIDTH = 2
TILE_HEIGHT = 2

# Tamaño visual (Se mantiene igual, se ve bien)
VISUAL_WIDTH = 54     
VISUAL_HEIGHT = 76    

# AQUÍ ESTÁ EL CAMBIO: Separamos X e Y
# Horizontal (29): Compacto, pegaditas laterales (hueco de 4px).
TILE_SCALE_X = 26 

# Vertical (36): Más alto. 
# 36 * 2 = 72px de paso vertical. 
# Como la ficha mide 76, solo se solapan 4px. ¡Mucho más aire vertical!
TILE_SCALE_Y = 36

# RELIEVE (AQUÍ ESTÁ EL CAMBIO)
# Reducimos a la mitad para que el borde marrón esté "pegadito" a la carta.
LAYER_SHIFT_X = -3    # Antes -6
LAYER_SHIFT_Y = -3    # Antes -6
TILE_THICKNESS = 4    # Antes 8 (Borde mucho más fino y sutil)  

# ... (Resto igual) ...
SUIT_COINS = "Coins"
SUIT_CUPS = "Cups"
SUIT_SWORDS = "Swords"
SUIT_CLUBS = "Clubs"
TYPE_KNIGHT = "Knight"
TYPE_JOKER = "Joker"
TYPE_JACK = "Jack"
TYPE_KING = "King"