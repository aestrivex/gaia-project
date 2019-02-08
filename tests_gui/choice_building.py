
from gaia_project.communication_layer import LocalCommunicationLayer
from gaia_project.engine import Engine
from gaia_project.move_action import PassiveCharge

from gaia_project.tile import TechTile, FederationTile

if __name__ == '__main__':

  cl = LocalCommunicationLayer()

  en = Engine(cl) 

  #cl.player_panels[cl.players[0]].show_choice('building_upgrade', None)

  #cl.players[0].tiles.append(TechTile('TECH9'))
  #cl.player_panels[cl.players[0]].show_choice('special_action', None)

  #cl.player_panels[cl.players[0]].show_choice('bonus_tile', None)

  #cl.players[0].tiles.append(FederationTile('FED2'))
  #cl.player_panels[cl.players[0]].show_choice('which_federation_owned', None)

  #cl.player_panels[cl.players[0]].show_choice('which_federation_supply', None)

  #cl.players[0].tiles.append(TechTile('TECH4'))
  #cl.player_panels[cl.players[0]].show_choice('tech_replace', None)

  #cl.player_panels[cl.players[0]].show_choice('coordinate', None)
  #cl.player_panels[cl.players[0]].show_choice('tech_tile', None)
  #cl.player_panels[cl.players[0]].show_choice('tech_track', None)
  #cl.player_panels[cl.players[0]].show_choice('power_action', None)
  cl.player_panels[cl.players[0]].show_choice('pass_gaia', None)

  en.run()
