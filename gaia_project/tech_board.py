import pygame
import pygame.freetype
from traits.api import (HasPrivateTraits, List, Bool, Property, Dict, Instance,
                        Int, Tuple, Range, Str)
from .tile import TechTile, AdvancedTechTile, FederationTile
from .move_action import EventDescription
from .constants import (TECH_BOARD_COLOR_MAP, COMPONENT_COLOR_MAP, TECH_ORDER,
                        TECH_BOARD_DESCS, TECH_BOARD_LONG_DESCS,
                        TECH_LEVEL_TO_IDX, POWER_ACTIONS, STARTING_TECHS)
from .utils import GaiaProjectUIError, text
import numpy as np

class TechBoardRender(pygame.Surface):

  def __init__(self, width, height, advanced_tech_tiles, tech_tiles,
               player_techs, terraforming_federation, power_actions, 
               font_size=14, 
               *args, **kwargs):
    super().__init__((width, height), *args, **kwargs)

    self.width = width
    self.height = height 

    self.advanced_tech_tiles = advanced_tech_tiles
    self.tech_tiles = tech_tiles
    self.player_techs = player_techs

    self.terraforming_federation = terraforming_federation

    self.power_actions = power_actions

    self.font_size=font_size

    pygame.font.init()

  def update_state(self, advanced_tech_tiles, player_techs, 
                   terraforming_federation=None):
    self.advanced_tech_tiles = advanced_tech_tiles
    self.player_techs = player_techs
    self.terraforming_federation = terraforiming_federation
    #TODO add available power actions

  def draw(self):
    #draw the grid
    gx = np.around(np.linspace(0, self.width, 6, endpoint=False)).astype(int)
    gy = np.around(np.linspace(0, self.height, 10, endpoint=False)).astype(int)

    ex = self.width//6
    ey = self.height//10


    for i, x in enumerate(gx):
      for j, y in enumerate(gy):

        if y == gy[-1:]:
          #handle power actions later
          continue

        if j in (1,7,8):
          color = TECH_BOARD_COLOR_MAP['gray']
        else:
          color = TECH_BOARD_COLOR_MAP[TECH_ORDER[i]]

        #draw rectangular grid
        pygame.draw.rect(self, color, (x, y, ex, ey))
        pygame.draw.rect(self, pygame.Color('black'), (x, y, ex, ey), 1)

        #draw cell information
        if i==0 and j==0: 
          #render which federation
          text(self, self.terraforming_federation.desc, x, y, ex, ey)
            

        elif j==1:
          #render advanced techs

          try:
            text(self, "{0}\n{1}".format(self.advanced_tech_tiles[i].tile_id,
                                        self.advanced_tech_tiles[i].long_desc),
                      x, y, ex, ey)
          except GaiaProjectUIError:
            #redraw gray rectangle
            pygame.draw.rect(self, color, (x, y, ex, ey))
            pygame.draw.rect(self, pygame.Color('black'), (x, y, ex, ey), 1)
      
            #draw smaller text
            text(self, "{0}".format(self.advanced_tech_tiles[i].desc),
                      x, y, ex, ey)

        elif j==7:
          #render regular techs
          try:
            text(self, "{0}\n{1}".format(self.tech_tiles[i].tile_id,
                                        self.tech_tiles[i].long_desc),
                      x, y, ex, ey)
          except GaiaProjectUIError:
            #redraw gray rectangle
            pygame.draw.rect(self, color, (x, y, ex, ey))
            pygame.draw.rect(self, pygame.Color('black'), (x, y, ex, ey), 1)

            #draw smaller text
            text(self, "{0}".format(self.tech_tiles[i].desc), x, y, ex, ey)

        elif j==8:
          #render regular techs
          if i in (1, 3, 5):
            continue       
          tile_idx = i//2+6

          try:
            text(self, "{0}\n{1}".format(self.tech_tiles[tile_idx].tile_id,
                                        self.tech_tiles[tile_idx].long_desc),
                      x, y, ex, ey)
          except GaiaProjectUIError:
            #redraw gray rectangle
            pygame.draw.rect(self, color, (x, y, ex, ey))
            pygame.draw.rect(self, pygame.Color('black'), (x, y, ex, ey), 1)

            #draw smaller text
            text(self, "{0}".format(self.tech_tiles[tile_idx].desc), 
                 x, y, ex, ey)
    
        else:
        #render text for every level
          try:
            text(self, TECH_BOARD_DESCS[(i,j)], x, y, ex, ey)
          except GaiaProjectUIError:
            #if we failed to render text that is the same every game, give up
            #and continue
            pygame.draw.rect(self, color, (x, y, ex, ey))
            pygame.draw.rect(self, pygame.Color('black'), (x, y, ex, ey), 1)
    

    #render each player marker
    for i, tech_tree in enumerate(self.player_techs.values()):
      for x_off, (player, level) in enumerate(tech_tree.items()):

        j = TECH_LEVEL_TO_IDX[level]
        pygame.draw.circle(self, pygame.Color('black'),
                           (ex*(x_off+1)//5 + gx[i], ey*2//3 + gy[j]),
                           self.font_size//2 + 2)

        pygame.draw.circle(self, COMPONENT_COLOR_MAP[player], 
                           (ex*(x_off+1)//5 + gx[i], ey*2//3 + gy[j]),
                           self.font_size//2)
      
    #render power actions
    gx_p = np.around(np.linspace(0, self.width, 10, endpoint=False)
                     ).astype(int)
    ex_p = self.width//10

    octy = tuple(gy[-1:] + int(ey*y_mult) for y_mult in np.linspace(.2, .7, 4))

    for i, x in enumerate(gx_p):
      #draw gray squares and black grid outlines
      pygame.draw.rect(self, TECH_BOARD_COLOR_MAP['gray'], (x, y, ex_p, ey))
      pygame.draw.rect(self, pygame.Color('black'), (x, y, ex_p, ey), 1)

      #draw power action octagons
      octx = tuple(x + int(ex_p*x_mult) for x_mult in np.linspace(.1, .9, 4))

      oct_points = ((octx[1], octy[0]), (octx[2], octy[0]), (octx[3], octy[1]),
                    (octx[3], octy[2]), (octx[2], octy[3]), (octx[1], octy[3]),
                    (octx[0], octy[2]), (octx[0], octy[1]))
  
      if i<7:
        pa_color = TECH_BOARD_COLOR_MAP['power action']
      else:
        pa_color = TECH_BOARD_COLOR_MAP['qubit action']

      pygame.draw.polygon(self, pa_color, oct_points)
      
      #determine whether the action has been used or not
      if self.power_actions[i].available:
        #render the correct text

        try:
          text(self, self.power_actions[i].desc, octx[0], octy[1],
                    octx[3]-octx[0], octy[2]-octy[1])
        except GaiaProjectUIError:
          pass

      else:
        #draw a red X over the action

        pygame.draw.polygon(self, TECH_BOARD_COLOR_MAP['action used'],
                            ((octx[3], octy[1]), (octx[1], octy[3]),
                             (octx[0], octy[2]), (octx[2], octy[0])))

        pygame.draw.polygon(self, TECH_BOARD_COLOR_MAP['action used'],
                            ((octx[0], octy[1]), (octx[2], octy[3]),
                             (octx[3], octy[2]), (octx[1], octy[0])))

      #draw the actions cost
      text(self, str(self.power_actions[i]._cost_amount), 
                  octx[0], gy[-1:]+(octy[0]-gy[-1:])//3,
                  octx[1]-octx[0], octy[1]-octy[0], color=pa_color)
                  

      #draw the action outline again
      pygame.draw.polygon(self, pygame.Color('black'), oct_points, 1)
        
        
  def blit(self, window, origin):
    window.blit(self, origin)

  def paint(self, window, origin):
    self.draw()
    self.blit(window, origin)


class TechBoard( HasPrivateTraits ):

  render = Instance(TechBoardRender)

  tech_tiles=List(TechTile)
  advanced_tech_tiles=List(AdvancedTechTile)

  power_actions = Tuple

  terraforming_federation = Instance(FederationTile)

  player_techs = Dict(Str, Dict(Str, Int)) #track -> (color -> int)

  width = Range(high=750)
  height = Int

  def __init__(self, width, height, players, 
               tech_tiles=None, advanced_tech_tiles=None,
               terraforming_federation=None,
               power_actions=POWER_ACTIONS,
               *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.width = width
    self.height = height

    self.power_actions = power_actions

    #set some default values if they are not specified
    if players is not None:
      #figure out the true player tech levels
      self.player_techs = dict(zip(TECH_ORDER,
                                   [dict(zip([p.color for p in players],
                                             [0]*len(players)))]*6))
      for player in players:
        if player.faction in STARTING_TECHS:
          self.player_techs[STARTING_TECHS[player.faction]][player.color] = 1

    else:
      zero_dummy_techs = {'red' : 0, 'yellow' : 0}
      self.player_techs = {'terraforming' : zero_dummy_techs,
                           'navigation' : zero_dummy_techs.copy(),
                           'AI' : zero_dummy_techs.copy(),
                           'gaiaforming' : zero_dummy_techs.copy(),
                           'economy' : zero_dummy_techs.copy(),
                           'science' : zero_dummy_techs.copy()}

    if tech_tiles is not None:
      self.tech_tiles = tech_tiles
    else:
      self.tech_tiles = [TechTile('TECH{0}'.format(i)) for i in range(1,10)]

    if advanced_tech_tiles is not None:
      self.advanced_tech_tiles = advanced_tech_tiles
    else:
      self.advanced_tech_tiles = [AdvancedTechTile('ADV{0}'.format(i))
                                  for i in range(1,7)]

    if terraforming_federation is not None:
      self.terraforming_federation = terraforming_federation
    else:
      self.terraforming_federation = FederationTile('FED1')

    self.render = TechBoardRender(width, height,
                                  self.advanced_tech_tiles,
                                  self.tech_tiles,
                                  self.player_techs,
                                  self.terraforming_federation,
                                  self.power_actions
                                 )

  def _width_changed(self):
    if self.render is not None:
      self.render.width = self.width
  
  def _height_changed(self):
    if self.render is not None:
      self.render.height = self.height

  def paint(self, window, origin):
    self.render.paint(window, origin)

  def process_event(self, x, y):
    ex = self.width//6
    ey = self.height//10

    x_box = x // ex
    y_box = y // ey

    if y_box == 1:
      return EventDescription(
        tech_tile_choice = self.advanced_tech_tiles[x_box])

    if y_box == 7:
      return EventDescription(tech_tile_choice = self.tech_tiles[x_box])

    elif y_box == 8:
      if x_box in (1,3,5):
        return
      else:
        return EventDescription(
          tech_tile_choice = self.tech_tiles[6 + x_box // 2])

    elif y_box == 9:
      ex_p = self.width//10
      return EventDescription(power_action = POWER_ACTIONS[x // ex_p])

    else:
      return EventDescription(tech_track = TECH_ORDER[x_box])

  def techup(color, tech_track): 
    self.player_techs[tech_track][color] += 1
    self.render.player_techs = self.player_techs

  def update_power_actions(available_power_actions):
    for action in self.power_actions:
      action.available = available_power_actions[action]
    self.render.power_actions = self.power_actions

if __name__ == '__main__':
  b = TechBoard([], [])
  print(b.traits())
  print(b.power_actions)
  print(b.power_actions[4])
