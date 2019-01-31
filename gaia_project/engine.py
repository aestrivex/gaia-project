from traits.api import (HasPrivateTraits, Instance, List)

from .player import Player

class Engine(HasPrivateTraits):

  clayer = Instance(CommunicationLayer)

  turn_order = List(Instance(Player))

  def run(self):

    while True:

      for player in self.turn_order:
        clayer.make_move(player)

        #validate move and do things
        
