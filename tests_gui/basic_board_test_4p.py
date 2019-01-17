import sys
import pygame

from gaia_project.board import GameBoard
from gaia_project.constants import BASIC_4P_SETUP

if __name__ == '__main__':

  b = GameBoard(cfg=BASIC_4P_SETUP)

  print(b.m.ascii())


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
          print(units.get_cell(event.pos)) 

      window.fill( pygame.Color('black'))
      b.paint(window, (0,0))
      
      pygame.display.update()
      fps_clock.tick(10)
  finally:
    pygame.quit()
