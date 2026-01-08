"""
Layouts Module.

This module defines the specific tile arrangements (maps) for the game.
Each layout function calculates and returns a list of (x, y, z) coordinates
representing the 3D position of every tile on the board.
"""

def get_turtle_layout():
    """
    Generates the classic 'Turtle' formation.
    
    This layout features a large central pyramid (the shell) built up to
    5 layers, with distinct extensions representing the head, tail, and legs.
    
    Returns:
        list: A list of (x, y, z) tuples representing tile coordinates.
    """
    positions = []
    
    # --- LAYER 0: BASE BODY ---
    # Main rectangular body
    for x in range(6, 44, 2):
        for y in range(2, 18, 2):
            positions.append((x, y, 0))
            
    # Head (Left) and Tail (Right) extensions
    positions.append((2, 8, 0)); positions.append((2, 10, 0))   # Head tip
    positions.append((4, 8, 0)); positions.append((4, 10, 0))   # Neck
    positions.append((44, 8, 0)); positions.append((44, 10, 0)) # Tail base
    positions.append((46, 8, 0)); positions.append((46, 10, 0)) # Tail tip
    
    # Legs (Top and Bottom corners)
    for x in [8, 10, 38, 40]:
        positions.append((x, 0, 0))  # Top legs
        positions.append((x, 18, 0)) # Bottom legs

    # --- LAYER 1: SHELL TIER 1 ---
    for x in range(12, 38, 2):
        for y in range(4, 16, 2):
            positions.append((x, y, 1))

    # --- LAYER 2: SHELL TIER 2 ---
    for x in range(16, 34, 2):
        for y in range(6, 14, 2):
            positions.append((x, y, 2))

    # --- LAYER 3: SHELL TIER 3 ---
    for x in range(20, 30, 2):
        for y in range(8, 12, 2):
            positions.append((x, y, 3))

    # --- LAYER 4: SUMMIT ---
    positions.append((24, 8, 4))
    positions.append((24, 10, 4))

    return positions


def get_butterfly_layout():
    """
    Generates the 'Butterfly' formation.
    
    A highly symmetric layout featuring a tall central column (the body)
    and wide, tiered triangles on either side representing spreading wings.
    
    Returns:
        list: A list of (x, y, z) tuples representing tile coordinates.
    """
    positions = []
    
    # --- CENTRAL BODY ---
    # A tall column in the center (x=24)
    for z in range(5):
        for y in range(2, 18, 2):
            positions.append((24, y, z))

    # --- WINGS (SYMMETRIC) ---
    
    # Layer 0: Wide base wings
    for y in range(2, 18, 2):
        # Left Wing
        start_x_left = 2 + abs(y - 10)
        end_x_left = 22
        for x in range(start_x_left, end_x_left, 2):
            positions.append((x, y, 0))
        
        # Right Wing
        start_x_right = 28
        end_x_right = 48 - abs(y - 10)
        for x in range(start_x_right, end_x_right, 2):
            positions.append((x, y, 0))

    # Layer 1: Inner Wing Relief
    for y in range(4, 16, 2):
        # Left
        for x in range(8, 20, 2):
            positions.append((x, y, 1))
        # Right
        for x in range(30, 42, 2):
            positions.append((x, y, 1))

    # Layer 2: Wing Details
    for y in range(6, 14, 2):
        # Left detail
        positions.append((16, y, 2)); positions.append((18, y, 2))
        # Right detail
        positions.append((30, y, 2)); positions.append((32, y, 2))

    return positions


def get_colosseum_layout():
    """
    Generates the 'Fortress' (Colosseum) formation.
    
    A strategic layout with high outer walls forming a perimeter,
    protecting a lower interior courtyard with scattered piles.
    
    Returns:
        list: A list of (x, y, z) tuples representing tile coordinates.
    """
    positions = []
    
    # --- LAYER 0: SOLID FOUNDATION ---
    for x in range(6, 44, 2):
        for y in range(2, 18, 2):
            positions.append((x, y, 0))
            
    # --- LAYERS 1-3: OUTER WALLS ---
    # Build walls on the perimeter (Top, Bottom, Left, Right)
    for z in [1, 2, 3]:
        # Top and Bottom walls
        for x in range(6, 44, 2):
            positions.append((x, 2, z))
            positions.append((x, 16, z))
        # Left and Right walls (excluding corners to avoid double counting)
        for y in range(4, 16, 2):
            positions.append((6, y, z))
            positions.append((42, y, z))
            
    # --- LAYER 4: CORNER TOWERS ---
    corners = [(6, 2), (42, 2), (6, 16), (42, 16)]
    for (x, y) in corners:
        positions.append((x, y, 4))
        
    # --- LAYER 1: INTERIOR COURTYARD ---
    # Small clusters in the center
    positions.append((24, 8, 1)); positions.append((24, 10, 1))
    positions.append((22, 8, 1)); positions.append((22, 10, 1))
    positions.append((26, 8, 1)); positions.append((26, 10, 1))

    return positions