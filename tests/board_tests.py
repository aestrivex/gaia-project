import unittest

from gaia_project.board import GameBoard

class Test(unittest.TestCase):
 
  def test_illegal_planet(self):
    with self.assertRaises(ValueError):
      b = GameBoard()
      b.add_building(3, 3, 'yellow', 'mine')
    
if __name__ == "__main__":
  unittest.main()
