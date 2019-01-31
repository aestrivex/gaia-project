from traits.api import (HasPrivateTraits, Dict, Bool, Enum, Property, Str,
                        Instance, Int, Any)

class Effect(HasPrivateTraits):
  #coded
  income = Dict(Str, Int)
  immediate = Dict(Str, Int)
  special_action = Dict(Str, Any)
  when = Dict
  whenpass = Dict

  #uncoded
  endgame = Bool
  power_value_ACPI_4 = Bool

class TakeableAction(HasPrivateTraits):
  action_id = Str
  available = Bool(True)

  effect = Instance(Effect)

  desc = Property
  def _get_desc(self):
    return ValueError("Abstract class TakeableAction has no desc")

  long_desc = Property
  def _get_long_desc(self):
    return self.desc

  def __init__(self, action_id):
    super().__init__()
    self.action_id = action_id

  def __str__(self):
    return '{0}({1})'.format(self.__class__.__name__, self.action_id)

  def __repr__(self):
    return self.__str__()

class PowerAction(TakeableAction):
  action_id = Enum('PA1', 'PA2', 'PA3', 'PA4', 'PA5', 'PA6', 'PA7',
                         'QA1', 'QA2', 'QA3')

  cost_type = Property
  cost = Property

  def _get_cost_type(self):
    if self.action_id[0] == 'Q':
      return 'qubit'
    else:
      return 'power'
  
  def _get_cost(self): 
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
      return Effect(immediate={'terraform' : 2})
    elif self.action_id == 'PA3':
      return Effect(immediate={'ore' : 2})
    elif self.action_id == 'PA4':
      return Effect(immediate={'coin' : 7})
    elif self.action_id == 'PA5':
      return Effect(immediate={'knowledge' : 2})
    elif self.action_id == 'PA6':
      return Effect(immediate={'terraform' : 1})
    elif self.action_id == 'PA7':
      return Effect(immediate={'power token' : 2})
    elif self.action_id == 'QA1':
      return Effect(immediate={'tech tile' : 1})
    elif self.action_id == 'QA2':
      return Effect(immediate={'rescore_fed' : 1})
    elif self.action_id == 'QA3':
      return Effect(immediate={'VP' : 1,
                               'per' : {'planet type' : {'VP' : 1}}})

class FreeAction(TakeableAction):
  action_id = Enum('FA1', 'FA2', 'FA3', 'FA4', 'FA5', 'FA6', 'FA7', 'FA8',
                   'FA9')

  cost_type = Property
  cost = Property

  def _get_cost(self):
    if self.action_id == 'FA1':
      return 0
    elif self.action_id in ('FA2', 'FA5'):
      return 4
    elif self.action_id == 'FA3':
      return 3
    else:
      return 1

  def _get_cost_type(self):
    if self.action_id == 'FA4':
      return 'qubit'
    elif self.action_id == 'FA7':
      return 'knowledge'
    elif self.action_id in ('FA8', 'FA9'):
      return 'ore'
    else:
      return 'power'

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
  action_id = Property
  def _get_action_id(self): 
    if self.effect is None:
      return ValueError("Special action is not defined")

    sa = self.effect.special_action

    if sa is None:
      return ValueError("SpecialAction must have special_action defined")

    elif sa == {'build' : 'space_station'}:
      return 'SPEC_IVIT'
    elif sa == {'special' : 'bescods_techup'}:
      return 'SPEC_BESCOD'
    elif sa == {'special' : 'firaks_demote'}:
      return 'SPEC_FIRAK'
    elif sa == {'special' : 'ambas_swap'}:
      return 'SPEC_AMBA'
    elif sa == {'coin' : 4}:
      return 'SPEC_BTAC'
    elif sa == {'qubit' : 1, 'coin' : 5}:
      return 'SPEC_ADV3'
    elif sa == {'qubit' : 1}:
      return 'SPEC_AC'
    elif sa == {'charge' : 4}:
      return 'SPEC_TECH9'
    elif sa == {'ore' : 3}:
      return 'SPEC_ADV11'
    elif sa == {'knowledge' : 3}:
      return 'SPEC_ADV13'
    elif sa == {'terraform' : 1}:
      return 'SPEC_BON4'
    elif sa == {'+range' : 3}:
      return 'SPEC_BON5'

  def _get_desc(self):
    if self.effect is None:
      return ValueError("Special Action is not defined")
    else:
      return self.action_id

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


