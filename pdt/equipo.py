from enum import Enum

class Equipo(str, Enum):
  AZUL = "azul"
  ROJO = "rojo"

  def es_valido(e):
    return e in [Equipo.AZUL, Equipo.ROJO]

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)