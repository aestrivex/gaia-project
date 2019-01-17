from hexmap import Map, MapUnit, RenderGrid, RenderUnits
import sys
import pygame

import numpy as np
from traits.api import HasPrivateTraits, Enum, Property
SQRT3 = np.sqrt(3)


class Planet_Meta(type(HasPrivateTraits), type(MapUnit)):
  pass

class HasPrivateTraits(MapUnit):
  pass


class Planet(HasPrivateTraits):
  __metaclass__ = Planet_Meta

  planet_type = Enum('gaia', 'volcanic', 'oxide', 'terra', 'ice', 'titanium',
                     'swamp', 'desert', 'transdim')
  color = Property(depends_on = 'planet_type')
  def _get_color(self):
    planet_color_map = {'gaia' : pygame.Color( 51, 204, 51),
                        'volcanic' : pygame.Color( 255, 116, 0),
                        'oxide' : pygame.Color( 153, 0, 51),
                        'terra' : pygame.Color( 0, 153, 255),
                        'ice' : pygame.Color( 221, 221, 221),
                        'titanium' : pygame.Color( 122, 122, 122),
                        'swamp' : pygame.Color( 153, 102, 51),
                        'desert' : pygame.Color( 220, 170, 0),
                        'transdim' : pygame.Color( 140, 26, 225)}
    return planet_color_map[planet_type]

  def __init__(self, planet_type):
    self.planet_type = planet_type
    
  def paint(self, surface):
    radius = surface.get_width() // 2
    pygame.draw.circle(surface, self.color, (radius, int(SQRT3 / 2 * radius)),
                       int(radius - radius * .3) )




if __name__ == '__main__':

  m = Map( (15, 14) )

  grid = RenderGrid(m, radius=50)
  units = RenderUnits(m, radius=50)

  m.units[(4, 7)] = Planet('volcanic')
  m.units[(8, 8)] = Planet('oxide')
  m.units[(6, 2)] = Planet('titanium')
  m.units[(11, 5)] = Planet('swamp')
  m.units[(13, 9)] = Planet('desert')
  m.units[(14, 11)] = Planet('transdim')
  m.units[(6, 12)] = Planet('terra')
  m.units[(4, 10)] = Planet('ice')
  m.units[(13, 3)] = Planet('gaia')


  try:
    pygame.init()
    fps_clock = pygame.time.Clock()
  
    window = pygame.display.set_mode( (800, 600), 1)
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
    fpsClock.tick(10)
  finally:
    pygame.quit()
