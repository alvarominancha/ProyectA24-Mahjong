import json
import os

SAVE_FILE = "savegame.json"

def save_game(game_window):
    """Guarda el estado actual del juego en un JSON."""
    data = {
        "score": game_window.score,
        "total_tiles": game_window.total_tiles,
        "board_state": game_window.board.get_state(),
        # Nota: Guardar el historial de Undo es complejo porque tiene referencias a objetos.
        # Por simplicidad, al cerrar y abrir se pierde el historial de deshacer de la sesión anterior.
    }
    
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
        print("Game saved successfully.")
    except Exception as e:
        print(f"Error saving game: {e}")

def load_game(game_window):
    """Carga el juego si existe el archivo de guardado."""
    if not os.path.exists(SAVE_FILE):
        print("No save file found. Starting new game.")
        return False

    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            
        game_window.score = data.get("score", 0)
        game_window.total_tiles = data.get("total_tiles", 144)
        
        # Reconstruir el tablero
        board_data = data.get("board_state", [])
        if board_data:
            game_window.board.set_state(board_data)
            
        print("Game loaded successfully.")
        return True
    except Exception as e:
        print(f"Error loading game: {e}")
        return False

def delete_save():
    """Borra la partida guardada (útil al ganar o reiniciar)."""
    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
            print("Save file deleted.")
        except Exception as e:
            print(f"Error deleting save: {e}")