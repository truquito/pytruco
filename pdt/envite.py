from __future__ import annotations
from typing import Dict

# from pdt import equipo
from enum import Enum
from .jugador import Jugador
from .manojo import Manojo

class EstadoEnvite(Enum):

  DESHABILITADO     = "deshabilitado"
  NOGRITADOAUNAUN      = "noCantadoAun"
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
  
  def __eq__(self, other) -> bool:
    return str(self) == str(other)
  
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
  
  def parse(ee:str) -> EstadoEnvite:
    if ee not in map(lambda x: str(x), [ 
        EstadoEnvite.DESHABILITADO, EstadoEnvite.NOGRITADOAUNAUN, 
        EstadoEnvite.ENVIDO, EstadoEnvite.REALENVIDO, EstadoEnvite.FALTAENVIDO, 
        EstadoEnvite.FLOR, EstadoEnvite.CONTRAFLOR, 
        EstadoEnvite.CONTRAFLORALRESTO ]):
      raise Exception("Estado envite invalido")
    
    return EstadoEnvite.DESHABILITADO if ee == EstadoEnvite.DESHABILITADO \
      else EstadoEnvite.NOGRITADOAUNAUN if ee == EstadoEnvite.NOGRITADOAUNAUN \
      else EstadoEnvite.ENVIDO if ee == EstadoEnvite.ENVIDO \
      else EstadoEnvite.REALENVIDO if ee == EstadoEnvite.REALENVIDO \
      else EstadoEnvite.FALTAENVIDO if ee == EstadoEnvite.FALTAENVIDO \
      else EstadoEnvite.FLOR if ee == EstadoEnvite.FLOR \
      else EstadoEnvite.CONTRAFLOR if ee == EstadoEnvite.CONTRAFLOR \
      else EstadoEnvite.CONTRAFLORALRESTO
  
class Envite():
  def __init__(self):
    self.estado              :EstadoEnvite = EstadoEnvite.NOGRITADOAUNAUN
    self.puntaje             :int          = 0
    self.cantado_por         :str          = ""
    self.jugadores_con_flor :list[Manojo] = None
    self.sin_cantar          :list[str]    = None # sin cantar "la flor"
  
  def to_dict(self) -> Dict[str, any]:
    return {
      "estado": str(self.estado),
      "puntaje": self.puntaje,
      "cantadoPor": self.cantado_por,
      # "jugadores_con_flor": self.jugadores_con_flor,
      "sinCantar": self.sin_cantar,
    }

  def no_canto_flor_aun(self, j:str) -> bool:
    return j in self.sin_cantar
  
  """Elimina a `j` de los jugadores que tienen pendiente cantar flor"""
  def canto_flor(self, j:str):
    # ix = self.sin_cantar.index(j)
    # del self.sin_cantar[ix]
    if j in self.sin_cantar:
      self.sin_cantar.remove(j)

    