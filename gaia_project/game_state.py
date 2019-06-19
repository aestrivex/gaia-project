from hexmap import Map
from traits.api import (HasPrivateTraits, List, Instance, Int, Dict, Str, 
                       Tuple, Enum, Bool)

from .move_action import Interaction
from .player import Player
from .tile import (FederationTile, TechTile, AdvancedTechTile, 
                   FinalScoringTile, RoundScoringTile, BonusTile)
from .constants import (BASIC_4P_SETUP, BUILDING_HEIGHTS, STARTING_TECHS,
                        TECH_ORDER, POWER_ACTIONS)

import numpy as np

class GameState(HasPrivateTraits):

  players = List(Instance(Player))

  turn_order = List(Instance(Player))
  next_turn_order = List(Instance(Player))

  score = Dict(Instance(Player), Int)

  federations_in_supply = Dict(Instance(FederationTile), Int)

  tech_tiles = List(Instance(TechTile))
  advanced_tech_tiles = List(Instance(AdvancedTechTile))

  terraforming_federation = Instance(FederationTile)
  tech_progress = Dict(Str, Dict(Instance(Player), Int))
  final_scoring_tiles = List(FinalScoringTile)
  round_scoring_tiles = List(RoundScoringTile)
  bonus_tiles = Dict(Instance(BonusTile), Instance(Player))

  power_actions_available = Dict(Instance(Interaction), Bool)
  special_actions_available = Dict(Instance(Player), 
                                            Dict(Instance(Interaction),
                                            Bool))

  buildings = Dict(Tuple, Tuple) #(x,y) -> (owner, type)
  lantid_shares = List(Tuple)

  orbitals = Dict(Tuple, Tuple)

  lost_planet = Tuple #(owner, (x,y))

  board_configuration = Dict(Tuple, Str)
  sectors = Dict(Tuple, Dict(Tuple, Str))
  map = Instance(Map)

  federations_formed = List(Tuple) #(owner, [(x,y)...])

  game_phase = Enum('Income', 'Gaia', 'Action', 'Cleanup')
  game_round = Enum(1, 2, 3, 4, 5, 6)

  def __init__(self, players, 
               cfg=BASIC_4P_SETUP,
               turn_order=None,
               score=None, 
               bonus_tiles=None,
               round_scoring=None,
               final_scoring=None,
               available_federations=None,
               tech_tiles=None,
               advanced_tech_tiles=None,
               terraforming_federation=None,
               *args, **kwargs):
    super().__init__(*args, **kwargs)
    
    self.players = players

    self.sectors = cfg
    self.board_configuration = {}

    self.power_actions_available = dict(zip( POWER_ACTIONS, 
                                             [True]*(len(POWER_ACTIONS)) ))
    self.special_actions_available = dict(zip( players, [{}]*len(players) ))
    #initially populate special actions, need a way to automatically populate 
    #when actions are added TODO trait notification
    for player in players:
      self.special_actions_available[player].update(
        player.possible_special_actions)

    for tile_placement in cfg:
      tx, ty = tile_placement
      tile = cfg[tile_placement]

      for planet in tile:
        px, py = planet
        self.board_configuration[(tx+px, ty+py)] = tile[planet]

    #determine board size and instantiate map
    max_x = 0
    max_y = 0
    for x,y in cfg:
      if x > max_x:
        max_x = x
      if y > max_y:
        max_y = y
    self.map = Map( (max_x+5, max_y+5) )

    if turn_order is not None:
      self.turn_order = turn_order
    else:
      self.turn_order = self.players.copy()

    if score is not None:
      self.score = score
    else:
      for player in self.players:
        self.score[player] = 10

    if bonus_tiles is not None:
      self.bonus_tiles = bonus_tiles
    else:
      self.bonus_tiles = dict(zip([BonusTile('BON{0}'.format(i)) for 
                                            i in range(1, len(players)+4)],
                                  [None]*6))

    if round_scoring is not None:
      self.round_scoring_tiles = round_scoring
    else:
      self.round_scoring_tiles = [RoundScoringTile('RS{0}'.format(i)) for
                                                    i in range(1, 7)]

    if final_scoring is not None:
      self.final_scoring_tiles = final_scoring
    else:
      self.final_scoring_tiles = [FinalScoringTile('FS1'),
                                  FinalScoringTile('FS2')]

    if available_federations is not None:
      self.federations_in_supply = available_federations
    else:
      federations_in_supply = dict(zip([FederationTile('FED{0}'.format(i))
                                                       for i in range(1, 7)],
                                            [2, 3, 3, 3, 3, 3]))
      self.federations_in_supply = federations_in_supply

    if tech_tiles is not None:
      self.tech_tiles = tech_tiles
    else:
      self.tech_tiles = [TechTile('TECH{0}'.format(i)) for i in range(1,10)]

    if advanced_tech_tiles is not None:
      self.advanced_tech_tiles = advanced_tech_tiles
    else:
      self.advanced_tech_tiles = [AdvancedTechTile('ADV{0}'.format(i))
                                  for i in range(1,7)]

    if terraforming_federation is not None:
      self.terraforming_federation = terraforming_federation
    else:
      self.terraforming_federation = FederationTile('FED1')

    self.tech_progress = dict(zip(TECH_ORDER, 
                                  [dict(zip(self.players,
                                           [0]*len(self.players)))]*6))
    for player in self.players:
      if player.faction in STARTING_TECHS:
        self.tech_progress[STARTING_TECHS[player.faction]][player] = 1

    print(self.tech_progress)
                                           
  def get_available_bonus_tiles(self):
    available_tiles = []
    for tile in self.bonus_tiles:
      if self.bonus_tiles[tile] is None:
        available_tiles.append(tile)
    return available_tiles

  def get_terrain(self, coordinates):
    return self.board_configuration[coordinates]

  def get_lowest_track(self, player):
    lowest_value = 5
    lowest_tracks = []
    for track in self.tech_progress:
      value = self.tech_progress[track][player]
      if value < lowest_value:
        lowest_value = value
        lowest_tracks = [track]
      elif value == lowest_value:
        lowest_tracks.append(track)
    return lowest_tracks

  def get_highest_track(self, player):
    highest_value = 0
    highest_tracks = []
    for track in self.tech_progress:
      value = self.tech_progress[track][player]
      if value > highest_value:
        highest_value = value
        highest_tracks = [track]
      elif value == highest_value:
        highest_tracks.append(track)
    return highest_tracks

  def get_nonmaxed_tracks(self, player):
    nonmaxed_tracks = []
    for track in self.tech_progress:
      if self.tech_progress[track][player] < 5:
        nonmaxed_tracks.append(track) 
    return nonmaxed_tracks

  def is_track_maxed_by_somebody(self, track):
    for player in self.players:
      if self.tech_progress[track][player] == 5:
        return True
    return False

  def in_effective_range(self, player, coordinates, bonus=0):
    return self._navigate(player, coordinates)[0]

  def get_nav_cost(self, player, coordinates, bonus=0):
    return self._navigate(player, coordinates)[1]

  def _navigate(self, player, coordinates, bonus=0):
    nav_level = self.tech_progress['navigation'][player]
    if nav_level > 2:
      nav_range = 1
    elif nav_level > 4:
      nav_range = 2
    elif nav_level > 5:
      nav_range = 3
    else:
      nav_range = 4

    for q in range(player.qubit+1):

      #hexes_in_range = self.m.spread(coordinates, radius=nav_range+q*2+bonus)
      working_range = nav_range + q * 2 + bonus
  
      if self.in_literal_range(player, coordinates, working_range):
        return True, q

    return False, np.nan

  def in_literal_range(self, player, coordinates, nav):
    for loc in self.buildings:
      building = self.buildings[loc]
      if building[0] is player:
        if self.map.distance(building[1], coordinates) < nav:
          return True
    return False

  def charge_height(self, player, coordinates):
    #hexes_in_range = self.m.spread(coordinates, radius=2)
    
    max_height = 0

    for loc in self.buildings:
      building = self.buildings[loc]
      if building[0] is player:
        #if building[1] in hexes_in_range:
        if self.map.distance(building[1], coordinates) <= 2:
          max_height = self._height_of_building_or_orbital(building[1])

    return max_height

  def _height_of_building_or_orbital(self, coordinates):
    if coordinates in self.buildings:
      player, building_type = self.buildings[coordinates]
      height = BUILDING_HEIGHTS[building_type]
  
      #check TECH3
      if (len(list(filter(lambda tile: tile.tile_id == 'TECH3', 
                          player.tiles))) > 1):
        if building_type in ('planetary institute', 'academy'):
          height += 1
      
      #check bescod PI
      if player.faction == 'Bescods' and player.pi_built:
        if self.board_configuration[coordinates] == 'titanium':
          height += 1 

      return height 

    elif coordinates in self.orbitals:
      player, orbital_type = self.orbitals[coordinates]
      if orbital_type == 'space station':
        return 1
      else:
        return 0

    raise ValueError("No building or orbital at coordinates")

  def collection_height(self, coords):
    collection_height = 0
    for xy in coords:    
      collection_height += self._height_of_building_or_orbitals(xy)
    return collection_height

  def is_collection_contiguous(self, coords):
    contigs = set()
    for loc in coords:
      if loc in contigs:
        continue
      for coordinates in coords:
        if self.map.distance(loc, coordinates) == 1:
          contigs.add(loc)
          contigs.add(coordinates)

    return len(contigs) == len(coords)

  def get_all_buildings_of_type_from_player(self, player, building_type):
    player_buildings = []
    for loc in self.buildings:
      if self.buildings[loc][0] == player:
        if self.buildings[loc][1] == building_type:
          player_buildings.append(loc)
    return player_buildings

  def closest_building_of_type_to_any_other_player(self, player, bulding_type):
    buildings = self.get_all_buildings_of_type_from_player(player, building_type)

    min_dist = np.inf
    for building in buildings:
      dist = self.min_distance_to_any_other_player(player, building) 
      if dist < min_dist:
        min_dist = dist
        closest_buildings = [building]
      if dist == min_dist:
        closest_buildings.append(building)

    return closest_buildings

  def min_distance_to_any_other_player(self, player, coordinates):
    min_dist = np.inf

    for loc in self.buildings:
      if self.buildings[loc][0] != player:
        dist = self.map.distance(loc, coordinates)
        if dist < min_dist:
          min_dist = dist

    return min_dist

  def get_num_gaias_owned_by_player(self, player):
    n_gaia = 0
    for loc in self.buildings:
      if self.buildings[loc][0] == player:
        if self.board_configuration[loc] == 'gaia':
          n_gaia += 1
    return n_gaia

  def get_empty_planets(self):
    empty_planets = []
    for loc in self.board_configuration:
      if loc not in self.buildings:
        empty_planets.append(loc)
    return empty_planets

  def is_loc_in_sector(self, loc, sector):
    sx, sy = sector
    sector_center = (sx + 3, sy + 2)
    return loc in self.map.spread(sector_center, radius=2)

  def is_building_urban(self, player, loc):
    urban_zone = self.map.spread(loc, radius=2)

    for urban_loc in urban_zone:
      if urban_loc in self.buildings:
        if self.buildings[urban_loc][0] == player:
          continue
        else:
          return True
    return False

  def is_federation_legal(self, player, fed_struct):

    if player.faction == 'Ivits':
      target_height = 7 * (player._federations_acquired + 1)
    else:
      target_height = 7
    
    #check to see if the federation has sufficient height
    fed_height = self.collection_height(fed_struct)
    if self.collection_height(fed_struct) > target_height:
      explanation = 'Federation needs at least {0} height'.format(
        target_height)
      return False, explanation

    #check to see if the federation is contiguous
    if not self.is_collection_contiguous(fed_struct):
      explanation = 'Federation is not contiguous'
      return False, explanation

    acceptable_orbital_removal = False
    acceptable_building_removal = False

    for nstructure in fed_struct:

      #check to see if candidate federation has intersects or borders
      #player's existing federation 
      for fed in self.federations_formed:
        if not fed[0] == player:
          continue
        for structure in fed[1]:
          if (self.map.distance(structure, nstructure) <= 1 and 
              player.faction != 'Ivits'): 
            explanation = "Your federations border or intersect"
            return False, explanation
            
      #check if candidate federation has other player's building in it
      if nstructure in self.buildings:
        if self.buildsings[nstructure][0] != player:
          explanation = "Building in federation is not yours"
          return False, explanation

      #check to see if the federation would be valid without each structure
      fed_without = fed_struct.copy()
      fed_without.remove(nstructure)
      height_without = self.collection_height(fed_without)
      continuous_without = self.is_collection_contiguous(fed_without)
      if (self.collection_height(fed_without) >= target_height and
          self.is_collection_contiguous(fed_without)):

        if nstructure in self.buildings:
          acceptable_building_removal = True
        else:
          acceptable_satellite_removal = True

    #check to see if the federation could be formed with fewer satellites
    #TODO very hard
      #form a parallelogram between each pair of planets and space stations
      #if any planets fall inside this parallelogram, throw away the smallest
        #parallelograms and only look at the largest parallelogram
      #calculate the fewest satellite routes moving in only two directions for
        #each parallelogram needing connection
      #if that route is blocked, hug the perimeter in both directions and pick
        #the more efficient

      #for all such pairs, brute force 
      #calculate the amount of satellites with the most overlap
        #this is NP complete        
      

    #check to see if the federation would be valid with one fewer satellite
    #and one fewer building
    if acceptable_building_removal and acceptable_satellite_removal:
      explanation = ("Federation would be valid with one fewer satellites "
                     "and one fewer buildings")
      return False, explanation
      
  def add_to_bordering_federations(self, player, coordinates):
    for fed in self.federations_formed:
      if not fed[0] == player:
        continue
      for structure in fed[1]:
        if self.map.distance(structure, coordinates) <= 1:
          fed[1].append(coordinates)

    



