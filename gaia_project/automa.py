from traits.api import (HasPrivateTraits, List, Instance, Enum, Int, Bool,
                        Range,
                       )

from .automa_card import AUTOMA_CARDS, FACTION_CARDS, AutomaCard
from .constants import TECH_ORDER, POWER_ACTIONS
from .move_action import AutomaAction, EventDescription

import numpy as np

class Automa(HasPrivateTraits):

  faction = Enum('Terrans', 'Itars', 'Firaks', 'Taklons', 'Xenos', 'Geodens',
                 'Hadsch Hallas')

  automa_difficulty_level = Enum('automa', 'automalein', 'automachtig',
                                 'ultoma', 'alptrauma')

  cards = List(Instance(AutomaCard))

  deck = List(Instance(AutomaCard)) 

  action_card = Instance(AutomaCard)
  support_card = Instance(AutomaCard)

  use_supports = Bool

  def __init__(self, automa_difficulty_level='automa', custom_cards=(), 
               *args, **kwargs):
    super().__init__()

    if custom_cards is not ():
      self.cards = custom_cards

    else:
      if automa_difficulty_level == 'automa':
        self.cards = [AUTOMA_CARDS[i] for i in (1, 2, 4, 5, 7, 13)]
      elif automa_difficulty_level == 'automalein':
        self.cards = [AUTOMA_CARDS[i] for i in (1, 4, 5, 7, 13)]
      elif automa_difficulty_level == 'automachtig':
        self.cards = [AUTOMA_CARDS[i] for i in (1, 2, 4, 5, 7, 9, 13)]
      elif automa_difficulty_level in ('ultoma', 'alptrauma'):
        self.cards = [AUTOMA_CARDS[i] for i in (1, 2, 4, 5, 7, 9, 13, 15)]

  def add_new_random_automa_card(self):
    current_card_ids = [card.card_id for card in self.cards]
    i = np.random.randint(17) + 1
    while i in current_card_ids:
      i = np.random.randint(17) + 1
    self.cards.append(AUTOMA_CARDS[i])

  def shuffle(self): 
    self.deck = self.cards.copy()
    np.random.shuffle(self.deck)

  def make_initial_placements(self):
    NotImplemented

  def setup_round(self):
    self.shuffle()
    self.support_card = self.deck.pop()
    self.action_card = self.deck.pop()

  def make_move(self, player, game_state):
    #determine if the automa is passing
    if self.determine_pass():
      automa_action = self.determine_pass_move(game_state)
    
    #determine the automa's action
    else:
      automa_action = self.determine_action(player, game_state)

    #take the VP
    action.automa_vp += self.action_card.vp

    #set up the next decision card
    self.support_card = self.action_card
    self.action_card = self.deck.pop()

    return automa_action

  def determine_pass(self):
    if len(self.deck) > 3: 
      return False
    if self.use_supports:
      return self.action_card.pass_check
    else:
      return np.random.rand() > .5294

  def determine_pass_move(self, game_state):
    #get the tile
    available_tiles = self.game_state.get_available_bonus_tiles()
    #TODO implement the support card exactly
    #tracking the order the cards came in is hard and unnecessary
    #probably just brute force the automa to make a random decision is best
    tile = np.random.choice(available_tiles)

    return AutomaAction(automa_pass=True,
                        description=EventDescription(bonus_tile=tile))

  def determine_action(self, player, game_state):

    if self.action_card.action == 'advance_highest':
      return self.do_advance_highest(player, game_state)

    elif self.action_card.action == 'advance_random':
      return self.do_advance_random(player, game_state)

    elif self.action_card.action == 'power_or_qic_action':
      return self.do_power_action(game_state,
                                  repeat=(self.faction=='Xenos'))

    elif self.action_card.action == 'build':
      return self.do_build_mine(player, game_state)
      #geodens have a special

    elif self.action_card.action == 'upgrade':
      return self.do_upgrade_building(player, game_state)

    elif self.action_card.action == 'faction_action':
      if self.faction == 'Itars':
        move = self.do_power_action(game_state, repeat=True)
        move.automa_vp += 4
      elif self.faction == 'Taklons':
        move = self.do_build_mine(player, game_state, nav_override=3,
                             faction_tiebreaker='closest')
        move.second_action = self.do_power_action(game_state).description
        move.automa_vp += 2
      elif self.faction == 'Terrans':
        move = self.do_build_mine(player, game_state, nav_override=4,
                             faction_tiebreaker='transdim')
        move.second_action = self.do_advance_gaia().desscription
        move.automa_vp += 2
      elif self.faction == 'Xenos':
        move = self.do_build_mine(player, game_state, nav_override=2)
        move.second_action = self.do_power_action(game_state).description
        move.automa_vp += 2
      elif self.faction == 'Hadsch Hallas':
        move = self.do_upgrade_building(player, game_state)
        move.automa_vp += 1
      elif self.faction == 'Firaks':
        priority_list = [{'research lab' : 'trading post'},
                         {'trading post' : 'planetary institute'},
                         {'mine' : 'trading post'},
                         {'research lab' : 'action academy'},
                         {'research lab' : 'knowledge academy'},
                         {'trading post' : 'research lab'}]
  
        move = self.do_upgrade_building(player, game_state, priority_list)
        if move.do_nothing:
          move = self.do_build_mine(player, game_state, nav_override=3)
        move.automa_vp += 2
      elif self.faction == 'Geodens':
        move = self.do_advance_random(player, game_state)
        move.second_action = self.do_power_action(game_state).description
        move.automa_vp += 1 

      return move

  def do_advance_highest(self, player, game_state):
    eligible_tracks = game_state.get_highest_track(player)
    return self._advance_tech(eligible_tracks)

  def do_advance_random(self, player, game_state):
    eligible_tracks = game_state.get_nonmaxed_tracks(player)
    return self._advance_tech(eligible_tracks)

  def do_advance_gaia(self):
    eligible_tracks = ['gaiaforming']
    return self._advance_tech(eligible_tracks)

  def _check_eligible_at_level_4(self, candidate_tracks):
    for track in candidate_tracks:
      if self.game_state.tech_progress[track][player] == 4:
        #check if the advanced tile is available
        track_ix = TECH_ORDER.index(track)
        if self.game_state.advanced_tech_tiles[track_ix].available:
          continue
        else:
        #check if level 5 is available
          if self.game_state.is_track_maxed_by_somebody(track):
            candidate_tracks.remove(track)
    return

  def _advance_tech(self, eligible_tracks):
    self._check_eligible_at_level_4(eligible_tracks)

    if len(eligible_tracks) == 0:
      return AutomaAction(do_nothing=True)

    track = self.numbered_selection(eligible_tracks)

    take_adv_tile_instead = False
    if self.game_state.tech_progress[track][player] == 4:
      track_ix = TECH_ORDER.index(track)
      tile = self.game_state.advanced_tech_tiles[track_ix]
      if tile.available: 
        return AutomaAction(description=EventDescription(tech_tile_choice=tile))
    
    return AutomaAction(description=EventDescription(tech_track=track))

  def do_power_action(self, game_state, repeat=False):
    eligible_actions = filter(lambda a:a.available,
                              game_state.power_actions_available)

    if len(eligible_actions) == 0:
      return AutomaAction(do_nothing=True)

    action = self.numbered_selection(eligible_actions)
    move = AutomaAction(description(power_action=action))

    if repeat:
      #repeat this action
      eligible_actions.remove(action)

      if len(elgibile_actions) == 0:
        return move

      second_action = self.numbered_selection(eligible_actions)
      move.second_action = EventDescription(power_action=second_action)

    return move

  def do_upgrade_building(self, player, game_state,
          priority_list=[{'trading post' : 'planetary institute'},
                         {'mine' : 'trading post'},
                         {'research lab' : 'action academy'},
                         {'research lab' : 'knowledge academy'},
                         {'trading post' : 'research lab'}]):
    any_valid_upgrade_found = False
    for i in priority_list:
      upgrade_from, upgrade_to = i.items()
      if player.buildings[upgrade_to] == 0:
        continue
      froms = self.game_state.get_all_buildings_of_type_from_player(player, 
                                                                   upgrade_from)
      if len(froms) == 0:
        continue
      any_valid_upgrade_found = True
      break

    if not any_valid_upgrade_found:
      return AutomaAction(do_nothing=True)

    #we decided what type to upgrade, now pick one
    #tiebreak #1 closest to your planets
    min_dist = np.inf
    for loc in froms:
      dist = self.min_distance_to_any_other_player(player, loc)
      if dist < min_dist:
        min_dist = dist
        candidates = [loc]
      if dist == min_dist:
        candidates.append(loc)
      
    #tiebreak #2 directional selection
    loc = self.directional_selection(candidates)

    upgrade_action = AutomaAction(
      description=EventDescription(coordinates=loc, upgrade=upgrade_to))

    if self.faction == 'Hadsch Hallas' and upgrade_to == 'trading post':
      upgrade_action.automa_vp += 3

    if self.faction == 'Firaks' and upgrade_to == 'research lab':
      eligible_tracks = game_state.get_nonmaxed_tracks(player)
      adv_tech_action = self._advance_tech(eligible_tracks)
      upgrade_action.merge_input(adv_tech_action.description)

    return upgrade_action

  def do_build_mine(self, player, game_state, nav_override=None,
                    faction_tiebreaker=None):
    #determine if the automa has mines
    if player.buildings['mine'] == 0:
      return self.do_upgrade_building(player, game_state)
    #determine eligible locations
    empty_planets = game_state.get_empty_planets()
    if nav_override is not None:
      nav = nav_override
    else:
      nav = self.support_card.support_range

    eligible_planets = []
    for planet in empty_planets:
      if game_state.in_literal_range(player, planet, nav):
        eligible_planets.append(planet)

    if len(eligible_planets) == 0:
      return self.do_upgrade_building(player, game_state)

    #faction tiebreaker
    if faction_tiebreaker == 'transdim':
      for planet in eligible_planets:
        if game_state.get_terrain(planet) != 'transdim':
          eligible_planets.remove(planet)
    elif faction_tiebreaker == 'closest':
      eligible_planets = self._closest_planet_tiebreaker(eligible_planets,
                                                         player, game_state)

    #final scoring tiebreaker
    #determine which final scoring tile to use, if any
    if self.use_supports: 
      if self.support_card.support_endgame_scoring == 'neither':
        final_scoring_tile = None
      elif self.support_card.support_endgame_scoring == 'top':
        final_scoring_tile = game_state.final_scoring_tiles[0]
      elif self.support_card.support_endgame_scoring == 'bottom':
        final_scoring_tile = game_state.final_scoring_tiles[1]
    else:
      if np.random.rand() < .12:
        final_scoring_tile = None
      elif np.random.rand() > .5:
        final_scoring_tile = game_state.final_scoring_tiles[0]
      else:
        final_scoring_tile = game_state.final_scoring_tiles[1]

    #use the relevant final scoring tiles
    if final_scoring_tile is None:
      pass
    elif final_scoring_tile.tile_id in ('FS1', 'FS2', 'FS6'):
      pass
    elif final_scoring_tile.tile_id == 'FS3':
      eligible_planets = self._most_planet_types_tiebreaker(eligible_planets,
                                                            player, game_state)
    elif final_scoring_tile.tile_id == 'FS4':
      eligible_planets = self._most_gaia_planets_tiebreaker(eligible_planets,
                                                            game_state)
    elif final_scoring_tile.tile_id == 'FS5':
      eligible_planets = self._most_sectors_tiebreaker(eligible_planets,
                                                       player, game_state)
      
    #least terraforming tiebreaker
    eligible_planets = self._least_terraforming_tiebreaker(eligible_planets,
                                                           player, game_state)

    #closest planet tiebreaker
    eligible_planets = self._closest_planet_tiebreaker(eligible_planets,
                                                       player, game_state)

    #directional selection
    loc = self.directional_selection(eligible_planets)

    return AutomaAction(description=EventDescription(cooordinates=loc))

  def _least_terraforming_tiebreaker(self, eligibles, player, game_state):
    distances = {0: [], 1: [], 2: [], 3: []}
    for planet in eligibles:
      terrain = game_state.get_terrain(planet)
      terraform_dist = automa_terraform_distance(player.home_terrain, terrain)
      distances[terraform_dist].append(planet)
    if len(distances[0] > 0):
      return distances[0]
    elif len(distances[1] > 0):
      return distances[1]
    elif len(distances[2] > 0):
      return distances[2]
    elif len(distances[3] > 0):
      return distances[3]

  def _most_sectors_tiebreaker(self, eligibles, player, game_state):
    sectors_owned = set()
    for sector in game_state.sectors:
      for loc in game_state.sectors[sector]:
        if loc in game_state.buildings:
          if game_state.buildings[loc][0] == player:
            sectors_owned.add(sector)
            break
    new_eligibles = eligibles.copy()
    for planet in eligibles:
      for sector in sectors_owned:
        if game_state.is_loc_in_sector(planet, sector):
          new_eligibles.remove(planet)
          break
    if len(new_eligibles) > 0:
      return new_eligibles
    return eligibles

  def _most_gaia_planets_tiebreaker(self, eligibles, game_state):
    new_eligibles = []
    for planet in eligibles:
      if game_state.get_terrain(planet) in ('gaia', 'transdim'):
        new_eligibles.append(planet)
    if len(new_eligibles) > 0:
      return new_eligibles
    return eligibles

  def _most_planet_types_tiebreaker(self, eligibles, player, game_state):      
    planet_types_owned = set()
    for building in game_state.buildings:
      if game_state.buildings[building][0] == player:
        planet_type = game_state.board_configuration[building]
        if planet_type not in planet_types_owned:
          planet_types_owned.add(planet_type)
    new_eligibles = []
    for planet in eligibles:
      if game_state.get_terrain(planet) not in planet_types_owned:
        new_eligibles.append(planet)
    if len(new_eligibles) > 0:
      return new_eligibles
    return eligibles

  def _closest_planet_tiebreaker(self, eligibles, player, game_state):
    min_dist = np.inf
    for planet in eligibles:
      dist = game_state.min_distance_to_any_other_player(player, planet)
      if dist < min_dist:
        min_dist = dist
        new_eligibles = [planet]
      elif dist == min_dist:
        new_eligibles.append(planet)
    return new_eligibles

  def numbered_selection(self, eligibles):
    if not self.use_supports:
      return np.random.choice(eligibles)

    d = self.support_numbered_selection_direction
    n = self.support_numbered_selection_number
    if d == 'right':
      return eligibles[(n-1)%len(eligibles)]
    else:
      return eligibles[(-n)%len(eligibles)]

  def directional_selection(self, eligibles):
    #TODO implement directional selection as on the cards
    return np.random.choice(eligibles)
