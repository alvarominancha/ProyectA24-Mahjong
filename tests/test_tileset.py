"""
Unit tests for the TileSet class.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

import unittest
from tile import Tile
from tileset import TileSet


class TestTileSet(unittest.TestCase):
    """Test cases for the TileSet class."""
    
    def test_tileset_creation(self):
        """Test creating a complete tileset."""
        tileset = TileSet()
        # Standard Mahjong has 144 tiles
        self.assertEqual(len(tileset), 144)
    
    def test_tileset_tile_count(self):
        """Test the correct number of tiles per suit."""
        tileset = TileSet()
        
        # 3 suits x 9 ranks x 4 copies = 108 suited tiles
        bamboo_tiles = tileset.get_tiles_by_suit(Tile.BAMBOO)
        self.assertEqual(len(bamboo_tiles), 36)
        
        character_tiles = tileset.get_tiles_by_suit(Tile.CHARACTER)
        self.assertEqual(len(character_tiles), 36)
        
        dot_tiles = tileset.get_tiles_by_suit(Tile.DOT)
        self.assertEqual(len(dot_tiles), 36)
        
        # 4 winds x 4 copies = 16 tiles
        wind_tiles = tileset.get_tiles_by_suit(Tile.WIND)
        self.assertEqual(len(wind_tiles), 16)
        
        # 3 dragons x 4 copies = 12 tiles
        dragon_tiles = tileset.get_tiles_by_suit(Tile.DRAGON)
        self.assertEqual(len(dragon_tiles), 12)
        
        # 4 flower tiles
        flower_tiles = tileset.get_tiles_by_suit(Tile.FLOWER)
        self.assertEqual(len(flower_tiles), 4)
        
        # 4 season tiles
        season_tiles = tileset.get_tiles_by_suit(Tile.SEASON)
        self.assertEqual(len(season_tiles), 4)
    
    def test_tileset_unique_ids(self):
        """Test that each tile has a unique ID."""
        tileset = TileSet()
        unique_ids = set(tile.unique_id for tile in tileset.tiles)
        self.assertEqual(len(unique_ids), 144)
    
    def test_tileset_shuffle(self):
        """Test shuffling the tileset."""
        tileset1 = TileSet()
        tileset2 = TileSet()
        
        # Get initial order
        order1 = [tile.unique_id for tile in tileset1.tiles]
        order2 = [tile.unique_id for tile in tileset2.tiles]
        
        # Should start in the same order
        self.assertEqual(order1, order2)
        
        # Shuffle one
        tileset1.shuffle()
        order1_shuffled = [tile.unique_id for tile in tileset1.tiles]
        
        # Order should likely be different (very high probability)
        # We'll just check that all tiles are still there
        self.assertEqual(set(order1_shuffled), set(order2))
    
    def test_tileset_get_tiles_by_rank(self):
        """Test getting tiles by rank."""
        tileset = TileSet()
        
        # Get all tiles with rank 5
        rank5_tiles = tileset.get_tiles_by_rank(5)
        # Should have 3 suits x 4 copies = 12 tiles
        self.assertEqual(len(rank5_tiles), 12)


if __name__ == '__main__':
    unittest.main()
