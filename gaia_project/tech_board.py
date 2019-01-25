import pygame
import pygame.freetype
from traits.api import (HasPrivateTraits, List, Bool, Property, Dict, Instance,
                        Int)
from .tile import TechTile, AdvancedTechTile, FederationTile
from .constants import (TECH_BOARD_COLOR_MAP, COMPONENT_COLOR_MAP, TECH_ORDER,
                        TECH_BOARD_DESCS, TECH_BOARD_LONG_DESCS,
                        TECH_LEVEL_TO_IDX)
from .utils import GaiaProjectUIError
import numpy as np

class TechBoardRender(pygame.Surface):

  def __init__(self, width, height, advanced_tech_tiles, tech_tiles,
               player_techs, terraforming_federation, font_size=14, 
               *args, **kwargs):
    super().__init__((width, height), *args, **kwargs)

    self.width = width
    self.height = height 

    self.advanced_tech_tiles = advanced_tech_tiles
    self.tech_tiles = tech_tiles
    self.player_techs = player_techs

    self.terraforming_federation = terraforming_federation

    self.power_actions_taken = [False]*10

    self.font_size=font_size

    pygame.font.init()

  def update_state(self, advanced_tech_tiles, player_techs, power_actions,
                   federation_taken):
    self.advanced_tech_tiles = advanced_tech_tiles
    self.player_techs = player_techs
    self.power_actions_taken = power_actions

    if federation_taken:
      self.terraforming_federation = None
    
  def draw(self):
    #draw the grid
    gx = np.around(np.linspace(0, self.width, 6, endpoint=False)).astype(int)
    gy = np.around(np.linspace(0, self.height, 9, endpoint=False)).astype(int)

    ex = self.width//6
    ey = self.height//9

    for i, x in enumerate(gx):
      for j, y in enumerate(gy):

        if j in (1,7,8):
          color = pygame.Color(130, 130, 130)
        else:
          color = TECH_BOARD_COLOR_MAP[TECH_ORDER[i]]

        pygame.draw.rect(self, color, (x, y, ex, ey))
        pygame.draw.rect(self, pygame.Color('black'), (x, y, ex, ey), 1)

        #draw cell information
        if i==0 and j==0: 
          #render which federation
          pass

        elif j==1:
          #render advanced techs

          try:
            self.text("{0}\n{1}".format(self.advanced_tech_tiles[i].tech_id,
                                        self.advanced_tech_tiles[i].long_desc),
                      x, y, ex, ey)
          except GaiaProjectUIError:
            #redraw gray rectangle
            pygame.draw.rect(self, color, (x, y, ex, ey))
            pygame.draw.rect(self, pygame.Color('black'), (x, y, ex, ey), 1)
      
            #draw smaller text
            self.text("{0}".format(self.advanced_tech_tiles[i].desc),
                      x, y, ex, ey)

        elif j==7:
          try:
            self.text("{0}\n{1}".format(self.tech_tiles[i].tech_id,
                                        self.tech_tiles[i].long_desc),
                      x, y, ex, ey)
          except GaiaProjectUIError:
            #redraw gray rectangle
            pygame.draw.rect(self, color, (x, y, ex, ey))
            pygame.draw.rect(self, pygame.Color('black'), (x, y, ex, ey), 1)

            #draw smaller text
            self.text("{0}".format(self.tech_tiles[i].desc), x, y, ex, ey)

        elif j==8:
          #render regular techs
          if i in (1, 3, 5):
            continue       
          tech_idx = i//2+6

          try:
            self.text("{0}\n{1}".format(self.tech_tiles[tech_idx].tech_id,
                                        self.tech_tiles[tech_idx].long_desc),
                      x, y, ex, ey)
          except GaiaProjectUIError:
            #redraw gray rectangle
            pygame.draw.rect(self, color, (x, y, ex, ey))
            pygame.draw.rect(self, pygame.Color('black'), (x, y, ex, ey), 1)

            #draw smaller text
            self.text("{0}".format(self.tech_tiles[tech_idx].desc), 
                      x, y, ex, ey)
    
        else:
        #render text for every level
          try:
            self.text(TECH_BOARD_DESCS[(i,j)], x, y, ex, ey)
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
      


  def text(self, msg, x_pos, y_pos, box_size_x, box_size_y):
    lines = msg.split('\n') 
    f = pygame.freetype.SysFont(pygame.freetype.get_default_font(),
                                self.font_size)

    line_spacing = f.get_sized_height() + 2
    x, y = 2, 2

    space_w = f.get_rect(' ').width
    for i,line in enumerate(lines):
      words = line.split(' ')

      for word in words:

        bounds = f.get_rect(word)
        if x + bounds.width + bounds.x >= box_size_x:
          x, y = 2, y+line_spacing
        if y + bounds.height - bounds.y >= box_size_y:
          errmsg = 'Tile "{0}" too big to show on board size {1}x{2}'.format(
                      msg, self.width, self.height)
          print(errmsg)
          raise GaiaProjectUIError(errmsg)    
  
        f.render_to(self, (x_pos+x, y_pos+y), 
                    None, pygame.Color('black')) 
        x += bounds.width + space_w

      x = 2
      y += line_spacing

  def blit(self, window, origin):
    window.blit(self, origin)

  def paint(self, window, origin):
    self.draw()
    self.blit(window, origin)


class TechBoard( HasPrivateTraits ):

  render = Instance(TechBoardRender)

  tech_tiles=List(TechTile)
  advanced_tech_tiles=List(AdvancedTechTile)

  power_actions_taken = List(Bool)

  terraforming_federation = Instance(FederationTile)

  player_techs = Dict

  width = Int
  height = Int

  def _power_actions_taken_default(self):
    return [False]*10

  def __init__(self, width, height, players, 
               tech_tiles=None, advanced_tech_tiles=None,
               *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.width = width
    self.height = height

    #set some default values if they are not specified
    if players is not None:
      #figure out the true player tech levels
      pass
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

    self.render = TechBoardRender(width, height,
                                  self.advanced_tech_tiles,
                                  self.tech_tiles,
                                  self.player_techs,
                                  self.terraforming_federation
                                 )

  def paint(self, window, origin):
    self.render.paint(window, origin)

    
    




if __name__ == '__main__':
  b = TechBoard([], [])
  print(b.traits())
  print(b.power_actions_taken)
  print(b.power_actions_taken[4])
