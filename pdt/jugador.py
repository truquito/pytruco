from typing import Dict

# from pdt import equipo
from .equipo import Equipo

class Jugador():
  def __init__(self, id:str, equipo: Equipo):
    if not Equipo.es_valido(equipo):
      raise Exception("Equipo invalido")

    self.id     = id
    self.equipo = equipo
  
  def __dict__(self) -> Dict[str, any]:
    return {
      "id": self.id,
      "equipo": str(self.equipo),
    }
  def __str__(self) -> str:
    return f"{self.id}"

  def __repr__(self) -> str:
    return str(self)
  
  def GetEquipoContrario(self) -> str:
    return Equipo.AZUL if self.equipo == Equipo.ROJO else Equipo.ROJO