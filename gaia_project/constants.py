import pygame

PLANET_COLOR_MAP = {'gaia' : pygame.Color( 51, 204, 51),
                    'volcanic' : pygame.Color( 255, 116, 0),
                    'oxide' : pygame.Color( 153, 0, 51),
                    'terra' : pygame.Color( 0, 153, 255),
                    'ice' : pygame.Color( 221, 221, 221),
                    'titanium' : pygame.Color( 122, 122, 122),
                    'swamp' : pygame.Color( 153, 102, 51),
                    'desert' : pygame.Color( 220, 170, 0),
                    'transdim' : pygame.Color( 140, 26, 225)}

TILE_1 = {(2,1) : 'swamp',
          (2,0) : 'desert',
          (3,3) : 'terra',
          (4,4) : 'transdim',
          (5,3) : 'volcanic',
          (5,2) : 'oxide'}

TILE_2 = {(1,1) : 'volcanic',
          (1,2) : 'titanium',
          (3,3) : 'ice',
          (3,1) : 'swamp',
          (4,4) : 'desert',
          (4,1) : 'oxide',
          (5,3) : 'transdim'}

TILE_3 = {(1,2) : 'transdim',
          (2,1) : 'gaia',
          (4,4) : 'titanium',
          (4,3) : 'ice',
          (4,1) : 'terra',
          (5,2) : 'desert'}

TILE_4 = {(1,2) : 'titanium',
          (2,2) : 'oxide',
          (2,0) : 'ice',
          (3,1) : 'volcanic',
          (4,3) : 'swamp',
          (5,4) : 'terra'}

TILE_5F = {(1,2) : 'ice',
           (2,1) : 'gaia',
           (3,4) : 'transdim',
           (4,4) : 'oxide',
           (4,1) : 'volcanic',
           (5,2) : 'desert'}

TILE_5B = {(1,2) : 'ice',
           (2,1) : 'gaia',
           (3,4) : 'transdim',
           (4,4) : 'oxide',
           (4,1) : 'volcanic'}

TILE_6F = {(2,3) : 'transdim',
           (2,1) : 'swamp',
           (3,3) : 'terra',
           (4,2) : 'gaia',
           (5,4) : 'desert',
           (5,3) : 'transdim'}

TILE_6B = {(2,3) : 'transdim',
           (3,3) : 'terra',
           (4,2) : 'gaia',
           (5,4) : 'desert',
           (5,3) : 'transdim'}

TILE_7F = {(1,0) : 'transdim',
           (2,2) : 'oxide',
           (2,3) : 'swamp',
           (3,1) : 'gaia',
           (4,3) : 'gaia',
           (5,2) : 'titanium'}

TILE_7B = {(1,0) : 'transdim',
           (2,2) : 'gaia',
           (3,1) : 'gaia',
           (4,3) : 'swamp',
           (5,2) : 'titanium'}

TILE_8 = {(1,2) : 'terra',
          (2,2) : 'ice',
          (3,4) : 'transdim',
          (3,1) : 'volcanic',
          (4,3) : 'titanium',
          (4,1) : 'transdim'}

TILE_9 = {(1,1) : 'volcanic',
          (2,3) : 'transdim',
          (3,4) : 'ice',
          (3,1) : 'titanium',
          (3,0) : 'swamp',
          (4,3) : 'gaia'}

TILE_10 = {(2,3) : 'transdim',
           (2,1) : 'desert',
           (3,4) : 'transdim',
           (3,0) : 'terra',
           (4,3) : 'gaia',
           (4,1) : 'oxide'}

BASIC_2P_SETUP = {(2,3) : TILE_1,
                  (4,0) : TILE_2,
                  (7,5) : TILE_3,
                  (9,2) : TILE_4,
                  (5,8) : TILE_5B,
                  (10,10) : TILE_6B,
                  (12,7) : TILE_7B}

BASIC_4P_SETUP = {(2,3) : TILE_10,
                  (4,0) : TILE_9,
                  (7,5) : TILE_2,
                  (9,2) : TILE_8,
                  (5,8) : TILE_1,
                  (10,10) : TILE_3,
                  (12,7) : TILE_4,
                  (8,13): TILE_5F,
                  (13,15) : TILE_6F,
                  (15,12) : TILE_7F}
