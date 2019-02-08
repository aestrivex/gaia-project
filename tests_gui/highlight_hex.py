
from gaia_project.communication_layer import LocalCommunicationLayer
from gaia_project.engine import Engine


if __name__ == '__main__':

  cl = LocalCommunicationLayer()

  en = Engine(cl) 

  cl.board.highlight_hex((6,6))
  cl.update_gfx()

  en.run()
