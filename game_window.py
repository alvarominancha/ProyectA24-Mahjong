import pygame
import os
import constants as c
from board import Board
import persistence
from sound_manager import SoundManager

class GameWindow:
    """
    Main controller class for the Spanish Mahjong game.
    
    This class manages the game loop, handles user input (events),
    updates the game state, and renders the graphics to the screen.
    """

    def __init__(self):
        """
        Initializes the game window, loads assets, and sets up the initial state.
        
        Tasks performed:
        - Initialize Pygame and the display window.
        - Initialize the audio system and start background music.
        - Load custom fonts (Medieval style) or fallbacks.
        - Load the background image.
        - Define game states and configuration variables.
        - Load UI assets (buttons, icons).
        - Define interactive areas (rectangles) for mouse input.
        """
        # --- INITIALIZATION & SETUP ---
        pygame.init()
        self.screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        pygame.display.set_caption("Spanish Mahjong - Medieval Edition")
        self.clock = pygame.time.Clock()
        
        # --- AUDIO SYSTEM ---
        self.sound_manager = SoundManager()
        self.music_enabled = True
        # Ensure music.mp3 exists in assets/sounds
        self.sound_manager.play_music("music.mp3", 0.2)
        
        # --- FONTS LOADING ---
        font_path = os.path.join("assets", "fonts", "medieval.otf")
        
        # Determine appropriate font to load
        self.title_font = pygame.font.Font(font_path, 80)
        self.menu_font = pygame.font.Font(font_path, 30) 
        self.message_font = pygame.font.Font(font_path, 90)
        self.rules_medieval_font = pygame.font.SysFont("Times New Roman", 24)

        self.ui_font = pygame.font.SysFont("Arial", 20, bold=True)
        
        # --- BACKGROUND LOADING ---
        self.background_img = None
        bg_path = os.path.join("assets/ui", "background.jpeg")
        if os.path.exists(bg_path):
            try:
                img = pygame.image.load(bg_path).convert()
                self.background_img = pygame.transform.smoothscale(img, (c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
                # Apply dark overlay for better visibility
                darkener = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
                darkener.set_alpha(60) 
                darkener.fill((0,0,0))
                self.background_img.blit(darkener, (0,0))
            except Exception as e:
                # Fail silently if background cannot be loaded
                pass

        # --- GAME STATES ---
        self.state = "MENU"         # Current screen: MENU, PLAYING, RULES
        self.game_state = "PLAYING" # Game status: PLAYING, WON, LOST
        self.board = None   
        
        # Config Variables
        self.selected_map = "TURTLE"     
        self.selected_diff = "MEDIUM"    
        
        # --- UI ASSETS LOADING ---
        self.ui_images = {}
        ui_path = os.path.join("assets", "ui")
        
        # Button icon size
        BTN_SIZE = 130
        
        if os.path.exists(ui_path):
            def load_ui_btn(filename, w, h):
                try:
                    full_p = os.path.join(ui_path, filename)
                    if not os.path.exists(full_p): return None
                    img = pygame.image.load(full_p).convert_alpha()
                    return pygame.transform.smoothscale(img, (w, h))
                except Exception as e:
                    return None

            # Load Map Icons
            self.ui_images['map_classic'] = load_ui_btn("map_classic.jpeg", BTN_SIZE, BTN_SIZE)
            self.ui_images['map_butterfly'] = load_ui_btn("map_butterfly.jpeg", BTN_SIZE, BTN_SIZE)
            self.ui_images['map_fortress'] = load_ui_btn("map_fortress.jpeg", BTN_SIZE, BTN_SIZE)
            
            # Load Difficulty Icons
            self.ui_images['diff_easy'] = load_ui_btn("diff_easy.jpeg", BTN_SIZE, BTN_SIZE)
            self.ui_images['diff_medium'] = load_ui_btn("diff_medium.jpeg", BTN_SIZE, BTN_SIZE)
            self.ui_images['diff_hard'] = load_ui_btn("diff_hard.jpeg", BTN_SIZE, BTN_SIZE)
            
            # Load Rule Examples
            self.ui_images['ex_jack'] = load_ui_btn("example_jack.jpg", 60, 90) 
            self.ui_images['ex_king'] = load_ui_btn("example_king.jpg", 60, 90)

        # --- INTERACTIVE ZONES (RECTS) ---
        cx, cy = c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2
        
        # In-Game UI Buttons
        self.btn_hint = pygame.Rect(cx - 200, 10, 100, 30)
        self.btn_shuffle = pygame.Rect(cx - 80, 10, 100, 30)
        self.btn_undo = pygame.Rect(cx + 40, 10, 100, 30)
        self.btn_menu = pygame.Rect(cx + 160, 10, 100, 30)
        
        # Menu: Map Selection
        self.rect_map1 = pygame.Rect(cx - 255, cy - 120, BTN_SIZE, BTN_SIZE)
        self.rect_map2 = pygame.Rect(cx - 65,  cy - 120, BTN_SIZE, BTN_SIZE)
        self.rect_map3 = pygame.Rect(cx + 125, cy - 120, BTN_SIZE, BTN_SIZE)
        
        # Menu: Difficulty Selection
        self.rect_diff1 = pygame.Rect(cx - 255, cy + 60, BTN_SIZE, BTN_SIZE)
        self.rect_diff2 = pygame.Rect(cx - 65,  cy + 60, BTN_SIZE, BTN_SIZE)
        self.rect_diff3 = pygame.Rect(cx + 125, cy + 60, BTN_SIZE, BTN_SIZE)
        
        # Menu: Action Buttons
        self.rect_play = pygame.Rect(cx - 120, cy + 220, 240, 50)
        self.rect_load = pygame.Rect(cx - 120, cy + 280, 240, 40)

        # Menu: Extras
        self.rect_music = pygame.Rect(c.SCREEN_WIDTH - 160, 20, 140, 30)
        self.rect_rules = pygame.Rect(c.SCREEN_WIDTH - 160, 60, 140, 30)

        # Game Session Variables
        self.selected_tile = None
        self.score = 0
        self.hint_tiles = []
        self.history = []
        self.total_tiles = 0
        self.start_x = 0
        self.start_y = 0
        self.images = {}

    # --- GAME FLOW CONTROL ---

    def _start_game(self, load_saved=False):
        """
        Starts a new game session or loads an existing one.
        
        Args:
            load_saved (bool): If True, attempts to load from 'savegame.json'.
                               If False, starts a new game with selected settings.
        """
        if load_saved:
            self.board = Board() 
            if persistence.load_game(self):
                self.state = "PLAYING"
                self.game_state = "PLAYING"
                self._load_images()
                self._center_board()
                return
            else:
                return 
        
        # Initialize new board
        self.board = Board(layout_mode=self.selected_map, difficulty=self.selected_diff)
        self.score = 0
        self.history = []
        self.hint_tiles = []
        self.total_tiles = len(self.board.tiles) 

        self.state = "PLAYING"
        self.game_state = "PLAYING"
        self._load_images()
        self._center_board()

    def _center_board(self):
        """
        Calculates the rendering offset (start_x, start_y) to ensure the 
        game board is centered on the screen based on its dimensions.
        """
        if not self.board.tiles: return
        xs = [t.x for t in self.board.tiles]
        ys = [t.y for t in self.board.tiles]
        min_x, max_x = min(xs), max(xs)
        min_y, max_y = min(ys), max(ys)
        
        board_width = ((max_x - min_x) * c.TILE_SCALE_X) + c.VISUAL_WIDTH
        board_height = ((max_y - min_y) * c.TILE_SCALE_Y) + c.VISUAL_HEIGHT
        
        self.start_x = (c.SCREEN_WIDTH - board_width) // 2 - (min_x * c.TILE_SCALE_X)
        self.start_y = (c.SCREEN_HEIGHT - board_height) // 2 - (min_y * c.TILE_SCALE_Y) + 30

    def _load_images(self):
        """
        Dynamically loads card images from the assets folder.
        Only loads images required for the current board to optimize memory.
        """
        base_path = "assets"
        if not os.path.exists(base_path): return
        extensions = [".jpg", ".png", ".jpeg", ".JPG", ".PNG"]
        self.images = {}
        
        for tile in self.board.tiles:
            # Construct filename based on suit and value
            base_name = ""
            if tile.suit in [c.SUIT_COINS, c.SUIT_CUPS, c.SUIT_SWORDS]:
                name = "Ace" if tile.value == 1 else str(tile.value)
                base_name = f"{name}_of_{tile.suit}"
            elif tile.suit == c.TYPE_KNIGHT: base_name = f"Knight_of_{tile.value}"
            elif tile.suit == c.TYPE_JOKER: base_name = f"Joker_{tile.value}"
            elif tile.suit == c.TYPE_JACK: base_name = f"Jack_of_{tile.value}"
            elif tile.suit == c.TYPE_KING: base_name = f"King_of_{tile.value}"

            if base_name:
                key = f"{tile.suit}_{tile.value}"
                if key in self.images: continue
                # Try to find the file with supported extensions
                for ext in extensions:
                    full_path = os.path.join(base_path, base_name + ext)
                    if os.path.exists(full_path):
                        try:
                            img = pygame.image.load(full_path).convert_alpha()
                            img = pygame.transform.smoothscale(img, (c.VISUAL_WIDTH-2, c.VISUAL_HEIGHT-2))
                            self.images[key] = img
                            break
                        except: pass

    # --- MAIN LOOP ---

    def run(self):
        """
        The main execution loop of the application.
        Responsible for Event Handling, Update Logic, and Rendering.
        """
        running = True
        while running:
            # 1. EVENT HANDLING
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    if self.state == "PLAYING" and self.game_state == "PLAYING":
                        persistence.save_game(self)
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    # ESCAPE: Save and Exit
                    if event.key == pygame.K_ESCAPE:
                        if self.state == "PLAYING" and self.game_state == "PLAYING":
                            persistence.save_game(self)
                        running = False
                    
                    # 'S': Shuffle Board
                    if event.key == pygame.K_s:
                        if self.state == "PLAYING": self._shuffle_game()
                    
                    # 'H': Toggle Rules
                    if event.key == pygame.K_h:
                         if self.state == "MENU": self.state = "RULES"
                         elif self.state == "RULES": self.state = "MENU"

                    # 'M': Return to Menu
                    if event.key == pygame.K_m:
                        if self.state == "PLAYING" and self.game_state == "PLAYING":
                            persistence.save_game(self)
                        self.state = "MENU"
                    
                    # 'U': Undo Move
                    if event.key == pygame.K_u:
                        if self.state == "PLAYING": 
                            self._undo_move()
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.state == "MENU": self._handle_menu_click(event.pos)
                        elif self.state == "PLAYING": self._handle_game_click(event.pos)
                        elif self.state == "RULES": self.state = "MENU"
            
            # 2. DRAWING PHASE
            # Draw Background
            if self.background_img:
                self.screen.blit(self.background_img, (0,0))
            else:
                self.screen.fill(c.COLOR_BACKGROUND)
            
            # Draw specific state
            if self.state == "MENU": self._draw_menu()
            elif self.state == "PLAYING": self._draw_game()
            elif self.state == "RULES": self._draw_rules()
                
            pygame.display.flip()
            self.clock.tick(c.FPS)
        pygame.quit()

    # --- LOGIC HANDLERS ---

    def _handle_menu_click(self, pos):
        """Processes mouse clicks within the Main Menu state."""
        # Map Selection
        if self.rect_map1.collidepoint(pos): self.selected_map = "TURTLE"
        if self.rect_map2.collidepoint(pos): self.selected_map = "BUTTERFLY"
        if self.rect_map3.collidepoint(pos): self.selected_map = "COLOSSEUM"
        
        # Difficulty Selection
        if self.rect_diff1.collidepoint(pos): self.selected_diff = "EASY"
        if self.rect_diff2.collidepoint(pos): self.selected_diff = "MEDIUM"
        if self.rect_diff3.collidepoint(pos): self.selected_diff = "HARD"
        
        # Action Buttons
        if self.rect_play.collidepoint(pos): self._start_game(load_saved=False)
        if self.rect_load.collidepoint(pos): self._start_game(load_saved=True)
        
        # Settings
        if self.rect_music.collidepoint(pos):
            self.music_enabled = not self.music_enabled
            if self.music_enabled: self.sound_manager.play_music("music.mp3", 0.2)
            else: self.sound_manager.stop_music()
            
        if self.rect_rules.collidepoint(pos): self.state = "RULES"

    def _handle_game_click(self, pos):
        """
        Processes mouse clicks within the Game state.
        Handles UI buttons and Tile selection logic.
        """
        # Check UI Buttons
        if self.btn_menu.collidepoint(pos):
            persistence.save_game(self)
            self.state = "MENU"
            return
        if self.btn_undo.collidepoint(pos):
            self._undo_move(); return
        if self.btn_hint.collidepoint(pos):
            self._activate_hint(); return
        if self.btn_shuffle.collidepoint(pos):
            self._shuffle_game(); return
            
        # Check Tile Selection (Raycasting / Collision logic)
        self.hint_tiles = []
        # Sort reverse to click top-most tiles first
        tiles_rev = sorted(self.board.tiles, key=lambda t: (t.z, t.y, t.x), reverse=True)
        
        for tile in tiles_rev:
            if not tile.is_visible: continue
            
            px = self.start_x + (tile.x * c.TILE_SCALE_X) + (tile.z * c.LAYER_SHIFT_X)
            py = self.start_y + (tile.y * c.TILE_SCALE_Y) + (tile.z * c.LAYER_SHIFT_Y)
            tr = pygame.Rect(px, py, c.VISUAL_WIDTH, c.VISUAL_HEIGHT)
            
            if tr.collidepoint(pos):
                # Validate move
                if not self.board.can_move(tile):
                    self.sound_manager.play("error")
                    return
                
                self.sound_manager.play("click")
                
                # Selection Logic
                if self.selected_tile is None:
                    self.selected_tile = tile
                    tile.is_selected = True
                elif self.selected_tile == tile:
                    self.selected_tile = None
                    tile.is_selected = False
                else:
                    # Attempt Match
                    if self.board.is_match(tile, self.selected_tile):
                        self.sound_manager.play("match")
                        tile.is_visible = False
                        self.selected_tile.is_visible = False
                        self.history.append((tile, self.selected_tile, 100))
                        self.score += 100
                        self.total_tiles -= 2 
                        self.selected_tile = None
                        self._check_game_status()
                    else:
                        self.sound_manager.play("error")
                        self.selected_tile.is_selected = False
                        tile.is_selected = True
                        self.selected_tile = tile
                return

    def _undo_move(self):
        """
        Reverts the last successful matching move.
        Restores the tiles to the board and deducts score.
        """
        if self.score < 100: 
            self.sound_manager.play("error")
            return
        if self.history:
            t1, t2, pts = self.history.pop()
            t1.is_visible = t2.is_visible = True
            t1.is_selected = t2.is_selected = False
            self.score -= pts
            self.total_tiles += 2
            self.sound_manager.play("undo")
            self.score = max(0, self.score - 100)
            
            # If game was lost, undoing allows playing again
            if self.game_state == "LOST": self.game_state = "PLAYING"

    def _activate_hint(self):
        """Highlights a pair of matching free tiles if available."""
        if self.score < 50: 
            self.sound_manager.play("error")
            return
        pair = self.board.get_hint_pair()
        if pair:
            self.hint_tiles = [pair[0], pair[1]]
            self.score = max(0, self.score - 50)
            self.sound_manager.play("hint")

    def _shuffle_game(self):
        """Randomly rearranges the remaining tiles on the board."""
        if self.score < 150: 
            self.sound_manager.play("error")
            return
        if self.total_tiles > 0:
            self.sound_manager.play("shuffle")
            self.score = max(0, self.score - 150)
            for _ in range(100):
                self.board.shuffle_remaining()
                if self.board.has_valid_moves(): break
            
            self.game_state = "PLAYING" 
            self.history = []
            self.selected_tile = None
            self.hint_tiles = []
            
    def _check_game_status(self):
        """Checks victory or defeat conditions after every move."""
        visible_count = sum(1 for t in self.board.tiles if t.is_visible)
        if visible_count == 0:
            self.game_state = "WON"
            self.sound_manager.play("win")
            persistence.delete_save()
        elif not self.board.has_valid_moves():
            self.game_state = "LOST"
            self.sound_manager.play("lose")

    # --- DRAWING METHODS ---

    def _draw_menu(self):
        """Renders the Main Menu interface."""
        # Title
        title_text = "SPANISH MAHJONG"
        title_shadow = self.title_font.render(title_text, True, (0, 0, 0))
        self.screen.blit(title_shadow, (c.SCREEN_WIDTH//2 - title_shadow.get_width()//2 + 5, 45))
        title = self.title_font.render(title_text, True, (255, 215, 0))
        self.screen.blit(title, (c.SCREEN_WIDTH//2 - title.get_width()//2, 40))
        
        # Labels
        def draw_label(text, y):
            lbl = self.menu_font.render(text, True, (200, 200, 200))
            self.screen.blit(lbl, (c.SCREEN_WIDTH//2 - lbl.get_width()//2, y))
            
        draw_label("- SELECT MAP -", self.rect_map1.top - 40)
        draw_label("- DIFFICULTY -", self.rect_diff1.top - 40)

        # Helper: Image Button
        def draw_img_btn(rect, img_key, selected=False, label_text=""):
            img = self.ui_images.get(img_key)
            if selected:
                # Highlight effect
                glow_rect = rect.inflate(14, 14)
                pygame.draw.rect(self.screen, (255, 215, 0), glow_rect, border_radius=15)
                pygame.draw.rect(self.screen, (0, 0, 0), rect.inflate(4, 4), border_radius=15)
            
            if img:
                self.screen.blit(img, rect)
            else:
                pygame.draw.rect(self.screen, (100, 100, 100), rect)
            
            # Label
            color = (255, 215, 0) if selected else (150, 150, 150)
            txt_s = self.ui_font.render(label_text, True, color)
            self.screen.blit(txt_s, (rect.centerx - txt_s.get_width()//2, rect.bottom + 10))

        # Draw Option Buttons
        draw_img_btn(self.rect_map1, 'map_classic', self.selected_map=="TURTLE", )
        draw_img_btn(self.rect_map2, 'map_butterfly', self.selected_map=="BUTTERFLY", )
        draw_img_btn(self.rect_map3, 'map_fortress', self.selected_map=="COLOSSEUM", )
        
        draw_img_btn(self.rect_diff1, 'diff_easy', self.selected_diff=="EASY",)
        draw_img_btn(self.rect_diff2, 'diff_medium', self.selected_diff=="MEDIUM", )
        draw_img_btn(self.rect_diff3, 'diff_hard', self.selected_diff=="HARD", )
        
        # Helper: Text Button
        def draw_text_btn(rect, text, highlight=False):
             bg_col = (50, 150, 50) if highlight else c.COLOR_BUTTON
             pygame.draw.rect(self.screen, bg_col, rect, border_radius=8)
             pygame.draw.rect(self.screen, (200, 200, 200), rect, 3, border_radius=8)
             txt_s = self.menu_font.render(text, True, (255,255,255))
             self.screen.blit(txt_s, (rect.centerx - txt_s.get_width()//2, rect.centery - txt_s.get_height()//2))

        # Draw Action Buttons
        draw_text_btn(self.rect_play, "START GAME", True)
        draw_text_btn(self.rect_load, "LOAD GAME")
        
        music_txt = "Music: ON" if self.music_enabled else "Music: OFF"
        temp_font = self.menu_font; self.menu_font = self.ui_font 
        draw_text_btn(self.rect_music, music_txt)
        draw_text_btn(self.rect_rules, "Rules (H)")
        self.menu_font = temp_font

    def _draw_rules(self):
        """Draws the Rules Overlay with graphical examples."""
        box_w, box_h = 1000, 650
        overlay = pygame.Surface((box_w, box_h))
        overlay.fill((55, 45, 35)) # Dark parchment style
        rect = overlay.get_rect(center=(c.SCREEN_WIDTH//2, c.SCREEN_HEIGHT//2))
        
        # Dim background
        s = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 180))
        self.screen.blit(s, (0,0))
        self.screen.blit(overlay, rect)
        
        # Border
        pygame.draw.rect(self.screen, (218, 165, 32), rect, 6) 
        pygame.draw.rect(self.screen, (30, 20, 10), rect.inflate(-10,-10), 4)

        # Header
        header = self.menu_font.render("GAME RULES", True, (255, 215, 0))
        self.screen.blit(header, (rect.centerx - header.get_width()//2, rect.y + 30))
        
        lines = [
            "1. Remove tiles by matching identical pairs.",
            "2. You can only select 'FREE' tiles.",
            "   (Free = No tile on top & at least one side, right or left, open)",
            "Attention: Each tile has a certain hight, so a tile",
            "can be free if it is higher than a tile next to it.",
            "",
            "3. SPECIAL BONUSES:",
            "   - JACKS (Sotas) match with any Jack.", 
            "   - KINGS (Reyes) match with any King.",
            "4. BUTTONS:",
            "   - HINT (-50 points): Shows a possible match.",
            "   - SHUFFLE (-150 points): Randomly rearranges remaining tiles.",
            "   - UNDO (-100 points): Reverts the last move.",
            "",
            "Press 'M' to return to Menu."
        ]
        
        start_y = rect.y + 100
        line_spacing = 32
        
        # Render Lines
        for i, line in enumerate(lines):
            col = (230, 220, 190)
            txt_surf = self.rules_medieval_font.render(line, True, col)
            text_rect = txt_surf.get_rect(topleft=(rect.x + 60, start_y + i * line_spacing))
            self.screen.blit(txt_surf, text_rect)

        # Render Example Cards
        images_x = rect.right - 180 
        current_img_y = start_y + 4 * line_spacing + 10

        img_jack = self.ui_images.get('ex_jack')
        if img_jack:
            self.screen.blit(img_jack, (images_x, current_img_y))
            current_img_y += img_jack.get_height() + 20

        img_king = self.ui_images.get('ex_king')
        if img_king:
            self.screen.blit(img_king, (images_x, current_img_y))

    def _draw_game(self):
        """Draws the main gameplay screen."""
        # Top HUD Bar
        pygame.draw.rect(self.screen, (30, 30, 30), (0, 0, c.SCREEN_WIDTH, 50))
        pygame.draw.line(self.screen, (218, 165, 32), (0, 50), (c.SCREEN_WIDTH, 50), 3)
        
        # UI Buttons
        def draw_ui_btn(rect, txt):
            pygame.draw.rect(self.screen, c.COLOR_BUTTON, rect)
            pygame.draw.rect(self.screen, (200,200,200), rect, 2)
            ts = self.ui_font.render(txt, True, (255,255,255))
            self.screen.blit(ts, (rect.centerx-ts.get_width()//2, rect.centery-ts.get_height()//2))
            
        draw_ui_btn(self.btn_hint, "HINT (-50)")
        draw_ui_btn(self.btn_shuffle, "SHUFFLE")
        draw_ui_btn(self.btn_undo, "UNDO")
        draw_ui_btn(self.btn_menu, "MENU")
        
        # Score Display
        sc = self.ui_font.render(f"SCORE: {self.score}", True, (255,255,255))
        self.screen.blit(sc, (20, 15))
        
        # Render Tiles (Sorted by depth)
        vis = sorted(self.board.tiles, key=lambda t: (t.z, t.y, t.x))
        for tile in vis:
            if tile.is_visible: self._draw_tile(tile, self.start_x, self.start_y)
            
        # Game Over / Victory Messages
        if self.game_state == "WON": self._draw_message("VICTORY!", (255, 215, 0))
        elif self.game_state == "LOST": self._draw_message("NO MOVES LEFT", (255, 50, 50))

    def _draw_tile(self, tile, ox, oy):
        """Draws a single tile with 3D depth and shadows."""
        pos_x = ox + (tile.x * c.TILE_SCALE_X) + (tile.z * c.LAYER_SHIFT_X)
        pos_y = oy + (tile.y * c.TILE_SCALE_Y) + (tile.z * c.LAYER_SHIFT_Y)
        depth = c.TILE_THICKNESS
        
        # 1. Shadow/Side
        shadow_rect = pygame.Rect(pos_x + depth, pos_y + depth, c.VISUAL_WIDTH, c.VISUAL_HEIGHT)
        pygame.draw.rect(self.screen, c.COLOR_TILE_SIDE, shadow_rect)
        pygame.draw.rect(self.screen, (0,0,0), shadow_rect, 1)
        
        # 2. Top Face
        face_rect = pygame.Rect(pos_x, pos_y, c.VISUAL_WIDTH, c.VISUAL_HEIGHT)
        pygame.draw.rect(self.screen, c.COLOR_TILE_FACE, face_rect)
        
        # 3. Card Image
        key = f"{tile.suit}_{tile.value}"
        if key in self.images:
            img = self.images[key]
            self.screen.blit(img, img.get_rect(center=face_rect.center))
            
            # Effects (Highlight / Hint)
            if tile.is_selected:
                s = pygame.Surface((c.VISUAL_WIDTH, c.VISUAL_HEIGHT))
                s.set_alpha(100); s.fill(c.COLOR_HIGHLIGHT)
                self.screen.blit(s, (pos_x, pos_y))
            elif tile in self.hint_tiles:
                s = pygame.Surface((c.VISUAL_WIDTH, c.VISUAL_HEIGHT))
                s.set_alpha(100); s.fill(c.COLOR_HINT)
                self.screen.blit(s, (pos_x, pos_y))
        
        # 4. Border
        pygame.draw.rect(self.screen, c.COLOR_BORDER, face_rect, 2)

    def _draw_message(self, txt, col):
        """Draws a centered message overlay (e.g., Victory)."""
        overlay = pygame.Surface((c.SCREEN_WIDTH, c.SCREEN_HEIGHT))
        overlay.set_alpha(200); overlay.fill((0,0,0))
        self.screen.blit(overlay, (0,0))
        
        ts = self.message_font.render(txt, True, col)
        rect = ts.get_rect(center=(c.SCREEN_WIDTH//2, c.SCREEN_HEIGHT//2))
        self.screen.blit(ts, rect)
        
        sub = self.ui_font.render("Press 'M' for Menu or 'ESC' to Exit", True, (200,200,200))
        self.screen.blit(sub, sub.get_rect(center=(c.SCREEN_WIDTH//2, rect.bottom + 20)))
        
        if self.game_state == "LOST":
            sub2 = self.ui_font.render("(Press 'U' to Undo or 'S' to Shuffle and continue)", True, (150,150,150))
            self.screen.blit(sub2, sub2.get_rect(center=(c.SCREEN_WIDTH//2, rect.bottom + 50)))
        
if __name__ == "__main__":
    GameWindow().run()