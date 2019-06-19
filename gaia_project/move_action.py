from traits.api import (HasPrivateTraits, Property, Enum, Int, Tuple, List,
                        Instance, Dict, Str, Bool, Either)
from .tile import BonusTile, FederationTile, TechTile, AdvancedTechTile
from .effect import Effect


class Interaction(HasPrivateTraits):
  action_id = Either(Str, None)

  desc = Property
  def _get_desc(self):
    return ''

  def __eq__(self, other):
    if not type(self) == type(other):
      return False
    return self.action_id == other.action_id

  def __hash__(self):
    return hash(self.action_id)

  def __init__(self, action_id=None, *args, **kwargs):
    super().__init__(*args, **kwargs)

#  def validate(self, choice, description):
#    if self.choice == 'tech_tile':
#      assert self.action_id in ('ACT3', 'QA1', 'GAIA_ITAR'):
#
#      if description.upgrade is None:
#        raise GaiaProjectValidationError("Bad validation tech_tile")
#
#      if description.upgrade == 'planetary institute':
#        return False
#      else:
#        return True
#
#    elif self.choice == 'tech_replace':
#      assert self.action_id in ('ACT3', 'QA1', 'GAIA_ITAR'):
#
#      if description.tech_tile is None:
#        raise GaiaProjectValidationError("Bad validation tech_replace")
#
#      if type(description.tech_tile) == AdvancedTechTile:
#        return True
#      else:
#        return False
#
#    elif self.choice == 'tech_track':
#      assert self.action_id in ('ACT3', 'QA1', 'GAIA_ITAR', 'ACT5', 
#                                'SPEC_BESCOD', 'SPEC_FIRAK') 
#                                 
#
#      if self.action_id in ('ACT5', 'ACT7', 'SPEC_BESCOD', 'SPEC_FIRAK')
#        return True
#      elif self.action_id == 'GAIA_ITAR':
#        return not description.bonus_declined
#      else:
#        #if the choice is forced, the tech track will already be set
#        return description.tech_track is None
#
#    elif self.choice == 'coordinate':
#      assert self.action_id in ('ACT1', 'ACT2', 'ACT3', 'ACT4', 'ACT5', 
#                                'QA1', 'PA2', 'PA6', 'BON4', 'BON5', 
#                                'SPEC_BESCOD', 'SPEC_FIRAK', 'SPEC_IVIT',
#                                'SPEC_AMBA', 'GAIA_ITAR')
#
#      if self.action_id in ('ACT1', 'ACT2', 'ACT4', 'PA2', 'PA6', 'BON4',
#                            'BON5', 'SPEC_IVIT', 'SPEC_AMBA'):
#        return True
#
#      elif description.tech_track != 'navigation':
#        return True

class EventDescription(HasPrivateTraits):

  #x,y coordinate used to identify map locations on actions 1, 2, 3
  #used in SPEC_IVIT, SPEC_FIRAK, SPEC_AMBA, SPEC_BON4, SPEC_BON5
  coordinates = Either(None, Tuple)

  #used to identify placement of lost planet
  lost_planet_coords = Tuple

  #used to identify upgrade path in ACT3
  upgrade = Enum(None, 'planetary institute', 'research lab',
                 'action academy', 'knowledge academy')
        
  #list of x,y map coordinates used to identify satellites in ACT4
  feds_satellites = List(Tuple)

  #index of tech track to move up ACT5 or SPEC_BESCOD
  tech_track = Enum(None, 'terraforming', 'navigation', 'AI', 'gaiaforming',
                    'economy', 'science')

  #index of power action choice for ACT6
  power_action = Instance(Interaction)

  #the special action chosen for ACT7
  special_action = Instance(Interaction)

  #the bonus tile selected for ACT8
  bonus_tile = Instance(BonusTile)

  #the federation token picked in ACT5 or ACT6:QA2
  federation_choice = Instance(FederationTile)

  #the technology tile picked in ACT3:RL, ACT3:AC, or ACT6:QA1 or ITAR:SPEC
  tech_tile_choice = Instance(TechTile)

  #the technology tile to replace with an advanced tech tile pick
  #in ACT3:RL, ACT3:AC or ACT6:QA1 or ITAR:SPEC
  tech_replace_choice = Instance(TechTile)

  #which power tokens to utilize in ACT2, ACT4, SPEC_BON5
  which_power_tokens_choice = Dict(Str, Int)

  bonus_declined = Bool

  cancel_choice = Bool

class TakeableAction(Interaction):
  action_id = Str
  available = Bool(True)

  effect = Instance(Effect)
  choices = Property
  def _get_choices(self):
    return self.effect.choices

  description = Instance(EventDescription, ())

  desc = Property
  def _get_desc(self):
    return ValueError("Abstract class TakeableAction has no desc")

  long_desc = Property
  def _get_long_desc(self):
    return self.desc

  def __init__(self, action_id, *args, **kwargs):
    super().__init__(*args, **kwargs)
    self.action_id = action_id

  def __str__(self):
    return '{0}({1})'.format(self.__class__.__name__, self.action_id)

  def __repr__(self):
    return self.__str__()

  def merge_input(self, description):
    for attr in description.trait_names():
      if attr in ('trait_added', 'trait_modified'):
        continue
#      if attr == 'automa_vp':
#        setattr(self.description, attr, 
#          getattr(self.description, attr) + getattr(description, attr))
        
      if getattr(description, attr) not in ((), [], None, False, {}):
        setattr(self.description, attr, getattr(description, attr))

class PowerAction(TakeableAction):
  action_id = Enum('PA1', 'PA2', 'PA3', 'PA4', 'PA5', 'PA6', 'PA7',
                         'QA1', 'QA2', 'QA3')

  _cost_type = Property
  _cost_amount = Property

  def _get__cost_type(self):
    if self.action_id[0] == 'Q':
      return 'qubit'
    else:
      return 'power'
  
  def _get__cost_amount(self): 
    if self.action_id == 'PA1':
      return 7
    elif self.action_id == 'PA2':
      return 5
    elif self.action_id in ('PA3', 'PA4', 'PA5', 'QA1'):
      return 4
    elif self.action_id in ('PA6', 'PA7', 'QA2'):
      return 3
    elif self.action_id == 'QA3':
      return 2

  cost = Property
  def _get_cost(self):
    return {self._cost_type : self._cost_amount}

  def _get_desc(self):
    if self.action_id == 'PA1':
      return '+3K'
    elif self.action_id == 'PA2':
      return '+2dig'
    elif self.action_id == 'PA3':
      return '+2o'
    elif self.action_id == 'PA4':
      return '+7C'
    elif self.action_id == 'PA5':
      return '+2K'
    elif self.action_id == 'PA6':
      return '+1dig'
    elif self.action_id == 'PA7':
      return '+2pt'
    elif self.action_id == 'QA1':
      return '+tech'
    elif self.action_id == 'QA2':
      return 'fed'
    elif self.action_id == 'QA3':
      return 'VPs'

  def _effect_default(self):
    if self.action_id == 'PA1':
      return Effect(immediate={'knowledge' : 3})
    elif self.action_id == 'PA2':
      return Effect(immediate={'terraform' : 2},
                    choices=['coordinate'])
    elif self.action_id == 'PA3':
      return Effect(immediate={'ore' : 2})
    elif self.action_id == 'PA4':
      return Effect(immediate={'coin' : 7})
    elif self.action_id == 'PA5':
      return Effect(immediate={'knowledge' : 2})
    elif self.action_id == 'PA6':
      return Effect(immediate={'terraform' : 1},
                    choices=['coordinate'])
    elif self.action_id == 'PA7':
      return Effect(immediate={'power token' : 2})
    elif self.action_id == 'QA1':
      return Effect(immediate={'tech tile' : 1},
                    choices=['tech_tile', 'tech_replace', 'tech_track'])
    elif self.action_id == 'QA2':
      return Effect(immediate={'rescore_fed' : 1},
                    choices=['which_federation_owned'])
    elif self.action_id == 'QA3':
      return Effect(immediate={'VP' : 3,
                               'per' : {'planet type' : {'VP' : 1}}})


class FreeAction(TakeableAction):
  action_id = Enum('FA1', 'FA2', 'FA3', 'FA4', 'FA5', 'FA6', 'FA7', 'FA8',
                   'FA9')

  _cost_type = Property
  _cost_amount = Property

  def _get__cost_amount(self):
    if self.action_id == 'FA1':
      return 0
    elif self.action_id in ('FA2', 'FA5'):
      return 4
    elif self.action_id == 'FA3':
      return 3
    else:
      return 1

  def _get__cost_type(self):
    if self.action_id == 'FA4':
      return 'qubit'
    elif self.action_id == 'FA7':
      return 'knowledge'
    elif self.action_id in ('FA8', 'FA9'):
      return 'ore'
    else:
      return 'power'

  cost = Property
  def _get_cost(self):
    return {self._cost_type : self._cost_amount}

  def _get_desc(self):
    if self.action_id == 'FA1':
      return 'Burn 1'
    elif self.action_id == 'FA2':
      return '4pw -> 1Q'
    elif self.action_id == 'FA3':
      return '3pw -> 1o'
    elif self.action_id == 'FA4':
      return '1Q -> 1o'
    elif self.action_id == 'FA5':
      return '4pw -> 1K'
    elif self.action_id == 'FA6':
      return '1pw -> 1C'
    elif self.action_id == 'FA7':
      return '1K -> 1C'
    elif self.action_id == 'FA8':
      return '1o -> 1C'
    elif self.action_id == 'FA9':
      return '1o -> 1pt'
  
  def _effect_default(self):
    if self.action_id == 'FA1':
      return Effect(immediate={'burn' : 1})
    elif self.action_id == 'FA2':
      return Effect(immediate={'qubit' : 1})
    elif self.action_id == 'FA3':
      return Effect(immediate={'ore' : 1})
    elif self.action_id == 'FA4':
      return Effect(immediate={'ore' : 1})
    elif self.action_id == 'FA5':
      return Effect(immediate={'knowledge' : 1})
    elif self.action_id == 'FA6':
      return Effect(immediate={'coin' : 1})
    elif self.action_id == 'FA7':
      return Effect(immediate={'coin' : 1})
    elif self.action_id == 'FA8':
      return Effect(immediate={'coin' : 1})
    elif self.action_id == 'FA9':
      return Effect(immediate={'power token' : 1})

class SpecialAction(TakeableAction):
  action_id = Enum('SPEC_IVIT', 'SPEC_BESCOD', 'SPEC_FIRAK', 'SPEC_AMBA',
                   'SPEC_BTAC', 'SPEC_ADV3', 'SPEC_AC', 'SPEC_TECH9',
                   'SPEC_ADV11', 'SPEC_ADV13', 'SPEC_BON4', 'SPEC_BON5')

  def _get_desc(self):
    aid = self.action_id

    if aid == 'SPEC_IVIT':
      return 'Space Station'
    elif aid == 'SPEC_BESCOD':
      return 'Advance lowest'
    elif aid == 'SPEC_FIRAK':
      return 'Downgrade'
    elif aid == 'SPEC_AMBA':
      return 'Swap PI'
    elif aid == 'SPEC_BTAC':
      return '+4C'
    elif aid == 'SPEC_ADV3':
      return '+1Q, +5C'
    elif aid == 'SPEC_AC':
      return '+1Q'
    elif aid == 'SPEC_TECH9':
      return '+4pw'
    elif aid == 'SPEC_ADV11':
      return '+3o'
    elif aid == 'SPEC_ADV13':
      return '+3K'
    elif aid == 'SPEC_BON4':
      return '+1dig'
    elif aid == 'SPEC_BON5':
      return '+3range'

  def _get_long_desc(self):
    aid = self.action_id

    if aid == 'SPEC_IVIT':
      return 'Build space station'
    elif aid == 'SPEC_BESCOD':
      return 'Advance lowest tech'
    elif aid == 'SPEC_FIRAK':
      return 'Downgrade research lab'
    elif aid == 'SPEC_AMBA':
      return 'Swap PI and mine'
    elif aid == 'SPEC_BTAC':
      return '+4C'
    elif aid == 'SPEC_ADV3':
      return '+1Q, +5C'
    elif aid == 'SPEC_AC':
      return '+1Q'
    elif aid == 'SPEC_TECH9':
      return '+4pw'
    elif aid == 'SPEC_ADV11':
      return '+3o'
    elif aid == 'SPEC_ADV13':
      return '+3K'
    elif aid == 'SPEC_BON4':
      return '+1 dig'
    elif aid == 'SPEC_BON5':
      return '+3 range action'

  def _effect_default(self):
    aid = self.action_id

    if aid == 'SPEC_IVIT':
      return Effect(special_action={'special' : 'ivits_ss'},
                    choices=['coordinate'])
    elif aid == 'SPEC_BESCOD':
      return Effect(special_action={'special' : 'bescods_techup'},
                    choices=['tech_track'])
    elif aid == 'SPEC_FIRAK':
      return Effect(special_action={'special' : 'firaks_demote'},
                    choices=['coordinate', 'tech_track'])
    elif aid == 'SPEC_AMBA':
      return Effect(special_action={'special' : 'ambas_swap'},
                    choices=['coordinate'])
    elif aid == 'SPEC_BTAC':
      return Effect(special_action={'coin' : 4})
    elif aid == 'SPEC_ADV3':
      return Effect(special_action={'qubit' : 1, 'coin' : 5})
    elif aid == 'SPEC_AC':
      return Effect(special_action={'qubit' : 1})
    elif aid == 'SPEC_TECH9':
      return Effect(special_action={'charge' : 4})
    elif aid == 'SPEC_ADV11':
      return Effect(special_action={'ore' : 3})
    elif aid == 'SPEC_ADV13':
      return Effect(special_action={'knowledge' : 3})
    elif aid == 'SPEC_BON4':
      return Effect(special_action={'terraform' : 1},
                    choices=['coordinate'])
    elif aid == 'SPEC_BON5':
      return Effect(special_action={'+range' : 3},
                    choices=['coordinate'])


class TechupAction(TakeableAction):
  tech_track = Enum('terraforming', 'navigation', 'AI',
                    'gaiaforming', 'economy', 'science')
  tech_level = Enum(1,2,3,4,5)

  _possible_action_ids = List(['TECHUP_{0}_{1}'.format(x,y)
                       for x in ('TERR', 'NAV', 'AI', 'GAIA', 'ECON', 'SCI')
                       for y in range(1,6)])
  action_id = Enum('TECHUP_TERR_1', values='_possible_action_ids')

  def _determine_action_id(self, tech_track, tech_level):
    aid = 'TECHUP_'

    if tech_track == 'terraforming':
      aid += 'TERR'
    elif tech_track == 'navigation':
      aid += 'NAV'
    elif tech_track == 'AI':
      aid += 'AI'
    elif tech_track == 'gaiaforming':
      aid += 'GAIA'
    elif tech_track == 'economy':
      aid += 'ECON'
    elif tech_track == 'science':
      aid += 'SCI'

    aid += '_{0}'.format(str(tech_level))

    return aid

  def _effect_default(self):
    aid = self.action_id

    if aid in ('TERR3', 'GAIA3', 'ECON3', 'SCI3'):
      return Effect(immediate={'charge' : 3})

    if aid in ('TERR1', 'TERR4'):
      return Effect(immediate={'ore' : 2})
    elif aid == 'TERR5':
      return Effect(immediate={'terraforming_fed' : 1})

    elif aid in ('NAV1', 'AI1', 'AI2'):
      return Effect(immediate={'qubit' : 1})
    elif aid == 'NAV3':
      return Effect(immediate={'qubit' : 1, 'charge' : 3})
    elif aid == 'NAV5':
      return Effect(choices=['coordinate'])
    elif aid == 'AI3':
      return Effect(immediate={'qubit' : 2, 'charge' : 3})
    elif aid == 'AI4':
      return Effect(immediate={'qubit' : 2})

    elif aid == 'AI5':
      return Effect(immediate={'qubit' : 4})

    elif aid == 'GAIA2':
      return Effect(immediate={'power token' : 3})
    elif aid == 'GAIA5': 
      return Effect(immediate={'VP' : 4,
                               'per' : {'gaia' : {'VP' : 1}}})


    elif aid == 'ECON1':
      return Effect(income={'coin' : 2, 'charge' : 1})
    elif aid == 'ECON2':
      return Effect(income={'ore' : 1, 'coin' : 2, 'charge' : 2})
    elif aid == 'ECON3':
      return Effect(income={'ore' : 1, 'coin' : 3, 'charge' : 3})
    elif aid == 'ECON4':
      return Effect(income={'ore' : 2, 'coin' : 4, 'charge' : 4})
    elif aid == 'ECON5':
      return Effect(immediate={'ore' : 3, 'coin' : 6, 'charge' : 6}, income={})

    elif aid in ('SCI1', 'SCI2', 'SCI3', 'SCI4'):
      return Effect(income={'knowledge' : self.tech_level})
    elif aid == 'SCI5':
      return Effect(immediate={'knowledge' : 9}, income={})
    else:
      return Effect()

  def __init__(self, tech_track, tech_level, *args, **kwargs):
    super().__init__(self._determine_action_id(tech_track, tech_level), 
                   *args, **kwargs)
    self.tech_track = tech_track
    self.tech_level = tech_level



  
  
class MoveAction(TakeableAction):
  action_id = Enum('ACT1', 'ACT2', 'ACT3', 'ACT4', 'ACT5', 'ACT6', 'ACT7', 
                   'ACT8') 

  choices = Property

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

  def _get_choices(self):
    if self.action_id == 'ACT1':
      return ['coordinate']
    elif self.action_id == 'ACT2':
      return ['coordinate', 'which_power_tokens']
    elif self.action_id == 'ACT3':
      return ['coordinate', 'building_upgrade', 'tech_tile', 'tech_replace',
              'tech_track']
    elif self.action_id == 'ACT4':
      return ['satellites', 'which_power_tokens', 'which_federation_supply']
    elif self.action_id == 'ACT5':
      return ['tech_track']
    elif self.action_id == 'ACT6':
      return ['power_action', 'subsequent_effect']
    elif self.action_id == 'ACT7':
      return ['special_action', 'subsequent_effect']
    elif self.action_id == 'ACT8':
      return ['bonus_tile']

class AutomaAction(MoveAction):
  automa_vp = Int
  automa_pass = Bool
  do_nothing = Bool

  action_id = Enum('AUTOMA')

  second_action = Instance(EventDescription, ())

  def _get_choices(self):
    return []

  def __init__(self, *args, **kwargs):
    super().__init__(self, 'AUTOMA', *args, **kwargs)
  
class PassiveCharge(TakeableAction):
  action_id = Enum('PASSIVE_CHARGE')

  description = Instance(EventDescription, ())

  choices = Property
  def _get_choices(self):
    return ['charge_passive']

  height = Int
  vp = Int

  adjusted_charge = Int

  gains = Property
  def _get_gains(self):
    return {'charge' : self.adjusted_charge, 'VP' : -(self.adjusted_charge-1)}

  def __init__(self, *args, **kwargs):
    super().__init__(action_id='PASSIVE_CHARGE', *args, **kwargs)
  
  def adjust_charge(self, cur_power):
    self.adjusted_charge = self.height

    potential = cur_power['1'] * 2 + cur_power['2']
    if potential < self.adjusted_charge:
      self.adjusted_charge = potential

    if self.vp + 1 < self.adjusted_charge:
      self.adjusted_charge = self.vp + 1

    return self.adjusted_charge

class InitialPlacement(TakeableAction):
  action_id = Enum('INITIAL_PLACEMENT')
  description = Instance(EventDescription, ())

  choices = Property
  def _get_choices(self):
    return ['coordinate']

  def __init__(self, *args, **kwargs):
    super().__init__(action_id='INITIAL_PLACEMENT', *args, **kwargs)

class InitialBonus(TakeableAction):
  action_id = Enum('INITIAL_BONUS')
  description = Instance(EventDescription, ())

  choices = Property
  def _get_choices(self):
    return ['bonus_tile']

  def __init__(self, *args, **kwargs):
    super().__init__(action_id='INITIAL_BONUS', *args, **kwargs)


class Reaction(TakeableAction):
  action_id = Enum('GAIA_TERRAN', 'GAIA_ITAR')

  description = Instance(EventDescription, ())

  def _get_desc(self):
    if self.action_id == 'GAIA_TERRAN':
      return 'FREE ACTIONS'
    elif self.action_id == 'GAIA_ITAR':
      return 'TECH TILES'

  def _effect_default(self):
    if self.action_id == 'GAIA_TERRAN':
      return Effect(gaia_action='Terrans',
                    choices=['pass_gaia'])
    elif self.action_id == 'GAIA_ITAR':
      return Effect(gaia_action='Itars',
                    choices=['pass_gaia', 
                             'tech_tile', 'tech_replace', 'tech_track'])
