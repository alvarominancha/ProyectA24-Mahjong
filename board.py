# board.py
import random
import constants as c
import layouts
from tile import Tile

class Board:
    def __init__(self):
        self.tiles = []
        self._generate_spanish_deck() # <--- Nombre nuevo
        self._load_layout()

    def _generate_spanish_deck(self):
        """Genera las 144 fichas usando la estructura de Baraja Española."""
        self.tiles = []
        tile_id = 0
        
        # 1. CARTAS NUMÉRICAS (1 al 9) de OROS, COPAS, ESPADAS
        # (Equivalente a los 3 palos del Mahjong)
        # 3 palos x 9 cartas x 4 copias = 108 fichas
        main_suits = [c.SUIT_COINS, c.SUIT_CUPS, c.SUIT_SWORDS]
        for suit in main_suits:
            for value in range(1, 10): # Del 1 al 9
                for _ in range(4):     # 4 copias de cada
                    self.tiles.append(Tile(suit, value, tile_id))
                    tile_id += 1
        
        # 2. CABALLOS (Knights) - 4 Tipos
        # (Equivalente a Vientos)
        # Usamos los 4 palos para los caballos: Coins, Cups, Swords, Clubs
        # 4 tipos x 4 copias = 16 fichas
        knights = [c.SUIT_COINS, c.SUIT_CUPS, c.SUIT_SWORDS, c.SUIT_CLUBS]
        for k_suit in knights:
            for _ in range(4):
                self.tiles.append(Tile(c.TYPE_KNIGHT, k_suit, tile_id))
                tile_id += 1

        # 3. COMODINES (Jokers) - 3 Tipos
        # (Equivalente a Dragones)
        # 3 tipos x 4 copias = 12 fichas
        jokers = ["Red", "Green", "Blue"] # Tus archivos son Joker_Red, Joker_Green...
        for color in jokers:
            for _ in range(4):
                self.tiles.append(Tile(c.TYPE_JOKER, color, tile_id))
                tile_id += 1
        
        # 4. SOTAS (Jacks) - Bonus 1
        # (Equivalente a Flores)
        # 4 tipos x 1 copia = 4 fichas
        jacks = [c.SUIT_COINS, c.SUIT_CUPS, c.SUIT_SWORDS, c.SUIT_CLUBS]
        for j_suit in jacks:
            self.tiles.append(Tile(c.TYPE_JACK, j_suit, tile_id))
            tile_id += 1

        # 5. REYES (Kings) - Bonus 2
        # (Equivalente a Estaciones)
        # 4 tipos x 1 copia = 4 fichas
        kings = [c.SUIT_COINS, c.SUIT_CUPS, c.SUIT_SWORDS, c.SUIT_CLUBS]
        for k_suit in kings:
            self.tiles.append(Tile(c.TYPE_KING, k_suit, tile_id))
            tile_id += 1
        
        random.shuffle(self.tiles)

    def _load_layout(self):
        # (Esto NO cambia, usa layouts.py igual)
        positions = layouts.get_turtle_layout()
        if len(self.tiles) > len(positions):
            self.tiles = self.tiles[:len(positions)]
        
        for i, tile in enumerate(self.tiles):
            if i < len(positions):
                x, y, z = positions[i]
                tile.set_position(x, y, z)

    def can_move(self, tile):
        # (Copia tu método can_move anterior, ese es pura física y no cambia)
        # ... (código de colisiones igual que antes) ...
        left = tile.x
        right = tile.x + c.TILE_WIDTH
        top = tile.y
        bottom = tile.y + c.TILE_HEIGHT
        layer = tile.z
        
        blocked_above = False
        blocked_left = False
        blocked_right = False
        
        for other in self.tiles:
            if other.id == tile.id: continue
            if not other.is_visible: continue # Importante
            
            if other.z == layer + 1:
                if (other.x < right and other.x + c.TILE_WIDTH > left and
                        other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    blocked_above = True
            
            if other.z == layer:
                if (other.x + c.TILE_WIDTH == left and
                        other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    blocked_left = True
                if (other.x == right and
                        other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    blocked_right = True

        if blocked_above: return False
        if blocked_left and blocked_right: return False
        return True

    def is_match(self, t1, t2):
        """
        NUEVA LÓGICA DE BARAJA ESPAÑOLA.
        """
        # 1. Regla de SOTAS (Jacks) - Bonus
        # Todas las sotas casan entre ellas (sin importar palo)
        if t1.suit == c.TYPE_JACK and t2.suit == c.TYPE_JACK:
            return True
            
        # 2. Regla de REYES (Kings) - Bonus
        # Todos los reyes casan entre ellos
        if t1.suit == c.TYPE_KING and t2.suit == c.TYPE_KING:
            return True
            
        # 3. Regla General (Números, Caballos, Jokers)
        # Deben ser idénticos en Palo y Valor
        if t1.suit == t2.suit and t1.value == t2.value:
            return True
            
        return False

    # (Mantén has_valid_moves, get_hint_pair y shuffle_remaining igual que antes
    # porque solo llaman a can_move e is_match, así que funcionarán solas).
    def has_valid_moves(self):
        free_tiles = [t for t in self.tiles if t.is_visible and self.can_move(t)]
        for i in range(len(free_tiles)):
            for j in range(i + 1, len(free_tiles)):
                if self.is_match(free_tiles[i], free_tiles[j]):
                    return True
        return False

    def get_hint_pair(self):
        free_tiles = [t for t in self.tiles if t.is_visible and self.can_move(t)]
        for i in range(len(free_tiles)):
            for j in range(i + 1, len(free_tiles)):
                if self.is_match(free_tiles[i], free_tiles[j]):
                    return (free_tiles[i], free_tiles[j])
        return None

    def shuffle_remaining(self):
        visible_tiles = [t for t in self.tiles if t.is_visible]
        content_list = [(t.suit, t.value) for t in visible_tiles]
        random.shuffle(content_list)
        for i, tile in enumerate(visible_tiles):
            tile.suit = content_list[i][0]
            tile.value = content_list[i][1]
            tile.is_selected = False