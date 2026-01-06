"""
Board Module.

This module manages the core game logic, including deck generation,
layout loading, and the validation of legal moves according
to Mahjong Solitaire rules.
"""

import random
import constants as c
import layouts
from tile import Tile

class Board:
    """
    Represents the game board and enforces game rules.

    Attributes:
        tiles (list[Tile]): A list containing all active Tile instances.
    """

    def __init__(self):
        """
        Initializes the board.
        """
        self.tiles = []
        self._generate_deck()
        self._load_layout()

    def _generate_deck(self):
        """Generates the standard 144 Mahjong tiles."""
        self.tiles = []
        tile_id = 0
        
        # 1. Suits
        suits = [c.SUIT_BAMBOO, c.SUIT_DOTS, c.SUIT_CHARACTERS]
        for suit in suits:
            for value in range(1, 10):
                for _ in range(4):
                    self.tiles.append(Tile(suit, value, tile_id))
                    tile_id += 1
        
        # 2. Winds
        winds = ["North", "South", "East", "West"]
        for wind in winds:
            for _ in range(4):
                self.tiles.append(Tile(c.SUIT_WINDS, wind, tile_id))
                tile_id += 1

        # 3. Dragons
        dragons = ["Red", "Green", "White"]
        for dragon in dragons:
            for _ in range(4):
                self.tiles.append(Tile(c.SUIT_DRAGONS, dragon, tile_id))
                tile_id += 1
        
        # 4. Flowers & Seasons
        for i in range(1, 5):
            self.tiles.append(Tile(c.SUIT_FLOWERS, i, tile_id))
            tile_id += 1
        for i in range(1, 5):
            self.tiles.append(Tile(c.SUIT_SEASONS, i, tile_id))
            tile_id += 1
        
        random.shuffle(self.tiles)

    def _load_layout(self):
        """Assigns coordinates based on Layout."""
        positions = layouts.get_turtle_layout()
        if len(self.tiles) > len(positions):
            self.tiles = self.tiles[:len(positions)]
        
        for i, tile in enumerate(self.tiles):
            if i < len(positions):
                x, y, z = positions[i]
                tile.set_position(x, y, z)

    def can_move(self, tile):
        """
        Determines if a tile is unblocked.
        """
        left = tile.x
        right = tile.x + c.TILE_WIDTH
        top = tile.y
        bottom = tile.y + c.TILE_HEIGHT
        layer = tile.z
        
        blocked_above = False
        blocked_left = False
        blocked_right = False
        
        for other in self.tiles:
            if other.id == tile.id:
                continue
            
            # --- CORRECCIÓN CRÍTICA ---
            # Si la otra ficha ya fue eliminada (no es visible), NO BLOQUEA.
            if not other.is_visible: 
                continue
            # --------------------------
            
            # Check collision above (Layer Z+1)
            if other.z == layer + 1:
                if (other.x < right and other.x + c.TILE_WIDTH > left and
                        other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    blocked_above = True
            
            # Check lateral collision (Same Layer Z)
            if other.z == layer:
                # Left neighbor
                if (other.x + c.TILE_WIDTH == left and
                        other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    blocked_left = True
                
                # Right neighbor
                if (other.x == right and
                        other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    blocked_right = True

        if blocked_above: return False
        if blocked_left and blocked_right: return False
        return True

    def get_blockers(self, tile):
        """
        Debug helper to find WHO is blocking a tile.
        """
        blockers = []
        left = tile.x
        right = tile.x + c.TILE_WIDTH
        top = tile.y
        bottom = tile.y + c.TILE_HEIGHT
        layer = tile.z
        
        has_left = False
        has_right = False
        l_blocker = None
        r_blocker = None
        
        for other in self.tiles:
            if other.id == tile.id: continue
            
            # --- CORRECCIÓN CRÍTICA TAMBIÉN AQUÍ ---
            if not other.is_visible: continue
            
            # Check Top
            if other.z == layer + 1:
                if (other.x < right and other.x + c.TILE_WIDTH > left and
                    other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    blockers.append(f"Blocked ABOVE by {other}")
            
            # Check Sides
            if other.z == layer:
                if (other.x + c.TILE_WIDTH == left and 
                    other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    has_left = True
                    l_blocker = other
                
                if (other.x == right and 
                    other.y < bottom and other.y + c.TILE_HEIGHT > top):
                    has_right = True
                    r_blocker = other

        if has_left and has_right:
            blockers.append(f"Blocked LATERALLY by Left:{l_blocker} and Right:{r_blocker}")
            
        return blockers
    
    def has_valid_moves(self):
        """
        Comprueba si existe al menos una pareja de fichas libres en el tablero.
        Returns:
            bool: True si hay movimientos posibles, False si no (Game Over).
        """
        # 1. Obtener todas las fichas visibles que NO están bloqueadas
        free_tiles = []
        for tile in self.tiles:
            if tile.is_visible and self.can_move(tile):
                free_tiles.append(tile)
        
        # 2. Fuerza bruta: Comparar cada ficha libre con las demás
        # Como n es pequeño (max 144), esto es muy rápido para el ordenador.
        for i in range(len(free_tiles)):
            for j in range(i + 1, len(free_tiles)):
                t1 = free_tiles[i]
                t2 = free_tiles[j]
                
                # Comprobar si son pareja (Mismo palo y valor)
                # NOTA: Aquí podrías añadir lógica especial para Flores/Estaciones si quisieras
                if t1.suit == t2.suit and t1.value == t2.value:
                    print(f"DEBUG: Movimiento posible encontrado: {t1} y {t2}")
                    return True
                    
        return False
    
    def get_hint_pair(self):
        """
        Busca y devuelve una pareja de fichas libres que coincidan.
        
        Returns:
            tuple[Tile, Tile] | None: La pareja de fichas encontrada, 
                                      o None si no hay movimientos.
        """
        # 1. Obtener fichas libres visibles
        free_tiles = []
        for tile in self.tiles:
            if tile.is_visible and self.can_move(tile):
                free_tiles.append(tile)
        
        # 2. Buscar pareja
        for i in range(len(free_tiles)):
            for j in range(i + 1, len(free_tiles)):
                t1 = free_tiles[i]
                t2 = free_tiles[j]
                
                if t1.suit == t2.suit and t1.value == t2.value:
                    return (t1, t2)
                    
        return None