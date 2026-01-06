"""
Main Module - Phase 1 Final Check.

Entry point for the Mahjong Solitaire game logic.
Generates a full Turtle board and validates the initial state rules.
"""

from board import Board

def main():
    """
    Main execution function.
    
    1. Generates a full 144-tile deck.
    2. Arranges them in the 'Turtle' layout.
    3. Scans the board to find all currently legal moves.
    4. Prints the game state summary.
    """
    print("--- Phase 1: Board Generation & Logic Check ---\n")
    
    # 1. Initialize Board (Generates deck + loads Layout)
    game = Board()
    
    # 2. Analyze the Board State
    total_tiles = len(game.tiles)
    removable_tiles = []
    
    print(f"Scanning board for valid moves...")
    
    for tile in game.tiles:
        if game.can_move(tile):
            removable_tiles.append(tile)
            
    # 3. Report Results
    print("\n" + "="*30)
    print("      GAME STATE REPORT      ")
    print("="*30)
    print(f"Total Tiles on Board: {total_tiles}")
    print(f"Locked Tiles:         {total_tiles - len(removable_tiles)}")
    print(f"Free (Removable):     {len(removable_tiles)}")
    
    print("\n--- List of Valid Opening Moves ---")
    if not removable_tiles:
        print("No moves available! (This shouldn't happen on a fresh board)")
    else:
        for i, t in enumerate(removable_tiles):
            # Print formatted string from Tile.__repr__
            print(f"{i+1}. {t}")

    print("\nPhase 1 Complete: Logic Engine is operational.")

if __name__ == "__main__":
    main()