from traits.api import (HasPrivateTraits, Dict, Bool)

class Effect(HasPrivateTraits):
  #coded
  income = Dict
  immediate = Dict
  special_action = Dict
  when = Dict
  whenpass = Dict

  #uncoded
  endgame = Bool
  power_value_ACPI_4 = Bool
