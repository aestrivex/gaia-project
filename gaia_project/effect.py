from traits.api import (HasPrivateTraits, Dict, Bool, Enum, Property, Str,
                        Instance, Int, Any, List)

class Effect(HasPrivateTraits):
  #coded
  income = Dict(Str, Int)
  immediate = Dict(Str, Int)
  special_action = Enum('SPEC_IVIT', 'SPEC_BESCOD', 'SPEC_FIRAK', 'SPEC_AMBA',
                   'SPEC_BTAC', 'SPEC_ADV3', 'SPEC_AC', 'SPEC_TECH9',
                   'SPEC_ADV11', 'SPEC_ADV13', 'SPEC_BON4', 'SPEC_BON5')
  gaia_action = Enum('Terrans', 'Itars')
  when = Dict
  whenpass = Dict
  choices = List(Enum('building_upgrade', 'special_action', 'bonus_tile',
                      'which_federation_owned', 'which_federation_supply',
                      'which_power_tokens', 'tech_replace',
                      'coordinate', 'tech_tile', 'tech_track', 'power_action',
                      'charge_passive', 'pass_gaia', 'subsequent_effect'))

  #uncoded
  endgame = Bool
  power_value_ACPI_4 = Bool

