"""
Unit tests for the Board class.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from tile import Tile
from tileset import TileSet
from board import Board


class TestBoard(unittest.TestCase):
    """Test cases for the Board class."""
    
    def test_board_creation(self):
        """Test creating a board."""
        board = Board()
        self.assertEqual(len(board.tiles), 0)
    
    def test_board_setup(self):
        """Test setting up a board with tiles."""
        board = Board()
        tileset = TileSet()
        tileset.shuffle()
        board.setup_board(tileset)
        
        # Should have tiles placed
        self.assertGreater(len(board.tiles), 0)
    
    def test_board_turtle_layout(self):
        """Test that the turtle layout has the expected number of positions."""
        board = Board()
        tileset = TileSet()
        board.setup_board(tileset)
        
        # Count positions in turtle layout
        expected_positions = 0
        for layer in Board.TURTLE_LAYOUT:
            for row in layer:
                expected_positions += row.count('X')
        
        # Should have tiles for all positions
        self.assertEqual(len(board.tiles), expected_positions)
    
    def test_get_tile_at(self):
        """Test getting a tile at specific coordinates."""
        board = Board()
        tileset = TileSet()
        board.setup_board(tileset)
        
        # Get first tile and check we can retrieve it
        if board.tiles:
            first_tile = board.tiles[0]
            found_tile = board.get_tile_at(first_tile.x, first_tile.y, first_tile.z)
            self.assertEqual(found_tile, first_tile)
    
    def test_remove_tiles(self):
        """Test removing a matching pair of tiles."""
        board = Board()
        
        # Create two matching tiles that are free
        tile1 = Tile(Tile.BAMBOO, 5, 0)
        tile1.x = 0
        tile1.y = 0
        tile1.z = 0
        
        tile2 = Tile(Tile.BAMBOO, 5, 1)
        tile2.x = 5
        tile2.y = 0
        tile2.z = 0
        
        board.tiles = [tile1, tile2]
        
        # Remove the tiles
        result = board.remove_tiles(tile1, tile2)
        self.assertTrue(result)
        self.assertEqual(len(board.tiles), 0)
        self.assertEqual(len(board.removed_tiles), 2)
    
    def test_remove_tiles_invalid(self):
        """Test removing non-matching tiles fails."""
        board = Board()
        
        # Create two non-matching tiles
        tile1 = Tile(Tile.BAMBOO, 5, 0)
        tile1.x = 0
        tile1.y = 0
        tile1.z = 0
        
        tile2 = Tile(Tile.BAMBOO, 3, 1)
        tile2.x = 5
        tile2.y = 0
        tile2.z = 0
        
        board.tiles = [tile1, tile2]
        
        # Attempt to remove should fail
        result = board.remove_tiles(tile1, tile2)
        self.assertFalse(result)
        self.assertEqual(len(board.tiles), 2)
    
    def test_undo_move(self):
        """Test undoing a move."""
        board = Board()
        
        tile1 = Tile(Tile.BAMBOO, 5, 0)
        tile1.x = 0
        tile1.y = 0
        tile1.z = 0
        
        tile2 = Tile(Tile.BAMBOO, 5, 1)
        tile2.x = 5
        tile2.y = 0
        tile2.z = 0
        
        board.tiles = [tile1, tile2]
        
        # Remove tiles
        board.remove_tiles(tile1, tile2)
        self.assertEqual(len(board.tiles), 0)
        
        # Undo
        result = board.undo_last_move()
        self.assertTrue(result)
        self.assertEqual(len(board.tiles), 2)
    
    def test_is_game_won(self):
        """Test game won condition."""
        board = Board()
        board.tiles = []
        self.assertTrue(board.is_game_won())
        
        tile = Tile(Tile.BAMBOO, 5, 0)
        board.tiles = [tile]
        self.assertFalse(board.is_game_won())
    
    def test_get_matching_pairs(self):
        """Test finding matching pairs."""
        board = Board()
        
        # Create two matching free tiles
        tile1 = Tile(Tile.BAMBOO, 5, 0)
        tile1.x = 0
        tile1.y = 0
        tile1.z = 0
        
        tile2 = Tile(Tile.BAMBOO, 5, 1)
        tile2.x = 5
        tile2.y = 0
        tile2.z = 0
        
        board.tiles = [tile1, tile2]
        
        pairs = board.get_matching_pairs()
        self.assertEqual(len(pairs), 1)
        self.assertEqual(pairs[0], (tile1, tile2))
    
    def test_clear_board(self):
        """Test clearing the board."""
        board = Board()
        tileset = TileSet()
        board.setup_board(tileset)
        
        self.assertGreater(len(board.tiles), 0)
        
        board.clear_board()
        self.assertEqual(len(board.tiles), 0)
        self.assertEqual(len(board.removed_tiles), 0)


if __name__ == '__main__':
    unittest.main()
