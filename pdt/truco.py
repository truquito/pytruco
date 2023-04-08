from __future__ import annotations
from enum import Enum
from .jugador import Jugador

class EstadoTruco(Enum):

  NOCANTADO      = "noCantado"
  TRUCO          = "truco"
  TRUCOQUERIDO   = "trucoQuerido"
  RETRUCO        = "reTruco"
  RETRUCOQUERIDO = "reTrucoQuerido"
  VALE4          = "vale4"
  VALE4QUERIDO   = "vale4Querido"

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)
  
  def __lt__(self, other: 'EstadoTruco'):
    if self == other:
      return False
    # the following works because the order of elements in the definition is 
    # preserved
    for elem in EstadoTruco:
      if self == elem:
        return True
      elif other == elem:
        return False
    raise RuntimeError('Bug: we should never arrive here')
  
  def __le__(self, other: 'EstadoTruco'):
    return self < other or self == other
  
  def es_truco_respondible(e:EstadoTruco) -> bool:
    return e in [EstadoTruco.TRUCO, EstadoTruco.RETRUCO, EstadoTruco.VALE4]

class Truco():
  def __init__(self):
    self.cantado_por :str         = ""
    self.estado      :EstadoTruco = EstadoTruco.NOCANTADO

    