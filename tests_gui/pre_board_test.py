import sys
import pygame

from hexmap import Map, MapUnit, RenderGrid, RenderUnits
from gaia_project.board import Planet


if __name__ == '__main__':

  m = Map( (15, 14) )

  grid = RenderGrid(m, radius=42)
  units = RenderUnits(m, radius=42)

  vp = Planet(m, 'volcanic')

  m.units[(4, 7)] = vp 
  m.units[(8, 8)] = Planet(m, 'oxide')
  m.units[(6, 2)] = Planet(m, 'titanium')
  m.units[(11, 5)] = Planet(m, 'swamp')
  m.units[(13, 9)] = Planet(m, 'desert')
  m.units[(14, 11)] = Planet(m, 'transdim')
  m.units[(6, 12)] = Planet(m, 'terra')
  m.units[(3, 6)] = Planet(m, 'ice')
  m.units[(13, 3)] = Planet(m, 'gaia')

  print(m.ascii())


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
      grid.draw()
      units.draw()
      
      window.blit( grid, (0,0))
      window.blit( units, (0,0))
  
      pygame.display.update()
      fps_clock.tick(10)
  finally:
    pygame.quit()
