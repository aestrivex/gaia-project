from traits.api import (HasPrivateTraits, Property, Enum, Int, Tuple, List,
                        Instance, Dict, Str, Bool)
from .tile import BonusTile, FederationTile, TechTile
from .effect import Effect, SpecialAction, PowerAction

class Interaction(HasPrivateTraits):
  action_id = Str

  desc = Property

  def __init__(self, action_id):
    super().__init__()
    self.action_id = action_id

class EventDescription(Interaction):

  #x,y coordinate used to identify map locations on actions 1, 2, 3
  #used in SPEC_IVIT, SPEC_FIRAK, SPEC_AMBA, SPEC_BON4, SPEC_BON5
  x = Int
  y = Int

  #used to identify upgrade path in ACT3
  upgrade = Enum('planetary institute', 'research lab',
                 'action academy', 'knowledge academy')
        
  #list of x,y map coordinates used to identify satellites in ACT4
  satellites = List(Tuple)

  #index of tech track to move up ACT5 or SPEC_BESCOD
  tech_track = Enum('terraforming', 'navigation', 'AI', 'gaiaforming',
                    'economy', 'science')

  #index of power action choice for ACT6
  power_action = Instance(PowerAction)

  #the special action chosen for ACT7
  special_action = Instance(SpecialAction)

  #the bonus tile selected for ACT8
  bonus_tile = Instance(BonusTile)

  #the federation token picked in ACT5 or ACT6:QA2
  federation_choice = Instance(FederationTile)

  #the technology tile picked in ACT3:RL, ACT3:AC, or ACT6:QA1
  tech_tile_choice = Instance(TechTile)

  #the technology tile to replace with an advanced tech tile pick
  #in ACT3:RL, ACT3:AC or ACT6:QA1
  tech_replace_choice = Instance(TechTile)

  #which power tokens to utilize in ACT2, ACT4, SPEC_BON5
  which_power_tokens_choice = Dict(Str, Int)
  
class MoveAction(EventDescription):
  action_id = Enum('ACT1', 'ACT2', 'ACT3', 'ACT4', 'ACT5', 'ACT6', 'ACT7', 
                   'ACT8')

  def _get_desc(self):
    if self.action_id == 'ACT1':
      return 'BUILD'
    elif self.action_id == 'ACT2':
      return 'GAIAFORM'
    elif self.action_id == 'ACT3':
      return 'UPGRADE'
    elif self.action_id == 'ACT4':
      return 'CONFEDERATE'
    elif self.action_id == 'ACT5':
      return 'ADVANCE TECH'
    elif self.action_id == 'ACT6':
      return 'POWER ACTION'
    elif self.action_id == 'ACT7':
      return 'SPECIAL ACTION'
    elif self.action_id == 'ACT8':
      return 'PASS'

class PassiveAction(Interaction):
  action_id = Enum('PASSIVE_CHARGE')

  height = Int
  vp = Int

  adjusted_charge = Int

  #used to denote the player choice
  charge_accepted = Bool

  def adjust_charge(self, cur_power):
    self.adjusted_charge = self.height

    potential = cur_power['1'] * 2 + cur_power['2']
    if potential < self.adjusted_charge:
      self.adjusted_charge = potential

    if self.vp + 1 < self.adjusted_charge:
      self.adjusted_charge = self.vp + 1
