from traits.api import (HasPrivateTraits, List, Enum, Str, Property, Instance, 
                        Bool, Any)
from .effect import Effect
#from .player import Player

class Tile(HasPrivateTraits):
  desc = Property
  long_desc = Property
  effect = Instance(Effect)

  def _get_desc(self):
    return ValueError("Abstract class Tile has no desc")
  def _get_long_desc(self):
    return ValueError("Abstract class Tile has no long_desc")

class ObtainableTile(Tile):
  owner = Any

class TechTile(ObtainableTile):
  tech_id = Enum('TECH1', 'TECH2', 'TECH3', 'TECH4', 'TECH5',
                 'TECH6', 'TECH7', 'TECH8', 'TECH9')

  def __init__(self, tech_id):
    super().__init__()
    self.tech_id = tech_id

  def _get_desc(self):
    if self.tech_id == 'TECH1':
      return '+1o +1Q'
    elif self.tech_id == 'TECH2':
      return '+1K per ptype'
    elif self.tech_id == 'TECH3':
      return 'AC=4pw, PI=4pw'
    elif self.tech_id == 'TECH4':
      return '+7VP'
    elif self.tech_id == 'TECH5':
      return 'i: 1o, 1pw'
    elif self.tech_id == 'TECH6':
      return 'i: 1K, 1C'
    elif self.tech_id == 'TECH7':
      return 'gaia=3VP'
    elif self.tech_id == 'TECH8':
      return 'i: 4C'
    elif self.tech_id == 'TECH9':
      return 'action: 4pw'
 
  def _get_long_desc(self):
    if self.tech_id == 'TECH1':
      return 'gain 1 ore immediate gain 1 QIC immediately'
    elif self.tech_id == 'TECH2':
      return 'gain 1 knowledge per planet type immediate'
    elif self.tech_id == 'TECH3':
      return 'academy and PI have 4 power value'
    elif self.tech_id == 'TECH4':
      return 'gain 7 VP immediate'
    elif self.tech_id == 'TECH5':
      return '1 ore income 1 power charge income'
    elif self.tech_id == 'TECH6':
      return '1 knowledge income 1 coin income'
    elif self.tech_id == 'TECH7':
      return 'colonizing gaia gives 3VP'
    elif self.tech_id == 'TECH8':
      return '4 coin income'
    elif self.tech_id == 'TECH9':
      return 'special action 4 power charge'

  def _effect_default(self):
    if self.tech_id == 'TECH1':
      return Effect(income={'ore' : 1, 'qubit' : 1})
    elif self.tech_id == 'TECH2':
      return Effect(immediate={'per' : {'planet type' : {'knowledge' : 1}}})
    elif self.tech_id == 'TECH3':
      return Effect(power_value_AcadPI_4=True)
    elif self.tech_id == 'TECH4':
      return Effect(immediate={'VP' : 7})
    elif self.tech_id == 'TECH5':
      return Effect(income={'ore' : 1, 'charge' : 1})
    elif self.tech_id == 'TECH6':
      return Effect(income={'knowledge' : 1, 'coin' : 1})
    elif self.tech_id == 'TECH7':
      return Effect(when={'build' : {'gaia' : {'VP' : 3}}})
    elif self.tech_id == 'TECH8':
      return Effect(income={'coin' : 4})
    elif self.tech_id == 'TECH9':
      return Effect(action={'charge' : 4})

class AdvancedTechTile(TechTile):
  tech_id = Enum('ADV1', 'ADV2', 'ADV3', 'ADV4', 'ADV5', 'ADV6',
                'ADV7', 'ADV8', 'ADV9', 'ADV10', 'ADV11', 'ADV12',
                'ADV13', 'ADV14', 'ADV15')

  def __init__(self, tech_id):
    super().__init__(tech_id)

  def _get_desc(self):
    if self.tech_id == 'ADV1':
      return 'passVP 3 per fed'
    elif self.tech_id == 'ADV2':
      return 'tech=2VP'
    elif self.tech_id == 'ADV3':
      return 'action: 1Q, 5C'
    elif self.tech_id == 'ADV4':
      return '+2VP per mine'
    elif self.tech_id == 'ADV5':
      return 'passVP 3 per RL'
    elif self.tech_id == 'ADV6':
      return '+1o per sector'
    elif self.tech_id == 'ADV7':
      return 'passVP 1 per ptype'
    elif self.tech_id == 'ADV8':
      return '+1VP per gaia'
    elif self.tech_id == 'ADV9':
      return '+4VP per tradepost'
    elif self.tech_id == 'ADV10':
      return '+2VP per sector'
    elif self.tech_id == 'ADV11':
      return 'action: 3o'
    elif self.tech_id == 'ADV12':
      return '+5VP per fed'
    elif self.tech_id == 'ADV13':
      return 'action: 3K'
    elif self.tech_id == 'ADV14':
      return 'mine=3VP'
    elif self.tech_id == 'ADV15':
      return 'tradepost=3VP'

  def _get_long_desc(self):
    if self.tech_id == 'ADV1':
      return 'when passing 3VP per federation'
    elif self.tech_id == 'ADV2':
      return 'advancing tech gives 2VP'
    elif self.tech_id == 'ADV3':
      return 'special action 1 QIC and 5 coins'
    elif self.tech_id == 'ADV4':
      return 'gain 2 VP per mine immediate'
    elif self.tech_id == 'ADV5':
      return 'when passing 3VP per research lab'
    elif self.tech_id == 'ADV6':
      return 'gain 1 ore per sector immediate'
    elif self.tech_id == 'ADV7':
      return 'when passing 1VP per planet type'
    elif self.tech_id == 'ADV8':
      return 'gaia 2VP per gaia planet immediate'
    elif self.tech_id == 'ADV9':
      return 'gain 4VP per trading post immediate'
    elif self.tech_id == 'ADV10':
      return 'gain 2VP per sector immediate'
    elif self.tech_id == 'ADV11':
      return 'special action 3 ore'
    elif self.tech_id == 'ADV12':
      return 'gain 5VP per federation immediate'
    elif self.tech_id == 'ADV13':
      return 'special action 3 knowledge'
    elif self.tech_id == 'ADV14':
      return 'building mine gives 3VP'
    elif self.tech_id == 'ADV15':
      return 'building trading post gives 3VP'

  def _effect_default(self):
    if self.tech_id == 'ADV1':
      return Effect(whenpass={'per' : {'federation' : {'VP' : 3}}})
    elif self.tech_id == 'ADV2':
      return Effect(when={'techup' : {'VP' : 2}})
    elif self.tech_id == 'ADV3':
      return Effect(special_action={'qubit' : 1, 'coin' : 5})
    elif self.tech_id == 'ADV4':
      return Effect(immediate={'per' : {'mine' : {'VP' : 2}}})
    elif self.tech_id == 'ADV5':
      return Effect(whenpass={'per' : {'research lab' : {'VP' : 3}}})
    elif self.tech_id == 'ADV6':
      return Effect(immediate={'per' : {'sector' : {'ore' : 1}}})
    elif self.tech_id == 'ADV7':
      return Effect(whenpass={'per' : {'planet type' : {'VP' : 1}}})
    elif self.tech_id == 'ADV8':
      return Effect(immediate={'per' : {'gaia' : {'VP' : 2}}})
    elif self.tech_id == 'ADV9':
      return Effect(immediate={'per' : {'trading post' : {'VP' : 4}}})
    elif self.tech_id == 'ADV10':
      return Effect(immediate={'per' : {'sector' : {'VP' : 2}}})
    elif self.tech_id == 'ADV11':
      return Effect(special_action={'ore' : 3})
    elif self.tech_id == 'ADV12':
      return Effect(immediate={'per' : {'federation' : {'VP' : 5}}})
    elif self.tech_id == 'ADV13':
      return Effect(special_action={'knowledge' : 3})
    elif self.tech_id == 'ADV14':
      return Effect(when={'build' : {'mine' : {'VP' : 3}}})
    elif self.tech_id == 'ADV15':
      return Effect(when={'build' : {'trading post' : {'VP' : 3}}})


class FederationTile(ObtainableTile):
  fed_id = Enum('FED1', 'FED2', 'FED3', 'FED4', 'FED5', 'FED6', 'FEDGLEEN')

  def __init__(self, fed_id):
    super().__init__()
    self.fed_id = fed_id

  def _get_desc(self):
    if self.fed_id == 'FED1':
      return 'FED 12VP'
    elif self.fed_id == 'FED2':
      return 'FED 8VP 1Q'
    elif self.fed_id == 'FED3':
      return 'FED 8VP 2pt'
    elif self.fed_id == 'FED4':
      return 'FED 7VP 2o'
    elif self.fed_id == 'FED5':
      return 'FED 7VP 6C'
    elif self.fed_id == 'FED6':
      return 'FED 6VP 2K'
    elif self.fed_id == 'FEDGLEEN':
      return 'FED 1o 1K 2C'

  def _get_long_desc(self):
    if self.fed_id == 'FED1':
      return 'FED 12VP'
    elif self.fed_id == 'FED2':
      return 'FED 8VP 1 QIC'
    elif self.fed_id == 'FED3':
      return 'FED 8VP 2 new pwr token'
    elif self.fed_id == 'FED4':
      return 'FED 7VP 2 ore'
    elif self.fed_id == 'FED5':
      return 'FED 7VP 6 coins'
    elif self.fed_id == 'FED6':
      return 'FED 6VP 2 knowledge'
    elif self.fed_id == 'FEDGLEEN':
      return 'FED Gleen 1 ore 1 knol 2 coin'

  def _effect_default(self):
    if self.fed_id == 'FED1':
      return Effect(immediate={'VP' : 12})
    elif self.fed_id == 'FED2':
      return Effect(immediate={'VP' : 8, 'qubit' : 1, 'key' : 1})
    elif self.fed_id == 'FED3':
      return Effect(immediate={'VP' : 8, 'power token' : 1, 'key' : 1})
    elif self.fed_id == 'FED4':
      return Effect(immediate={'VP' : 7, 'ore' : 2, 'key' : 1})
    elif self.fed_id == 'FED5':
      return Effect(immediate={'VP' : 7, 'coin' : 6, 'key' : 1})
    elif self.fed_id == 'FED6':
      return Effect(immediate={'VP' : 6, 'knowledge' : 2, 'key' : 1})
    elif self.fed_id == 'FEDGLEEN':
      return Effect(immediate={'ore' : 1, 'knowledge' : 1, 'coin' : 2,
                               'key' : 1})


class BonusTile(ObtainableTile):
  bonus_id = Enum('BON1', 'BON2', 'BON3', 'BON4', 'BON5',
                  'BON6', 'BON7', 'BON8', 'BON9', 'BON10')

  def __init__(self, bonus_id):
    super().__init__()
    self.bonus_id = bonus_id

  def _get_desc(self):
    if self.bonus_id == 'BON1':
      return "i: 1o, 1K"
    elif self.bonus_id == 'BON2':
      return "i: 2pt, 1o"
    elif self.bonus_id == 'BON3':
      return "i: 2C, 1Q"
    elif self.bonus_id == 'BON4':
      return 'i: 2C action: 1dig'
    elif self.bonus_id == 'BON5':
      return 'i: 2pw action: +3range'
    elif self.bonus_id == 'BON6':
      return 'i: 1o passVP 1 per mine'
    elif self.bonus_id == 'BON7':
      return 'i: 1o passVP 2 per trade post'
    elif self.bonus_id == 'BON8':
      return 'i: 1K passVP 3 per RL'
    elif self.bonus_id == 'BON9':
      return 'i: 4pw passVP 4 per PI/AC'
    elif self.bonus_id == 'BON10':
      return 'i: 4C passVP 1 per gaia'

  def _get_long_desc(self):
    if self.bonus_id == 'BON1':
      return "1 ore income, 1 knowledge income"
    elif self.bonus_id == 'BON2':
      return "2 new power token income, 1 ore income"
    elif self.bonus_id == 'BON3':
      return "2 coin income, 1 QIC income"
    elif self.bonus_id == 'BON4':
      return "2 coin income, special action 1 terraform"
    elif self.bonus_id == 'BON5':
      return "2 power charge income, special action +3 range"
    elif self.bonus_id == 'BON6':
      return "1 ore income, when passing 1VP per mine"
    elif self.bonus_id == 'BON7':
      return "1 ore income, when passing 2VP per trading post"
    elif self.bonus_id == 'BON8':
      return "1 knowledge income, when passing 3VP per research lab"
    elif self.bonus_id == 'BON9':
      return "4 power charge income, when passing 4VP per PI/academy"
    elif self.bonus_id == 'BON10':
      return "4 coin income, when passing 1VP per gaia planet"

  def _effect_default(self):
    if self.bonus_id == 'BON1':
      return Effect(income={'ore' : 1, 'knowledge' : 1})
    elif self.bonus_id == 'BON2':
      return Effect(income={'power token' : 1, 'ore' : 1})
    elif self.bonus_id == 'BON3':
      return Effect(income={'coin' : 2, 'qubit' : 1})
    elif self.bonus_id == 'BON4':
      return Effect(income={'coin' : 2}, special_action={'terraform' : 1})
    elif self.bonus_id == 'BON5':
      return Effect(income={'charge' : 2}, special_action={'+range' : 3})
    elif self.bonus_id == 'BON6':
      return Effect(income={'ore' : 1},
                    whenpass={'per' : {'mine' : {'VP' : 1}}})
    elif self.bonus_id == 'BON7':
      return Effect(income={'ore' : 1},
                    whenpass={'per' : {'trading post' : {'VP' : 2}}})
    elif self.bonus_id == 'BON8':
      return Effect(income={'knowledge' : 1},
                    whenpass={'per' : {'research lab' : {'VP' : 3}}})
    elif self.bonus_id == 'BON9':
      return Effect(income={'charge' : 4},
                    whenpass={'per' : {'academy' : {'VP' : 4},
                                       'planetary institute' : {'VP' : 4}}})
    elif self.bonus_id == 'BON10':
      return Effect(income={'coin' : 4},
                    whenpass={'per' : {'gaia' : {'VP' : 1}}})

class RoundScoringTile(Tile):
  round_scoring_id = Enum('RS1', 'RS2', 'RS3', 'RS4', 'RS5', 'RS6', 'RS7')

  def __init__(self, round_scoring_id):
    super().__init__()
    self.round_scoring_id = round_scoring_id

  def _get_desc(self):
    if self.round_scoring_id == 'RS1':
      return 'dig=2VP'
    elif self.round_scoring_id == 'RS2':
      return 'tech=2VP'
    elif self.round_scoring_id == 'RS3':
      return 'mine=2VP'
    elif self.round_scoring_id == 'RS4':
      return 'fed=5VP'
    elif self.round_scoring_id == 'RS5':
      return 'tradepost=4VP'
    elif self.round_scoring_id == 'RS6':
      return 'gaia=3VP'
    elif self.round_scoring_id == 'RS7':
      return 'PI/AC=5VP'

  def _get_long_desc(self):
    if self.round_scoring_id == 'RS1':
      return '2VP per terraform step this round'
    elif self.round_scoring_id == 'RS2':
      return '2VP per tech advanced this round'
    elif self.round_scoring_id == 'RS3':
      return '2VP per mine built this round'
    elif self.round_scoring_id == 'RS4':
      return '5VP per federation formed this round'
    elif self.round_scoring_id == 'RS5':
      return '4VP per trade post built this round'
    elif self.round_scoring_id == 'RS6':
      return '3VP per gaia planet colonized this round'
    elif self.round_scoring_id == 'RS7':
      return '5VP per academy or PI built this round'

  def _effect_default(self):
    if self.round_scoring_id == 'RS1':
      return Effect(when={'per' : {'terraform' : {'VP' : 2}}})
    elif self.round_scoring_id == 'RS2':
      return Effect(when={'techup' : {'VP' : 2}})
    elif self.round_scoring_id == 'RS3':
      return Effect(when={'build' : {'mine' : {'VP' : 2}}})
    elif self.round_scoring_id == 'RS4':
      return Effect(when={'build' : {'federation' : {'VP' : 5}}})
    elif self.round_scoring_id == 'RS5':
      return Effect(when={'build' : {'trading post' : {'VP' : 4}}})
    elif self.round_scoring_id == 'RS6':
      return Effect(when={'build' : {'gaia' : {'VP' : 3}}})
    elif self.round_scoring_id == 'RS7':
      return Effect(when={'build' : {'academy' : {'VP' : 5}},
                                     'planetary institute' : {'VP' : 5}})

class FinalScoringTile(Tile):
  final_scoring_id = Enum('FS1', 'FS2', 'FS3', 'FS4', 'FS5', 'FS6')

  def __init__(self, final_scoring_id):
    super().__init__()
    self.final_scoring_id = final_scoring_id

  def _get_desc(self):
    if self.final_scoring_id == 'FS1':
      return 'Most federation buildings'
    elif self.final_scoring_id == 'FS2':
      return 'Most buildings'
    elif self.final_scoring_id == 'FS3':
      return 'Most planet types'
    elif self.final_scoring_id == 'FS4':
      return 'Most gaia planets'
    elif self.final_scoring_id == 'FS5':
      return 'Most sectors'
    elif self.final_scoring_id == 'FS6':
      return 'Most satellites'

  def _get_long_desc(self):
    return self.desc

  def _effect_default(self):
    return Effect(endgame=True) 

class PowerAction(Tile):
  power_action_id = Enum('PA1', 'PA2', 'PA3', 'PA4', 'PA5', 'PA6', 'PA7',
                         'QA1', 'QA2', 'QA3')

  available = Bool(True)
  qubit_action = Bool(False)
  cost = Property

  def __init__(self, power_action_id):
    self.power_action_id = power_action_id

    if power_action_id[0] == 'Q':
      self.qubit_action = True
  
  def _get_cost(self): 
    if self.power_action_id == 'PA1':
      return 7
    elif self.power_action_id == 'PA2':
      return 5
    elif self.power_action_id in ('PA3', 'PA4', 'PA5', 'QA1'):
      return 4
    elif self.power_action_id in ('PA6', 'PA7', 'QA2'):
      return 3
    elif self.power_action_id == 'QA3':
      return 2

  def _get_desc(self):
    if self.power_action_id == 'PA1':
      return '+3K'
    elif self.power_action_id == 'PA2':
      return '+2dig'
    elif self.power_action_id == 'PA3':
      return '+2o'
    elif self.power_action_id == 'PA4':
      return '+7C'
    elif self.power_action_id == 'PA5':
      return '+2K'
    elif self.power_action_id == 'PA6':
      return '+1dig'
    elif self.power_action_id == 'PA7':
      return '+2pt'
    elif self.power_action_id == 'QA1':
      return '+tech'
    elif self.power_action_id == 'QA2':
      return 'fed'
    elif self.power_action_id == 'QA3':
      return 'VPs'

  def _get_long_desc(self):
    return self.desc

  def _effect_default(self):
    if self.power_action_id == 'PA1':
      return Effect(immediate={'knowledge' : 3})
    elif self.power_action_id == 'PA2':
      return Effect(immediate={'terraform' : 2})
    elif self.power_action_id == 'PA3':
      return Effect(immediate={'ore' : 2})
    elif self.power_action_id == 'PA4':
      return Effect(immediate={'coin' : 7})
    elif self.power_action_id == 'PA5':
      return Effect(immediate={'knowledge' : 2})
    elif self.power_action_id == 'PA6':
      return Effect(immediate={'terraform' : 1})
    elif self.power_action_id == 'PA7':
      return Effect(immediate={'power token' : 2})
    elif self.power_action_id == 'QA1':
      return Effect(immediate={'tech tile' : 1})
    elif self.power_action_id == 'QA2':
      return Effect(immediate={'rescore_fed' : 1})
    elif self.power_action_id == 'QA3':
      return Effect(immediate={'VP' : 1,
                               'per' : {'planet type' : {'VP' : 1}}})
