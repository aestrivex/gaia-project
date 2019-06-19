from traits.api import (HasPrivateTraits, Instance, List, Dict, Any)

from .player import Player
from .board import GameBoard
from .tech_board import TechBoard
from .player_panel import PlayerPanel
from .layout import Layout

from .constants import BASIC_4P_SETUP

import pygame
import sys
import threading

class CommunicationLayer(HasPrivateTraits):
  pass
  
class LocalCommunicationLayer(CommunicationLayer):
  players = List(Instance(Player))

  board = Instance(GameBoard)
  tech_board = Instance(TechBoard)
  player_panels = Dict(Instance(Player), Instance(PlayerPanel))

  layout = Instance(Layout)

  def __init__(self, players=None, cfg=BASIC_4P_SETUP, *args, **kwargs):
    super().__init__(*args, **kwargs)

    if players is not None:
      self.players = players
    else:
      self.players = [Player('Hadsch Hallas', 'Freddy'),
                      Player('Xenos', 'Jebediah'),
                      Player('Taklons', 'Vivian')]

    self.layout = Layout(self.players, cfg)

    self.board = self.layout.board
    self.tech_board = self.layout.tech_board

    
    pp_w, pp_h = self.layout.player_panel_coords()
    self.player_panels = {
      player : ( 
         PlayerPanel(pp_w, pp_h, player) 
              if player is not self.players[0] else
              self.layout.player_panel) for player in self.players}


    pygame.init()

    pygame.event.set_allowed(None)
    pygame.event.set_allowed((pygame.QUIT, pygame.MOUSEBUTTONUP,
                              pygame.VIDEORESIZE))
    

  def make_move(self, player, game_state):
    # set the layout to have the current player panel showing

    if player.intelligence == 'human':

      self.layout.player_panel = self.player_panels[player]
      self.layout.player_panel.hide_choice()
      self.update_gfx()
  
      move = self.process_events() 

      return move

    elif player.intelligence == 'automa':
      move = player.automa.make_move(player, game_state)

    elif player.intelligence == 'ai':
      raise NotImplementedError

    else:
      raise NotImplemented

  def make_choice(self, player, choice, move):
    self.layout.player_panel = self.player_panels[player]
    self.layout.player_panel.show_choice(choice, move.description)
    self.update_gfx()

    choice = self.process_events()
    print('gottud chois')
    return choice

  def inform_illegal_choice(self, player, explanation):
    self.layout.player_panel = self.player_panels[player]
    self.layout.player_panel.display_error(explanation)
    self.update_gfx()
    
    self.process_events()

  def process_events(self):
    while True:

      #we are now accepting mouse events
      pygame.event.set_allowed(pygame.MOUSEBUTTONUP)

      for event in pygame.event.get():
  
        #this event does not need to be executed in order
        if event.type == pygame.QUIT:
          pygame.quit()
          sys.exit()
    
        #this event does not need to be executed in order
        elif event.type == pygame.VIDEORESIZE:
          self.layout.resize(event.w, event.h)
    
        elif event.type == pygame.MOUSEBUTTONUP:
          #disallow mouse events until this is handled
          pygame.event.set_blocked(pygame.MOUSEBUTTONUP)
  
          origin_surf = self.layout.determine_origin(event.pos) 
    
          if origin_surf is None:
            continue
  
          event = self.layout.pass_event(origin_surf, event.pos)
  
          if event is not None:
            return event

  def add_building(self, player, coords, building_type, lantid_share=False):
    x, y = coords
    self.board.add_building(x, y, player.color, building_type, 
      lantid_share=lantid_share)

  def add_orbital(self, player, coords, orbital_type):
    x, y = coords
    self.board.add_orbital(x, y, player.color, orbital_type)

  def techup(self, player, tech_track):
    self.tech_board.techup(player.color, tech_track)

  def update_available_buildings(self, player):
    pass

  def update_bonus_tiles(self, tiles):
    for player in self.player_panels:
      panel = self.player_panels[player]
      panel.update_bonus_tiles(tiles)

  def update_turn_order(self, next_order):
    pass
    
  def update_advanced_tech_tiles(self, tiles):
    pass

  def update_terraforming_fed(self, fed):
    pass

  def update_available_feds(self, feds):
    pass

  def update_available_power_actions(self, power_actions):
    self.tech_board.update_power_actions(power_actions)

  def update_available_special_actions(self, player, spec_actions):
    panel = self.player_panels[player]
    panel.update_special_actions( spec_actions[player] )

  def update_misc_info(self, score):
    pass

  def update_gfx(self):
    self.layout.paint()
    
