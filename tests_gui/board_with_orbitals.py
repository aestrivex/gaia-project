import sys
import pygame

from gaia_project.board import GameBoard


if __name__ == '__main__':

  b = GameBoard()


  b.add_orbital(7, 7, ['yellow', 'orange'])
  b.add_orbital(8, 8, ['blue'])
  b.add_orbital(8, 5, ['red', 'white', 'gray'])
  b.add_orbital(13, 11, ['red', 'yellow', 'blue', 'orange'])
  

  b.add_orbital(9, 5, ['gray', 'yellow', 'brown'], space_station=True)
  b.add_orbital(11, 5, ['white'], space_station=True)
  b.add_orbital(11, 11, ['gray', 'yellow'], space_station=True)
  b.add_orbital(4, 6, [], space_station=True)

  #print(b.m.units[9,5].traits())
  b.m.units[9,5].space_station = 5
  print(b.m.units[9,5].space_station)

  #print(b.m.ascii())


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
