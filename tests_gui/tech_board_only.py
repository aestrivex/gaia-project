import sys
import pygame
from gaia_project.tech_board import TechBoard, TechBoardRender

if __name__ == '__main__':

  t = TechBoard(600, 800, None)

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
          pass

      window.fill( pygame.Color('black'))
      t.paint(window, (1000,0))
      
      pygame.display.update()
      fps_clock.tick(10)
  finally:
    pygame.quit()
