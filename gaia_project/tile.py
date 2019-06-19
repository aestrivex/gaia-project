from traits.api import (HasPrivateTraits, List, Enum, Str, Property, Instance, 
                        Bool, Any, Either)
from .effect import Effect

class Tile(HasPrivateTraits):
  tile_id = Str

  desc = Property
  long_desc = Property
  effect = Instance(Effect)

  def _get_desc(self):
    return ValueError("Abstract class Tile has no desc")
  def _get_long_desc(self):
    return ValueError("Abstract class Tile has no long_desc")

  def __init__(self, tile_id):
    super().__init__()
    self.tile_id = tile_id

  def __str__(self):
    return '{0}({1})'.format(self.__class__.__name__, self.tile_id)

  def __repr__(self):
    return self.__str__()

  def __eq__(self, other):
    if not type(self) == type(other):
      return False
    return self.tile_id == other.tile_id

  def __hash__(self):
    return hash(self.tile_id)
    

class ObtainableTile(Tile):
  owner = Any

class TechTile(ObtainableTile):
  tile_id = Enum('TECH1', 'TECH2', 'TECH3', 'TECH4', 'TECH5',
                 'TECH6', 'TECH7', 'TECH8', 'TECH9')

  def _get_desc(self):
    if self.tile_id == 'TECH1':
      return '+1o +1Q'
    elif self.tile_id == 'TECH2':
      return '+1K per ptype'
    elif self.tile_id == 'TECH3':
      return 'AC=4pw, PI=4pw'
    elif self.tile_id == 'TECH4':
      return '+7VP'
    elif self.tile_id == 'TECH5':
      return 'i: 1o, 1pw'
    elif self.tile_id == 'TECH6':
      return 'i: 1K, 1C'
    elif self.tile_id == 'TECH7':
      return 'gaia=3VP'
    elif self.tile_id == 'TECH8':
      return 'i: 4C'
    elif self.tile_id == 'TECH9':
      return 'action: 4pw'
 
  def _get_long_desc(self):
    if self.tile_id == 'TECH1':
      return 'gain 1 ore immediate gain 1 QIC immediately'
    elif self.tile_id == 'TECH2':
      return 'gain 1 knowledge per planet type immediate'
    elif self.tile_id == 'TECH3':
      return 'academy and PI have 4 power value'
    elif self.tile_id == 'TECH4':
      return 'gain 7 VP immediate'
    elif self.tile_id == 'TECH5':
      return '1 ore income 1 power charge income'
    elif self.tile_id == 'TECH6':
      return '1 knowledge income 1 coin income'
    elif self.tile_id == 'TECH7':
      return 'colonizing gaia gives 3VP'
    elif self.tile_id == 'TECH8':
      return '4 coin income'
    elif self.tile_id == 'TECH9':
      return 'special action 4 power charge'

  def _effect_default(self):
    if self.tile_id == 'TECH1':
      return Effect(income={'ore' : 1, 'qubit' : 1})
    elif self.tile_id == 'TECH2':
      return Effect(immediate={'per' : {'planet type' : {'knowledge' : 1}}})
    elif self.tile_id == 'TECH3':
      return Effect()
    elif self.tile_id == 'TECH4':
      return Effect(immediate={'VP' : 7})
    elif self.tile_id == 'TECH5':
      return Effect(income={'ore' : 1, 'charge' : 1})
    elif self.tile_id == 'TECH6':
      return Effect(income={'knowledge' : 1, 'coin' : 1})
    elif self.tile_id == 'TECH7':
      return Effect(when={'build' : {'gaia' : {'VP' : 3}}})
    elif self.tile_id == 'TECH8':
      return Effect(income={'coin' : 4})
    elif self.tile_id == 'TECH9':
      return Effect(special_action ='SPEC_TECH9')

class AdvancedTechTile(TechTile):
  tile_id = Enum('ADV1', 'ADV2', 'ADV3', 'ADV4', 'ADV5', 'ADV6',
                'ADV7', 'ADV8', 'ADV9', 'ADV10', 'ADV11', 'ADV12',
                'ADV13', 'ADV14', 'ADV15')

  available = Bool
  replaced = Either(None, Instance(TechTile))

  def _get_desc(self):
    if self.tile_id == 'ADV1':
      return 'passVP 3 per fed'
    elif self.tile_id == 'ADV2':
      return 'tech=2VP'
    elif self.tile_id == 'ADV3':
      return 'action: 1Q, 5C'
    elif self.tile_id == 'ADV4':
      return '+2VP per mine'
    elif self.tile_id == 'ADV5':
      return 'passVP 3 per RL'
    elif self.tile_id == 'ADV6':
      return '+1o per sector'
    elif self.tile_id == 'ADV7':
      return 'passVP 1 per ptype'
    elif self.tile_id == 'ADV8':
      return '+1VP per gaia'
    elif self.tile_id == 'ADV9':
      return '+4VP per tradepost'
    elif self.tile_id == 'ADV10':
      return '+2VP per sector'
    elif self.tile_id == 'ADV11':
      return 'action: 3o'
    elif self.tile_id == 'ADV12':
      return '+5VP per fed'
    elif self.tile_id == 'ADV13':
      return 'action: 3K'
    elif self.tile_id == 'ADV14':
      return 'mine=3VP'
    elif self.tile_id == 'ADV15':
      return 'tradepost=3VP'

  def _get_long_desc(self):
    if self.tile_id == 'ADV1':
      return 'when passing 3VP per federation'
    elif self.tile_id == 'ADV2':
      return 'advancing tech gives 2VP'
    elif self.tile_id == 'ADV3':
      return 'special action 1 QIC and 5 coins'
    elif self.tile_id == 'ADV4':
      return 'gain 2 VP per mine immediate'
    elif self.tile_id == 'ADV5':
      return 'when passing 3VP per research lab'
    elif self.tile_id == 'ADV6':
      return 'gain 1 ore per sector immediate'
    elif self.tile_id == 'ADV7':
      return 'when passing 1VP per planet type'
    elif self.tile_id == 'ADV8':
      return 'gaia 2VP per gaia planet immediate'
    elif self.tile_id == 'ADV9':
      return 'gain 4VP per trading post immediate'
    elif self.tile_id == 'ADV10':
      return 'gain 2VP per sector immediate'
    elif self.tile_id == 'ADV11':
      return 'special action 3 ore'
    elif self.tile_id == 'ADV12':
      return 'gain 5VP per federation immediate'
    elif self.tile_id == 'ADV13':
      return 'special action 3 knowledge'
    elif self.tile_id == 'ADV14':
      return 'building mine gives 3VP'
    elif self.tile_id == 'ADV15':
      return 'building trading post gives 3VP'

  def _effect_default(self):
    if self.tile_id == 'ADV1':
      return Effect(whenpass={'per' : {'federation' : {'VP' : 3}}})
    elif self.tile_id == 'ADV2':
      return Effect(when={'techup' : {'VP' : 2}})
    elif self.tile_id == 'ADV3':
      #return Effect(special_action={'qubit' : 1, 'coin' : 5})
      return Effect(special_action='SPEC_ADV3')
    elif self.tile_id == 'ADV4':
      return Effect(immediate={'per' : {'mine' : {'VP' : 2}}})
    elif self.tile_id == 'ADV5':
      return Effect(whenpass={'per' : {'research lab' : {'VP' : 3}}})
    elif self.tile_id == 'ADV6':
      return Effect(immediate={'per' : {'sector' : {'ore' : 1}}})
    elif self.tile_id == 'ADV7':
      return Effect(whenpass={'per' : {'planet type' : {'VP' : 1}}})
    elif self.tile_id == 'ADV8':
      return Effect(immediate={'per' : {'gaia' : {'VP' : 2}}})
    elif self.tile_id == 'ADV9':
      return Effect(immediate={'per' : {'trading post' : {'VP' : 4}}})
    elif self.tile_id == 'ADV10':
      return Effect(immediate={'per' : {'sector' : {'VP' : 2}}})
    elif self.tile_id == 'ADV11':
      #return Effect(special_action={'ore' : 3})
      return Effect(special_action='SPEC_ADV11')
    elif self.tile_id == 'ADV12':
      return Effect(immediate={'per' : {'federation' : {'VP' : 5}}})
    elif self.tile_id == 'ADV13':
      #return Effect(special_action={'knowledge' : 3})
      return Effect(special_action='SPEC_ADV13')
    elif self.tile_id == 'ADV14':
      return Effect(when={'build' : {'mine' : {'VP' : 3}}})
    elif self.tile_id == 'ADV15':
      return Effect(when={'build' : {'trading post' : {'VP' : 3}}})


class FederationTile(ObtainableTile):
  tile_id = Enum('FED1', 'FED2', 'FED3', 'FED4', 'FED5', 'FED6', 'FEDGLEEN')

  def _get_desc(self):
    if self.tile_id == 'FED1':
      return 'FED 12VP'
    elif self.tile_id == 'FED2':
      return 'FED 8VP 1Q'
    elif self.tile_id == 'FED3':
      return 'FED 8VP 2pt'
    elif self.tile_id == 'FED4':
      return 'FED 7VP 2o'
    elif self.tile_id == 'FED5':
      return 'FED 7VP 6C'
    elif self.tile_id == 'FED6':
      return 'FED 6VP 2K'
    elif self.tile_id == 'FEDGLEEN':
      return 'FED 1o 1K 2C'

  def _get_long_desc(self):
    if self.tile_id == 'FED1':
      return 'FED 12VP'
    elif self.tile_id == 'FED2':
      return 'FED 8VP 1 QIC'
    elif self.tile_id == 'FED3':
      return 'FED 8VP 2 new pwr token'
    elif self.tile_id == 'FED4':
      return 'FED 7VP 2 ore'
    elif self.tile_id == 'FED5':
      return 'FED 7VP 6 coins'
    elif self.tile_id == 'FED6':
      return 'FED 6VP 2 knowledge'
    elif self.tile_id == 'FEDGLEEN':
      return 'FED Gleen 1 ore 1 knol 2 coin'

  def _effect_default(self):
    if self.tile_id == 'FED1':
      return Effect(immediate={'VP' : 12})
    elif self.tile_id == 'FED2':
      return Effect(immediate={'VP' : 8, 'qubit' : 1, 'key' : 1})
    elif self.tile_id == 'FED3':
      return Effect(immediate={'VP' : 8, 'power token' : 1, 'key' : 1})
    elif self.tile_id == 'FED4':
      return Effect(immediate={'VP' : 7, 'ore' : 2, 'key' : 1})
    elif self.tile_id == 'FED5':
      return Effect(immediate={'VP' : 7, 'coin' : 6, 'key' : 1})
    elif self.tile_id == 'FED6':
      return Effect(immediate={'VP' : 6, 'knowledge' : 2, 'key' : 1})
    elif self.tile_id == 'FEDGLEEN':
      return Effect(immediate={'ore' : 1, 'knowledge' : 1, 'coin' : 2,
                               'key' : 1})


class BonusTile(ObtainableTile):
  tile_id = Enum('BON1', 'BON2', 'BON3', 'BON4', 'BON5',
                  'BON6', 'BON7', 'BON8', 'BON9', 'BON10')

  def _get_desc(self):
    if self.tile_id == 'BON1':
      return "i: 1o, 1K"
    elif self.tile_id == 'BON2':
      return "i: 2pt, 1o"
    elif self.tile_id == 'BON3':
      return "i: 2C, 1Q"
    elif self.tile_id == 'BON4':
      return 'i: 2C action: 1dig'
    elif self.tile_id == 'BON5':
      return 'i: 2pw action: +3range'
    elif self.tile_id == 'BON6':
      return 'i: 1o passVP 1 per mine'
    elif self.tile_id == 'BON7':
      return 'i: 1o passVP 2 per trade post'
    elif self.tile_id == 'BON8':
      return 'i: 1K passVP 3 per RL'
    elif self.tile_id == 'BON9':
      return 'i: 4pw passVP 4 per PI/AC'
    elif self.tile_id == 'BON10':
      return 'i: 4C passVP 1 per gaia'

  def _get_long_desc(self):
    if self.tile_id == 'BON1':
      return "1 ore income, 1 knowledge income"
    elif self.tile_id == 'BON2':
      return "2 new power token income, 1 ore income"
    elif self.tile_id == 'BON3':
      return "2 coin income, 1 QIC income"
    elif self.tile_id == 'BON4':
      return "2 coin income, special action 1 terraform"
    elif self.tile_id == 'BON5':
      return "2 power charge income, special action +3 range"
    elif self.tile_id == 'BON6':
      return "1 ore income, when passing 1VP per mine"
    elif self.tile_id == 'BON7':
      return "1 ore income, when passing 2VP per trading post"
    elif self.tile_id == 'BON8':
      return "1 knowledge income, when passing 3VP per research lab"
    elif self.tile_id == 'BON9':
      return "4 power charge income, when passing 4VP per PI/academy"
    elif self.tile_id == 'BON10':
      return "4 coin income, when passing 1VP per gaia planet"

  def _effect_default(self):
    if self.tile_id == 'BON1':
      return Effect(income={'ore' : 1, 'knowledge' : 1})
    elif self.tile_id == 'BON2':
      return Effect(income={'power token' : 1, 'ore' : 1})
    elif self.tile_id == 'BON3':
      return Effect(income={'coin' : 2, 'qubit' : 1})
    elif self.tile_id == 'BON4':
      return Effect(income={'coin' : 2}, 
                    #special_action={'terraform' : 1},
                    special_action='SPEC_BON4',
                    choices=['coordinate'])
    elif self.tile_id == 'BON5':
      return Effect(income={'charge' : 2},
                    #special_action={'+range' : 3},
                    special_action='SPEC_BON5',
                    choices=['coordinate'])
    elif self.tile_id == 'BON6':
      return Effect(income={'ore' : 1},
                    whenpass={'per' : {'mine' : {'VP' : 1}}})
    elif self.tile_id == 'BON7':
      return Effect(income={'ore' : 1},
                    whenpass={'per' : {'trading post' : {'VP' : 2}}})
    elif self.tile_id == 'BON8':
      return Effect(income={'knowledge' : 1},
                    whenpass={'per' : {'research lab' : {'VP' : 3}}})
    elif self.tile_id == 'BON9':
      return Effect(income={'charge' : 4},
                    whenpass={'per' : {'academy' : {'VP' : 4},
                                       'planetary institute' : {'VP' : 4}}})
    elif self.tile_id == 'BON10':
      return Effect(income={'coin' : 4},
                    whenpass={'per' : {'gaia' : {'VP' : 1}}})

class RoundScoringTile(Tile):
  tile_id = Enum('RS1', 'RS2', 'RS3', 'RS4', 'RS5', 'RS6', 'RS7')

  def _get_desc(self):
    if self.tile_id == 'RS1':
      return 'dig=2VP'
    elif self.tile_id == 'RS2':
      return 'tech=2VP'
    elif self.tile_id == 'RS3':
      return 'mine=2VP'
    elif self.tile_id == 'RS4':
      return 'fed=5VP'
    elif self.tile_id == 'RS5':
      return 'tradepost=4VP'
    elif self.tile_id == 'RS6':
      return 'gaia=3VP'
    elif self.tile_id == 'RS7':
      return 'PI/AC=5VP'

  def _get_long_desc(self):
    if self.tile_id == 'RS1':
      return '2VP per terraform step this round'
    elif self.tile_id == 'RS2':
      return '2VP per tech advanced this round'
    elif self.tile_id == 'RS3':
      return '2VP per mine built this round'
    elif self.tile_id == 'RS4':
      return '5VP per federation formed this round'
    elif self.tile_id == 'RS5':
      return '4VP per trade post built this round'
    elif self.tile_id == 'RS6':
      return '3VP per gaia planet colonized this round'
    elif self.tile_id == 'RS7':
      return '5VP per academy or PI built this round'

  def _effect_default(self):
    if self.tile_id == 'RS1':
      return Effect(when={'terraform' : {'VP' : 2}})
    elif self.tile_id == 'RS2':
      return Effect(when={'techup' : {'VP' : 2}})
    elif self.tile_id == 'RS3':
      return Effect(when={'build' : {'mine' : {'VP' : 2}}})
    elif self.tile_id == 'RS4':
      return Effect(when={'build' : {'federation' : {'VP' : 5}}})
    elif self.tile_id == 'RS5':
      return Effect(when={'build' : {'trading post' : {'VP' : 4}}})
    elif self.tile_id == 'RS6':
      return Effect(when={'build' : {'gaia' : {'VP' : 3}}})
    elif self.tile_id == 'RS7':
      return Effect(when={'build' : {'academy' : {'VP' : 5}},
                                     'planetary institute' : {'VP' : 5}})

class FinalScoringTile(Tile):
  tile_id = Enum('FS1', 'FS2', 'FS3', 'FS4', 'FS5', 'FS6')

  def _get_desc(self):
    if self.tile_id == 'FS1':
      return 'Most federation buildings'
    elif self.tile_id == 'FS2':
      return 'Most buildings'
    elif self.tile_id == 'FS3':
      return 'Most planet types'
    elif self.tile_id == 'FS4':
      return 'Most gaia planets'
    elif self.tile_id == 'FS5':
      return 'Most sectors'
    elif self.tile_id == 'FS6':
      return 'Most satellites'

  def _get_long_desc(self):
    return self.desc

  def _effect_default(self):
    return Effect(endgame=True) 
