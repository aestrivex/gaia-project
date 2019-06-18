from traits.api import (HasPrivateTraits, List, Instance, Dict, Enum, Property,
                        Int, cached_property, Str, Tuple, Bool)
from .constants import (INCOME_CHART, STARTING_POWER, BUILDING_COSTS,
                        BUILDING_PATHS, STARTING_RESOURCES)
from .tile import Tile
from .effect import Effect
from .terrain import terrain_distance
from .automa import Automa

import numpy as np

class Player(HasPrivateTraits):
  username = Str

  intelligence = Enum('human', 'ai', 'automa')

  automa = Instance(Automa)

  tiles = List(Instance(Tile))
  
  buildings = Dict(Str, Int)  
                    #building type -> number remaining on player board)

  faction = Enum('Terrans', 'Lantids', 'Nevlas', 'Itars', 'Bescods', 'Firaks',
                 'Ambas', 'Taklons', 'Gleens', 'Xenos', 'Geodens', 'Bal Taks',
                 'Hadsch Hallas', 'Ivits')

  building_costs = Dict(Str, Dict(Str, Int)) #{building-> {resource -> cost}}

  building_paths = Dict(Str, Tuple) #{mine -> trade post}

  #the income chart holds all the income information on the player board,
  #including base income, which incomes come from which buildings
  #structure {base -> {knowledge -> 1, coin -> 1},
  #           mines -> ({ore -> 1}, {ore -> 1}, {ore -> 0})
  #           etc}
  _income_chart = Dict(Str, Tuple)

  #available resources
  knowledge = Int
  coin = Int
  ore = Int
  qubit = Int
  key = Int(0)
  power = Dict(Str, Int)      #bowl str -> int

  academy_action = Instance(Effect)

  planet_types = Int(0)
  sectors = Int(0)
  federation_buildings = Int(0)
  _federations_acquired = Int(0)

  pi_bonus = Instance(Effect)
  racial_bonus = Instance(Effect)

  when_effects = List(Instance(Effect))
  whenpass_effects = List(Instance(Effect))

  passed = Bool(False)

  def __str__(self):
    return self.faction
  
  def __repr__(self):
    return '{0}: {1}'.format(self.username, self.faction)

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

  home_terrain = Property
  def _get_home_terrain(self):
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

  action_acad_built = Property
  def _get_action_acad_built(self):
    return self.buildings['action academy'] == 0

  tech_income = Dict(Str, Dict(Str, Int))

  building_income = Property(depends_on = 'buildings')
  @cached_property
  def _get_building_income(self):
    income = {'ore' : 0, 'knowledge' : 0, 'coin' : 0, 'qubit' : 0,
              'power token' : 0, 'charge' : 0}
    for building in self._income_chart:
      if building == 'base':
        continue

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
    income = {'ore' : 0, 'knowledge' : 0, 'coin' : 0, 'qubit' : 0,
              'power token' : 0, 'charge' : 0}
    for tile in self.tiles:
      if tile.effect.income is None:
        continue
      for resource in tile.effect.income:
        income[resource] += tile.effect.income[resource]

    return income

  income = Property(depends_on = 'building_income, tile_income, tech_income')
  @cached_property
  def _get_income(self):
    income = {'ore' : 0, 'knowledge' : 0, 'coin' : 0, 'qubit' : 0,
              'power token' : 0, 'charge' : 0}

    base_income = self._income_chart['base'][0]
    for resource in base_income:
      income[resource] += base_income[resource]

    for resource in self.tile_income:
      income[resource] += self.tile_income[resource]

    for resource in self.building_income:
      income[resource] += self.building_income[resource]

    return income

  
  possible_special_actions = Property(depends_on = 'tiles, buildings')
  @cached_property
  def _get_possible_special_actions(self):
    sas = []

    if self.faction in ('Ivits', 'Firaks', 'Ambas') and self.pi_built:
      sas.append(SpecialAction(self.pi_bonus.special_action))

    elif self.faction == 'Bescods':
      sas.append(SpecialAction(self.racial_bonus.special_action))

    if self.action_acad_built:
      sas.append(SpecialAction(self.academy_action.special_action))

    for tile in self.tiles:
      if tile.effect.special_action is not None:
        sas.append(SpecialAction(tile.effect.special_action))

    return sas 

  def __init__(self, faction, username='Freddy'):
    super().__init__()

    self.faction = faction
    self.power = STARTING_POWER[faction]
    self.buildings = {'mine' : 8,
                      'trading post' : 4,
                      'research lab' : 3,
                      'action academy' : 1,
                      'knowledge academy' : 1,
                      'planetary institute' : 1,
                'space station' : 6 if faction == 'Ivits' else 0,
                'gaiaformer' : 1 if faction in ('Terrans', 'Bal Taks') else 0}

    self.username = username

    self._income_chart = INCOME_CHART[faction] 
    self.tiles = []
    self.building_costs = BUILDING_COSTS

    if faction == 'Bescods':
      self.building_paths = BUILDING_PATHS['bescods']
    else:
      self.building_paths = BUILDING_PATHS['normal']

    if faction == 'Bal Taks':
      self.academy_action = Effect(special_action='SPEC_BTAC')
    else:
      self.academy_action = Effect(special_action='SPEC_AC')

    self.ore = STARTING_RESOURCES[faction]['ore']
    self.knowledge = STARTING_RESOURCES[faction]['knowledge']
    self.coin = STARTING_RESOURCES[faction]['coin']
    self.qubit = STARTING_RESOURCES[faction]['qubit']

    if faction == 'Ivits':
      self.pi_bonus = Effect(special_action='SPEC_IVIT')
    elif faction == 'Firaks':
      self.pi_bonus = Effect(special_action='SPEC_FIRAK')
    elif faction == 'Bescods':
      self.racial_bonus = Effect(special_action='SPEC_BESCOD')
    elif faction == 'Gleens': 
      self.pi_bonus = Effect(immediate={'federation' : 'FEDGLEEN'})
    elif faction == 'Ambas':
      self.pi_bonus = Effect(special_action='SPEC_AMBA')

  def can_afford(self, cost):
    for resource in cost:
      if resource == 'power':
        effective_power = self.power['3']
        if 'brainstone' in self.power:
          if self.power['brainstone'] == 3:
            effective_power += 3
        if effective_power < cost[resource]:
          return False

      #all other resource types
      else:
        if getattr(self, resource) < cost[resource]:
          return False

    #if every resource cost is satisfied, we can afford it
    return True

  def can_terraform(self, terrain, terraform_progress, bonus=0):
    terraform_cost = self.cost_to_terraform(terrain, terraform_progress, bonus)

    if terrain == 'transdim':
      return False
    elif terrain == 'gaia':
      return self.can_afford({'qubit' : 1, 'ore' : 1, 'coin' : 2})
    else:
      return self.can_afford({'ore' : terraform_cost + 1, 'coin' : 2})

  def cost_to_terraform(self, terrain, terraform_progress, bonus=0):
    if terrain == 'transdim':
      return False
    elif terrain == 'gaia':
      #gaiaformers handled elsewhere
      return {'qubit' : 1}

    shovels_needed = terrain_distance(terrain, self.home_terrain) - bonus

    if terraform_progress < 2: 
      terraform_cost = 3
    elif terraform__progress < 3:
      terraform_cost = 2
    else:
      terraform_cost = 1

    return {'ore' : terraform_cost * shovels_needed}


  def can_destroy_power(self, n_power):
    available_destroyable_power = (
      sum([self.power['{0}'.format(i)] for i in range(1,4)]))

    if 'brainstone' in self.power:
      if self.power['brainstone'] != -1:
        available_destroyable_power += 1

    return available_destroyable_power >= n_power
    
  def can_gaiaform(self, gaiaform_progress):
    if not self.buildings['gaiaformer'] > 0:
      return False

    return self.can_destroy_power(self.cost_to_gaiaform(gaiaform_progress))

  def cost_to_gaiaform(self, gaiaform_progress):
    if gaiaform_progress < 1:
      return np.inf
    elif gaiaform_progress < 3:
      return 6
    elif gaiaform_progress < 4:
      return 4
    else:
      return 3

  def can_burn(self):
    n_power_needed = 2
    if 'brainstone' in self.power:
      if self.power['brainstone'] == 2:
        n_power_needed -= 1
    return self.power['2'] >= n_power_needed

  def execute_spend(self, cost):
    for resource in cost:
      if resource == 'power':
        regular_power = self.power['3']
        power_cost = cost['power']
        if 'brainstone' in self.power:
          if power_cost >= 3:
            self.power['brainstone'] = 1
            power_cost -= 3
        self.power['3'] -= power_cost
        self.power['1'] += power_cost
        
      else:
        setattr(player, resource, getattr(player, resource) - cost[resource])

  def execute_destroy_power(self, n_power):
    if self.power['1'] >= n_power:
      self.power['1'] -= n_power
      return
    else:
      n_power -= self.power['1']
      self.power['1'] = 0

    if self.power['2'] >= n_power:
      self.power['2'] -= n_power
      return
    else:
      n_power -= self.power['2']
      self.power['2'] = 0

    if self.power['3'] >= n_power:
      self.power['3'] -= n_power
      return
    else:
      n_power -= self.power['3']
      self.power['3'] = 0

    if not self.power['brainstone'] != -1 and n_power == 1:
      raise GaiaProjectValidationError("Tried to destroy too much power")

      del self.power['brainstone']

  def execute_gain(self, gains, n_times=1):
    for resource in gains:
      if resource == 'charge':
        n_charge = gains['charge'] * n_times
        while n_charge > 0:
          if 'brainstone' in self.power:
            if self.power['brainstone'] == 1:
              self.power['brainstone'] == 2
              n_charge -= 1
              continue
          if self.power['1'] > 0:
            charge_bowl = max(n_charge, self.power['1'])
            self.power['2'] += charge_bowl
            self.power['1'] -= charge_bowl
            n_charge -= charge_bowl
            continue
          if 'brainstone' in self.power:
            if self.power['brainstone'] == 2:
              self.power['brainstone'] == 3
              n_charge -= 1
              continue
          if self.power['2'] > 0:
            charge_bowl = max(n_charge, self.power['2'])
            self.power['3'] += charge_bowl
            self.power['2'] -= charge_bowl
            n_charge -= charge_bowl
            continue

          #if reached here and still have charge, it is wasted
          break
  
      if resource == 'power token':
        self.power['1'] += gains['power token'] * n_times

      elif resource in ('coin', 'ore', 'knowldge', 'qubit', 'key'):
        setattr(player, resource, 
                getattr(player, resource) + gains[resource] * n_times)
