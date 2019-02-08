from .utils import GaiaProjectValidationError

def terrain_distance(a, b):
  terrains = {'terra' : 0,
              'oxide' : 1,
              'volcanic' : 2,
              'desert' : 3,
              'swamp' : 4,
              'titanium' : 5,
              'ice' : 6}

  if a not in terrains or b not in terrains:
    raise GaiaProjectValidationError('Cannot compare terrain distance')

  ai = terrains[a]
  bi = terrains[b]

  if (ai-bi)%7 > 3:
    return (bi-ai)%7
  else:
    return (ai-bi)%7
