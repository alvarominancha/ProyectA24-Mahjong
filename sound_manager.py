import pygame
import os

class SoundManager:
    def __init__(self):
        # Inicializar el mezclador de pygame
        if not pygame.mixer.get_init():
            pygame.mixer.init()
        
        self.sounds = {}
        self.music_playing = False
        
        # Diccionario de archivos esperados
        self.sound_files = {
            "click": "click.wav",       # Al seleccionar una ficha
            "match": "match.wav",       # Al hacer pareja (éxito)
            "error": "error.wav",       # Al intentar seleccionar una bloqueada
            "shuffle": "shuffle.wav",   # Al barajar
            "win": "win.wav",           # Victoria
            "lose": "lose.wav",         # Derrota
            "undo": "undo.wav",         # Deshacer
            "hint": "hint.wav"          # Pista
        }
        
        self._load_sounds()

    def _load_sounds(self):
        """Carga los efectos de sonido en memoria."""
        base_path = "assets"
        
        if not os.path.exists(base_path):
            print("Warning: 'assets' folder not found. Audio disabled.")
            return

        print("--- LOADING AUDIO ---")
        for name, filename in self.sound_files.items():
            path = os.path.join(base_path, filename)
            if os.path.exists(path):
                try:
                    self.sounds[name] = pygame.mixer.Sound(path)
                    # Ajustar volúmenes individuales si es necesario
                    if name == "click": self.sounds[name].set_volume(0.5)
                    if name == "match": self.sounds[name].set_volume(0.6)
                except Exception as e:
                    print(f"Error loading sound {filename}: {e}")
            else:
                print(f"Missing sound file: {filename}")

    def play(self, sound_name):
        """Reproduce un efecto de sonido si existe."""
        if sound_name in self.sounds:
            self.sounds[sound_name].play()

    def play_music(self, filename, volume=0.3):
        """
        Reproduce una canción en bucle infinito.
        :param filename: Nombre del archivo (ej. 'music.mp3') dentro de assets
        :param volume: Volumen de la música (0.0 a 1.0). Por defecto 0.3 (suave).
        """
        path = os.path.join("assets", filename)
        
        if os.path.exists(path):
            try:
                # Cargar y reproducir en bucle (-1)
                pygame.mixer.music.load(path)
                pygame.mixer.music.set_volume(volume)
                pygame.mixer.music.play(-1) 
                print(f"Playing background music: {filename}")
            except Exception as e:
                print(f"Error playing music: {e}")
        else:
            print(f"Music file not found: {filename}")

    def stop_music(self):
        """Detiene la música."""
        pygame.mixer.music.stop()