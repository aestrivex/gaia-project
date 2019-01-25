from traits.api import (HasPrivateTraits, List, Instance, Dict, Enum, Property,
                        )
from .constants import (INCOME_CHART, STARTING_POWER, BUILDING_COSTS,
                        BUILDING_PATHS, STARTING_RESOURCES)


class Player(HasPrivateTraits):
  tiles = List(Instance(Tile))
  
  buildings = Dict  #str -> int
                    #building type -> number remaining on player board)

  faction = Enum('Terrans', 'Lantids', 'Nevlas', 'Itars', 'Bescods', 'Firaks',
                 'Ambas', 'Taklons', 'Gleens', 'Xenos', 'Geodens', 'Bal Taks',
                 'Hadsch Hallas', 'Ivits')

  building_costs = Dict #dict {str-> {resource -> cost}}

  building_paths = Dict #dict {mine -> trade post}

  starting_buildings = List
  special_placement_order = Int

  #the income chart holds all the income information on the player board,
  #including base income, which incomes come from which buildings
  #structure {base -> {knowledge -> 1, coin -> 1},
  #           mines -> ({ore -> 1}, {ore -> 1}, {ore -> 0})
  #           etc}
  _income_chart = Dict

  #available resources
  knowledge = Int
  coin = Int
  ore = Int
  qubit = Int
  key = Int(0)
  power = Dict      #bowl str -> int

  academy_action = Instance(Effect)

  planet_types = Int(0)
  sectors = Int(0)
  federation_buildings = Int(0)

  pi_bonus = Instance(Effect)
  racial_bonus = Instance(Effect)

  color = Property
  def _get_color(self):
    if self.faction in ('Terrans', 'Lantids'):
      return 'blue'
    elif self.faction in ('Nevlas', 'Itars'):
      return 'white'
    elif self.faction in ('Bescods', 'Firaks'):
      return 'gray'
    elif self.faction in ('Ambas', 'Taklons'):
      return 'brown'
    elif self.faction in ('Gleens', 'Xenos'):
      return 'yellow'
    elif self.faction in ('Geodens', 'Bal Taks'):
      return 'orange'
    elif self.faction in ('Hadsch Hallas', 'Ivits'):
      return 'red'

  home_planet = Property
  def _get_home_planet(self):
    if self.faction in ('Terrans', 'Lantids'):
      return 'terra'
    elif self.faction in ('Nevlas', 'Itars'):
      return 'ice'
    elif self.faction in ('Bescods', 'Firaks'):
      return 'titanium'
    elif self.faction in ('Ambas', 'Taklons'):
      return 'swamp'
    elif self.faction in ('Gleens', 'Xenos'):
      return 'desert'
    elif self.faction in ('Geodens', 'Bal Taks'):
      return 'volcanic'
    elif self.faction in ('Hadsch Hallas', 'Ivits'):
      return 'oxide'

  pi_built = Property
  def _get_pi_built(self):
    return self.buildings['planetary institute'] == 0

  building_income = Property(depends_on = 'buildings')
  @cached_property
  def _get_building_income(self):
    income = {'mine' : 0, 'knowledge' : 0, 'coin' : 0, 'qubit' : 0,
              'power token' : 0, 'charge' : 0}
    for building in self._income_chart:
      n_placed = self.buildings[building]
      n_produced = 0
      for building_copy in self._income_chart[building]:
        if n_produced >= n_placed:
          break

        for resource in building_copy:
          income[resource] += building_copy[resource]
        n_produced += 1

    return income
  
  tile_income = Property(depends_on = 'tiles')
  @cached_property
  def _get_tile_income(self):
    income = {'mine' : 0, 'knowledge' : 0, 'coin' : 0, 'qubit' : 0,
              'power token' : 0, 'charge' : 0}
    for tile in self.tiles:
      for resource in tile.effect.income:
        income[resource] += tile.effect.income[resource]

    return income

  income = Property(depends_on = 'building_income, tile_income')
  @cached_property
  def _get_income(self):
    income = {'mine' : 0, 'knowledge' : 0, 'coin' : 0, 'qubit' : 0,
              'power token' : 0, 'charge' : 0}

    for resource in self.tile_income:
      income[resource] += self.tile_income[resource]

    for resource in self.building_income:
      income[resource] += self.building_income[resource]

    return income

  def __init__(self, faction):
    super().__init__()

    self.faction = faction
    self.power = STARTING_POWER[faction]
    self.buildings = {'mine' : 8,
                      'trading post' : 4,
                      'research lab' : 3,
                      'academy' : 2,
                      'planetary institute' : 1,
                      'gaiaformer' : 3}

    self._income_chart = INCOME_CHART[faction] 
    self.tiles = []
    self.building_costs = BUILDING_COSTS

    if faction == 'Bescods':
      self.building_paths = BUILDING_PATHS['bescods']
    else:
      self.building_paths = BUILDING_PATHS['normal']

    if faction == 'Bal Taks':
      self.academy_action = Effect(special_action={'coin' : 4})
    else:
      self.academy_action = Effect(special_action={'qubit' : 4})

    self.ore = STARTING_RESOURCES[faction]['ore']
    self.knowledge = STARTING_RESOURCES[faction]['knowledge']
    self.coin = STARTING_RESOURCES[faction]['coin']
    self.qubit = STARTING_RESOURCES[faction]['qubit']

    if faction == 'Ivits':
      self.starting_buildings = ['planetary institute']
      self.special_placement_order = 2
    elif faction == 'Xenos':
      self.starting_buildings = ['mine', 'mine', 'mine']
      self.special_placement_order = 1
    else:
      self.starting_buildings = ['mine', 'mine']

    if faction == 'Ivits':
      self.pi_bonus = Effect(special_action={'build' : 'space_station'})
    elif faction == 'Firaks':
      self.pi_bonus = Effect(special_action={'special' : 'firaks_demote'}) 
    elif faction == 'Bescods':
      self.racial_bonus = Effect(special_action={'special' : 'bescods_techup'})
    elif faction == 'Gleens': 
      self.pi_bonus = Effect(immediate={'federation' : 'FEDGLEEN'})
    elif faction == 'Ambas':
      self.pi_bonus = Effect(special_action={'special' : 'ambas_swap'})
