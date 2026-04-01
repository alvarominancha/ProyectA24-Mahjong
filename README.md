# ProyectA24-Mahjong

A complete Mahjong Solitaire game implementation in Python using Pygame.

## Features

### Phase 1: Board Model and Logic ✓
- Complete tile set with 144 Mahjong tiles (suited, wind, dragon, flower, season)
- Board layout with turtle/pyramid configuration
- Tile matching and selection logic
- Rule validation (free tiles, adjacency checks)

### Phase 2: GUI and Rendering ✓
- Interactive pygame window
- Visual tile rendering with layering
- Mouse interaction (hover and click)
- UI buttons (New Game, Undo, Hint, Quit)

### Phase 3: Game Mechanics ✓
- Tile selection and highlighting
- Matching and removal logic
- Undo functionality
- Hint system

### Phase 4: Game States ✓
- Game state management (menu, playing, won, lost)
- Move counter
- Game timer
- Win/loss detection

### Phase 5: Save/Load System (Coming Soon)
- Save/load game state
- Player profiles
- Settings menu
- High scores

### Phase 6: Advanced Features (Coming Soon)
- Multiple board layouts
- Sound effects and music
- Game solver
- Shuffle feature

## Installation

1. Clone the repository:
```bash
git clone https://github.com/alvarominancha/ProyectA24-Mahjong.git
cd ProyectA24-Mahjong
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Play

Run the game:
```bash
python mahjong.py
```

### Controls

- **Mouse Click**: Select/deselect tiles
- **New Game Button** or **N key**: Start a new game
- **Undo Button** or **U key**: Undo last move
- **Hint Button** or **H key**: Show a valid matching pair
- **Quit Button** or **ESC key**: Exit game

### Rules

- Match pairs of identical tiles to remove them from the board
- Only free tiles can be selected (not blocked from above and at least one side open)
- Flower and season tiles match any within their category
- Clear all tiles to win!

## Running Tests

Run the test suite:
```bash
python -m unittest discover tests -v
```

## Project Structure

```
ProyectA24-Mahjong/
├── src/
│   ├── tile.py          # Tile class definition
│   ├── tileset.py       # TileSet management
│   ├── board.py         # Board and game logic
│   ├── renderer.py      # Pygame rendering
│   ├── game.py          # Main game engine
│   └── create_tiles.py  # Tile image generator
├── tests/
│   ├── test_tile.py     # Tile tests
│   ├── test_tileset.py  # TileSet tests
│   └── test_board.py    # Board tests
├── assets/
│   └── tiles/           # Tile images
├── requirements.txt
├── mahjong.py          # Game launcher
└── README.md
```

## License

This project is open source and available for educational purposes.