"""
Layouts Module.

This module defines the coordinate maps for Mahjong Solitaire board configurations.
It currently implements the classic 'Turtle' layout structure.
"""

def get_turtle_layout():
    """
    Generates the 3D coordinates for the standard Turtle layout.
    Target: Exactly 144 tiles.

    Structure:
    - Layer 0: 87 tiles (Base shape)
    - Layer 1: 36 tiles (6x6 square) - Corrected
    - Layer 2: 16 tiles (4x4 square) - Corrected
    - Layer 3: 4 tiles (2x2 square)
    - Layer 4: 1 tile (Top)
    Total: 144.

    Returns:
        list[tuple[int, int, int]]: A list of 144 (x, y, z) tuples.
    """
    coords = []
    
    # --- Layer 0: The Base (87 tiles) ---
    
    # 1. Main Block (Rows 2 to 12, Cols 2 to 24) -> 6 rows * 12 cols = 72 tiles
    # range(start, stop, step) -> stop is exclusive
    for y in range(2, 14, 2):  # y: 2, 4, 6, 8, 10, 12
        for x in range(2, 26, 2): # x: 2, 4, ..., 24
            coords.append((x, y, 0))

    # 2. Add "Ears" (Extensions on Left and Right) -> 4 tiles
    coords.append((0, 6, 0)); coords.append((0, 8, 0))   # Left
    coords.append((26, 6, 0)); coords.append((26, 8, 0)) # Right
    
    # 3. Add Bottom protrusion -> 8 tiles
    # Row y=14, x from 6 to 20
    for x in range(6, 22, 2):
        coords.append((x, 14, 0))
        
    # 4. Add Top protrusion -> 3 tiles
    # Row y=0, x=10, 12, 14
    coords.append((10, 0, 0)); coords.append((12, 0, 0)); coords.append((14, 0, 0))

    # --- Layer 1: 6x6 Block (36 tiles) ---
    # Rows 2 to 12 (6 rows), Cols 8 to 18 (6 cols)
    # WARNING: Must sit roughly centrally on top of Layer 0
    for y in range(2, 14, 2):      # y: 2, 4, 6, 8, 10, 12
        for x in range(8, 20, 2):  # x: 8, 10, 12, 14, 16, 18
            coords.append((x, y, 1))

    # --- Layer 2: 4x4 Block (16 tiles) ---
    # Rows 4 to 10 (4 rows), Cols 10 to 16 (4 cols)
    for y in range(4, 12, 2):       # y: 4, 6, 8, 10
        for x in range(10, 18, 2):  # x: 10, 12, 14, 16
            coords.append((x, y, 2))

    # --- Layer 3: 2x2 Block (4 tiles) ---
    coords.append((12, 8, 3)); coords.append((14, 8, 3))
    coords.append((12, 10, 3)); coords.append((14, 10, 3))

    # --- Layer 4: The Top Tile (1 tile) ---
    coords.append((13, 9, 4)) 

    return coords