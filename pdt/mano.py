from __future__ import annotations
from enum import Enum
from .carta import Carta

class Resultado(str, Enum):
  GANO_ROJO = "ganoRojo"
  GANO_AZUL = "ganoAzul"
  EMPARDADA = "empardada"

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)
  
class NumMano(str, Enum):
  PRIMERA = "primera"
  SEGUNDA = "segunda"
  TERCERA = "tercera"

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)
  
  def __lt__(self, other: 'NumMano'):
    if self == other:
      return False
    # the following works because the order of elements in the definition is 
    # preserved
    for elem in NumMano:
      if self == elem:
        return True
      elif other == elem:
        return False
    raise RuntimeError('Bug: we should never arrive here')
  
  def __le__(self, other: 'NumMano'):
    return self < other or self == other
  
  def to_int(nm:NumMano) -> int:
    return 1 if nm == NumMano.PRIMERA \
      else 2 if nm == NumMano.SEGUNDA \
      else 3
  
  def inc(nm:NumMano) -> NumMano:
    return NumMano.SEGUNDA if nm == NumMano.PRIMERA else NumMano.TERCERA

class CartaTirada():
  def __init__(self, jugador:str, carta:Carta):
    self.jugador :str   = jugador
    self.carta   :Carta = carta

class Mano():
  def __init__(self):
    self.resultado      :Resultado         = None
    self.ganador        :str               = ""
    self.cartas_tiradas :list[CartaTirada] = []
  
  def agregar_tirada(self, c:CartaTirada):
    self.cartas_tiradas += [c]
  
  