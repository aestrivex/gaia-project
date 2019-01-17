from hexmap import Map, MapUnit, RenderGrid, RenderUnits, RenderFog
import sys
import pygame

import numpy as np
from traits.api import HasPrivateTraits, Enum, Property, Instance
SQRT3 = np.sqrt(3)

from .constants import PLANET_COLOR_MAP, BASIC_2P_SETUP


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
    planet_color_map = {'gaia' : pygame.Color( 51, 204, 51),
                        'volcanic' : pygame.Color( 255, 116, 0),
                        'oxide' : pygame.Color( 153, 0, 51),
                        'terra' : pygame.Color( 0, 153, 255),
                        'ice' : pygame.Color( 221, 221, 221),
                        'titanium' : pygame.Color( 122, 122, 122),
                        'swamp' : pygame.Color( 153, 102, 51),
                        'desert' : pygame.Color( 220, 170, 0),
                        'transdim' : pygame.Color( 140, 26, 225)}
    return planet_color_map[self.planet_type]

  def paint(self, surface):
    radius = surface.get_width() // 2
    pygame.draw.circle(surface, self._get_color(), (radius, int(SQRT3 / 2 * radius)),
                       int(radius - radius * .3) )



class GameBoard(HasPrivateTraits):
  m = Instance(Map)
  grid = Instance(RenderGrid)
  units = Instance(RenderUnits)
  fog = Instance(RenderFog)

  
  def __init__(self, cfg=BASIC_2P_SETUP, radius=42, *args, **kwargs):


    print(cfg)
    #determine board size
    max_x = 0
    for x,y in cfg:
      if x > max_x:
        max_x = x
  
    #instantiate board components
    self.m = Map( (max_x+5, max_x+5) )
  
    self.grid = RenderGrid(self.m, radius=radius)
    self.units = RenderUnits(self.m, radius=radius)
    self.fog = RenderFog(self.m, radius=radius)
  
    #Place planets
    for (x, y), tile in cfg.items():
      
      for (planet_x, planet_y), planet_type in tile.items():
        self.m.units[(x+planet_x, y+planet_y)] = Planet(self.m, planet_type)
  
    #fog out hexes not on board
      for cell in self.m.spread( (x+3, y+2), radius=2):
        self.m.fog[cell] = self.fog.VISIBLE
  

  def draw(self):
    self.grid.draw()
    self.units.draw()
    self.fog.draw()

  def blit(self, window, origin):
    window.blit(self.grid, origin)
    window.blit(self.units, origin)
    window.blit(self.fog, origin)

  def paint(self, window, origin):
    self.draw()
    self.blit(window, origin)
