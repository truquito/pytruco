from __future__ import annotations
from enum import Enum
# from typing import Self

class Palo(str, Enum):
  ESPADA = "espada"
  COPA = "copa"
  ORO = "oro"
  BASTO = "basto"

  # def parse(p:str) -> Self:
  def parse(p:str) -> Palo:
    p = p.lower()
    if p not in map(lambda x: str(x), 
      [Palo.ESPADA,Palo.COPA,Palo.ORO,Palo.BASTO]):
      raise Exception("Palo invalido")
    
    return Palo.ESPADA if p == Palo.ESPADA \
      else Palo.COPA if p == Palo.COPA \
      else Palo.ORO if p == Palo.ORO \
      else Palo.BASTO

  def es_valido(e):
    return e in [Palo.ESPADA, Palo.COPA, Palo.ORO, Palo.BASTO]

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)


class Carta():
  def __init__(self, valor: int, palo:Palo|str):
    if not (1 <= valor <= 12 and valor not in [8,9]):
      raise Exception("Valor invalido")
    
    if isinstance(palo, str):
      palo = Palo.parse(palo)

    if not Palo.es_valido(palo):
      raise Exception("Palo invalido")
     
    self.palo  = palo
    self.valor = valor
  
  def __str__(self) -> str:
    return f"{self.valor} de {self.palo}"

  def __repr__(self) -> str:
    return str(self)
  
  def __eq__(self, __value: Carta) -> bool:
    mismo_palo = self.palo == __value.palo
    mismo_valor = self.valor == __value.valor
    return mismo_palo and mismo_valor
  