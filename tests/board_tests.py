import unittest

from gaia_project.board import GameBoard

class Test(unittest.TestCase):
 
  def test_illegal_planet(self):
    with self.assertRaises(ValueError):
      b = GameBoard()
      b.add_building(3, 3, 'yellow', 'mine')

  def test_illegal_gaiaformer(self):
    with self.assertRaises(ValueError):
      b = GameBoard()
      b.add_building(4, 4, 'yellow', 'gaiaformer')

  def test_illegal_nongaiaformer(self):
    with self.assertRaises(ValueError):
      b = GameBoard()
      b.add_building(6, 7, 'yellow', 'mine')

  def test_lantid_share_gaiaformer(self):
    with self.assertRaises(ValueError):
      b = GameBoard()
      b.add_building(6, 7, 'yellow', 'gaiaformer', lantid_share=True)
    
if __name__ == "__main__":
  unittest.main()
