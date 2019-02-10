import pygame
from .move_action import PowerAction

PLANET_COLOR_MAP = {'gaia' : pygame.Color( 51, 204, 51),
                    'volcanic' : pygame.Color( 255, 116, 0),
                    'oxide' : pygame.Color( 153, 0, 51),
                    'terra' : pygame.Color( 0, 153, 255),
                    'ice' : pygame.Color( 221, 221, 221),
                    'titanium' : pygame.Color( 122, 122, 122),
                    'swamp' : pygame.Color( 153, 102, 51),
                    'desert' : pygame.Color( 220, 170, 0),
                    'transdim' : pygame.Color( 140, 26, 225),
                    'lost planet' : pygame.Color( 120, 120, 255)}

COMPONENT_COLOR_MAP = {
                      'orange' : pygame.Color( 255, 116, 0),
                      'red' : pygame.Color( 153, 0, 51),
                      'blue' : pygame.Color( 0, 153, 255),
                      'white' : pygame.Color( 221, 221, 221),
                      'gray' : pygame.Color( 122, 122, 122),
                      'brown' : pygame.Color( 153, 102, 51),
                      'yellow' : pygame.Color( 220, 170, 0),
                      'space station' : pygame.Color(185, 146, 9),
                      }

TECH_BOARD_COLOR_MAP = {
                        'terraforming' : pygame.Color( 179, 89, 0 ),
                        'navigation' : pygame.Color( 55, 121, 242 ),
                        'AI' : pygame.Color( 0, 165, 0),
                        'gaiaforming' : pygame.Color(153, 51, 255),
                        'economy' : pygame.Color(255, 128, 128),
                        'science' : pygame.Color(0, 200, 200),
                        'power action' : pygame.Color(115, 0, 115),
                        'qubit action' : pygame.Color(0, 115, 0),
                        'action used' : pygame.Color(240, 0, 0),
                        'gray' : pygame.Color(130, 130, 130),
                        'button' : pygame.Color(85, 85, 85),
                       }

POWER_ACTIONS = (PowerAction('PA1'), PowerAction('PA2'), PowerAction('PA3'),
                 PowerAction('PA4'), PowerAction('PA5'), PowerAction('PA6'),
                 PowerAction('PA7'), PowerAction('QA1'), PowerAction('QA2'),
                 PowerAction('QA3'))

TECH_ORDER=('terraforming', 'navigation', 'AI',
            'gaiaforming', 'economy', 'science')

STARTING_TECHS = {'Terrans' : 'gaiaforming',
                  'Xenos' : 'AI',
                  'Gleens' : 'navigation',
                  'Ambas' : 'navigation',
                  'Hadsch Hallas' : 'economy',
                  'Bal Taks' : 'gaiaforming',
                  'Geodens' : 'terraforming',
                  'Nevlas' : 'science'
                 }
      
TECH_BOARD_LONG_DESCS = {
                     (1, 0) : 'navigation range is 4, place lost planet',
                     (2, 0) : 'gain 4 QICs immediately',
                     (3, 0) : 'gain 3VP and +1VP per gaia immediately',
                     (4, 0) : ('gain 3 ore and 6 coin and charge 6 power '
                               'immediately'),
                     (5, 0) : 'gain 9 knowledge immediately',

                     (0, 2) : 'gain 2 ore immediately',
                     (1, 2) : 'navigation range is 3',
                     (2, 2) : 'gain 2 QICs immediately',
                     (3, 2) : ('gaia project costs 3 power tokens, unlock '
                               '3rd gaiaformer'),
                     (4, 2) : ('2 ore income, 4 coin income, 4 charge power '
                               'income'),
                     (5, 2) : '4 knowledge income',

                     (0, 3) : ('terraforming costs 1 ore, charge 3 power '
                               'immediately'),
                     (1, 3) : 'gain 1 QIC and charge 3 power immediately',
                     (2, 3) : 'gain 2 QICs and charge 3 power immediately',
                     (3, 3) : ('gaia project costs 4 power tokens, unlock '
                               '2nd gaiaformer, charge 3 power immediately'),
                     (4, 3) : ('1 ore income, 3 coin income, 3 charge power '
                               'income and charge 3 power immediately'),
                     (5, 3) : ('3 knowledge income and charge 3 power' 
                               'immediately'),

                     (0, 4) : 'terraforming costs 2 ore',
                     (1, 4) : 'navigation range is 2',
                     (2, 4) : 'gain 1 QIC immediately',
                     (3, 4) : 'gain 3 new power tokens immediately',
                     (4, 4) : ('1 ore income, 2 coin income, 2 charge power '
                               'income'),
                     (5, 4) : '2 knowledge income',

                     (0, 5) : 'gain 2 ore immediately',
                     (1, 5) : 'gain 1 QIC immediately',
                     (2, 5) : 'gain 1 QIC immediately',
                     (3, 5) : ('gaia project costs 6 power tokens, unlock '
                               '1st gaiaformer'),
                     (4, 5) : '2 coin income, 1 charge power income',
                     (5, 5) : '1 knowedge income',

                     (0, 6) : 'terraforming costs 3 core',
                     (1, 6) : 'navigation range is 1',
                     (2, 6) : 'no effect',
                     (3, 6) : 'cannot initiate gaia project',
                     (4, 6) : 'no effect',
                     (5, 6) : 'no effect',
                      
                   }

TECH_BOARD_DESCS = {
                     (1, 0) : 'range=4, lost planet',
                     (2, 0) : '+4Q',
                     (3, 0) : '+3VP +1VP per gaia',
                     (4, 0) : '+3o +6C +6pw',
                     (5, 0) : '+9K',

                     (0, 2) : '+2o',
                     (1, 2) : 'range=3',
                     (2, 2) : '+2Q',
                     (3, 2) : 'gaiaform=3pt',
                     (4, 2) : 'i: 2o, 4C, 4pw',
                     (5, 2) : 'i: 4K',

                     (0, 3) : 'dig=1o, +3pw',
                     (1, 3) : '+1Q, +3pw',
                     (2, 3) : '+2Q, +3pw',
                     (3, 3) : 'gaiaform=4pt, +3pw',
                     (4, 3) : 'i: 1o, 3C, 3pw, +3pw',
                     (5, 3) : 'i: 3K, +3pw',

                     (0, 4) : 'dig=2o',
                     (1, 4) : 'range=2',
                     (2, 4) : '+1Q', 
                     (3, 4) : '+3pt',
                     (4, 4) : 'i: 1o, 2C, 2pw',
                     (5, 4) : 'i : 2K',

                     (0, 5) : '+2o',
                     (1, 5) : '+1Q',
                     (2, 5) : '+1Q',
                     (3, 5) : 'gaiaform=6pt',
                     (4, 5) : 'i : 2C, 1pw',
                     (5, 5) : 'i : 1K',

                     (0, 6) : '',
                     (1, 6) : '',
                     (2, 6) : '',
                     (3, 6) : '',
                     (4, 6) : '',
                     (5, 6) : '',
                   }

TECH_LEVEL_TO_IDX = {0:6, 1:5, 2:4, 3:3, 4:2, 5:0}

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

INCOME_CHART = {
                'Terrans' : 
                   {'base' : ({'ore' : 1, 'knowledge' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 1},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Lantids' : 
                   {'base' : ({'ore' : 1, 'knowledge' : 1}),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Nevlas' :
                   {'base' : ({'ore' : 1, 'knowledge' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 1},),
                    'research lab' : ({'charge' : 2}, {'charge' : 2},
                                      {'charge' : 2}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Itars' : 
                   {'base' : ({'ore' : 1, 'knowledge' : 1, 
                                    'power token' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 1},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 3},)},
                'Bescods' : 
                   {'base' : ({'ore' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}, {'knowledge' : 1}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 2},),
                    'research lab' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 5}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Firaks' : 
                   {'base' : ({'ore' : 1, 'knowledge' : 2},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 1},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Ambas' : 
                   {'base' : ({'ore' : 2, 'knowledge' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 2},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Taklons' :
                   {'base' : ({'ore' : 1, 'knowledge' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 1},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Gleens' : 
                   {'base' : ({'ore' : 1, 'knowledge' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'ore' : 1},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Xenos' : 
                   {'base' : ({'ore' : 1, 'knowledge' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'qubit' : 1},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Geodens' : 
                   {'base' : ({'ore' : 1, 'knowledge' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 1},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Bal Taks' : 
                   {'base' : ({'ore' : 1, 'knowledge' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 1},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Hadsch Hallas' : 
                   {'base' : ({'ore' : 1, 'knowledge' : 1, 'coin' : 3},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 1},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
                'Ivits' : 
                   {'base' : ({'ore' : 1, 'knowledge' : 1, 'qubit' : 1},),
                    'mine' : ({'ore' : 1}, {'ore' : 1}, {}, {'ore' : 1},
                              {'ore' : 1}, {'ore' : 1}, {'ore' : 1}, 
                              {'ore' : 1}),
                    'trading post' : ({'coin' : 3}, {'coin' : 4}, {'coin' : 4},
                                      {'coin' : 5}),
                    'planetary institute' : ({'charge' : 4, 
                                              'power token' : 1},),
                    'research lab' : ({'knowledge' : 1}, {'knowledge' : 1},
                                      {'knowledge' : 1}),
                    'knowledge academy' : ({'knowledge' : 2},)},
               }

          

STARTING_POWER = {'Terrans' : {'gaia' : 0, '1' : 4, '2' : 4, '3' : 0},
                  'Lantids' : {'gaia' : 0, '1' : 4, '2' : 0, '3' : 0},
                  'Nevlas' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0},
                  'Itars' : {'gaia' : 0, '1' : 4, '2' : 4, '3' : 0},
                  'Bescods' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0},
                  'Firaks' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0},
                  'Ambas' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0},
                  'Taklons' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0, 
                               'brainstone' : 1},
                  'Gleens' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0},
                  'Xenos' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0},
                  'Geodens' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0},
                  'Bal Taks' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0},
                  'Hadsch Hallas' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0},
                  'Ivits' : {'gaia' : 0, '1' : 2, '2' : 4, '3' : 0},
                  }

STARTING_RESOURCES = {
          #the gleens, geodens, and xenos bonus resources from technology
          #are included here
          'Terrans' : {'coin' : 15, 'knowledge' : 3, 'ore' : 4, 'qubit' : 1},
          'Lantids' : {'coin' : 13, 'knowledge' : 3, 'ore' : 4, 'qubit' : 1},
          'Nevlas' : {'coin' : 15, 'knowledge' : 2, 'ore' : 4, 'qubit' : 1},
          'Itars' : {'coin' : 15, 'knowledge' : 3, 'ore' : 5, 'qubit' : 1},
          'Bescods' : {'coin' : 15, 'knowledge' : 1, 'ore' : 4, 'qubit' : 1},
          'Firaks' : {'coin' : 15, 'knowledge' : 2, 'ore' : 3, 'qubit' : 1},
          'Ambas' : {'coin' : 15, 'knowledge' : 3, 'ore' : 4, 'qubit' : 1},
          'Taklons' : {'coin' : 15, 'knowledge' : 3, 'ore' : 4, 'qubit' : 1},
          'Gleens' : {'coin' : 15, 'knowledge' : 3, 'ore' : 5},
          'Xenos' : {'coin' : 15, 'knowledge' : 3, 'ore' : 4, 'qubit' : 2},
          'Geodens' : {'coin' : 15, 'knowledge' : 3, 'ore' : 6, 'qubit' : 1},
          'Bal Taks' : {'coin' : 15, 'knowledge' : 3, 'ore' : 4, 'qubit' : 1},
          'Hadsch Hallas' : {'coin' : 15, 'knowledge' : 3, 'ore' : 4, 
                             'qubit' : 1},
          'Ivits' : {'coin' : 15, 'knowledge' : 3, 'ore' : 4, 'qubit' : 1},
                     }

BUILDING_COSTS = {'mine' : {'coin' : 2, 'ore' : 1},
                  'rural trading post' : {'coin' : 6, 'ore' : 2},
                  'urban trading post' : {'coin' : 3, 'ore' : 2},
                  'planetary institute' : {'coin' : 6, 'ore' : 4},
                  'research lab' : {'coin' : 5, 'ore' : 3},
                  'academy' : {'coin' : 6, 'ore' : 6}
                 }

BUILDING_HEIGHTS = {'mine' : 1,
                    'trading post' : 2,
                    'planetary institute' : 3,
                    'research lab' : 2,
                    'academy' : 1,
                    'space station' : 1}

BUILDING_PATHS = {
                  'normal' : {'mine' : (('trading post'),),
                              'trading post' : ('planetary institute',
                                                     'research lab'),
                              'research lab' : (('academy'),)
                             },
                  'bescods' : {'mine' : (('trading post'),),
                               'trading post' : ('academy',
                                                      'research lab'),
                               'research lab' : (('planetary institute'),)
                              }
                 }
