import pytest
from .carta import Carta, Palo
from .jugador import Jugador
from .equipo import Equipo
from .manojo import Manojo

def test_carta_str_rep():
  # cartas
  c1 = Carta(12, Palo.BASTO)
  c2 = Carta(7, Palo.COPA)
  c3 = Carta(7, "oro")
  cs = [c1, c2, c3]

  # jugadores
  j_anna = Jugador("Anna", Equipo.AZUL)
  j_bob = Jugador("Bob", Equipo.ROJO)

  # manojos
  m_anna = Manojo(j_anna)
  m_anna.cartas = cs
  
  assert m_anna.get_carta_idx(Carta(12, "basto")) == 0
  assert m_anna.get_carta_idx(Carta(7, "copa")) == 1
  assert m_anna.get_carta_idx(Carta(7, "oro")) == 2

  with pytest.raises(Exception):
    m_anna.get_carta_idx(Carta(2, "oro"))

def test_tiene_flor():
  # muestra
  muestra = Carta(5, "copa")
  
  # jugadores
  j_anna = Jugador("Anna", Equipo.AZUL)

  # manojos
  m_anna = Manojo(j_anna)

  m_anna.cartas = [
    Carta(6, "oro"),
    Carta(10, "copa"),
    Carta(7, "copa"),
  ]
  
  assert m_anna.tiene_flor(muestra) == (False, -1), "no deberia tener flor"

  m_anna.cartas = [
    Carta(1, "copa"),
    Carta(2, "oro"),
    Carta(3, "basto"),
  ]
  
  assert m_anna.tiene_flor(muestra) == (False, -1), "no deberia tener flor"

  m_anna.cartas = [
    Carta(4, "copa"),
    Carta(2, "copa"),
    Carta(3, "basto"),
  ]
  
  assert m_anna.tiene_flor(muestra) == (True, 1), "deberia tener flor"

  # nueva muestra
  muestra = Carta(1, "copa")

  m_anna.cartas = [
    Carta(12, "copa"),
    Carta(10, "copa"),
    Carta(1, "basto"),
  ]
  
  assert m_anna.tiene_flor(muestra) == (False, -1), "no deberia tener flor"

  # nueva muestra
  muestra = Carta(5, "copa")

  m_anna.cartas = [
    Carta(4, "copa"),
    Carta(10, "espada"),
    Carta(7, "espada"),
  ]
  
  assert m_anna.tiene_flor(muestra) == (True, 3), "deberia tener flor"

  m_anna.cartas = [
    Carta(1, "oro"),
    Carta(2, "oro"),
    Carta(3, "oro"),
  ]
  
  assert m_anna.tiene_flor(muestra) == (True, 2), "deberia tener flor"


