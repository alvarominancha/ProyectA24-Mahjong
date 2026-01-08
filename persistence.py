"""
Persistence Module.

This module handles the saving and loading of game sessions.
It serializes the game state to a JSON file to allow players to resume their progress
exactly where they left off.
"""

import json
import os

# The filename used for storing save data
SAVE_FILE = "savegame.json"

def save_game(game_window):
    """
    Saves the current game state to a JSON file.
    
    This function captures the player's score, the count of remaining tiles,
    and the exact position and state of every tile on the board.
    
    Note: The 'Undo' history is not serialized to keep the save file architecture
    simple; history is effectively reset upon reloading a session.
    
    Args:
        game_window (GameWindow): The main game controller instance containing the state.
    """
    # Prepare the data dictionary
    data = {
        "score": game_window.score,
        "total_tiles": game_window.total_tiles,
        "board_state": game_window.board.get_state(),
    }
    
    try:
        with open(SAVE_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        # In a production environment, we might log this error.
        # For the presentation, we fail silently to avoid console clutter.
        pass

def load_game(game_window):
    """
    Attempts to load a saved game session from disk.
    
    If a save file exists, it restores the score, tile counts, and reconstructs 
    the board layout using the data.
    
    Args:
        game_window (GameWindow): The main game controller instance to populate.
        
    Returns:
        bool: True if the game was successfully loaded, False otherwise.
    """
    if not os.path.exists(SAVE_FILE):
        return False

    try:
        with open(SAVE_FILE, "r") as f:
            data = json.load(f)
            
        # Restore Game Session Variables
        game_window.score = data.get("score", 0)
        game_window.total_tiles = data.get("total_tiles", 144)
        
        # Reconstruct the Board State
        board_data = data.get("board_state", [])
        if board_data:
            game_window.board.set_state(board_data)
            
        return True
    except Exception:
        return False

def delete_save():
    """
    Deletes the save file.
    
    This is automatically called when a game is won or lost to prevent 
    players from reloading a session that has effectively ended.
    """
    if os.path.exists(SAVE_FILE):
        try:
            os.remove(SAVE_FILE)
        except Exception:
            pass