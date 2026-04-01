#!/usr/bin/env python3
"""
Launcher script for Mahjong Solitaire game.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from game import main

if __name__ == "__main__":
    main()
