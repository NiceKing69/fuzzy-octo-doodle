import unittest
from file_parser import load_puzzle
from grid_utils import get_available_positions
from solver import smart_solution, brute_force_solution


class TestPuzzleSolver(unittest.TestCase):

    def test_load_puzzle_mad_1(self):
        grid, blocks, lazors, targets = load_puzzle("mad_1.bff")
        self.assertGreater(len(grid), 0, "Grid should not be empty")
        self.assertGreater(sum(blocks.values()), 0,
                           "There should be some available blocks")
        self.assertGreater(
            len(lazors),
            0,
            "There should be at least one lazor")
        self.assertGreater(
            len(targets),
            0,
            "There should be at least one target")

    def test_available_positions(self):
        grid, _, _, _ = load_puzzle("mad_1.bff")
        positions = get_available_positions(grid)
        self.assertTrue(all(grid[y][x] == 'o' for x, y in positions),
                        "All returned positions should be marked with 'o'")

    def test_smart_solution(self):
        result = smart_solution("mad_1.bff")
        self.assertIsNotNone(
            result, "Smart solution should return a valid result or fallback")
        self.assertIsInstance(result, tuple)
        grid, placed_blocks = result
        self.assertTrue(len(placed_blocks) > 0,
                        "There should be at least one placed block")

    def test_brute_force_solution(self):
        result = brute_force_solution("mad_4.bff")
        self.assertIsNotNone(
            result, "Brute-force solution should return a result")
        grid, placed_blocks = result
        self.assertTrue(
            len(placed_blocks) > 0,
            "Brute-force should place some blocks")


if __name__ == "__main__":
    unittest.main()
