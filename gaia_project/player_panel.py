import pygame

from traits.api import (HasPrivateTraits, Instance, Int, Dict, List, Enum, Str)
from .player import Player
from .constants import TECH_BOARD_COLOR_MAP, COMPONENT_COLOR_MAP
from .tile import BonusTile, RoundScoringTile, FinalScoringTile, FederationTile
from .effect import FreeAction

import numpy as np

from .move_action import Interaction, MoveAction
from .utils import text, GaiaProjectUIError

class PlayerPanelRender(pygame.Surface):

  def __init__(self, width, height, player, other_players, bonus_tiles, 
               round_scoring, 
               final_scoring, available_federations,
               *args, **kwargs):
    super().__init__((width, height), *args, **kwargs)
    self.width = width
    self.height = height

    self.player = player

    self.other_players = other_players

    self.bonus_tiles = bonus_tiles
    self.round_scoring = round_scoring
    self.final_scoring = final_scoring
    self.available_federations = available_federations


  def update_state(self, bonus_tiles, round_scoring, available_federations,
                         choice_type, choice_instructions, choice_repr): 
    self.bonus_tiles = bonus_tiles
    self.round_scoring = round_scoring
    self.available_federations = available_federations

    self.choice_type = choice_type
    self.choice_instructions = choice_instructions
    self.choice_repr = choice_repr

  def draw(self):
    gx = np.around(np.linspace(0, self.width, 30, endpoint=False)).astype(int)
    ex = self.width // 30
    ey = self.height

    bg_color = TECH_BOARD_COLOR_MAP['gray']
    button_color = TECH_BOARD_COLOR_MAP['button']
    line_color = pygame.Color('black')

    #information window 3/30 units
    pygame.draw.rect(self, button_color, (0, 0, ex*3, ey))
    pygame.draw.rect(self, line_color, (0, 0, ex*3, ey), 1)

    msg = "PLAYER\n{0}\n{1}".format(self.player.faction, self.player.username)

    msg += "\n\nOTHER PLAYERS"
    for player in self.other_players:
      msg += "\n{0}\n{1}\n".format(player.faction, player.username)


    text(self, msg, 0, 0, ex*3, ey)

    #income window 3/30 units
    pygame.draw.rect(self, bg_color, (gx[3], 0, ex*3, ey))
    pygame.draw.rect(self, line_color, (gx[3], 0, ex*3, ey), 1)

    msg = ("INCOME\ncoins: {0}\nore: {1}\nknowledge: {2}\nqubits: {3}\n"
           "charge power: {4}\nnew power tokens: {5}\n\n"
           "RESOURCES\ncoins: {6}\nore: {7}\nknowledge {8}\n"
           "qubits: {9}\n\n"
           "POWER\ngaia area: {10}\nbowl 1: {11}\nbowl 2: {12}\n"
           "bowl 3: {13}"
           .format(self.player.income['coin'],
                   self.player.income['ore'], 
                   self.player.income['knowledge'],
                   self.player.income['qubit'],
                   self.player.income['charge'],
                   self.player.income['power token'],
              
                   self.player.coin,
                   self.player.ore,
                   self.player.knowledge,
                   self.player.qubit,
                   self.player.power['gaia'],
                   self.player.power['1'],
                   self.player.power['2'],
                   self.player.power['3']))

    text(self, msg, gx[3], 0, ex*3, ey)

    #buildings window 3/30 units
    pygame.draw.rect(self, bg_color, (gx[6], 0, ex*3, ey))
    pygame.draw.rect(self, line_color, (gx[6], 0, ex*3, ey), 1)

    msg = ("BUILDINGS LEFT\nmines: {0}\ntrading posts: {1}\n"
           "research labs: {2}\nplanetary institute: {3}\n"
           "knowledge academy: {4}\naction academy: {5}\ngaiaformers: {6}"
           .format(self.player.buildings['mine'],
                   self.player.buildings['trading post'],
                   self.player.buildings['research lab'],
                   self.player.buildings['planetary institute'],
                   self.player.buildings['knowledge academy'],
                   self.player.buildings['action academy'],
                   self.player.buildings['gaiaformer']))

    msg += "\n\nFEDS AVAILABLE"
    for federation, n_left in self.available_federations.items():
      msg += "\n{0}: {1}".format(federation.desc, n_left)

    text(self, msg, gx[6], 0, ex*3, ey)

    #tiles window 6/30 units
    pygame.draw.rect(self, bg_color, (gx[9], 0, ex*6, ey))
    pygame.draw.rect(self, line_color, (gx[9], 0, ex*6, ey), 1)
  
    msg = "BONUS TILES"
    for tile, cur_owner in self.bonus_tiles.items():
      msg += "\n{0}: {1}: {2}".format(tile.tile_id, tile.desc, cur_owner) 

    msg += "\n\nTILES OWNED"
    for tile in self.player.tiles:
      msg += "\n{0}: {1}".format(tile.tile_id, tile.desc)

    text(self, msg, gx[9], 0, ex*7, ey)
  
    #scoring window 3/30 units
    pygame.draw.rect(self, bg_color, (gx[15], 0, ex*4, ey))
    pygame.draw.rect(self, line_color, (gx[15], 0, ex*4, ey), 1)

    msg = ("ROUND SCORING\nround 1: {0}\nround 2: {1}\nround 3: {2}\n"
           "round 4: {3}\nround 5: {4}\nround 6: {5}\n\n"
           "FINAL SCORING\n{6}\n{7}\n\n"
           "STATS\nplanet types: {8}\nsectors: {9}\n"
           "federation buildings: {10}"
           .format(self.round_scoring[0].desc,
                   self.round_scoring[1].desc,
                   self.round_scoring[2].desc,
                   self.round_scoring[3].desc,
                   self.round_scoring[4].desc,
                   self.round_scoring[5].desc,

                   self.final_scoring[0].desc,
                   self.final_scoring[1].desc,

                   self.player.planet_types,
                   self.player.sectors,
                   self.player.federation_buildings))

    text(self, msg, gx[15], 0, ex*4, ey)

    #actions window 4/30 units
    pygame.draw.rect(self, bg_color, (gx[19], 0, ex*3, ey))
    pygame.draw.rect(self, line_color, (gx[19], 0, ex*3, ey), 1)

    text(self, 'MOVE ACTIONS', gx[19], 0, ex*3, ey)

    gy = np.around(np.linspace(0, self.height, 18, endpoint=False)).astype(int)
    eky = ey // 51
    for j in range(8):
      at = gy[j*2 + 2] - eky
      ab = gy[j*2 + 3] + eky
      pygame.draw.rect(self, button_color, (gx[19]+ex//4, at, ex*5//2, ab-at))

      text(self, MoveAction('ACT{0}'.format(j+1)).desc, 
           gx[19]+ex//4, at + eky, ex*5//2, ab-at-eky)

    #free actions window 2/30 units clarifications window 6/30 units
    pygame.draw.rect(self, bg_color, (gx[22], 0, ex*2, ey))
    pygame.draw.rect(self, line_color, (gx[22], 0, ex*2, ey), 1)

    text(self, 'FREE ACTIONS', gx[22], 0, ex*2, ey)

    gy = np.around(np.linspace(0, self.height, 20, endpoint=False)).astype(int)

    for j in range(9):
      at = gy[j*2 + 2] - eky
      ab = gy[j*2 + 3] + eky
      pygame.draw.rect(self, button_color, (gx[22]+ex//4, at, ex*3//2, ab-at))

      text(self, FreeAction('FA{0}'.format(j+1)).desc,
           gx[22]+ex//4, at + eky, ex*5//2, ab-at-eky)

    #clarifications window 6/30 units
    pygame.draw.rect(self, bg_color, (gx[24], 0, ex*6, ey))
    pygame.draw.rect(self, line_color, (gx[24], 0, ex*6, ey))

    
    
    

  def blit(self, window, origin):
    window.blit(self, origin)

  def paint(self, window, origin):
    self.draw()
    self.blit(window, origin)

class PlayerPanel(HasPrivateTraits):
  
  render = Instance(PlayerPanelRender)

  player = Instance(Player)

  other_players = List(Instance(Player))

  width = Int
  height = Int

  bonus_tiles = Dict(Instance(BonusTile), Instance(Player))
  round_scoring = List(RoundScoringTile)
  final_scoring = List(FinalScoringTile)

  available_federations = Dict(Instance(FederationTile), Int)


  choice_type = Enum('building_upgrade', 'special_action', 'bonus_tile',
                     'federation_choice', 'which_power_tokens',
                     'tech_replace',
                     'coordinate', 'tech_tile', 'tech_track', 'power_action',
                     'charge_passive')
  
  choice_instructions = Str
  choice_repr = Str
  choice_options = List(Str)

  def __init__(self, width, height, player, other_players=None, 
               bonus_tiles=None, 
               round_scoring=None, final_scoring=None, 
               available_federations=None,
               *args, **kwargs):
    super().__init__(*args, **kwargs)

    self.width = width 
    self.height = height

    self.player = player

    if other_players is not None:
      self.other_players = other_players
    else:
      self.other_players = [Player('Xenos', 'Jebediah'),
                            Player('Taklons', 'Vivian')]

    if bonus_tiles is not None:
      self.bonus_tiles = bonus_tiles
    else:
      self.bonus_tiles = dict(zip([BonusTile('BON{0}'.format(i)) for 
                                            i in range(1, 7)],
                                  [None]*6))

    if round_scoring is not None:
      self.round_scoring = round_scoring
    else:
      self.round_scoring = [RoundScoringTile('RS{0}'.format(i)) for
                                             i in range(1, 7)]

    if final_scoring is not None:
      self.final_scoring = final_scoring
    else:
      self.final_scoring = [FinalScoringTile('FS1'),
                            FinalScoringTile('FS2')]

    if available_federations is not None:
      self.available_federations = available_federations
    else:
      self.available_federations = dict(zip([FederationTile('FED{0}'.format(i))
                                                       for i in range(1, 7)],
                                            [2, 3, 3, 3, 3, 3]))

    self.render = PlayerPanelRender(width, height, player, self.other_players,
                                    self.bonus_tiles,
                                    self.round_scoring, self.final_scoring,
                                    self.available_federations)

  def _width_changed(self):
    if self.render is not None:
      self.render.width = self.width

  def _height_changed(self):
    if self.render is not None:
      self.render.height = self.height

  def paint(self, window, origin):
    self.render.paint(window, origin)

  def process_event(self, x, y):
    #TODO
    pass

  def display_choice(self, move):
    if move == 'PASSIVE_CHARGE':
      self.choice_type = 'wateva'
    
    
