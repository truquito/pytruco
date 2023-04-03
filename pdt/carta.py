from __future__ import annotations
from enum import Enum
# from typing import Self

primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 
  67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 
  151, 157, 163, 167, 173]

"""
 Barajas; orden absoluto:
 ----------------------------------------------------------
| ID	| Carta	    ID | Carta	  ID | Carta	  ID | Carta |
|---------------------------------------------------------|
| 00 | 1,Basto   10 | 1,Copa   20 | 1,Espada   30 | 1,Oro |
| 01 | 2,Basto   11 | 2,Copa   21 | 2,Espada   31 | 2,Oro |
| 02 | 3,Basto   12 | 3,Copa   22 | 3,Espada   32 | 3,Oro |
| 03 | 4,Basto   13 | 4,Copa   23 | 4,Espada   33 | 4,Oro |
| 04 | 5,Basto   14 | 5,Copa   24 | 5,Espada   34 | 5,Oro |
| 05 | 6,Basto   15 | 6,Copa   25 | 6,Espada   35 | 6,Oro |
| 06 | 7,Basto   16 | 7,Copa   26 | 7,Espada   36 | 7,Oro |
 ----------------------------------------------------------
| 07 |10,Basto   17 |10,Copa   27 |10,Espada   37 |10,Oro |
| 08 |11,Basto   18 |11,Copa   28 |11,Espada   38 |11,Oro |
| 09 |12,Basto   19 |12,Copa   29 |12,Espada   39 |12,Oro |
 ----------------------------------------------------------
"""

class Palo(str, Enum):
  BASTO = "basto"
  COPA = "copa"
  ESPADA = "espada"
  ORO = "oro"

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

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)

  def es_valido(e):
    return e in [Palo.ESPADA, Palo.COPA, Palo.ORO, Palo.BASTO]
  
  def to_int(p):
    return 0 if p == Palo.BASTO \
      else 1 if p == Palo.COPA \
      else 2 if p == Palo.ESPADA \
      else 3

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
  
  def id(self) -> int:
    id = 10 * Palo.to_int(self.palo)
    id += self.valor - 1
    if self.valor >= 10: id -= 2;
    return id 
  
  def puid(self) -> int:
    return primes[self.id()]

  def es_numericamente_pieza(self) -> bool:
    return self.valor in [2,4,5,10,11]

  def es_pieza(self, muestra:Carta) -> bool:
    # caso 1
    es_de_la_muestra = self.palo == muestra.palo
    es_pieza_caso_1 = self.es_numericamente_pieza() and es_de_la_muestra
    # caso 2
    es_doce = self.valor == 12
    es_pieza_caso_2 = es_doce and es_de_la_muestra and \
      muestra.es_numericamente_pieza()

    return es_pieza_caso_1 or es_pieza_caso_2

  def es_mata(self) -> bool:
    if self.palo in [Palo.ESPADA, Palo.BASTO] and self.valor == 1:
      return True
    
    if self.palo in [Palo.ESPADA, Palo.ORO] and self.valor == 7:
      return True
    
    return False

  def calc_puntaje(self, muestra:Carta) -> int:
    if self.es_pieza(muestra):
      if self.valor == 2:
        return 30
      elif self.valor == 4:
        return 29
      elif self.valor == 5:
        return 28
      elif self.valor in [10,11]:
        return 27
      elif self.valor == 12:
        vale_como = Carta(muestra.valor, self.palo)
        return vale_como.calc_puntaje(muestra)
      
    elif self.es_mata():
      return self.valor
    
    elif self.valor <= 3:
      return self.valor
    
    elif 10 <= self.valor <= 12:
      return 0
    
    else:
      return self.valor

  def calc_poder(self, muestra:Carta) -> int:
    if self.es_pieza(muestra):
      if self.valor == 2:
        return 34
      elif self.valor == 4:
        return 33
      elif self.valor == 5:
        return 32
      elif self.valor == 11:
        return 31
      elif self.valor in 10:
        return 30
      elif self.valor == 12:
        vale_como = Carta(muestra.valor, self.palo)
        return vale_como.calc_poder(muestra)
    
    # matas
    elif self.palo == Palo.ESPADA and self.valor == 1:
      return 23
    elif self.palo == Palo.BASTO and self.valor == 1:
      return 22
    elif self.palo == Palo.ESPADA and self.valor == 7:
      return 21
    elif self.palo == Palo.ORO and self.valor == 7:
      return 20
    
    # chicas
    elif self.valor == 3:
      return 19
    elif self.valor == 2:
      return 18
    elif self.valor == 1:
      return 17
    elif self.valor == 12:
      return 16
    elif self.valor == 11:
      return 15
    elif self.valor == 10:
      return 14
    elif self.valor == 7:
      return 13
    elif self.valor == 6:
      return 12
    elif self.valor == 5:
      return 11
    elif self.valor == 4:
      return 10

class CartaID:
  def __init__(self, id):
    self.id = id
  
  def get_valor(self) -> int:
    ultimo_digito = self.id % 10
    return ultimo_digito + 1 if ultimo_digito <= 6 else 10 + ultimo_digito - 7
  
  def get_palo(self) -> Palo:
    return Palo.BASTO if 0 <= self.id <= 9 \
      else Palo.COPA if 10 <= self.id <= 19 \
      else Palo.ESPADA if 20 <= self.id <= 29 \
      else Palo.ORO
  
  def to_carta(self) -> Carta:
    return Carta(
      valor=self.get_valor(),
      palo=self.get_palo())


""" get_cartas_random retorna un array de `n` `Carta`s sin repeticion 
"""
def get_cartas_random(n:int) -> list[Carta]:
  import random
  max_carta_id = 40
  ids = list(range(max_carta_id))
  random.shuffle(ids)
  return [CartaID(id).to_carta() for id in ids[:n]]