# from pdt import equipo
from enum import Enum
from .jugador import Jugador
from .manojo import Manojo

class EstadoEnvite(str, Enum):

  DESHABILITADO     = "deshabilitado"
  NOCANTADOAUN      = "noCantadoAun"
  ENVIDO            = "envido"
  REALENVIDO        = "realEnvido"
  FALTAENVIDO       = "faltaEnvido"
  FLOR              = "flor"
  CONTRAFLOR        = "contraFlor"
  CONTRAFLORALRESTO = "contraFlorAlResto"

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)
  
  def __lt__(self, other: 'EstadoEnvite'):
    if self == other:
      return False
    # the following works because the order of elements in the definition is 
    # preserved
    for elem in EstadoEnvite:
      if self == elem:
        return True
      elif other == elem:
        return False
    raise RuntimeError('Bug: we should never arrive here')
  
  def __le__(self, other: 'EstadoEnvite'):
    return self < other or self == other
  
  # def to_ptr(self) -> int:
  #   return 33 if self == MyEnum.first_item \
  #     else 44 if self == MyEnum.whatever \
  #     else 55
  
class Envite():
  def __init__(self):
    self.estado              :EstadoEnvite = EstadoEnvite.NOCANTADOAUN
    self.puntaje             :int          = 0
    self.cantado_por         :str          = None
    self.juegadores_con_flor :list[Manojo] = None
    self.sin_cantar          :list[str]    = None # sin cantar "la flor"
  
  def no_canto_flor_aun(self, j:str) -> bool:
    return j in self.sin_cantar
  
  """Elimina a `j` de los jugadores que tienen pendiente cantar flor
  PRE:`j` se encuentra en la lista `sin_cantar`"""
  def canto_flor(self, j:str):
    # ix = self.sin_cantar.index(j)
    # del self.sin_cantar[ix]
    self.sin_cantar.remove(j)

    