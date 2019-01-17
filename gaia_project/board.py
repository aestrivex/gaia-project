from hexmap import Map, MapUnit, RenderGrid, RenderUnits, RenderFog
import sys
import pygame

import numpy as np
from traits.api import HasPrivateTraits, Enum, Property, Instance, List, Int
SQRT3 = np.sqrt(3)

from .constants import PLANET_COLOR_MAP, BASIC_2P_SETUP, BUILDING_COLOR_MAP


class MapUnit_Meta(type(HasPrivateTraits), type(MapUnit)):
  pass

class HasPrivateTraits(MapUnit):
  pass


class Planet(MapUnit):
  __metaclass__ = MapUnit_Meta

  planet_type = Enum('gaia', 'volcanic', 'oxide', 'terra', 'ice', 'titanium',
                     'swamp', 'desert', 'transdim')
  planet_color = Property(depends_on = 'planet_type')

  def __init__(self, grid, planet_type, *args, **kwargs):
    super().__init__(grid, *args, **kwargs)
    self.planet_type = planet_type
    
  def _get_planet_color(self):
    return PLANET_COLOR_MAP[self.planet_type]

  def paint(self, surface):
    radius = surface.get_width() // 2
    pygame.draw.circle(surface, self._get_planet_color(), 
                       (radius, int(SQRT3 / 2 * radius)),
                       int(radius - radius * .3) )

#TODO someday, maybe make the Buildings 3D models of real game pieces

#class Building(MapUnit):
#  __metaclass__ = MapUnit_Meta
#
#  sf = Instance(pygame.Surface)
#
#  def __init__(self, grid, sf, *args, **kwargs):
#    super().__init__(grid, *args, **kwargs)
#    self.sf = sf
#
#  def paint(self, surface):
#    radius = surface.get_width() // 2
#    #surface.blit(self.sf, (radius, int(SQRT3 / 2 * radius)))
#    #self.sf.blit(surface, (radius, int(SQRT3 / 2 * radius)))
#
#    x, y = self.position
#
#    surface.blit(self.sf, (x+radius//2, 
#                           y + (SQRT3 / 2 * radius)//2 ) )

class Building(Planet):
  building_type = Enum('mine', 'trading post', 'planetary institute',
                       'research lab', 'academy')

  building_color = Enum('orange', 'red', 'blue', 'white', 'gray',
                        'brown', 'yellow')
  

  def __init__(self, grid, planet_type, building_color, building_type='mine', 
               *args, **kwargs):
    super().__init__(grid, planet_type, *args, **kwargs)
    self.building_color = building_color
    self.building_type = building_type

  def paint(self, surface):
    radius = surface.get_width() // 2
    pygame.draw.circle(surface, self._get_planet_color(),
                       (radius, int(SQRT3 / 2 * radius)),
                       int(radius - radius * .3) )

    w, h = surface.get_size()

    left = w//4
    right = w*3//4
    top = h*7//20
    bottom = h*13//20

    building_rect = surface.subsurface( pygame.Rect( left, top, right-left, bottom-top ))
      

    if self.building_type == 'mine':
      bw, bh = building_rect.get_size()
      mine_top = int(bh * .8)
      mine_chimney_left = int(bw * .75)
      mine_chimney_right = int(bw * .88)
      points = ((0,0), (0, mine_top), (mine_chimney_left, mine_top),
                (mine_chimney_left, bh), (mine_chimney_right, bh),
                (mine_chimney_right, mine_top), (bw, mine_top), (bw, 0))

      pygame.draw.polygon(building_rect, 
                          BUILDING_COLOR_MAP[self.building_color], points)
    else:
      raise NotImplementedError



class GameBoard(HasPrivateTraits):
  m = Instance(Map)
  grid = Instance(RenderGrid)
  units = Instance(RenderUnits)
  fog = Instance(RenderFog)

  radius = Int
  
  def __init__(self, cfg=BASIC_2P_SETUP, radius=42, *args, **kwargs):

    self.radius = radius

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

  def add_building(self, x, y, player_color, building_type):
    #check if the specified hex is a planet
    if self.m.units[(x,y)] is None:
      raise ValueError("Cannot add building to non-planet")
    elif (self.m.units[(x,y)].planet_type == 'transdim' and 
          building_type != 'gaiaformer'):
      raise ValueError("Can only add gaiaformer to transdim planet")

    if self.m.units[(x,y)].planet_type == 'desert' and player_color == 'yellow':
      print("WARENING")


    planet_type = self.m.units[(x,y)].planet_type
    self.m.units[(x,y)] = Building(self.m, planet_type, player_color, 
                                   building_type)
    

#  def add_a_building(self):
#    chimg = pygame.image.load('/home/aestrivex/Downloads/component.png')
#
#    print(self.radius * .6)
#
#    #scale_chimg = pygame.transform.smoothscale(chimg, (int(self.radius * .6),
#    #                                                   int(self.radius * .6)))
#    
#
#    scale_chimg = pygame.transform.smoothscale(chimg, (self.radius, self.radius))
#
#    self.m.units[(3,3)] = Building(self.m.units, scale_chimg)
