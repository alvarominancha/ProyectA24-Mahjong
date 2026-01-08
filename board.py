# board.py
import random
import constants as c
import layouts
from tile import Tile

class Board:
    def __init__(self, layout_mode="TURTLE", difficulty="HARD"):
        self.tiles = []
        
        # 1. Cargar el mapa (posiciones)
        if layout_mode == "BUTTERFLY":
            self.positions = layouts.get_butterfly_layout()
        elif layout_mode == "COLOSSEUM":
            self.positions = layouts.get_colosseum_layout()
        else:
            self.positions = layouts.get_turtle_layout() # Default
            
        # 2. Generar fichas según dificultad
        self._generate_custom_deck(len(self.positions), difficulty)
        
        # 3. Asignar posiciones
        self._assign_positions()

    def _generate_custom_deck(self, total_needed, difficulty):
        """
        Genera exactamente 'total_needed' fichas.
        - HARD: Usa TODOS los tipos (36-40 tipos). Pocas repeticiones (difícil).
        - MEDIUM: Quita Reyes, Jokers y Caballos.
        - EASY: Solo usa los números 1-7 de 2 palos. Mucha repetición (fácil).
        """
        self.tiles = []
        
        # Definir el 'pool' de símbolos disponibles según dificultad
        available_types = []
        
        # --- CONFIGURACIÓN HARD (Todo) ---
        suits_num = [c.SUIT_COINS, c.SUIT_CUPS, c.SUIT_SWORDS]
        values_num = list(range(1, 10)) # 1 al 9
        special_sets = [(c.TYPE_KNIGHT, ["Coins", "Cups", "Swords", "Clubs"]),
                        (c.TYPE_JACK, ["Coins", "Cups", "Swords", "Clubs"]),
                        (c.TYPE_KING, ["Coins", "Cups", "Swords", "Clubs"]),
                        (c.TYPE_JOKER, ["Red", "Green", "Blue"])]
        
        if difficulty == "MEDIUM":
            # Quitamos Jokers y Reyes. Dejamos Sotas, Caballos y Números.
            special_sets = [(c.TYPE_KNIGHT, ["Coins", "Cups", "Swords", "Clubs"]),
                            (c.TYPE_JACK, ["Coins", "Cups", "Swords", "Clubs"])]
            
        elif difficulty == "EASY":
            # Quitamos TODAS las figuras y Jokers.
            # Quitamos también el palo de Espadas. Solo Oros y Copas del 1 al 7.
            suits_num = [c.SUIT_COINS, c.SUIT_CUPS]
            values_num = list(range(1, 8)) # Solo hasta el 7
            special_sets = []

        # Construir lista de tipos
        for s in suits_num:
            for v in values_num:
                available_types.append((s, v))
        
        for type_name, subtypes in special_sets:
            for sub in subtypes:
                available_types.append((type_name, sub))

        # --- RELLENAR EL MAZO ---
        # El Mahjong necesita PAREJAS. Siempre añadimos de 2 en 2.
        tile_id = 0
        current_deck = []
        
        while len(current_deck) < total_needed:
            # Elegimos un tipo al azar de los disponibles
            stype = random.choice(available_types)
            
            # Añadimos 2 copias (o 4 si queremos asegurar más facilidad)
            # Para que sea soluble, añadimos una PAREJA.
            for _ in range(2):
                if len(current_deck) < total_needed:
                    current_deck.append(Tile(stype[0], stype[1], tile_id))
                    tile_id += 1
        
        # Barajar
        random.shuffle(current_deck)
        self.tiles = current_deck

    def _assign_positions(self):
        # Asigna las coordenadas X,Y,Z de la lista 'positions' a las fichas
        # Si hay más posiciones que fichas (por ajuste impar), recortamos posiciones
        limit = min(len(self.tiles), len(self.positions))
        for i in range(limit):
            x, y, z = self.positions[i]
            self.tiles[i].set_position(x, y, z)
            
    # ... (Resto de métodos: can_move, is_match, etc. SE MANTIENEN IGUAL) ...
    def can_move(self, tile):
        # (Copia tu código anterior de can_move aquí)
        # Importante: Asegúrate de tener el código de colisiones aquí
        left, right = tile.x, tile.x + c.TILE_WIDTH
        top, bottom = tile.y, tile.y + c.TILE_HEIGHT
        layer = tile.z
        blocked_above, blocked_left, blocked_right = False, False, False
        for other in self.tiles:
            if other.id == tile.id or not other.is_visible: continue
            if other.z == layer + 1:
                if (other.x < right and other.x + c.TILE_WIDTH > left and other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    blocked_above = True
            if other.z == layer:
                if (other.x + c.TILE_WIDTH == left and other.y < bottom and other.y + c.TILE_HEIGHT > top): blocked_left = True
                if (other.x == right and other.y < bottom and other.y + c.TILE_HEIGHT > top): blocked_right = True
        return not blocked_above and not (blocked_left and blocked_right)

    def is_match(self, t1, t2):
        # (Copia tu código anterior de is_match aquí)
        if t1.suit == c.TYPE_JACK and t2.suit == c.TYPE_JACK: return True
        if t1.suit == c.TYPE_KING and t2.suit == c.TYPE_KING: return True
        if t1.suit == t2.suit and t1.value == t2.value: return True
        return False
        
    def has_valid_moves(self):
        # (Igual que antes)
        vis = [t for t in self.tiles if t.is_visible and self.can_move(t)]
        for i in range(len(vis)):
            for j in range(i+1, len(vis)):
                if self.is_match(vis[i], vis[j]): return True
        return False

    def get_hint_pair(self):
        # (Igual que antes)
        vis = [t for t in self.tiles if t.is_visible and self.can_move(t)]
        for i in range(len(vis)):
            for j in range(i+1, len(vis)):
                if self.is_match(vis[i], vis[j]): return (vis[i], vis[j])
        return None

    def shuffle_remaining(self):
        # (Igual que antes)
        vis = [t for t in self.tiles if t.is_visible]
        content = [(t.suit, t.value) for t in vis]
        random.shuffle(content)
        for i, t in enumerate(vis):
            t.suit, t.value = content[i]
            t.is_selected = False
            
    def get_state(self): return [t.to_dict() for t in self.tiles]

    def set_state(self, tiles_data):
        """Reconstruye el tablero desde una lista de datos."""
        self.tiles = []
        for t_data in tiles_data:
            # Usamos el método estático que creamos antes
            new_tile = Tile.from_dict(t_data)
            self.tiles.append(new_tile)