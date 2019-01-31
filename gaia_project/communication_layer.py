from traits.api import (HasPrivateTraits, Instance, List, Dict)

from .player import Player
from .board import GameBoard
from .tech_board import TechBoard
from .player_panel import PlayerPanel
from .layout import Layout

from .constants import BASIC_4P_SETUP

import pygame
import sys

class CommunicationLayer(HasPrivateTraits):
  pass
  
class LocalCommunicationLayer(CommunicationLayer):
  players = List(Instance(Player))

  board = Instance(GameBoard)
  tech_board = Instance(TechBoard)
  player_panels = Dict(Instance(Player), Instance(PlayerPanel))

  layout = Instance(Layout)

  window = Instance(pygame.Surface)
  clock = Instance(pygame.time.Clock)

  def __init__(self, players=None, cfg=BASIC_4P_SETUP):
    super().__init__()

    if players is not None:
      self.players = players
    else:
      self.players = [Player('Hadsch Hallas', 'Freddy'),
                      Player('Xenos', 'Jebediah'),
                      Player('Taklons', 'Vivian')]

    self.layout = Layout(n_tiles=len(cfg))
    self.layout.board = self.board = GameBoard(cfg=cfg)

    tb_w, tb_h = self.layout.tech_board_coords()
    self.layout.tech_board = TechBoard(tb_w, tb_h, None)

    pp_w, pp_h = self.layout.player_panel_coords()
    
    self.player_panels = [{player : PlayerPanel(pp_w, pp_h, player)}
                           for player in self.players]

    pygame.init()
    self.clock = pygame.time.Clock()
    window = pygame.display.set_mode( (self.layout_w, self.layout_h),
                                      pygame.RESIZABLE)
    

  def make_move(self, player):
    # set the layout to have the current player panel showing
    self.layout.player_panel = self.player_panels[player]
    self.layout.paint()

    move = self.process_events() 
    

  def process_events(self):
    if event.type == pygame.QUIT:
      pygame.quit()
      sys.exit()

    elif event.type == pygame.VIDEORESIZE:
      self.layout.resize(event.w, event.h)

    elif event.type == pygame.MOUSEBUTTONDOWN:
      origin_surf = self.layout.determine_origin(event.pos) 

      if origin_surf is not None:
        self.layout.pass_event(origin_surf, pos)
