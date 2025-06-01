import unittest
import numpy as np
import os
import json
from conways_game_of_life import GameOfLife # Assuming the main file is conways_game_of_life.py

class TestGameOfLife(unittest.TestCase):

    def setUp(self):
        # Common setup for tests: a small game instance
        # Suppress Pygame display initialization for tests if possible,
        # or ensure it doesn't block. For now, we'll assume GameOfLife
        # can be instantiated without full Pygame window setup for logic testing.
        # This might require GameOfLife __init__ to be more flexible or to mock Pygame.
        # For this subtask, we'll proceed as if it works, but it's a potential issue.
        self.game = GameOfLife(width=100, height=100, cell_size=10, fps=60)
        # Override Pygame's display dependent parts if they are called in __init__
        # This is a common challenge when testing Pygame apps.
        # A simple approach:
        self.game.screen = None # Prevent actual screen operations
        self.game.font = None # Prevent font operations

    def test_stable_pattern_block(self):
        # 2x2 block is stable
        self.game.grid.fill(0)
        self.game.grid[2:4, 2:4] = 1
        self.game.cell_ages.fill(0)
        self.game.cell_ages[self.game.grid == 1] = 1

        self.game.stable_count = 0
        self.game.generation = 0

        for _ in range(12): # Run for enough steps to trigger stability
            if self.game.stable_count >= 10:
                break
            previous_grid_state = np.copy(self.game.grid)
            self.game.grid = self.game.update_grid() # This now also updates self.cell_ages

            if np.array_equal(self.game.grid, previous_grid_state):
                self.game.stable_count += 1
            else:
                self.game.stable_count = 0
            self.game.generation +=1

        self.assertGreaterEqual(self.game.stable_count, 10, "Stable count should reach 10 for a block.")
        self.assertTrue(np.array_equal(self.game.grid[2:4, 2:4], np.ones((2,2))), "Block pattern should remain.")

    def test_oscillator_blinker(self):
        # Blinker (period 2)
        self.game.grid.fill(0)
        self.game.grid[2, 1:4] = 1 # Horizontal blinker
        initial_pattern = np.copy(self.game.grid)
        self.game.cell_ages.fill(0)
        self.game.cell_ages[self.game.grid == 1] = 1

        self.game.grid = self.game.update_grid() # Gen 1
        self.assertFalse(np.array_equal(self.game.grid, initial_pattern), "Blinker should change after 1 gen.")

        self.game.grid = self.game.update_grid() # Gen 2
        self.assertTrue(np.array_equal(self.game.grid, initial_pattern), "Blinker should return to initial state after 2 gens.")

    def test_save_and_load_grid(self):
        test_filename = "test_grid_save_load.json"
        self.game.grid.fill(0)
        self.game.grid[0, 0] = 1
        self.game.grid[1, 1] = 1
        self.game.grid[self.game.ROWS-1, self.game.COLS-1] = 1
        original_grid = np.copy(self.game.grid)

        self.game.save_grid_to_file(test_filename)

        # Clear grid before loading
        self.game.grid.fill(0)
        self.game.cell_ages.fill(0)

        self.game.load_grid_from_file(test_filename)

        self.assertTrue(np.array_equal(self.game.grid, original_grid), "Loaded grid should match original.")

        expected_ages = np.zeros_like(original_grid)
        expected_ages[original_grid == 1] = 1
        self.assertTrue(np.array_equal(self.game.cell_ages, expected_ages), "Cell ages not correctly set after load.")

        if os.path.exists(test_filename):
            os.remove(test_filename)

    def test_cell_age_update(self):
        self.game.grid.fill(0)
        # Setup for a new cell and a surviving cell
        # A line of 2 cells will die, a line of 3 will produce a blinker
        #   . . . .
        #   . X X .  -> X will survive, X will die
        #   . . . .
        self.game.grid[2,2] = 1 # Surviving
        self.game.grid[2,3] = 1 # Dying
        self.game.cell_ages.fill(0)
        self.game.cell_ages[2,2] = 2 # Assume this one is 2 generations old
        self.game.cell_ages[2,3] = 1 # Assume this one is 1 generation old

        # A cell that will be born:
        # X . X
        # . X . -> new cell at center if self.grid[1,1] and self.grid[1,3] and self.grid[3,2] are set
        # X . X
        # For simplicity, let's test a simpler birth:
        # . X .
        # . X .
        # . X .
        # This will create two new cells at (1,2) and (3,2) if grid is [0,1,0], [0,1,0], [0,1,0] at col 2
        self.game.grid.fill(0) # Reset
        self.game.grid[1,2] = 1
        self.game.grid[2,2] = 1
        self.game.grid[3,2] = 1
        self.game.cell_ages.fill(0)
        self.game.cell_ages[1:4,2] = 1 # All age 1 initially

        # Expected next state:
        # . . .
        # X X X  (cell at (2,1) is new, (2,2) survives, (2,3) is new)
        # . . .

        self.game.grid = self.game.update_grid() # This also updates self.cell_ages internally

        self.assertEqual(self.game.grid[2,1], 1, "Cell should be born at (2,1).")
        self.assertEqual(self.game.cell_ages[2,1], 1, "Newly born cell at (2,1) should have age 1.")

        self.assertEqual(self.game.grid[2,2], 1, "Cell should survive at (2,2).")
        self.assertEqual(self.game.cell_ages[2,2], 2, "Surviving cell at (2,2) should have age incremented to 2.")

        self.assertEqual(self.game.grid[2,3], 1, "Cell should be born at (2,3).")
        self.assertEqual(self.game.cell_ages[2,3], 1, "Newly born cell at (2,3) should have age 1.")

        self.assertEqual(self.game.grid[1,2], 0, "Cell should die at (1,2).")
        self.assertEqual(self.game.cell_ages[1,2], 0, "Dead cell at (1,2) should have age 0.")

        self.assertEqual(self.game.grid[3,2], 0, "Cell should die at (3,2).")
        self.assertEqual(self.game.cell_ages[3,2], 0, "Dead cell at (3,2) should have age 0.")

if __name__ == '__main__':
    unittest.main()
