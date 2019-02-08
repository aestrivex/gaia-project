from traits.api import (HasPrivateTraits, Instance, List)

from .player import Player
from .game_state import GameState
from .communication_layer import CommunicationLayer
from .move_action import (TakeableAction, EventDescription, MoveAction, 
                          FreeAction, SpecialAction, PowerAction, TechupAction)
from .tile import AdvancedTechTile
from .constants import BUILDING_COSTS

import pygame

class Engine(HasPrivateTraits):

  clayer = Instance(CommunicationLayer)

  game_state = Instance(GameState)

  def __init__(self, clayer):
    super().__init__()

    self.clayer = clayer
    self.game_state = GameState(clayer.players)

  def run(self):

    self.clayer.update_gfx()


    self.setup_board()

    for round_n in range(1, 7):
      self.run_income()
      self.run_gaia()
      self.run_action()
      self.run_cleanup()

    self.scoring()


  def run_income(self):
    pass

  def run_gaia(self):
    pass

  def run_action(self):

    print('turn order', self.game_state.turn_order)
    while True:
      if len(self.game_state.turn_order) == 0:
        break
      for player in self.game_state.turn_order:

        while True:
          move = self.clayer.make_move(player)
  
          if not issubclass(type(move), TakeableAction):
            continue
           
          move_successful = self.process_move(player, move)  
          if move_successful:
            break
        
  def run_cleanup(self):
    pass

  def setup_board(self):
    pass

  def fetch_choices(self, player, move):
    #in general, the choices are inserted into the move description
    for choice in move.choices:
      if self.is_choice_needed(player, choice, move):
        c_move = self.clayer.make_choice(player, choice, move)

        #if player made a different move choice, just 
        #return so player does not have queued sequence of strange moves
        if issubclass(type(c_move), TakeableAction):
          return False
        #TODO make the other buttons gray out when choice needed in clayer
        
        elif type(c_move) is EventDescription:
          move.merge_input(c_move)

        #if player hit cancel, go back to making moves
        if move.description.cancel_choice:
          return False

    return True

  def process_move(self, player, move):
    choices_successful = self.fetch_choices(player, move)
    if not choices_successful:
      return False

    move_decision, explanation = self.is_move_legal(player, move)
    if not move_decision:
      #player made illegal move
      self.clayer.inform_illegal_choice(player, explanation)
      return False

    self.execute_move(player, move) 
    return True

  def is_choice_needed(self, player, choice, move):
    desc = move.description
    if move.action_id == 'ACT3':
      if choice == 'tech_tile':
        return desc.upgrade in ('research lab', 'action academy',
                                'knowledge academy')
      elif choice == 'tech_track':
        return self.is_tech_track_choice_constrained_by_tile(move)
      elif choice == 'tech replace':
        return type(desc.tech_tile_choice) == AdvancedTechTile

    elif move.action_id == 'QA1':
      if choice == 'tech_track':
        return self.is_tech_track_choice_constrained_by_tile(move)
      elif choice == 'tech replace':
        return type(desc.tech_tile_choice) == AdvancedTechTile

    #in all other cases
    return True

  def is_tech_track_choice_constrained_by_tile(self, move):
    desc = move.description
    return self.game_state.tech_tiles.index(desc.tech_tile_choice) >= 6 

  def is_move_legal(self, player, move):

    desc = move.description

    #ACTION 1
    if move.action_id == 'ACT1':
      return self.is_build_mine_legal(player, move)

    #ACTION 2
    if move.action_id == 'ACT2':
      return self.is_gaiaform_legal(player, move)

    #ACTION 3
    if move.action_id == 'ACT3':
      if desc.coordinates is None:
        explanation = 'No hex selected'
        return False, explanation
      if desc.upgrade is None:
        explanation = 'No upgrade path selected'
        return False, explanation
      if not player.buildings[desc.upgrade] > 0:
        explanation = 'No {0}s left'.format(desc.upgrade)
        return False, explanation
      
      xy = desc.coordinates
      b = self.game_state.buildings

      if xy not in self.game_state.board_configuration:
        explanation = 'There is no planet there'
        return False, explanation
      if xy not in b:
        explanation = 'There is no building there'
        return False, explanation
      if b[xy][0] != player:
        explanation = 'Building belongs to a different player'
        return False, explanation
      if desc.upgrade not in player.building_paths[b[xy][1]]:
        explanation = 'Upgrade path not allowed'
        return False, explanation

      #if not needing to pick tech tile, stop and return
      if desc.tech_tile_choice is None:
        return True, None

      #tech tile selection
      return self.is_tech_tile_selection_legal(player, move)

    #ACTION 4
    if move.action_id == 'ACT4':
      return self.game_state.is_federation_legal(player, desc.fed_structures)

    #ACTION 5
    if move.action_id == 'ACT5':
      if desc.tech_track is None:
        explanation = 'No tech track selected'
        return False, explanation

      if self.game_state.tech_progress[desc.tech_track][player] == 5:
        explanation = 'Tech track is already maxed'
        return False, explanation
          
      if (self.game_state.tech_progress[desc.tech_track][player] == 4 and
          player.keys == 0):
        explanation = "Need fed to advance tech to max"
        return False, explanation

    #ACTION 6
    if move.action_id == 'ACT6':
      if desc.power_action is None:
        explanation = "No power action selected" 
        return False, explanation 
      if not desc.power_action.available:
        explanation = "Power action already taken"
        return False, explanation
      if not player.can_afford(desc.power_action.cost):
        explanation = "Not enough power"
        return False, explanation

    #ACTION 7 
    if move.action_id == 'ACT7':
      if desc.special_action is None:
        explanation = "No special action selected"
        return False, explanation
      if not desc.special_action.available:
        explanation = "Special action already taken"
        return False, explanation

    #ACTION 8
    if move.action_id == 'ACT8':
      if desc.bonus_tile is None:
        explanation = "No bonus tile selected"
        return False, explanation

    #ALL FREE AND POWER ACTIONS
    if type(move) in (FreeAction, PowerAction):
      if not player.can_afford(move.cost):
        explanation = "Can't afford cost"
        return False, explanation

    #POWER ACTION 2
    if move.action_id == 'PA2':
      return self.is_build_mine_legal(player, move, bonus_terraforming=2)

    #POWER ACTION 6, BONUS 4
    if move.action_id in ('PA6', 'BON4'):
      return self.is_build_mine_legal(player, move, bonus_terraforming=1)
    
    #QUBIT ACTION 1
    if move.action_id == 'QA1':
      if desc.tech_tile_choice is None:
        explanation = 'No tech tile selected'
        return False, explanation
      return self.is_tech_tile_selection_legal(player, move)

    #QUBIT ACTION 2  
    if move.action_id == 'QA2':
      if (len(list(filter(lambda tile: type(tile) == FederationTile,
                          player.tiles))) == 0):
        explanation = "No federations available to rescore"
        return False, explanation

    #IVITS PI
    if move.action_id == 'SPEC_IVIT':
      if desc.coordinates is None:
        explanation = 'No hex selected'
        return False, explanation
      if not player.buildings['space station'] > 0:
        explanation = 'No space stations left'
        return False, explanation

      xy = desc.coordinates

      if xy in self.game_state.board_configuration:
        explanation = 'There is a planet there'
        return False, explanation
      if (xy in self.game_state.orbitals and
          self.game_state.orbitals[xy][1] == 'space station'):
        explanation = 'There is already a space station there'
        return False, explanation
      if not self.game_state.in_navigation_range(player, xy, bonus):
        explanation = 'Selected hex not in range'
        return False, explanation

    #FIRAK PI
    if move.action_id == 'SPEC_FIRAK': 
      if desc.coordinates is None:
        explanation = 'No hex selected'
        return False, explanation
      if not player.buildsings['trading post'] > 0:
        explanation = 'No trading posts left'
        return False, explanation

      xy = desc.coordinates
      b = self.game_state.buildings
        
      if xy not in self.game_state.board_configuration:
        explanation = 'There is no planet there'
        return False, explanation
      if xy not in b:
        explanation = 'There is no building there'
        return False, explanation
      if b[xy][0] != player:
        explanation = 'Building belongs to a different player'
        return False, explanation
      if b[xy][1] != 'research lab':
        explanation = 'May only downgrade research labs'
        return False, explanation

    #BESCOD RACIAL
    if move.action_id == 'SPEC_BESCOD':
      if desc.tech_track is None:
        explanation = "No tech track selected"
        return False, explanation

      if desc.tech_track not in self.game_state.get_lowest_track(player):
        explanation = "Must pick lowest tech"
        return False, explanation

    #AMBA PI
    if move.action_id == 'SPEC_AMBA':
      if desc.coordinates is None:
        explanation = 'No hex selected'
        return False, explanation

      xy = desc.coordinates
      b = self.game_state.buildings
        
      if xy not in self.game_state.board_configuration:
        explanation = 'There is no planet there'
        return False, explanation
      if xy not in b:
        explanation = 'There is no building there'
        return False, explanation
      if b[xy][0] != player:
        explanation = 'Building belongs to a different player'
        return False, explanation
      if b[xy][1] != 'mine':
        explanation = 'May only swap with mine'
        return False, explanation

    #BONUS 5
    if move.action_id == 'BON5':
      mine_legal, expl1 = self.is_build_mine_legal(player, move, bonus_nav=3)
      gaia_legal, expl2 = self.is_gaiaform_legal(player, move, bonus_nav=3)
      if not mine_legal and not gaia_legal:
        explanation = 'Mine: {0}, Gaia: {1}'.format(expl1, expl2)
        return False, explanation

    #TECHUP NAV5
    if move.action_id == 'TECHUP_NAV5':
      if desc.coordinates is None:
        explanation = 'No hex selected'
        return False, explanation

      xy = desc.coordinates
      
      if xy in self.game_state.board_configuration:
        explanation = 'May not place lost planet on existing planet'
        return False, explanation

      if xy in self.game_state.orbitals:
        explanation = 'May not place lost planet on existing satellite'
        return False, explanation

      if not self.game_state.in_navigation_range(player, xy, bonus=1):
        explanation = 'Lost planet must be placed in range 4'
        return False, explanation

    return True, None

  def is_build_mine_legal(self, player, move,
                          bonus_terraforming=0,
                          bonus_nav=0):
    desc = move.description

    if desc.coordinates is None:
      explanation = 'No hex selected'
      return False, explanation
    if not player.can_afford(player.building_costs['mine']):
      explanation = 'Cannot afford to build mine'
      return False, explanation
    if not player.buildsings['mine'] > 0:
      explanation = 'No mines left'
      return False, explanation

    xy = desc.coordinates
    b = self.game_state.buildings

    if xy not in self.game_state.board_configuration:
      explanation = 'There is no planet there'
      return False, explanation

    #handle lantids
    if xy in b and b[xy][0] != player and player.faction != 'Lantids':
      explanation = 'Another player has already built there'
      return False, explanation
    if (xy in b and b[xy][0] != player and player.faction == 'Lantids' and
        b[xy][1] == 'gaiaformer'):
      explanation = 'Lantids may not share gaiaformer'
      return False, explanation
    if xy in b and b[xy][0] != player and player.faction == 'Lantids':
      if bonus_terraforming == 0:
        return True, None
      else:
        explanation = 'Cannot use lantid share with terraforming abilities'
        return False, explanation

    #handle gaiaformer
    if xy in b and b[xy] == (player, 'gaiaformer'):
      return True, None

    if xy in b and b[xy][0] == player:
      explanation = 'You have already built there'
      return False, explanation

    if not player.can_terraform(
          self.game_state.get_terrain(desc.coordinates),
          self.game_state.tech_progress['terraforming'][player],
          bonus=bonus_terraforming):
      explanation = 'Cannot afford to terraform'
      return False, explanation

    if not self.game_state.in_navigation_range(player, xy, bonus=bonus_nav):
      explanation = 'Selected hex not in range'
      return False, explanation

    if (self.game_state.board_configuration[xy] == 'gaia' and
        not self.get_nav_cost + 1 >= player.qubit):
      explanation = 'Insufficient qubits for both gaia build and navigation'

    return True, None

  def is_gaiaform_legal(self, player, move, bonus_nav=0):
    desc = move.description

    if desc.coordinates is None:
      explanation = 'No hex selected'
      return False, explanation
    
    xy = desc.coordinates
    b = self.game_state.buildings

    if xy not in self.game_state.board_configuration:
      explanation = 'There is no planet there'
      return False, explanation

    if xy in b:
      explanation = 'Another player has already built there'
      return False, explanation
    if not self.game_state.get_terrain(xy) == 'transdim':
      explanation = 'Cannot start gaia project on non transdim world'
      return False, explanation
    if not player.buildings['gaiaformer'] > 0:
      explanation = 'No gaiaformers available'
      return False, explanation
    if self.game_state.tech_progress['gaiaforming'][player] == 0:
      explanation = 'Cannot start gaia project without gaiaforming research'
      return False, explanation
    if not player.can_gaiaform(
          self.game_state.tech_progress['gaiaforming'][player]):
      explanation = 'Not enough power to start gaia project'
      return False, explanation
    if not self.game_state.in_navigation_range(player, xy, bonus=bonus_nav):
      explanation = 'Selected hex not in range'
      return False, explanation
  
    return True, None

  def is_tech_tile_selection_legal(self, player, move):
    desc = move.description

    if desc.tech_tile_choice in player.tiles:
      explanation = 'Cannot take second copy of tech tile'
      return False, explanation
    
    if (desc.tech_tile_replace is not None and 
        type(desc.tech_tile_replace) == AdvancedTechTile):
      explanation = 'May only replace basic tech tile'
      return False, explanation

    if (type(desc.tech_tile_choice) == AdvancedTechTile and 
        len(list(filter(lambda tile: type(tile) == TechTile,
                        player.tiles))) == 0):
      explanation = 'Cannot pick advanced tech without replacement'
      return False, explanation

    if type(desc.tech_tile_choice) == AdvancedTechTile and player.keys == 0:
      explanation = 'Need fed to take advanced tech tile'
      return False, explanation

    if (len(list(filter(lambda tile: type(tile) == AdvancedTechTile and
                                     tile.replaced == desc.tech_tile_choice,
                        player.tiles))) > 0):
      explanation = 'You already have a copy of that tile but replaced it'
      return False, explanation

    if self.game_state.tech_progress[desc.tech_track][player] == 5:
      explanation = 'Tech track is already maxed'
      return False, explanation
        
    if (self.game_state.tech_progress[desc.tech_track][player] == 4 and
        player.keys == 0):
      explanation = "Need fed to advance tech to max"
      return False, explanation

    if (self.game_state.tech_progress[desc.tech_track][player] == 4 and
        type(desc.tech_tile_choice) == AdvancedTechTile and 
        player.keys < 2):
      explanation = "Need 2 feds to advance max and take advanced tech"
      return False, explanation

    return True, None

  def execute_move(self, player, move):
    desc = move.description    

    if desc.bonus_declined:
      return
    
    #ACTION 1
    if move.action_id == 'ACT1':
      self.execute_build_mine(player, move)

    #ACTION 2
    if move.action_id == 'ACT2':
      self.execute_gaiaform(player, move)

    #ACTION 3
    if move.action_id == 'ACT3':
      xy = desc.coordinates
      building_type = desc.upgrade
      cur_building_type = self.game_state.buildings[xy]

      player.execute_spend(player.building_costs[building_type])
      self.clayer.add_building(player, xy, building_type)

      if desc.tech_tile_choice is not None:
        self.execute_obtain_tech_tile(player, move)

      self.execute_when_build_effects(player, building_type)

      self.game_state.buildings[xy] = (player, building_type)

      self.player.buildings[cur_building_type] += 1
      self.player.bulidings[building_type] -= 1

    #ACTION 4
    if move.action_id == 'ACT4':
      pass

    #ACTION 5
    if move.action_id == 'ACT5':
      self.execute_techup(player, move) 

    #ACTION 6
    if move.action_id == 'ACT6':
      desc.power_action.description = desc
      self.execute_move(player, desc.power_action)

    #ACTION 7
    if move.action_id == 'ACT7':
      desc.special_action.description = desc
      self.execute_move(player, desc.special_action)

    #ACTION 8
    if move.action_id == 'ACT8':

      for tile in player.tiles:
        if type(tile) == BonusTile:
          cur_bonus = tile

      #handle changes in whenpass effects
      self.execute_whenpass_effects(player)

      if len(cur_bonus.whenpass) > 0:
        player.whenpass_effects.remove(cur_bonus.whenpass)
      
      self.game_state.bonus_tiles[bonus_tile] = player
      player.tiles.remove(cur_bonus)
      self.game_state.bonus_tiles[cur_bonus] = None
      player.tiles.append(bonus_tile)
      
      self.game_state.next_turn_order.append(player)
      self.game_state.turn_order.remove(player)

      self.execute_effect(player, bonus_tile.effect)

    #POWER ACTION 2
    if move.action_id == 'PA2':
      self.execute_build_mine(player, move, bonus_terraforming=2)

    #POWER ACTION 6, BONUS 4
    if move.action_id in ('PA6', 'BON4'):
      self.execute_build_mine(player, move, bonus_terraforming=1)

    #QUBIT ACTION 1
    if move.action_id == 'QA1':
      self.execute_obtain_tech_tile(player, move)

    #QUBIT ACTION 2
    if move.action_id == 'QA2':
      self.execute_effect(player, desc.federation_choice.effect)
      # do not give the player an extra key
      if desc.federation_choice.tile_id != 'FED1':
        player.key -= 1

    #SPEC IVIT
    if move.action_id == 'SPEC_IVIT':
      xy = desc.coordinates

      nav_cost = self.game_state.get_nav_cost(player, xy)
      player.execute_spend({'qubit' : nav_cost})
      self.clayer.add_orbital(player, xy, 'space_station')
      
      self.game_state.orbitals[xy] = (player, 'space_station')
      self.game_state.add_to_bordering_federations(player, xy)

      player.buildings['space station'] -= 1

    #SPEC FIRAK
    if move.action_id == 'SPEC_FIRAK':
      xy = desc.cooordinates

      self.game_state.buildings[xy] = (player, 'trading post')
      self.execute_when_build_effects(player, 'trading post')

      self.clayer.add_building(player, xy, 'trading post')

      player.buildings['research lab'] += 1
      player.buildings['trading post'] -= 1

    #SPEC BESCOD
    if move.action_id == 'SPEC_BESCOD':
      self.execute_techup(player, move)

    #SPEC AMBA
    if move.action_id == 'SPEC_AMBA':
      xy = desc.coordinates
      b = self.game_state.buildings

      #find PI
      for bxy in b:
        if b[bxy][0] != player:      
          continue
        if b[bxy][1] == 'planetary institute':
          xy_pi = bxy

      b[xy_pi] = 'mine'
      b[xy] = 'planetary institute'
    
      self.clayer.add_building(player, xy_pi, 'mine')
      self.clayer.add_building(player, xy, 'planetary institute')

    #BONUS 5
    if move.action_id == 'BON5':
      xy = desc.coordinates

      if self.game_state.board_configuration[xy] == 'transdim':
        self.execute_gaiaform(player, move, bonus_nav=3)
      else:
        self.execute_build_mine(player, move, bonus_nav=3)

    #TECHUP NAV5
    if move.action_id == 'TECHUP_NAV5':
      xy = desc.coordinates

      self.clayer.add_building(player, xy, 'lost planet')

      self.execute_when_build_effects(player, 'mine')
      self.game_state.add_to_bordering_federations(player, xy)
      self.recalculate_area_control_metrics(player, move)
  
  def execute_build_mine(self, player, move, bonus_terraforming=0, 
                                             bonus_nav=0):
    desc = move.description
    xy = desc.coordinates

    #handle lantids and gaiaformers
    if xy in self.game_state.buildings:
      terraform_cost = 0
      if self.game_state.buildings[xy][1] == 'gaiaformer':
        lantid_flag = False
      else:
        lantid_flag = True
        self.game_state.lantid_shares.append(xy)

    else:
      lantid_flag = False
      terraform_cost = player.cost_to_terraform(
            self.game_state.get_terrain(xy),
            self.game_state.tech_progress['terraforming'][player],
            bonus=bonus_terraforming)

    nav_cost = self.game_state.get_nav_cost(player, xy, bonus=bonus_nav)

    player.execute_spend(player.building_costs['mine'])
    player.execute_spend(terraform_cost)
    player.execute_spend({'qubit' : nav_cost})

    self.clayer.add_building(player, xy, 'mine', lantid_share=lantid_flag)

    player.buildings['mine'] -= 1

    #execute when effects
    self.execute_when_build_effects(player, 'mine')
    if self.game_state.board_configuration[xy] == 'gaia':
      self.execute_when_build_effects(player, 'gaia')
    else:
      shovels_needed = terrain_distance(self.game_state.get_terrain(xy),
                                        player.home_terrain)
      self.execute_when_terraform_effects(player, n_times=shovels_needed)

    self.recalculate_area_control_metrics(player, move)

    self.game_state.buildings[xy] = (player, 'mine')
    self.game_state.add_to_bordering_federations(player, xy)

  def execute_gaiaform(self, player, move, bonus_nav=0):
    desc = move.description
    xy = desc.coordinates

    gaiaform_cost = player.cost_to_gaiaform(
              self.game_state.tech_progress['gaiaforming'][player])

    nav_cost = self.game_state.get_nav_cost(player, xy, bonus=bonus_nav)

    player.buildings['gaiaformer'] -= 1

    player.execute_spend({'qubit' : nav_cost})
    player.execute_destroy_power(gaiaform_cost)

    self.game_state.buildings[xy] = (player, 'gaiaformer')
    self.clayer.add_building(player, xy, 'gaiaformer')

  def execute_obtain_tech_tile(self, player, move):
    desc = move.description    

    player.tiles.append(desc.tech_tile_choice)
    self.game_state.tech_progress[desc.tech_track][player] += 1
    
    if desc.tech_replace_choice is not None:
      desc.tech_tile_choice.replaced = desc.tech_replace_choice
      player.tiles.remove(desc.tech_replace_choice)

    self.execute_techup(player, move)

  def execute_techup(self, player, move):
    desc = move.description    

    tech_track = desc.tech_track
    tech_level = self.game_state.tech_progress[desc.tech_track][player] + 1

    execute_when_techup_effects(player)
     
    techup_action = TechupAction(tech_track=tech_track, tech_level=tech_level)

    if tech_track in ('economy', 'science') and 1 <= tech_level <= 4:
      assert(len(techup_action.effect.income) > 0)
      player.tech_income[desc.tech_track] = techup_action.effect.income

    self.execute_move(player, techup_action)

  def execute_effect(self, player, effect, n_times=1):
    if 'per' in effect.immediate:
      self.execute_per(player, effect.immediate['per'])

    self._execute_vp_and_resource_gains(player, effect.immediate, 
                                        n_times=n_times)

    if effect.when is not None:
      player.when_effects.append(effect)
    if effect.whenpass is not None:
      player.whenpss_effects.append(effect)

  def execute_pass_effect(self, player, n_times=1):
    for effect in player.whenpass_effects:
      assert(len(effect.whenpass) > 0) 
      assert('per' in effect.whenpass)
      self.execute_per(player, effect.whenpass['per'])

  def execute_when_build_effects(self, player, build_what='mine', n_times=1):
    for effect in player.when_effects:
      assert(len(effect.when) > 0)
      if 'build' in effect.when:
        for building in effect.when['build']:
          if build_what == building:
            gains = effect.when['build'][build_what]
            self._execute_vp_and_resource_gains(player, gains, n_times=n_times)

  def execute_when_terraform_effects(self, player, n_times=1):
    for effect in player.when_effects:
      assert(len(effect.when) > 0)
      if 'terraform' in effect.when: 
        gains = effect.when['terraform']
        self._execute_vp_and_resource_gains(player, gains, n_times=n_times)

  def execute_when_techup_effects(self, player, n_times=1):
    for effect in player.when_effects:
      assert(len(effect.when) > 0)
      if 'techup' in effect.when: 
        gains = effect.when['techup']
        self._execute_vp_and_resource_gains(player, gains, n_times=n_times)
    
  def execute_per(self, player, per):
    for per_what in per:
      if per_what == 'federation':
        n = 0#TODO
        pass
      elif per_what == 'mine':
        n = 8 - player.buildings['mine']
      elif per_what == 'trading post':
        n = 4 - player.buildings['trading post']
      elif per_what == 'research lab':
        n = 3 - player.buildings['research lab']
      elif per_what == 'sector':
        n = player.sectors
      elif per_what == 'planet type':
        n = player.planet_types
      elif per_what == 'gaia':
        n = self.game_state.get_num_gaias(player)

      gains = per[per_what]

      self._execute_vp_and_resource_gains(player, gains, n_times=n)
      
  def _execute_vp_and_resource_gains(self, player, gains, n_times=1):
      if 'VP' in gains:
        self.game_state.score[player] += gains['VP'] * n_times

      player.execute_gain(gains, n_times=n_times)
