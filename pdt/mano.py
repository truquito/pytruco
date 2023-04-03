from __future__ import annotations
from enum import Enum

class NumMano(str, Enum):
  PRIMERA = "primera"
  SEGUNDA = "segunda"
  TERCERA = "tercera"

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)
  
  def to_int(nm:NumMano) -> int:
    return 1 if nm == NumMano.PRIMERA \
      else 2 if nm == NumMano.SEGUNDA \
      else 3