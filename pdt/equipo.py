from enum import Enum

class Equipo(Enum):
  AZUL = "azul"
  ROJO = "rojo"

  def es_valido(e):
    return e in [Equipo.AZUL, Equipo.ROJO]

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)
  
  def __hash__(self) -> str:
    return 0 if self == Equipo.AZUL \
      else 1
  
  def __eq__(self, other) -> bool:
    return str(self) == str(other)