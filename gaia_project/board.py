from hexmap import Map, MapUnit, RenderGrid, RenderUnits
import sys
import pygame

import numpy as np
from traits.api import HasPrivateTraits, Enum, Property
SQRT3 = np.sqrt(3)

from .constants import planet_color_map


class Planet_Meta(type(HasPrivateTraits), type(MapUnit)):
  pass

class HasPrivateTraits(MapUnit):
  pass


class Planet(MapUnit):
  __metaclass__ = Planet_Meta

  planet_type = Enum('gaia', 'volcanic', 'oxide', 'terra', 'ice', 'titanium',
                     'swamp', 'desert', 'transdim')
  color = Property(depends_on = 'planet_type')

  def __init__(self, grid, planet_type, *args, **kwargs):
    super().__init__(grid, *args, **kwargs)
    self.planet_type = planet_type
    
  def _get_color(self):
#    planet_color_map = {'gaia' : pygame.Color( 51, 204, 51),
#                        'volcanic' : pygame.Color( 255, 116, 0),
#                        'oxide' : pygame.Color( 153, 0, 51),
#                        'terra' : pygame.Color( 0, 153, 255),
#                        'ice' : pygame.Color( 221, 221, 221),
#                        'titanium' : pygame.Color( 122, 122, 122),
#                        'swamp' : pygame.Color( 153, 102, 51),
#                        'desert' : pygame.Color( 220, 170, 0),
#                        'transdim' : pygame.Color( 140, 26, 225)}
    return planet_color_map[self.planet_type]

  def paint(self, surface):
    radius = surface.get_width() // 2
    pygame.draw.circle(surface, self._get_color(), (radius, int(SQRT3 / 2 * radius)),
                       int(radius - radius * .3) )




if __name__ == '__main__':

  m = Map( (15, 14) )

  grid = RenderGrid(m, radius=32)
  units = RenderUnits(m, radius=32)

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
