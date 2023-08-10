from __future__ import annotations
from typing import Dict
from enum import Enum

class EstadoTruco(Enum):

  NOGRITADOAUN   = "noGritadoAun"
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
  
  def __eq__(self, other) -> bool:
    return str(self) == str(other)
  
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
  
  def parse(et:str) -> EstadoTruco:
    if et not in map(lambda x: str(x), [ 
        EstadoTruco.NOGRITADOAUN, EstadoTruco.TRUCO, EstadoTruco.TRUCOQUERIDO, 
        EstadoTruco.RETRUCO, EstadoTruco.RETRUCOQUERIDO, EstadoTruco.VALE4, 
        EstadoTruco.VALE4QUERIDO ]):
      raise Exception("Estado Truco invalido")
    
    return EstadoTruco.NOGRITADOAUN if et == EstadoTruco.NOGRITADOAUN \
      else EstadoTruco.TRUCO if et == EstadoTruco.TRUCO \
      else EstadoTruco.TRUCOQUERIDO if et == EstadoTruco.TRUCOQUERIDO \
      else EstadoTruco.RETRUCO if et == EstadoTruco.RETRUCO \
      else EstadoTruco.RETRUCOQUERIDO if et == EstadoTruco.RETRUCOQUERIDO \
      else EstadoTruco.VALE4 if et == EstadoTruco.VALE4 \
      else EstadoTruco.VALE4QUERIDO

class Truco():
  def __init__(self):
    self.cantado_por :str         = ""
    self.estado      :EstadoTruco = EstadoTruco.NOGRITADOAUN
  
  def to_dict(self) -> Dict[str, any]:
    return {
      "cantadoPor": self.cantado_por,
      "estado": str(self.estado),
    }

    