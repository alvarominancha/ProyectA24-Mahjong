"""
Unit tests for the Tile class.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from tile import Tile
from board import Board


class TestTile(unittest.TestCase):
    """Test cases for the Tile class."""
    
    def test_tile_creation(self):
        """Test creating a tile."""
        tile = Tile(Tile.BAMBOO, 5, 0)
        self.assertEqual(tile.suit, Tile.BAMBOO)
        self.assertEqual(tile.rank, 5)
        self.assertEqual(tile.unique_id, 0)
    
    def test_tile_matching_suited(self):
        """Test matching for suited tiles."""
        tile1 = Tile(Tile.BAMBOO, 5, 0)
        tile2 = Tile(Tile.BAMBOO, 5, 1)
        tile3 = Tile(Tile.BAMBOO, 3, 2)
        tile4 = Tile(Tile.CHARACTER, 5, 3)
        
        self.assertTrue(tile1.matches(tile2))
        self.assertFalse(tile1.matches(tile3))
        self.assertFalse(tile1.matches(tile4))
    
    def test_tile_matching_flowers(self):
        """Test matching for flower tiles."""
        flower1 = Tile(Tile.FLOWER, 1, 0)
        flower2 = Tile(Tile.FLOWER, 2, 1)
        season1 = Tile(Tile.SEASON, 1, 2)
        
        # Flowers match any flower
        self.assertTrue(flower1.matches(flower2))
        # But not seasons
        self.assertFalse(flower1.matches(season1))
    
    def test_tile_matching_seasons(self):
        """Test matching for season tiles."""
        season1 = Tile(Tile.SEASON, 1, 0)
        season2 = Tile(Tile.SEASON, 3, 1)
        
        # Seasons match any season
        self.assertTrue(season1.matches(season2))
    
    def test_tile_string_representation(self):
        """Test string representation of tiles."""
        tile = Tile(Tile.BAMBOO, 5, 0)
        self.assertEqual(str(tile), "bamboo-5")
        
        wind = Tile(Tile.WIND, Tile.EAST, 1)
        self.assertEqual(str(wind), "wind-east")
    
    def test_tile_equality(self):
        """Test tile equality."""
        tile1 = Tile(Tile.BAMBOO, 5, 0)
        tile2 = Tile(Tile.BAMBOO, 5, 1)
        tile3 = Tile(Tile.BAMBOO, 3, 2)
        
        # With unique IDs, tiles are different
        self.assertNotEqual(tile1, tile2)
        self.assertNotEqual(tile1, tile3)
    
    def test_tile_is_free_simple(self):
        """Test if a tile is free (simple case)."""
        board = Board()
        
        # Add a single tile
        tile = Tile(Tile.BAMBOO, 5, 0)
        tile.x = 0
        tile.y = 0
        tile.z = 0
        board.tiles.append(tile)
        
        # Single tile should be free
        self.assertTrue(tile.is_free(board))
    
    def test_tile_is_free_blocked_top(self):
        """Test if a tile is blocked from above."""
        board = Board()
        
        # Add a tile
        tile1 = Tile(Tile.BAMBOO, 5, 0)
        tile1.x = 0
        tile1.y = 0
        tile1.z = 0
        board.tiles.append(tile1)
        
        # Add a tile on top
        tile2 = Tile(Tile.BAMBOO, 3, 1)
        tile2.x = 0
        tile2.y = 0
        tile2.z = 1
        board.tiles.append(tile2)
        
        # Bottom tile should not be free
        self.assertFalse(tile1.is_free(board))
        # Top tile should be free (if sides are free)
        self.assertTrue(tile2.is_free(board))


if __name__ == '__main__':
    unittest.main()
