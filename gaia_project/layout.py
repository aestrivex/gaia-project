
from traits.api import (HasPrivateTraits, Int, Instance, Property, Enum, Any)

from .board import GameBoard
from .tech_board import TechBoard
from .player_panel import PlayerPanel

import pygame
import numpy as np

class Layout(HasPrivateTraits):
  radius = Int(42)

  fps = Int(10)

  board = Instance(GameBoard)
  tech_board = Instance(TechBoard)
  player_panel = Instance(PlayerPanel)

  window = Instance(pygame.Surface)
  clock = Any

  window_w = Int(1600)
  window_h = Int(1200)

  n_tiles = Enum(7, 8, 9, 10)

  board_h = Property
  board_w = Property

  def __init__(self, players, cfg, radius=None, *args, **kwargs):
    super().__init__(*args, **kwargs)

    first_player = players[0]

    self.n_tiles = len(cfg)

    if radius is None:
      if len(cfg) == 10:
        self.radius = 35
      elif len(cfg) == 7:
        self.radius = 42
      else:
        raise NotImplementedError("need configuration test for 8/9 tile")
    
    self.board = GameBoard(cfg=cfg, radius=self.radius)

    tb_w, tb_h = self.tech_board_coords()
    self.tech_board = TechBoard(tb_w, tb_h, players)

    pp_w, pp_h = self.player_panel_coords()
    self.player_panel = PlayerPanel(pp_w, pp_h, first_player)

    self.window = pygame.display.set_mode( (self.window_w, 
                                            self.window_h),
                       #                    pygame.RESIZABLE)
                                            )

    self.clock = pygame.time.Clock()


  def _get_board_h(self):
    if self.n_tiles == 7:
      #n_cell = 17
      n_cell = 14
    elif self.n_tiles == 10:
      #n_cell = 20
      n_cell = 14
    else:
      raise NotImplementedError
  
    return int(n_cell * self.board.radius * np.sqrt(3) + 1)

  def _get_board_w(self):
    if self.n_tiles == 7:
      n_cell = 15
    elif self.n_tiles == 10:
      n_cell = 20
    else:
      raise NotImplementedError

    return int(n_cell * self.board.radius * 1.5 + self.board.radius / 2)

  tech_board_x = Property
  def _get_tech_board_x(self):
    return self.board_w + 1

  player_panel_y = Property
  def _get_player_panel_y(self):
    return self.board_h + 1


  def tech_board_coords(self):
    return (self.window_w - self.board_w, self.board_h)

  def player_panel_coords(self):
    return (self.window_w, self.window_h - self.board_h)
  
  def paint(self):
    self.window.fill( pygame.Color('black') )
    self.board.paint(self. window, (0,0))
    self.tech_board.paint(self.window, (self.tech_board_x, 0))
    self.player_panel.paint(self.window, (0, self.player_panel_y))
    pygame.display.update()
    
    self.clock.tick(self.fps)

  def resize(self, w, h):
    self.window_w = w
    self.window_h = h
    
    try:
      self.tech_board.width = w - self.board_w
      self.tech_board.height = self.board_h
    except TraitError:
      self.tech_board.width = 750
      self.tech_board.height = self.board_h

    try:
      self.player_panel.width = w
      self.player_panel.height = h - self.board_h
    except TraitError:
      pass

    self.paint()

  def determine_origin(self, pos):
    x, y = pos
    if x < self.tech_board_x and y < self.player_panel_y:
      return self.board
    elif x >= self.tech_board_x and y < self.player_panel_y:
      return self.tech_board
    elif y >= self.player_panel_y:
      return self.player_panel
    else:
      return None

  def pass_event(self, origin_surf, pos):
    x, y = pos
    if origin_surf == self.board:
      return self.board.process_event(pos)
    elif origin_surf == self.tech_board:
      return self.tech_board.process_event(x - self.tech_board_x, y)
    elif origin_surf == self.player_panel:
      return self.player_panel.process_event(x, y - self.player_panel_y)
    
