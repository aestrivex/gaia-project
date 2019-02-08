import pygame
import pygame.freetype
import logging

class GaiaProjectUIError(ValueError):
  pass

class GaiaProjectValidationError(ValueError):
  pass

def text(surface, msg, x_pos, y_pos, box_size_x, box_size_y, 
         font_size=14, color=pygame.Color('black')):
  lines = msg.split('\n') 
  f = pygame.freetype.SysFont(pygame.freetype.get_default_font(), font_size)

  line_spacing = f.get_sized_height() + 2
  x, y = 1, 2

    
  space_w = f.get_rect(' ').width
  for i,line in enumerate(lines):
    words = line.split(' ')

    for word in words:

      bounds = f.get_rect(word)
      while x + bounds.width >= box_size_x - 1:
        x = 1
        y += line_spacing
        if y + line_spacing >= box_size_y:
          errmsg = 'Tile "{0}" too big to show on board size {1}x{2}'.format(
                      msg, surface.width, surface.height)
          logging.info(errmsg)
          raise GaiaProjectUIError(errmsg)    

      f.render_to(surface, (x_pos+x, y_pos+y), None, color)
      x += bounds.width + space_w

    x = 1
    y += line_spacing

def text_size(font_size=14):
  f = pygame.freetype.SysFont(pygame.freetype.get_default_font(), font_size)
  return f.get_sized_height() + 2
