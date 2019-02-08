from hexmap import Map, MapUnit, RenderGrid, RenderUnits, RenderFog
import sys
import pygame

import numpy as np
from traits.api import (HasPrivateTraits, Enum, Property, Instance, List, Int, 
                        Bool, Range, Tuple)

from .constants import PLANET_COLOR_MAP, BASIC_2P_SETUP, COMPONENT_COLOR_MAP
from .move_action import EventDescription


class Planet(MapUnit):

  def __init__(self, grid, planet_type, *args, **kwargs):
    super().__init__(grid, *args, **kwargs)
    self.planet_type = planet_type
    self.highlight = False
    
  def _get_planet_color(self):
    return PLANET_COLOR_MAP[self.planet_type]

  def paint(self, surface):
    radius = surface.get_width() // 2
    pygame.draw.circle(surface, self._get_planet_color(), 
                       (radius, int(np.sqrt(3) / 2 * radius)),
                       int(radius - radius * .3) )

    if self.highlight:
      pass

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
#    #surface.blit(self.sf, (radius, int(np.sqrt(3) / 2 * radius)))
#    #self.sf.blit(surface, (radius, int(np.sqrt(3) / 2 * radius)))
#
#    x, y = self.position
#
#    surface.blit(self.sf, (x+radius//2, 
#                           y + (np.sqrt(3) / 2 * radius)//2 ) )

class Building(Planet):
  def __init__(self, grid, planet_type, building_color, building_type='mine', 
               lantid_share=False, *args, **kwargs):
    super().__init__(grid, planet_type, *args, **kwargs)
    self.building_color = building_color
    self.building_type = building_type
    self.lantid_share = lantid_share

  def paint(self, surface):
    radius = surface.get_width() // 2
    pygame.draw.circle(surface, self._get_planet_color(),
                       (radius, int(np.sqrt(3) / 2 * radius)),
                       int(radius - radius * .3) )

    w, h = surface.get_size()

    left = w//4
    right = w*3//4
    top = h*7//20
    bottom = h*13//20

    building_rect = surface.subsurface( pygame.Rect( left, top, right-left, 
                                                     bottom-top ))
    bw, bh = building_rect.get_size()
      
    if self.building_type == 'lost planet':
      #draw the planet too
      radius = surface.get_width() // 2
      pygame.draw.circle(surface, PLANET_COLOR_MAP['lost planet'],
                        (radius, int(np.sqrt(3) / 2 * radius)),
                        int(radius - radius * .3),
                        1)

    if self.building_type in ('mine', 'lost planet'):
      outline_h = int(bh * .35)

      mine_h = int(bh * .4)

      chimney_l = int(bw * .7)
      chimney_r= int(bw * .8)

      outline_cl = int(bw * .65)
      outline_cr = int(bw * .85)

      mine_r = int(bw * .95)
      mine_l = int(bw * .05)

      mine_t = int(bh * .1)
      mine_b = int(bh * .9)

      outline_points = ((0, bh), (0, outline_h), 
                        (outline_cl, outline_h),
                        (outline_cl, 0), (outline_cr, 0),
                        (outline_cr, outline_h), (bw, outline_h), 
                        (bw, bh))

      building_points = ((mine_l, mine_b), (mine_l, mine_h), 
                         (chimney_l, mine_h), 
                         (chimney_l, mine_t), (chimney_r, mine_t), 
                         (chimney_r, mine_h), (mine_r, mine_h), 
                         (mine_r, mine_b))


    elif self.building_type == 'trading post':
      outline_h = int(bh * .35)

      post_h = int(bh * .4) 
      
      chimney_l = int(bw * .45)
      chimney_r = int(bw * .55)

      outline_cl = int(bw * .4)
      outline_cr = int(bw * .6)

      chimney_h = int(bh * .25)

      outline_ch = int(bh * .2)

      story_w = int(bw * .75)
      outline_sw = int(bw * .7)

      post_l = int(bw * .05)
      post_r = int(bw * .95)
      post_t = int(bh * .1)
      post_b = int(bh * .9)

      outline_points = ((0, bh), (0, outline_h), 
                        (outline_cl, outline_h),
                        (outline_cl, outline_ch), (outline_cr, outline_ch),
                        (outline_cr, outline_h), (outline_sw, outline_h),
                        (outline_sw, 0), (bw, 0), (bw, bh))

      building_points = ((post_l, post_b), (post_l, post_h),
                         (chimney_l, post_h),
                         (chimney_l, chimney_h), (chimney_r, chimney_h),
                         (chimney_r, post_h), (story_w, post_h),
                         (story_w, post_t), (post_r, post_t), (post_r, post_b))

    elif self.building_type == 'planetary institute':
      pi_h = int(bh * .5)
      story_h = int(bh * .25)

      story_l = int(bw * .25)
      story_r = int(bw * .75)

      mid_l = int(bw * .45)
      mid_r = int(bw * .55)

      pi_l = int(bw * .05)
      pi_r = int(bw * .95)
      pi_b = int(bh * .9)
      pi_t = int(bh * .1)

      outline_h = int(bh * .45)
      outline_sh = int(bh * .2)

      outline_sl = int(bw * .2)
      outline_sr = int(bw * .8)
      outline_ml = int(bw * .4)
      outline_mr = int(bw * .6)
      
      outline_points = ((0, bh), (0, outline_h), (outline_sl, outline_h),
                        (outline_sl, outline_sh), (outline_ml, outline_sh),
                        (outline_ml, 0), (outline_mr, 0),
                        (outline_mr, outline_sh), (outline_sr, outline_sh),
                        (outline_sr, outline_h), (bw, outline_h), (bw, bh))

      building_points = ((pi_l, pi_b), (pi_l, pi_h), (story_l, pi_h),
                         (story_l, story_h), (mid_l, story_h),
                         (mid_l, pi_t), (mid_r, pi_t),
                         (mid_r, story_h), (story_r, story_h),
                         (story_r, pi_h), (pi_r, pi_h), (pi_r, pi_b))

    elif self.building_type == 'research lab':
      rl_h = int(bh * .55)
      tower_h = int(bh * .35)

      tower_l = int(bw * .15)
      story_l = int(bw * .4)
      story_r = int(bw * .6)
      tower_r = int(bw * .85)

      outline_h = int(bh * .4)
      outline_th = int(bh * .2)
      outline_tl = int(bw * .2)
      outline_sl = int(bw * .35)
      outline_sr = int(bw * .65)
      outline_tr = int(bw * .8)

      rl_l = int(bw * .05)
      rl_r = int(bw * .95)
      rl_t = int(bh * .1)
      rl_b = int(bh * .9)
      
      outline_points = ((0, bh), (0, rl_h), (outline_tl, outline_th),
                        (outline_tl, outline_h), (outline_sl, 0),
                        (outline_sr, 0), (outline_tr, outline_h),
                        (outline_tr, outline_th), (bw, rl_h), (bw, bh))

      building_points = ((rl_l, rl_b), (rl_l, rl_h), (tower_l, tower_h),
                         (tower_l, rl_h), (story_l, rl_t),
                         (story_r, rl_t), (tower_r, rl_h),
                         (tower_r, tower_h), (rl_r, rl_h), (rl_r, rl_b))

    elif self.building_type == 'gaiaformer':
      g_h = int(bh * .45)
      
      gsl1 = int(bw * .2)
      gsr1 = int(bw * .4)
      gsl2 = int(bw * .6)
      gsr2 = int(bw * .8)

      outline_h = int(bh * .55)
      outline_gsl1 = int(bw * .15)
      outline_gsr1 = int(bw * .45)
      outline_gsl2 = int(bw * .55)
      outline_gsr2 = int(bw * .85)

      g_l = int(bw * .05)
      g_r = int(bw * .95)
      g_t = int(bh * .1)
      g_b = int(bh * .9)


      outline_points = ((0, bh), (0, g_h), (gsr1, 0), (gsl2, 0),
                        (bw, g_h), (bw, bh), (outline_gsr2, bh),
                        (outline_gsr2, outline_h), (outline_gsl2, outline_h),
                        (outline_gsl2, bh), (outline_gsr1, bh),
                        (outline_gsr1, outline_h), (outline_gsl1, outline_h),
                        (outline_gsl1, bh))

      building_points = ((g_l, g_b), (g_l, g_h), (gsr1, g_t), (gsl2, g_t),
                         (g_r, g_h), (g_r, g_b), (gsr2, g_b), 
                         (gsr2, g_h), (gsl2, g_h),
                         (gsl2, g_b), (gsr1, g_b),
                         (gsr1, g_h), (gsl1, g_h),
                         (gsl1, g_b))

    elif self.building_type == 'academy':
      ac_h = int(bh * .75)
      outline_h = int(bh * .7)

      story_h = int(bh * .5)
      outline_sh = int(bh * .45)

      ac_w = int(bw * .8)
      story_w = int(bw * .7)

      chimney_r = int(bw * .5)
      chimney_l = int(bw * .2)
      outline_cr = int(bw * .55)
      outline_cl = int(bw * .15)

      tri_l = int(bw * .3)
      tri_r = int(bw * .4)
      tri_h = int(bh * .25)
      outline_th = int(bh * .2)


      ac_l = int(bw * .05)
      ac_r = int(bw * .95)
      ac_t = int(bh * .1)
      ac_b = int(bh * .9)


      outline_points = ((0, bh), (outline_cl, ac_h), (outline_cl, outline_th),
                        (tri_l, 0), (tri_r, 0),
                        (outline_cr, outline_th), (outline_cr, outline_sh),
                        (story_w, outline_sh), (ac_w, outline_h),
                        (bw, outline_h), (bw, bh))

      building_points = ((ac_l, ac_b), (chimney_l, ac_h), (chimney_l, tri_h),
                         (tri_l, ac_t), (tri_r, ac_t),
                         (chimney_r, tri_h), (chimney_r, story_h),
                         (story_w, story_h), (ac_w, ac_h),
                         (ac_r, ac_h), (ac_r, ac_b))

    else:
      raise NotImplementedError("Cannot construct {0}".format(
                          self.building_type))

    pygame.draw.polygon(building_rect, pygame.Color('black'), outline_points)
    pygame.draw.polygon(building_rect, 
                        COMPONENT_COLOR_MAP[self.building_color], 
                        building_points)

    if self.lantid_share:
      lantid_b = h*4//5
      lantid_l = w*7//20
      lantid_r = w*13//20

      lantid_rect = surface.subsurface( pygame.Rect( lantid_l, bottom,
                                                     lantid_r - lantid_l,
                                                     lantid_b - bottom))

      lw, lh = lantid_rect.get_size()

      l_outh = int(lh * .3)

      l_mineh = int(lh * .4)

      l_chl = int(lw * .7)
      l_chr= int(lw * .8)

      l_outcl = int(lw * .65)
      l_outcr = int(lw * .85)

      l_miner = int(lw * .9)
      l_minel = int(lw * .1)

      l_minet = int(lh * .1)
      l_mineb = int(lh * .9)
    
      l_out_points = ((0, lh), (0, l_outh), (l_outcl, l_outh),
                      (l_outcl, 0), (l_outcr, 0),
                      (l_outcr, l_outh), (lw, l_outh), (lw, lh))

      l_mine_points = ((l_minel, l_mineb), (l_minel, l_mineh), 
                       (l_chl, l_mineh),
                       (l_chl, l_minet), (l_chr, l_minet),
                       (l_chr, l_mineh), (l_miner, l_mineh), 
                       (l_miner, l_mineb))

      pygame.draw.polygon(lantid_rect, pygame.Color('black'), l_out_points)
      pygame.draw.polygon(lantid_rect,
                          COMPONENT_COLOR_MAP['blue'],
                          l_mine_points)
      

class Orbital(MapUnit):

  def __init__(self, grid, satellites=[], space_station=False, *args, **kwargs):
    super().__init__(grid, *args, **kwargs)
    self.satellites = satellites
    self.space_station = space_station

  def paint(self, surface):

    w, h = surface.get_size()

    left = w*3//10
    right = w*7//10
    top = h//4
    bottom = h*3//4

    _, x1, x2, x3, x4 = np.linspace(left, right, num=5, endpoint=False)
    _, y1, y2, y3, y4 = np.linspace(top, bottom, num=5, endpoint=False)

    ex = w*2//25
    ey = h//10

    if self.space_station:

      station_points = ((left, y2), (x1, y2), (x2, y1), (x2, top), 
                        (x3, top), (x3, y1), (x4, y2), (right, y2),
                        (right, y3), (x4, y3), (x3, y4), (x3, bottom), 
                        (x2, bottom), (x2, y4), (x1, y3), (left, y3))

      pygame.draw.polygon(surface, COMPONENT_COLOR_MAP['space station'],
                          station_points)

      pygame.draw.rect(surface, COMPONENT_COLOR_MAP['red'],
                       pygame.Rect( (x2, y2, ex, ey)))

    sat_points_list = ((left, top), (x4, top), (left, y4), (x4, y4))

    for i, satellite_color in enumerate(self.satellites):
      pygame.draw.rect(surface, COMPONENT_COLOR_MAP[satellite_color],
                       (sat_points_list[i], (ex, ey)))
                      
class GameBoard(HasPrivateTraits):
  m = Instance(Map)
  grid = Instance(RenderGrid)
  units = Instance(RenderUnits)
  fog = Instance(RenderFog)

  radius = Range(low=25, value=42)

  width = Property
  height = Property
  size = Property

  highlighted_hexes = List(Tuple)
  
  def __init__(self, cfg=BASIC_2P_SETUP, radius=None, *args, **kwargs):

    #determine board size
    max_x = 0
    max_y = 0
    for x,y in cfg:
      if x > max_x:
        max_x = x
      if y > max_y:
        max_y = y
  
    #instantiate board components
    self.m = Map( (max_x+5, max_y+5) )

    if radius is not None:
      self.radius = radius
  
    radius_floor = int(self.radius)

    self.grid = RenderGrid(self.m, radius=radius_floor)
    self.units = RenderUnits(self.m, radius=radius_floor)
    self.fog = RenderFog(self.m, radius=radius_floor)
  
    #Place planets
    for (x, y), tile in cfg.items():
      
      for (planet_x, planet_y), planet_type in tile.items():
        self.m.units[(x+planet_x, y+planet_y)] = Planet(self.m, planet_type)
  
    #fog out hexes not on board
      for cell in self.m.spread( (x+3, y+2), radius=2):
        self.m.fog[cell] = self.fog.VISIBLE
  
  def _get_width(self):
    return self.grid.width

  def _get_height(self):
    return self.grid.height

  def _get_size(self):
    return (self.grid.width, self.grid.height)

  def get_cell(self, coords):
    return self.grid.get_cell(coords)

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

  def add_building(self, x, y, player_color, building_type, 
                   lantid_share=False):

    #check if the specified hex is a planet
    if self.m.units[(x,y)] is None and building_type != "lost planet":
      raise ValueError("Cannot add building to non-planet")

    #allow colonization of lost planet on random hex
    if building_type == 'lost planet':
      planet_type = 'lost planet'
    else:
      planet_type = self.m.units[(x,y)].planet_type

    #check for some illegal configurations of buildings
    if planet_type == 'transdim' and building_type != 'gaiaformer':
      raise ValueError("Can only add gaiaformer to transdim planet." 
                       " Planet at ({0},{1}) was {2}".format(
                       x, y, planet_type))
    elif planet_type != 'transdim' and building_type == 'gaiaformer':
      raise ValueError("Transdim planet can only allow gaiaformer")
    elif building_type == "gaiaformer" and lantid_share:
      raise ValueError("Lantids cannot share gaiaformer")


    self.m.units[(x,y)] = Building(self.m, planet_type, player_color, 
                                   building_type, lantid_share)
    
  def add_orbital(self, x, y, satellites, space_station=False):
    #check if specified hex is a planet
    if self.m.units[(x,y)] is not None:
      raise ValueError("Cannot add orbitals to planet hex")

    if len(satellites) == 0 and not space_station:
      raise ValueError("No orbitals specified")

    if len(satellites) > 4:
      raise NotImplementedError("No games above 4 players")
    if space_station and len(satellites) > 3:
      raise NotImplementedError("No games above 4 players")
    if space_station and 'red' in satellites:
      raise ValueError("Red player cannot have space station and satellite")

    self.m.units[(x,y)] = Orbital(self.m, satellites, space_station)

  def process_event(self, pos):
    if self.get_cell(pos) is None:
      return None

    x, y = self.get_cell(pos)

    if not self.is_valid_hex(x, y):
      return None

    return EventDescription(coordinates=(x, y))
      

  def highlight_hex(self, pos):
    x, y = pos
    if not self.is_valid_hex(x, y):
      return
    #self.m.units[pos].highlight = True
    self.m.fog[pos] = self.fog.HIGHLIGHTED
    self.highlighted_hexes.append(pos)

  def unhighlight_hex(self, pos):
    x, y = pos
    if not self.is_valid_hex(x, y):
      return
    self.m.fog[pos] = self.fog.VISIBLE
    #self.m.units[(x,y)].highlight = False

  def unhighlight_all(self):
    for pos in self.highlighted_hexes:
      #self.m.units[pos].highlight = False
      self.m.fog[pos] == self.fog.VISIBLE
      
    self.highlighted_hexes = []

  def is_valid_hex(self, x, y):
    return self.m.fog[(x,y)] in (self.fog.VISIBLE, self.fog.HIGHLIGHTED)

# TODO maybe someday the buildings will be pictures of game components
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
