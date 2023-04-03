# from pdt import equipo
from .jugador import Jugador
from .mano import NumMano
from .carta import Carta

class Manojo():
  def __init__(self, jugador:Jugador):
    self.se_fue_al_mazo :bool        = False
    self.cartas         :list[Carta] = [None] * 3
    self.tiradas        :list[bool]  = [False] * 3
    self.ultima_tirada  :int         = -1
    self.jugador        :Jugador     = jugador
  
  def __str__(self) -> str:
    cs = ", ".join([str(c) for c in self.cartas])
    return f"manojo::{self.jugador}[{cs}]"

  def __repr__(self) -> str:
    return str(self)
  
  def get_cant_cartas_tiradas(self) -> int:
    return sum(self.tiradas)
  
  def ya_tiro_carta(self, mano:int) -> bool:
    cant_tiradas = self.get_cant_cartas_tiradas()
    return cant_tiradas == 1 if mano == NumMano.PRIMERA \
      else cant_tiradas == 2 if mano == NumMano.SEGUNDA \
      else cant_tiradas == 3
  
  """retorna el indice de la `carta` o error si ni siquiera tiene 
  esa carta
  """
  def get_carta_idx(self, carta:Carta) -> int:
    return self.cartas.index(carta)
  
  """devuelve `true` si el jugador tiene flor.
  Y ademas, si tiene devuelve que tipo de flor: 1, 2 o 3"""
  def tiene_flor(self, muestra:Carta) -> tuple[bool, int]:
    # caso 1: al menos dos piezas
    piezas = [c.es_pieza(muestra) for c in self.cartas]
    t = sum(piezas)
    if t >= 2:
      return (True, 1)

    # caso 2: tres cartas del mismo palo
    palos = [c.palo for c in self.cartas]
    if palos.count(palos[0]) == len(palos):
      return (True, 2) 
    
    # caso 3: una pieza y dos cartas del mismo palo
    # Y ESAS DOS DIFERENTES DE LA PIEZA (piezaIdx)!
    if t == 1:
      idx = piezas.index(True)
      if (self.cartas[0].palo == self.cartas[1].palo and idx == 2) or \
         (self.cartas[0].palo == self.cartas[2].palo and idx == 1) or \
         (self.cartas[1].palo == self.cartas[2].palo and idx == 0):
        return (True, 3)

    return (False, -1)

    