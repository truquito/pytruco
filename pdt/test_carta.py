import pytest
from .carta import Carta, Palo

def test_carta_str_rep():
  c1 = Carta(12, Palo.BASTO)
  assert str(c1) == "12 de basto", "la rep. str de c1 no es la esperada" 

def test_carta_parse():
  with pytest.raises(Exception, match='invalido'):
    Carta(7, "aslkdlaksdm")
  
  with pytest.raises(Exception, match='invalido'):
    Carta(0, Palo.BASTO)

  with pytest.raises(Exception, match='invalido'):
    Carta(8, Palo.BASTO)

  assert Carta(7, Palo.ORO) == Carta(7, "oro"), "deberian ser iguales"
  assert Carta(10, "copa") == Carta(10, "cOpA"), "deberian ser iguales"

def test_carta_eq():
  c2 = Carta(7, Palo.ORO)
  c3 = Carta(7, "oro")
  assert c2 == c3, "cartas c2 y c3 deberian ser iguales"
