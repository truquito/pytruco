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


def test_calc_flor():
  # muestra
  muestra = Carta(11, "oro")
  
  # jugadores
  j_anna = Jugador("Anna", Equipo.AZUL)

  # manojos
  m_anna = Manojo(j_anna)

  m_anna.cartas = [
    Carta(2, "oro"),
    Carta(4, "oro"),
    Carta(5, "oro"),
  ]
  
  assert m_anna.tiene_flor(muestra)[0] == True, "deberia tener flor"

  assert m_anna.calc_flor(muestra) == 47, "deberia tener 47 de flor"


def test_calc_envido():
  # muestra
  muestra = Carta(1, "espada")
  
  # jugadores
  j_anna = Jugador("Anna", Equipo.AZUL)

  # manojos
  m_anna = Manojo(j_anna)

  m_anna.cartas = [
    Carta(6, "oro"),
    Carta(12, "oro"),
    Carta(5, "copa"),
  ]

  assert m_anna.calcular_envido(muestra) == 26, "deberia tener 26 de envido"

  m_anna.cartas = [
    Carta(12, "copa"),
    Carta(11, "copa"),
    Carta(3, "basto"),
  ]

  assert m_anna.calcular_envido(muestra) == 20, "deberia tener 20 de envido"

  m_anna.cartas = [
    Carta(2, "copa"),
    Carta(6, "copa"),
    Carta(1, "basto"),
  ]

  assert m_anna.calcular_envido(muestra) == 28, "deberia tener 28 de envido"

  m_anna.cartas = [
    Carta(2, "oro"),
    Carta(3, "oro"),
    Carta(2, "basto"),
  ]

  assert m_anna.calcular_envido(muestra) == 25, "deberia tener 25 de envido"

  m_anna.cartas = [
    Carta(6, "basto"),
    Carta(7, "basto"),
    Carta(5, "oro"),
  ]

  assert m_anna.calcular_envido(muestra) == 33, "deberia tener 33 de envido"

  m_anna.cartas = [
    Carta(3, "copa"),
    Carta(4, "copa"),
    Carta(4, "oro"),
  ]

  assert m_anna.calcular_envido(muestra) == 27, "deberia tener 27 de envido"

  

