import pytest
from .carta import Carta, Palo, get_cartas_random, CartaID

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

# pytest -s -k "test_cartas_random"
def test_cartas_random():
  cs = get_cartas_random(10)
  are_valids = [isinstance(c, Carta) for c in cs]
  assert len(cs) == 10
  assert all(are_valids), "todas deberian ser cartas validas"
  for i,c in enumerate(cs):
    print(f"#{i+1} - {c}")

  # no se repite ninguna
  for _ in range(100):
    cs = get_cartas_random(20)
    assert len(set([str(c) for c in cs])) == 20


def test_id_to_carta():
  assert CartaID(0).to_carta() == Carta(1,"basto"), "deberia coincidir"
  assert CartaID(4).to_carta() == Carta(5,"basto"), "deberia coincidir"
  assert CartaID(11).to_carta() == Carta(2,"Copa"), "deberia coincidir"
  assert CartaID(15).to_carta() == Carta(6,"Copa"), "deberia coincidir"
  assert CartaID(18).to_carta() == Carta(11,"Copa"), "deberia coincidir"
  assert CartaID(20).to_carta() == Carta(1,"espada"), "deberia coincidir"
  assert CartaID(27).to_carta() == Carta(10,"espada"), "deberia coincidir"
  assert CartaID(31).to_carta() == Carta(2,"oro"), "deberia coincidir"
  assert CartaID(35).to_carta() == Carta(6,"oro"), "deberia coincidir"
  assert CartaID(39).to_carta() == Carta(12,"oro"), "deberia coincidir"