from typing import Dict

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
  
  def to_dict(self) -> Dict[str, any]:
    return {
      "seFueAlMazo": self.se_fue_al_mazo,
      "cartas": [c.to_dict() if c is not None else None for c in self.cartas],
      "tiradas": self.tiradas,
      "ultimaTirada": self.ultima_tirada,
      "jugador": self.jugador.to_dict(),
    }
  
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
    for idx, c in enumerate(self.cartas):
      if c == carta:
        return idx
    return -1
  
  """devuelve `true` si el jugador tiene flor.
  Y ademas, si tiene devuelve que tipo de flor: 1, 2 o 3"""
  def tiene_flor(self, muestra:Carta) -> tuple[bool, int]:
    if None in self.cartas:
      return (False, -1)

    al_menos_una_carta_oculta = any(c.valor == 0 for c in self.cartas)
    if al_menos_una_carta_oculta:
      return (False, -1)

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
  
  """retorna el valor de la flor de un manojo
  si no tiene flor retorna -1"""
  def calc_flor(self, muestra:Carta) -> int:
    puntaje_flor = 0
    tiene_flor, tipo_flor = self.tiene_flor(muestra)

    if not tiene_flor: return -1

    ptjs = [c.calc_puntaje(muestra) for c in self.cartas]

    if tipo_flor == 1:
      _max = max(ptjs)
      mix = ptjs.index(_max)
      del ptjs[mix]
      puntaje_flor = _max + sum([p % 10 for p in ptjs])
    else: # casos 2 y 3 ~ elif tipo_flor in [2,3]:
      puntaje_flor = sum(ptjs)

    return puntaje_flor
  
  """tiene2DelMismoPalo devuelve `true` si tiene dos cartas
  del mismo palo, y ademas los indices de estas en el array manojo.Cartas"""
  def tiene_2_del_mismo_palo(self) -> tuple[bool, tuple[int, int]]:
    # hay cuatro casos
    # la primera es igual a la seguna
    # la primera es igual a la tercera
    # la seguna es igual a la tercera
    # ninguna de las anteriores
    for i in range(0,2):
      for j in range(i+1,3):
        mismo_palo = self.cartas[i].palo == self.cartas[j].palo
        if mismo_palo:
          return True, (i,j)

    return False, [None,None]
  
  """CalcularEnvido devuelve el puntaje correspondiente al envido del manojo
  PRE: no tiene flor"""
  def calcular_envido(self, muestra:Carta) -> int:
    def sum_las_dos_de_mas_valor() -> int:
      pts = sorted(
        [c.calc_puntaje(muestra) for c in self.cartas],
        reverse=True)
      return sum(pts[:2])

    tiene_2_del_mismo_palo, ixs = self.tiene_2_del_mismo_palo()
    if tiene_2_del_mismo_palo:
      x,y = [self.cartas[ix].calc_puntaje(muestra) for ix in ixs]
      no_tiene_niguna_pieza = max(x,y) < 27
      if no_tiene_niguna_pieza:
        return x + y + 20
      else:
        return max(x + y, sum_las_dos_de_mas_valor())
    else:
      # si no: simplemente sumo las 2 de mayor valor
      return sum_las_dos_de_mas_valor()


    
