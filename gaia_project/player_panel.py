import pygame

from traits.api import (HasPrivateTraits, Instance, Int)

class PlayerPanelRender(pygame.Surface):

  def __init__(self, width, height, player):
    self.width = width
    self.height = height

class PlayerPanel(HasPrivateTraits):
  
  render = Instance(PlayerPanelRender)

  player = Instance(Player)

  weight = Int
  height = Int
