"""
Layouts Module
Defines the tile positions (x, y, z) for different map configurations.
Each layout is designed to produce an even number of tiles for gameplay validity.
"""

def get_turtle_layout():
    """
    Map 1: The Classic Turtle (Refined).
    Features a large central pyramid with distinct head, tail, and legs.
    """
    positions = []
    
    # --- Layer 0: Base Body ---
    # Main rectangle body
    for x in range(6, 44, 2):
        for y in range(2, 18, 2):
            positions.append((x, y, 0))
            
    # Head (Left) and Tail (Right)
    positions.append((2, 8, 0)); positions.append((2, 10, 0))   # Head tip
    positions.append((4, 8, 0)); positions.append((4, 10, 0))   # Neck
    positions.append((44, 8, 0)); positions.append((44, 10, 0)) # Tail base
    positions.append((46, 8, 0)); positions.append((46, 10, 0)) # Tail tip
    
    # Legs (Top and Bottom corners)
    for x in [8, 10, 38, 40]:
        positions.append((x, 0, 0))  # Top legs
        positions.append((x, 18, 0)) # Bottom legs

    # --- Layer 1: Shell Tier 1 ---
    for x in range(12, 38, 2):
        for y in range(4, 16, 2):
            positions.append((x, y, 1))

    # --- Layer 2: Shell Tier 2 ---
    for x in range(16, 34, 2):
        for y in range(6, 14, 2):
            positions.append((x, y, 2))

    # --- Layer 3: Shell Tier 3 ---
    for x in range(20, 30, 2):
        for y in range(8, 12, 2):
            positions.append((x, y, 3))

    # --- Layer 4: Summit ---
    positions.append((24, 8, 4))
    positions.append((24, 10, 4))

    return positions


def get_butterfly_layout():
    """
    Map 2: The Butterfly.
    A highly symmetric layout with a tall central body and spreading wings.
    Symmetry guarantees an even tile count.
    """
    positions = []
    
    # --- Central Body (Tall column) ---
    for z in range(5):
        for y in range(2, 18, 2):
            positions.append((24, y, z))

    # --- Wings (Symmetric Left and Right) ---
    
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
    Map 3: The Fortress.
    A strategic layout with high outer walls protecting a lower interior courtyard.
    """
    positions = []
    
    # --- Layer 0: Solid Foundation ---
    for x in range(6, 44, 2):
        for y in range(2, 18, 2):
            positions.append((x, y, 0))
            
    # --- Layers 1, 2, 3: Outer Walls ---
    # We build walls on the perimeter (Top, Bottom, Left, Right)
    for z in [1, 2, 3]:
        # Top and Bottom walls
        for x in range(6, 44, 2):
            positions.append((x, 2, z))
            positions.append((x, 16, z))
        # Left and Right walls (excluding corners to avoid double counting)
        for y in range(4, 16, 2):
            positions.append((6, y, z))
            positions.append((42, y, z))
            
    # --- Layer 4: Corner Towers ---
    corners = [(6, 2), (42, 2), (6, 16), (42, 16)]
    for (x, y) in corners:
        positions.append((x, y, 4))
        
    # --- Layer 1: Interior Courtyard structures ---
    # Small clusters in the center
    positions.append((24, 8, 1)); positions.append((24, 10, 1))
    positions.append((22, 8, 1)); positions.append((22, 10, 1))
    positions.append((26, 8, 1)); positions.append((26, 10, 1))

    return positions