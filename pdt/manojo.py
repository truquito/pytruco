# from pdt import equipo
from .jugador import Jugador
from .mano import NumMano
from .carta import Carta

class Manojo():
  def __init__(self, jugador:Jugador):
    self.se_fue_al_mazo = False
    self.cartas         = [None] * 3
    self.tiradas        = [False] * 3
    self.ultima_tirada  = -1
    self.jugador        = jugador
  
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
    