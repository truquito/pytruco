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

    