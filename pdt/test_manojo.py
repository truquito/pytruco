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

