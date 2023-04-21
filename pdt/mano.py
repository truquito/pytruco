from __future__ import annotations
from enum import Enum
from .carta import Carta

class Resultado(Enum):
  GANO_ROJO = "ganoRojo"
  GANO_AZUL = "ganoAzul"
  EMPARDADA = "empardada"

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)
  
  def parse(r:str) -> Resultado:
    if r not in map(lambda x: str(x), 
      [Resultado.GANO_ROJO,Resultado.GANO_AZUL,Resultado.EMPARDADA]):
      raise Exception("Resultado invalido")

    return Resultado.GANO_ROJO if r == Resultado.GANO_ROJO \
      else Resultado.GANO_AZUL if r == Resultado.GANO_AZUL \
      else Resultado.EMPARDADA
  
class NumMano(Enum):
  PRIMERA = "primera"
  SEGUNDA = "segunda"
  TERCERA = "tercera"

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)
  
  def __eq__(self, other) -> bool:
    return str(self) == str(other)
  
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
  
  def to_ix(self) -> int:
    return 0 if self == NumMano.PRIMERA \
      else 1 if self == NumMano.SEGUNDA \
      else 2
  
  def inc(nm:NumMano) -> NumMano:
    return NumMano.SEGUNDA if nm == NumMano.PRIMERA else NumMano.TERCERA
  
  # deberia de usarse este, pero en la version Go, el numMano era codificado en
  # JSON como 0, 1 y 2. Por eso no se usa.
  def parse(nm:str) -> NumMano:
    if nm not in map(lambda x: str(x), 
      [NumMano.PRIMERA,NumMano.SEGUNDA,NumMano.TERCERA]):
      raise Exception("Palo invalido")

    return NumMano.PRIMERA if nm == NumMano.PRIMERA \
      else NumMano.SEGUNDA if nm == NumMano.SEGUNDA \
      else NumMano.TERCERA
    
  def parse_int(nm:int) -> NumMano:
    if not 0 <= nm <= 2: raise Exception("Palo invalido")
    return NumMano.PRIMERA if nm == 0 \
      else NumMano.SEGUNDA if nm == 1 \
      else NumMano.TERCERA

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
  
  