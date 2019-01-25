import sys
import pygame

from gaia_project.board import GameBoard


if __name__ == '__main__':

  b = GameBoard()

  b.add_building(4, 4, 'yellow', 'mine')
  b.add_building(4, 3, 'yellow', 'trading post', lantid_share=True)
  b.add_building(5, 6, 'red', 'planetary institute', lantid_share=True)
  b.add_building(6, 7, 'yellow', 'gaiaformer')
  b.add_building(7, 9, 'white', 'research lab')
  b.add_building(9, 9, 'white', 'academy')
  b.add_building(9, 10, 'white', 'lost planet')

  #print(b.m.ascii())

  print(b.get_size())

  try:
    pygame.init()
    fps_clock = pygame.time.Clock()
  
    window = pygame.display.set_mode( (1600, 1200), 1)
    from pygame.locals import QUIT, MOUSEBUTTONDOWN
  
    while True:
      for event in pygame.event.get():
        if event.type == QUIT:
          pygame.quit()
          sys.exit()
        if event.type == MOUSEBUTTONDOWN:
          #print(units.get_cell(event.pos)) 
          pass

      window.fill( pygame.Color('black'))
      b.paint(window, (0,0))
      
      pygame.display.update()
      fps_clock.tick(10)
  finally:
    pygame.quit()
