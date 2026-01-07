"""
Game Window Module (GUI) - Phase 6: Spanish Deck Graphics.

Updates:
- Implemented '_load_images' to load Spanish Deck assets.
- Updated '_draw_tile' to render images instead of text.
- Integrated all previous features (Undo, Shuffle, Hint).
"""

import pygame
import os
import constants as c
from board import Board

class GameWindow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("Solitario Baraja Española - ProyectA24")
        self.clock = pygame.time.Clock()
        
        # Fonts
        self.font = pygame.font.SysFont("Arial", 14, bold=True)
        self.ui_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.message_font = pygame.font.SysFont("Arial", 64, bold=True)
        
        self.start_x = 180
        self.start_y = 60
        
        # Game Logic
        self.board = Board()
        self.selected_tile = None 
        self.score = 0
        self.total_tiles = 144
        self.game_state = "PLAYING"
        
        self.history = []
        self.hint_tiles = []
        
        # --- UI LAYOUT ---
        center_x = c.SCREEN_WIDTH // 2
        
        # HINT (Izquierda)
        self.btn_hint_rect = pygame.Rect(center_x - 160, 10, 100, 30)
        # SHUFFLE (Centro)
        self.btn_shuffle_rect = pygame.Rect(center_x - 50, 10, 100, 30)
        # UNDO (Derecha)
        self.btn_undo_rect = pygame.Rect(center_x + 60, 10, 100, 30)

        # --- FASE 6: GRAPHICS ENGINE ---
        self.images = {} # Cache para guardar las fotos cargadas
        self._load_images()

    def _load_images(self):
        """
        Carga inteligente: Prueba .jpg y .png automáticamente.
        """
        import os
        base_path = "assets"
        
        if not os.path.exists(base_path):
            print("Warning: 'assets' folder not found.")
            return

        print("--- CARGANDO IMÁGENES (Buscando .jpg y .png) ---")

        # Lista de extensiones a probar
        extensions = [".jpg", ".png", ".jpeg", ".JPG", ".PNG"]

        for tile in self.board.tiles:
            base_name = ""
            
            # 1. Definir el nombre base (SIN extensión)
            if tile.suit in [c.SUIT_COINS, c.SUIT_CUPS, c.SUIT_SWORDS]:
                name = "Ace" if tile.value == 1 else str(tile.value)
                base_name = f"{name}_of_{tile.suit}"
            
            elif tile.suit == c.TYPE_KNIGHT:
                base_name = f"Knight_of_{tile.value}"
                
            elif tile.suit == c.TYPE_JOKER:
                base_name = f"Joker_{tile.value}"
                
            elif tile.suit == c.TYPE_JACK:
                base_name = f"Jack_of_{tile.value}"
                
            elif tile.suit == c.TYPE_KING:
                base_name = f"King_of_{tile.value}"

            # 2. Buscar el archivo probando todas las extensiones
            if base_name:
                key = f"{tile.suit}_{tile.value}"
                if key in self.images: continue
                
                found = False
                for ext in extensions:
                    full_path = os.path.join(base_path, base_name + ext)
                    if os.path.exists(full_path):
                        try:
                            # Cargar y redimensionar
                            img = pygame.image.load(full_path).convert_alpha()
                            img = pygame.transform.smoothscale(img, (c.VISUAL_WIDTH - 2, c.VISUAL_HEIGHT - 2))
                            self.images[key] = img
                            found = True
                            break 
                        except Exception as e:
                            print(f"Error: {e}")
                
                if not found:
                    print(f"FALTA: {base_name}.jpg (o .png)")

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    if event.key == pygame.K_r:
                            self._reset_game()
                    if event.key == pygame.K_s:
                        if self.total_tiles > 0:
                            self._shuffle_game()

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self._handle_click(event.pos)
            
            self._draw()
            pygame.display.flip()
            self.clock.tick(c.FPS)
        pygame.quit()

    def _reset_game(self):
        """Reinicia la partida y recarga las imágenes necesarias."""
        print("--- RESTARTING GAME ---")
        self.board = Board()
        self.selected_tile = None
        self.score = 0
        self.total_tiles = 144
        self.hint_tiles = []
        self.history = []
        self.game_state = "PLAYING"
        # Recargamos imágenes por si el nuevo tablero tiene fichas nuevas
        self._load_images()

    def _handle_click(self, mouse_pos):
        """Processes mouse clicks with UI priority."""
        
        # 1. SPECIAL CASE: SHUFFLE BUTTON
        if self.btn_shuffle_rect.collidepoint(mouse_pos):
            self._shuffle_game()
            return

        # 2. CHECK GAME STATE
        if self.game_state != "PLAYING":
            return

        # 3. CHECK HINT BUTTON
        if self.btn_hint_rect.collidepoint(mouse_pos):
            self._activate_hint()
            return 

        # 4. CHECK UNDO BUTTON
        if self.btn_undo_rect.collidepoint(mouse_pos):
            self._undo_move()
            return

        # Clear previous hints
        self.hint_tiles = []

        # 5. CHECK TILE CLICKS
        tiles_reverse = sorted(self.board.tiles, key=lambda t: (t.z, t.y, t.x), reverse=True)

        for tile in tiles_reverse:
            if not tile.is_visible:
                continue
            
            pos_x = self.start_x + (tile.x * c.TILE_SIZE_SCALE) + (tile.z * c.LAYER_SHIFT_X)
            pos_y = self.start_y + (tile.y * c.TILE_SIZE_SCALE) + (tile.z * c.LAYER_SHIFT_Y)
            tile_rect = pygame.Rect(pos_x, pos_y, c.VISUAL_WIDTH, c.VISUAL_HEIGHT)

            if tile_rect.collidepoint(mouse_pos):
                if not self.board.can_move(tile):
                    print(f"Blocked: {tile}")
                    return 

                # Selection / Match Logic
                if self.selected_tile is None:
                    self.selected_tile = tile
                    tile.is_selected = True
                
                elif self.selected_tile == tile:
                    self.selected_tile = None
                    tile.is_selected = False

                else:
                    if self.board.is_match(tile, self.selected_tile):
                        
                        # Match Found!
                        tile.is_visible = False
                        self.selected_tile.is_visible = False
                        
                        # Save to History
                        points = 100
                        move_record = (tile, self.selected_tile, points)
                        self.history.append(move_record)
                        
                        # Update Game State
                        self.score += points
                        self.total_tiles -= 2
                        self.selected_tile = None
                        
                        self._check_game_status()
                        
                    else:
                        # Match Failed
                        self.selected_tile.is_selected = False
                        tile.is_selected = True
                        self.selected_tile = tile 
                        
                return

    def _activate_hint(self):
        """Busca una pareja, penaliza puntos y la ilumina."""
        pair = self.board.get_hint_pair()
        
        if pair:
            self.hint_tiles = [pair[0], pair[1]]
            penalty = 50
            self.score -= penalty
            if self.score < 0: self.score = 0
            print(f"Hint used! -{penalty} points.")
        else:
            print("No valid moves available for hint!")

    def _check_game_status(self):
        if self.total_tiles == 0:
            self.game_state = "WON"
            return

        if not self.board.has_valid_moves():
            self.game_state = "LOST"

    def _draw(self):
        self.screen.fill(c.COLOR_BACKGROUND)
        self._draw_ui()
        
        visible_tiles = sorted(self.board.tiles, key=lambda t: (t.z, t.y, t.x))
        for tile in visible_tiles:
            if tile.is_visible:
                self._draw_tile(tile, self.start_x, self.start_y)
        
        if self.game_state == "WON":
            self._draw_message("VICTORY!", (255, 215, 0)) # Oro
        elif self.game_state == "LOST":
            self._draw_message("NO MOVES LEFT", (255, 50, 50)) # Rojo Brillante

    def _draw_message(self, main_text, color):
        overlay = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))
        
        shadow_surf = self.message_font.render(main_text, True, (0, 0, 0))
        text_surf = self.message_font.render(main_text, True, color)
        
        center_x = c.SCREEN_WIDTH // 2
        center_y = c.SCREEN_HEIGHT // 2
        
        shadow_rect = shadow_surf.get_rect(center=(center_x + 2, center_y - 28))
        self.screen.blit(shadow_surf, shadow_rect)
        
        text_rect = text_surf.get_rect(center=(center_x, center_y - 30))
        self.screen.blit(text_surf, text_rect)
        
        sub_font = pygame.font.SysFont("Arial", 30, bold=True)
        score_msg = f"Final Score: {self.score}"
        score_surf = sub_font.render(score_msg, True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(center_x, center_y + 30))
        self.screen.blit(score_surf, score_rect)
        
        restart_font = pygame.font.SysFont("Arial", 20, italic=True)
        if main_text == "NO MOVES LEFT":
            msg = "Press 'S' to Shuffle (-300pts) or 'R' to Restart or 'ESC' to Quit"
        else:
            msg = "Press 'R' to Restart or 'ESC' to Quit"
            
        restart_surf = restart_font.render(msg, True, (200, 200, 200))
        restart_rect = restart_surf.get_rect(center=(center_x, center_y + 80))
        self.screen.blit(restart_surf, restart_rect)

    def _draw_ui(self):
        # Fondo Barra
        pygame.draw.rect(self.screen, (30, 30, 30), (0, 0, c.SCREEN_WIDTH, 50))
        pygame.draw.line(self.screen, (218, 165, 32), (0, 50), (c.SCREEN_WIDTH, 50), 3)
        
        # Textos
        score_surface = self.ui_font.render(f"SCORE: {self.score}", True, (255, 255, 255))
        self.screen.blit(score_surface, (20, 10))
        
        tiles_surface = self.ui_font.render(f"TILES: {self.total_tiles}", True, (200, 200, 200))
        rect = tiles_surface.get_rect(right=c.SCREEN_WIDTH - 20, top=10)
        self.screen.blit(tiles_surface, rect)
        
        # BOTÓN HINT
        mouse_pos = pygame.mouse.get_pos()
        color = (70, 70, 220) if self.btn_hint_rect.collidepoint(mouse_pos) else c.COLOR_BUTTON
        pygame.draw.rect(self.screen, color, self.btn_hint_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.btn_hint_rect, 2)
        hint_text = self.font.render("HINT (-50)", True, (255, 255, 255))
        text_rect = hint_text.get_rect(center=self.btn_hint_rect.center)
        self.screen.blit(hint_text, text_rect)

        # BOTÓN UNDO
        if len(self.history) == 0:
            btn_color = (100, 100, 100)
        elif self.btn_undo_rect.collidepoint(mouse_pos):
            btn_color = (220, 100, 50)
        else:
            btn_color = (200, 70, 20)
        pygame.draw.rect(self.screen, btn_color, self.btn_undo_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.btn_undo_rect, 2)
        undo_text = self.font.render("UNDO", True, (255, 255, 255))
        text_rect = undo_text.get_rect(center=self.btn_undo_rect.center)
        self.screen.blit(undo_text, text_rect)

        # BOTÓN SHUFFLE
        color = (70, 70, 220) if self.btn_shuffle_rect.collidepoint(mouse_pos) else (100, 50, 150)
        pygame.draw.rect(self.screen, color, self.btn_shuffle_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.btn_shuffle_rect, 2)
        shuf_text = self.font.render("SHUFFLE", True, (255, 255, 255))
        text_rect = shuf_text.get_rect(center=self.btn_shuffle_rect.center)
        self.screen.blit(shuf_text, text_rect)

    def _draw_tile(self, tile, offset_x, offset_y):
        """
        Dibuja la ficha. Si hay imagen, la pone. Si hay selección o pista, pone un velo de color encima.
        """
        # Calcular posición
        pos_x = offset_x + (tile.x * c.TILE_SIZE_SCALE) + (tile.z * c.LAYER_SHIFT_X)
        pos_y = offset_y + (tile.y * c.TILE_SIZE_SCALE) + (tile.z * c.LAYER_SHIFT_Y)
        
        gap = 2
        visual_w = c.VISUAL_WIDTH - gap
        visual_h = c.VISUAL_HEIGHT - gap
        
        # 1. Dibujar Sombra (Grosor 3D)
        depth = 4
        shadow_rect = pygame.Rect(pos_x + depth, pos_y + depth, visual_w, visual_h)
        pygame.draw.rect(self.screen, c.COLOR_TILE_SIDE, shadow_rect)
        pygame.draw.rect(self.screen, c.COLOR_BORDER, shadow_rect, 1)
        
        # 2. Rectángulo base (Fondo)
        face_rect = pygame.Rect(pos_x, pos_y, visual_w, visual_h)
        pygame.draw.rect(self.screen, c.COLOR_TILE_FACE, face_rect) # Fondo crema base
        pygame.draw.rect(self.screen, c.COLOR_BORDER, face_rect, 1)
        
        # 3. DIBUJAR IMAGEN O TEXTO
        key = f"{tile.suit}_{tile.value}"
        
        if key in self.images:
            # PINTAR LA FOTO
            img = self.images[key]
            img_rect = img.get_rect(center=face_rect.center)
            self.screen.blit(img, img_rect)
            
            # --- AQUI ESTÁ LA CLAVE: COLOREAR ENCIMA DE LA FOTO ---
            
            # A) Si está SELECCIONADA -> Velo AMARILLO (Oro)
            if tile.is_selected:
                s = pygame.Surface((visual_w, visual_h))
                s.set_alpha(100) # Transparencia (0-255). 100 se ve bien.
                s.fill(c.COLOR_HIGHLIGHT) 
                self.screen.blit(s, (pos_x, pos_y))
            
            # B) Si es una PISTA (HINT) -> Velo CIAN (Azul claro) <--- NUEVO
            elif tile in self.hint_tiles:
                s = pygame.Surface((visual_w, visual_h))
                s.set_alpha(100) # Transparencia
                s.fill(c.COLOR_HINT) 
                self.screen.blit(s, (pos_x, pos_y))
                
    
    def _undo_move(self):
        """Reverts the last move made by the player."""
        if len(self.history) > 0:
            last_move = self.history.pop()
            tile1, tile2, points = last_move
            
            tile1.is_visible = True
            tile2.is_visible = True
            
            tile1.is_selected = False
            tile2.is_selected = False
            
            self.score -= points
            self.total_tiles += 2
            
            self.game_state = "PLAYING"
            self.selected_tile = None
            self.hint_tiles = []
            print(f"Undo success! Score reverted. History size: {len(self.history)}")
        else:
            print("History empty! Nothing to undo.")

    def _shuffle_game(self):
        """Smart Shuffle loop."""
        if self.total_tiles > 0:
            print("--- SHUFFLE ACTIVATED ---")
            penalty = 300
            self.score -= penalty
            if self.score < 0: self.score = 0
            
            attempts = 0
            max_attempts = 100 
            
            while attempts < max_attempts:
                self.board.shuffle_remaining()
                attempts += 1
                if self.board.has_valid_moves():
                    print(f"Valid moves found after {attempts} shuffles.")
                    break
            
            if attempts == max_attempts:
                print("WARNING: Could not find valid moves even after shuffling.")

            self.history = []
            self.selected_tile = None
            self.hint_tiles = []
            
            self.game_state = "PLAYING"
            self._check_game_status()

if __name__ == "__main__":
    game = GameWindow()
    game.run()