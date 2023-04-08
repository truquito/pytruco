import pytest
from .carta import Carta, Palo
from .jugador import Jugador
from .equipo import Equipo
from .manojo import Manojo
from .partida import Partida
from .envite import EstadoEnvite

def test_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  muestra = Carta(1, "espada")
  p.ronda.muestra = muestra
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])
  
  assert p.manojo("alice").calcular_envido(muestra) == 33, "deberia tener 33 de envido"
  assert p.manojo("bob").calcular_envido(muestra) == 5, "deberia tener 5 de envido"

  p.cmd("alice envido")
  p.cmd("bob quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2
  assert p.puntajes[Equipo.AZUL] == 2 and p.puntajes[Equipo.ROJO] == 0 
  

  

