import pytest
from .carta import Carta, Palo
from .jugador import Jugador
from .equipo import Equipo
from .manojo import Manojo
from .partida import Partida
from .envite import EstadoEnvite
from .mano import NumMano, Resultado

def test_envido_quiero():
  p = Partida(20, ["Alice"], ["Bob"])
  
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
  

def test_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 1
  assert p.puntajes[Equipo.AZUL] == 1 and p.puntajes[Equipo.ROJO] == 0

def test_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 1
  assert p.puntajes[Equipo.AZUL] == 1 and p.puntajes[Equipo.ROJO] == 0

def test_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 1
  assert p.puntajes[Equipo.AZUL] == 1 and p.puntajes[Equipo.ROJO] == 0

def test_real_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice real-envido")
  p.cmd("bob quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 3
  assert p.puntajes[Equipo.AZUL] == 3 and p.puntajes[Equipo.ROJO] == 0

def test_falta_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice falta-envido")
  p.cmd("bob quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 10
  assert p.puntajes[Equipo.AZUL] == 10 and p.puntajes[Equipo.ROJO] == 0

def test_falta_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice falta-envido")
  p.cmd("bob no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 1
  assert p.puntajes[Equipo.AZUL] == 1 and p.puntajes[Equipo.ROJO] == 0

def test_envido_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  assert p.ronda.envite.estado == EstadoEnvite.ENVIDO
  assert p.ronda.envite.puntaje == 2
  
  p.cmd("bob envido")

  assert p.ronda.envite.estado == EstadoEnvite.ENVIDO
  assert p.ronda.envite.puntaje == 4

def test_envido_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob envido")
  p.cmd("alice no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+1
  assert p.puntajes[Equipo.AZUL] == 0 and p.puntajes[Equipo.ROJO] == 2+1

def test_envido_real_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob real-envido")
  p.cmd("alice quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+3
  assert p.puntajes[Equipo.AZUL] == 2+3 and p.puntajes[Equipo.ROJO] == 0

def test_envido_real_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob real-envido")
  p.cmd("alice no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+1
  assert p.puntajes[Equipo.AZUL] == 0 and p.puntajes[Equipo.ROJO] == 2+1

def test_envido_falta_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob falta-envido")
  p.cmd("alice quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+10
  assert p.puntajes[Equipo.AZUL] == 2+10 and p.puntajes[Equipo.ROJO] == 0

def test_envido_falta_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob falta-envido")
  p.cmd("alice no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+1
  assert p.puntajes[Equipo.AZUL] == 0 and p.puntajes[Equipo.ROJO] == 2+1

def test_real_envido_falta_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice real-envido")
  p.cmd("bob falta-envido")
  p.cmd("alice quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 3+10
  assert p.puntajes[Equipo.AZUL] == 3+10 and p.puntajes[Equipo.ROJO] == 0

def test_real_envido_falta_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice real-envido")
  p.cmd("bob falta-envido")
  p.cmd("alice no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 3+1
  assert p.puntajes[Equipo.AZUL] == 0 and p.puntajes[Equipo.ROJO] == 3+1

def test_envido_envido_real_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob envido")
  p.cmd("alice real-envido")
  p.cmd("bob quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+2+3
  assert p.puntajes[Equipo.AZUL] == 2+2+3 and p.puntajes[Equipo.ROJO] == 0

def test_envido_envido_real_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob envido")
  p.cmd("alice real-envido")
  p.cmd("bob no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+2+1
  assert p.puntajes[Equipo.AZUL] == 2+2+1 and p.puntajes[Equipo.ROJO] == 0

def test_envido_envido_falta_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob envido")
  p.cmd("alice falta-envido")
  p.cmd("bob quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+2+10
  assert p.puntajes[Equipo.AZUL] == 2+2+10 and p.puntajes[Equipo.ROJO] == 0

def test_envido_envido_falta_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob envido")
  p.cmd("alice falta-envido")
  p.cmd("bob no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+2+1
  assert p.puntajes[Equipo.AZUL] == 2+2+1 and p.puntajes[Equipo.ROJO] == 0

def test_envido_real_envido_falta_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob real-envido")
  p.cmd("alice falta-envido")
  p.cmd("bob quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+3+10
  assert p.puntajes[Equipo.AZUL] == 2+3+10 and p.puntajes[Equipo.ROJO] == 0

def test_envido_real_envido_falta_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob real-envido")
  p.cmd("alice falta-envido")
  p.cmd("bob no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+3+1
  assert p.puntajes[Equipo.AZUL] == 2+3+1 and p.puntajes[Equipo.ROJO] == 0

def test_envido_envido_real_envido_falta_envido_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob envido")
  p.cmd("alice real-envido")
  p.cmd("bob falta-envido")
  p.cmd("alice quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+2+3+10
  assert p.puntajes[Equipo.AZUL] == 2+2+3+10 and p.puntajes[Equipo.ROJO] == 0

def test_envido_envido_real_envido_falta_envido_no_quiero():
  p = Partida(20, ["alice"], ["bob"])
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  p.cmd("alice envido")
  p.cmd("bob envido")
  p.cmd("alice real-envido")
  p.cmd("bob falta-envido")
  p.cmd("alice no-quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2+2+3+1
  assert p.puntajes[Equipo.AZUL] == 0 and p.puntajes[Equipo.ROJO] == 2+2+3+1

def test_calc_envido():
  p = Partida(20, ["a", "c", "e"], ["b", "d", "f"])

  p.puntajes[Equipo.AZUL] = 4
  p.puntajes[Equipo.ROJO] = 3
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(6, "oro"), Carta(12, "oro"), Carta(5, "copa") ], # envido: 26
    [ Carta(12, "copa"), Carta(11, "copa"), Carta(3, "basto") ], # envido: 20
    [ Carta(2, "copa"), Carta(6, "copa"), Carta(1, "basto") ], # envido: 28
    [ Carta(2, "oro"), Carta(3, "oro"), Carta(2, "basto") ], # envido: 25
    [ Carta(6, "basto"), Carta(7, "basto"), Carta(5, "oro") ], # envido: 33
    [ Carta(3, "copa"), Carta(4, "copa"), Carta(4, "oro") ], # envido: 27
  ])

  expected = [26, 20, 28, 25, 33, 27]

  for i,m in enumerate(p.ronda.manojos):
    got = m.calcular_envido(mu)
    assert got == expected[i], f"el envido del jugador {m.jugador.id} es incorrecto"

  p.ronda.turno = 3
  p.cmd("d envido")
  p.cmd("c quiero")

  assert p.puntajes[Equipo.AZUL] == 4+2

def test_calc_envido_2():
  p = Partida(20, ["a", "c", "e"], ["b", "d", "f"])

  p.puntajes[Equipo.AZUL] = 4
  p.puntajes[Equipo.ROJO] = 3
  
  mu = Carta(1, "espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(1, "basto"), Carta(12, "basto"), Carta(5, "copa") ], # envido: 21
    [ Carta(12, "oro"), Carta(3, "oro"), Carta(4, "basto") ], # envido: 23
    [ Carta(10, "basto"), Carta(6, "copa"), Carta(3, "basto") ], # envido: 23
    [ Carta(6, "oro"), Carta(4, "oro"), Carta(1, "copa") ], # envido: 30
    [ Carta(6, "basto"), Carta(4, "basto"), Carta(1, "oro") ], # envido: 30
    [ Carta(5, "espada"), Carta(4, "copa"), Carta(3, "espada") ], # envido: 31
  ])

  expected = [21, 23, 23, 30, 30, 31]

  for i,m in enumerate(p.ronda.manojos):
    got = m.calcular_envido(mu)
    assert got == expected[i], f"el envido del jugador {m.jugador.id} es incorrecto"

  p.ronda.turno = 3
  p.cmd("d envido")
  p.cmd("c quiero")

  assert p.puntajes[Equipo.ROJO] == 3+2

def test_no_deberian_tener_flor():
  p = Partida(20, ["alice"], ["bob"])  
  mu = Carta(5, "copa")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(6, "oro"), Carta(10, "copa"), Carta(7, "copa") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  tiene_flor, _ = p.ronda.manojos[0].tiene_flor(mu)
  assert tiene_flor == False

  tiene_flor, _ = p.ronda.manojos[1].tiene_flor(mu)
  assert tiene_flor == False

def test_no_deberian_tener_flor2():
  p = Partida(20, ["alice"], ["bob"])  
  mu = Carta(1, "copa")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(12, "copa"), Carta(10, "copa"), Carta(1, "basto") ],
    [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
  ])

  tiene_flor, _ = p.ronda.manojos[0].tiene_flor(mu)
  assert tiene_flor == False

def test_deberia_tener_flor():
  p = Partida(20, ["alice"], ["bob"])  
  mu = Carta(5, "copa")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(4, "copa"), Carta(10, "espada"), Carta(7, "espada") ],
    [ Carta(1, "oro"), Carta(2, "oro"), Carta(3, "oro") ],
  ])

  tiene_flor, _ = p.ronda.manojos[0].tiene_flor(mu)
  assert tiene_flor == True

  tiene_flor, _ = p.ronda.manojos[1].tiene_flor(mu)
  assert tiene_flor == True

def test_flor_flor_contra_flor_quiero():
  p = Partida(20, ["Alvaro", "Adolfo", "Andres"], ["Roro", "Renzo", "Richard"])  
  mu = Carta(3, "oro")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(2, "Oro"), Carta(6, "Basto"), Carta(7, "Basto") ], # Alvaro tiene flor
    [ Carta(5, "Oro"), Carta(5, "Espada"), Carta(5, "Basto") ], # Roro
    [ Carta(1, "Copa"), Carta(2, "Copa"), Carta(3, "Copa") ], # Adolfo tiene flor
    [ Carta(4, "Oro"), Carta(4, "Espada"), Carta(1, "Espada") ], # Renzo tiene flor
    [ Carta(10, "Copa"), Carta(7, "Oro"), Carta(11, "Basto") ], # Andres
    [ Carta(10, "Oro"), Carta(2, "Oro"), Carta(1, "Basto") ], # Richard tiene flor
  ])

  # print(p)

  p.cmd("Alvaro Flor")
  p.cmd("Roro Mazo")
  p.cmd("Renzo Flor")
  p.cmd("Adolfo Contra-flor-al-resto")
  p.cmd("Richard Quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.puntajes[Equipo.AZUL] == 10 and p.puntajes[Equipo.ROJO] == 0

def test_tirada1():
  p = Partida(20, ["Alvaro", "Adolfo", "Andres"], ["Roro", "Renzo", "Richard"])  
  mu = Carta(3, "oro")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(2, "Oro"), Carta(6, "Basto"), Carta(7, "Basto") ], # Alvaro tiene flor
    [ Carta(5, "Oro"), Carta(5, "Espada"), Carta(5, "Basto") ], # Roro
    [ Carta(1, "Copa"), Carta(2, "Copa"), Carta(3, "Copa") ], # Adolfo tiene flor
    [ Carta(4, "Oro"), Carta(4, "Espada"), Carta(1, "Espada") ], # Renzo tiene flor
    [ Carta(10, "Copa"), Carta(7, "Oro"), Carta(11, "Basto") ], # Andres
    [ Carta(10, "Oro"), Carta(2, "Oro"), Carta(1, "Basto") ], # Richard tiene flor
  ])

  # print(p)

  p.cmd("Richard flor")
  p.cmd("Adolfo contra-flor")
  p.cmd("Richard quiero")
  # p.cmd("Adolfo no-quiero") # si dice no quero autoamticamente acarrea a alvaro
  # ademas suma 12 puntos y renzo no llego a decir que tenia flor,
  # deberia cantar la de renzo tambien
  p.cmd("Renzo flor")
  p.cmd("Alvaro flor")
  p.cmd("Alvaro 2 Oro")
  p.cmd("Roro 5 Oro")
  p.cmd("Adolfo 1 Copa")
  p.cmd("Renzo 4 Oro")
  p.cmd("Andres 10 Copa")
  p.cmd("Richard 10 Oro")

  # print(p)

  assert len(p.ronda.manos[NumMano.PRIMERA.to_ix()].cartas_tiradas) == 6
  assert p.ronda.manos[NumMano.PRIMERA.to_ix()].ganador == "Alvaro"
  assert p.ronda.manos[NumMano.PRIMERA.to_ix()].resultado == Resultado.GANO_AZUL

  # como alvaro gano la mano anterior -> empieza tirando el
  p.cmd("Alvaro 6 Basto")
  p.cmd("Roro 5 Espada")
  p.cmd("Adolfo 2 Copa")
  p.cmd("Renzo 4 Espada")
  p.cmd("Andres 7 Oro")
  # print(p)
  p.cmd("Richard 2 Oro")

  assert len(p.ronda.manos[NumMano.SEGUNDA.to_ix()].cartas_tiradas) == 6
  assert p.ronda.manos[NumMano.SEGUNDA.to_ix()].ganador == "Richard"
  assert p.ronda.manos[NumMano.SEGUNDA.to_ix()].resultado == Resultado.GANO_ROJO

	# vuelvo a checkear que el estado de la pdt.Primera nos se haya editado
  assert len(p.ronda.manos[NumMano.PRIMERA.to_ix()].cartas_tiradas) == 6
  assert p.ronda.manos[NumMano.PRIMERA.to_ix()].ganador == "Alvaro"
  assert p.ronda.manos[NumMano.PRIMERA.to_ix()].resultado == Resultado.GANO_AZUL

  # como richard gano la mano anterior -> empieza tirando el
  p.cmd("Richard 1 Basto")
  p.cmd("Alvaro 7 Basto")
  p.cmd("Roro 5 Basto")
  p.cmd("Adolfo 3 Copa")
  p.cmd("Renzo 1 Espada")
  p.cmd("Andres 11 Basto")

  assert p.puntajes[Equipo.ROJO] == 1 



