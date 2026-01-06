"""
Game Window Module (GUI) - Phase 4: Hint System.

Updates:
- Added 'HINT' button in the UI.
- Implemented hint logic: Highlights a valid pair in Cyan.
- Added score penalty (-50 points) for using hints.
"""

import pygame
import constants as c
from board import Board

class GameWindow:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("Mahjong Solitaire - ProyectA24 (Phase 4 + Hints)")
        self.clock = pygame.time.Clock()
        
        self.board = Board()
        
        # Fonts
        self.font = pygame.font.SysFont("Arial", 14, bold=True)
        self.ui_font = pygame.font.SysFont("Arial", 24, bold=True)
        self.message_font = pygame.font.SysFont("Arial", 64, bold=True)
        
        # Offsets
        self.start_x = 150
        self.start_y = 60 
        
        # Game Logic
        self.selected_tile = None 
        self.score = 0
        self.total_tiles = 144
        self.game_state = "PLAYING"
        
        # --- SISTEMA DE PISTAS ---
        self.hint_tiles = []  # Lista para guardar las fichas sugeridas
        # Definimos el rectángulo del botón (X, Y, Ancho, Alto)
        # Lo ponemos en el centro-derecha de la barra superior
        self.btn_hint_rect = pygame.Rect(c.SCREEN_WIDTH - 250, 10, 100, 30)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                # Eventos de Teclado
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                    # Si pulsamos R y el juego ha terminado, reiniciamos
                    if event.key == pygame.K_r:
                        if self.game_state != "PLAYING":
                            self._reset_game()

                # Clics del ratón
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        self._handle_click(event.pos)
            
            self._draw()
            pygame.display.flip()
            self.clock.tick(c.FPS)
        pygame.quit()

    def _reset_game(self):
        """Reinicia todas las variables para una nueva partida."""
        print("--- RESTARTING GAME ---")
        self.board = Board() # Genera mazo y tablero nuevo
        self.selected_tile = None
        self.score = 0
        self.total_tiles = 144
        self.hint_tiles = []
        self.game_state = "PLAYING"

    def _handle_click(self, mouse_pos):
        if self.game_state != "PLAYING":
            return

        # 1. CHEQUEAR CLIC EN BOTÓN DE PISTA
        if self.btn_hint_rect.collidepoint(mouse_pos):
            print("Hint button clicked!")
            self._activate_hint()
            return # No seguimos comprobando fichas

        # Si clicamos en el tablero, borramos la pista anterior para no confundir
        self.hint_tiles = []

        # 2. CHEQUEAR CLIC EN FICHAS
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

                # Lógica de Selección / Match
                if self.selected_tile is None:
                    self.selected_tile = tile
                    tile.is_selected = True
                
                elif self.selected_tile == tile:
                    self.selected_tile = None
                    tile.is_selected = False

                else:
                    if (tile.suit == self.selected_tile.suit and 
                        tile.value == self.selected_tile.value):
                        
                        # MATCH!
                        tile.is_visible = False
                        self.selected_tile.is_visible = False
                        self.selected_tile = None
                        
                        self.score += 100
                        self.total_tiles -= 2
                        self._check_game_status()
                        
                    else:
                        self.selected_tile.is_selected = False
                        tile.is_selected = True
                        self.selected_tile = tile 
                        
                return 

    def _activate_hint(self):
        """Busca una pareja, penaliza puntos y la ilumina."""
        pair = self.board.get_hint_pair()
        
        if pair:
            # Guardamos las fichas en la lista de pistas
            self.hint_tiles = [pair[0], pair[1]]
            
            # Penalización
            penalty = 50
            self.score -= penalty
            # Evitar puntuación negativa (opcional)
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
        """
        Dibuja una pantalla de fin de juego elegante con transparencia.
        """
        # 1. Crear una superficie negra del tamaño de la pantalla
        overlay = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        overlay.set_alpha(200) # Transparencia: 0 (invisible) a 255 (sólido)
        overlay.fill((0, 0, 0)) # Color Negro
        
        # Dibujar el overlay sobre el tablero existente
        self.screen.blit(overlay, (0, 0))
        
        # 2. Renderizar Texto Principal (GAME OVER / VICTORY)
        # Añadimos una sombra negra para que se lea mejor
        shadow_surf = self.message_font.render(main_text, True, (0, 0, 0))
        text_surf = self.message_font.render(main_text, True, color)
        
        center_x = c.SCREEN_WIDTH // 2
        center_y = c.SCREEN_HEIGHT // 2
        
        # Dibujar sombra desplazada +2px
        shadow_rect = shadow_surf.get_rect(center=(center_x + 2, center_y - 28))
        self.screen.blit(shadow_surf, shadow_rect)
        
        # Dibujar texto principal
        text_rect = text_surf.get_rect(center=(center_x, center_y - 30))
        self.screen.blit(text_surf, text_rect)
        
        # 3. Renderizar Puntuación Final
        sub_font = pygame.font.SysFont("Arial", 30, bold=True)
        score_msg = f"Final Score: {self.score}"
        score_surf = sub_font.render(score_msg, True, (255, 255, 255))
        score_rect = score_surf.get_rect(center=(center_x, center_y + 30))
        self.screen.blit(score_surf, score_rect)
        
        # 4. Mensaje de Reinicio
        restart_font = pygame.font.SysFont("Arial", 20, italic=True)
        restart_msg = "Press 'R' to Restart or 'ESC' to Quit"
        restart_surf = restart_font.render(restart_msg, True, (200, 200, 200))
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
        
        # --- DIBUJAR BOTÓN HINT ---
        # 1. Fondo del botón
        # Cambiar color si pasamos el ratón por encima (Hover simple)
        mouse_pos = pygame.mouse.get_pos()
        color = (70, 70, 220) if self.btn_hint_rect.collidepoint(mouse_pos) else c.COLOR_BUTTON
        
        pygame.draw.rect(self.screen, color, self.btn_hint_rect)
        pygame.draw.rect(self.screen, (200, 200, 200), self.btn_hint_rect, 2) # Borde
        
        # 2. Texto del botón
        hint_text = self.font.render("HINT (-50)", True, (255, 255, 255))
        text_rect = hint_text.get_rect(center=self.btn_hint_rect.center)
        self.screen.blit(hint_text, text_rect)

    def _draw_tile(self, tile, offset_x, offset_y):
        pos_x = offset_x + (tile.x * c.TILE_SIZE_SCALE) + (tile.z * c.LAYER_SHIFT_X)
        pos_y = offset_y + (tile.y * c.TILE_SIZE_SCALE) + (tile.z * c.LAYER_SHIFT_Y)
        
        gap = 2
        visual_w = c.VISUAL_WIDTH - gap
        visual_h = c.VISUAL_HEIGHT - gap
        
        # Shadow
        shadow_rect = pygame.Rect(pos_x + 4, pos_y + 4, visual_w, visual_h)
        pygame.draw.rect(self.screen, c.COLOR_TILE_SIDE, shadow_rect)
        pygame.draw.rect(self.screen, c.COLOR_BORDER, shadow_rect, 1)
        
        # Face
        face_rect = pygame.Rect(pos_x, pos_y, visual_w, visual_h)
        
        # --- LÓGICA DE COLOR (Highlight, Hint, Normal) ---
        if tile.is_selected:
            color = c.COLOR_HIGHLIGHT # Oro
        elif tile in self.hint_tiles: # <--- NUEVO: Si es una pista
            color = c.COLOR_HINT      # Cian
        else:
            color = c.COLOR_TILE_FACE # Crema
            
        pygame.draw.rect(self.screen, color, face_rect)
        pygame.draw.rect(self.screen, c.COLOR_BORDER, face_rect, 1)
        
        # Text
        short_suit = tile.suit[:3] 
        text_str = f"{short_suit}-{tile.value}"
        text_surf = self.font.render(text_str, True, c.COLOR_TEXT)
        text_rect = text_surf.get_rect(center=face_rect.center)
        self.screen.blit(text_surf, text_rect)

if __name__ == "__main__":
    game = GameWindow()
    game.run()