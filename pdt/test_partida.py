import pytest
from .carta import Carta, Palo
from .jugador import Jugador
from .equipo import Equipo
from .manojo import Manojo
from .partida import Partida
from .envite import EstadoEnvite
from .truco import EstadoTruco
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

def test_parse_jugada():
  p = Partida(20, ["Alvaro"], ["Roro"])  
  mu = Carta(3, "oro")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(2, "Oro"), Carta(6, "Basto"), Carta(7, "Basto") ], # Alvaro tiene flor
    [ Carta(5, "Oro"), Carta(5, "Espada"), Carta(5, "Basto") ], # Roro no tiene flor
  ])

  shouldBeOK = [
    "alvaro envido",
		"Alvaro real-envido",
		"Alvaro falta-envido",
		"Alvaro flor",
		"Alvaro contra-flor",
		"Alvaro contra-flor-al-resto",
		"Alvaro truco",
		"Alvaro re-truco",
		"Alvaro vale-4",
		"Alvaro quiero",
		"Alvaro no-quiero",
		"Alvaro mazo",
		# tiradas
		"Alvaro 2 oro",
		"Alvaro 2 ORO",
		"Alvaro 2 oRo",
		"Alvaro 6 basto",
		"Alvaro 7 basto",
		"Roro 5 Oro",
		"Roro 5 Espada",
		"Roro 5 Basto",
  ]

  for c in shouldBeOK:
    _ = p.parse_jugada(c)

  shouldNotBeOK = [
    "Juancito envido",
		"Juancito envido asd",
		"Juancito envido 33",
		"Juancito envid0",
		# tiradas
		"Alvaro 2 oroo",
		"Alvaro 2 oRo ",
		"Alvaro 6 espada*",
		"Alvaro 7 asd",
		"Alvaro 2  copa",
		"Alvaro 54 Oro ",
		"Alvaro 0 oro",
		"Alvaro 9 oro",
		"Alvaro 8 oro",
		"Alvaro 111 oro",
		# roro trata de usar las de alvaro
		# esto se debe testear en jugadas
		# "roro 2 oRo",
		# "roro 6 basto",
		# "roro 7 basto",
  ]

  for c in shouldNotBeOK:
    with pytest.raises(Exception, match='invalido'):
      _ = p.parse_jugada(c)

def test_partida1():
  p = Partida(20, ["Alvaro", "Adolfo", "Andres"], ["Roro", "Renzo", "Richard"])  
  mu = Carta(3, "oro")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(2, "Oro"), Carta(6, "Basto"), Carta(7, "Basto") ], # Alvaro tiene flor
    [ Carta(5, "Oro"), Carta(5, "Espada"), Carta(5, "Basto") ], # Roro no tiene flor
    [ Carta(1, "Copa"), Carta(2, "Copa"), Carta(3, "Copa") ], # Adolfo tiene flor
    [ Carta(4, "Oro"), Carta(4, "Espada"), Carta(1, "Espada") ], # Renzo tiene flor
    [ Carta(10, "Copa"), Carta(7, "Oro"), Carta(11, "Basto") ], # Andres no tiene  flor
    [ Carta(10, "Oro"), Carta(2, "Oro"), Carta(1, "Basto") ], # Richard tiene flor
  ])

  # print(p)

  # no deberia dejarlo cantar envido xq tiene flor
  p.cmd("Alvaro Envido")
  assert p.ronda.envite.estado != EstadoEnvite.ENVIDO

  # deberia retornar un error debido a que ya canto flor
  pkts = p.cmd("Alvaro Flor")
  for pkt in pkts:
    print(pkt)

  # deberia dejarlo irse al mazo
  p.cmd("Roro Mazo")
  assert p.ronda.manojos[1].se_fue_al_mazo == True

  p.cmd("Adolfo Flor")
  
  p.cmd("Renzo Contra-flor")
  assert p.ronda.envite.estado == EstadoEnvite.CONTRAFLOR

  p.cmd("Alvaro Quiero")

def test_parse1():
  data = '{"puntuacion":20,"puntajes":{"Azul":3,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":2,"Rojo":2},"elMano":1,"turno":2,"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Ariana"]},"truco":{"cantadoPor":"","estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":4},{"palo":"Basto","valor":1},{"palo":"Basto","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alice","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Copa","valor":5},{"palo":"Copa","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Bob","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":3},{"palo":"Oro","valor":7},{"palo":"Oro","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Ariana","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":11},{"palo":"Basto","valor":6},{"palo":"Copa","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Ben","equipo":"Rojo"}}],"mixs":{"Alice":0,"Ariana":2,"Ben":3,"Bob":1},"muestra":{"palo":"Oro","valor":5},"manos":[{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null}]}}'
  p = Partida.parse(data)
  assert p.puntajes[Equipo.AZUL] == 3 and p.puntajes[Equipo.ROJO] == 0
  assert p.puntuacion == 20
  assert p.ronda.cant_jugadores_en_juego[Equipo.AZUL] == 2
  assert p.ronda.cant_jugadores_en_juego[Equipo.ROJO] == 2
  assert p.ronda.el_mano == 1
  assert p.ronda.turno == 2
  assert p.ronda.mano_en_juego == NumMano.PRIMERA
  assert len(p.ronda.manos) == 3
  # envite
  assert p.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN
  assert p.ronda.envite.puntaje == 0
  assert p.ronda.envite.cantado_por == ""
  assert p.ronda.envite.sin_cantar == ["Ariana"]
  # truco
  assert p.ronda.truco.estado == EstadoTruco.NOCANTADO
  assert p.ronda.truco.cantado_por == ""
  # manojos
  manojos = [
    ("Alice", [Carta(4,"Espada"), Carta(1,"Basto"), Carta(11,"Basto")], [False,False,False], 0),
    ("Bob", [Carta(2,"Basto"), Carta(5,"Copa"), Carta(7,"Copa")], [False,False,False], 0),
    ("Ariana", [Carta(3,"Oro"), Carta(7,"Oro"), Carta(2,"Oro")], [False,False,False], 0),
    ("Ben", [Carta(11,"Copa"), Carta(6,"Basto"), Carta(2,"Copa")], [False,False,False], 0),
  ]
  for i,m in enumerate(p.ronda.manojos):
    nom, cartas, tiradas, ult_tir = manojos[i]
    assert m.jugador.id == nom
    assert m.cartas == cartas
    assert m.tiradas == tiradas
    assert m.ultima_tirada == ult_tir

def test_parse2():
  data = '{"puntuacion":40,"puntajes":{"Azul":1,"Rojo":6},"ronda":{"manoEnJuego":2,"cantJugadoresEnJuego":{"Azul":1,"Rojo":1},"elMano":0,"turno":1,"envite":{"estado":"deshabilitado","puntaje":2,"cantadoPor":"Bob","sinCantar":[]},"truco":{"cantadoPor":"Bob","estado":"reTrucoQuerido"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":1},{"palo":"Basto","valor":2},{"palo":"Oro","valor":6}],"tiradas":[true,true,false],"ultimaTirada":1,"jugador":{"id":"Alice","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":7},{"palo":"Oro","valor":10},{"palo":"Copa","valor":5}],"tiradas":[true,false,true],"ultimaTirada":2,"jugador":{"id":"Bob","equipo":"Rojo"}}],"mixs":{"Alice":0,"Bob":1},"muestra":{"palo":"Copa","valor":2},"manos":[{"resultado":"ganoAzul","ganador":"Alice","cartasTiradas":[{"jugador":"Alice","carta":{"palo":"Copa","valor":1}},{"jugador":"Bob","carta":{"palo":"Copa","valor":7}}]},{"resultado":"ganoRojo","ganador":"Bob","cartasTiradas":[{"jugador":"Alice","carta":{"palo":"Basto","valor":2}},{"jugador":"Bob","carta":{"palo":"Copa","valor":5}}]},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null}]}}'
  p = Partida.parse(data)
  assert p.puntajes[Equipo.AZUL] == 1 and p.puntajes[Equipo.ROJO] == 6
  assert p.puntuacion == 40
  assert p.ronda.cant_jugadores_en_juego[Equipo.AZUL] == 1
  assert p.ronda.cant_jugadores_en_juego[Equipo.ROJO] == 1
  assert p.ronda.el_mano == 0
  assert p.ronda.turno == 1
  assert p.ronda.mano_en_juego == NumMano.TERCERA
  assert len(p.ronda.manos) == 3
  # envite
  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.ronda.envite.puntaje == 2
  assert p.ronda.envite.cantado_por == "Bob"
  assert p.ronda.envite.sin_cantar == []
  # truco
  assert p.ronda.truco.estado == EstadoTruco.RETRUCOQUERIDO
  assert p.ronda.truco.cantado_por == "Bob"
  # manojos
  manojos = [
    ("Alice", [Carta(1,"Copa"), Carta(2,"Basto"), Carta(6,"Oro")], [True,True,False], 1),
    ("Bob", [Carta(7,"Copa"), Carta(10,"Oro"), Carta(5,"Copa")], [True,False,True], 2),
  ]
  for i,m in enumerate(p.ronda.manojos):
    nom, cartas, tiradas, ult_tir = manojos[i]
    assert m.jugador.id == nom
    assert m.cartas == cartas
    assert m.tiradas == tiradas
    assert m.ultima_tirada == ult_tir
  
def test_fix_flor():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Richard"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Basto","valor":12},{"palo":"Oro","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":5},{"palo":"Basto","valor":10},{"palo":"Oro","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Copa","valor":10},{"palo":"Basto","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":6},{"palo":"Espada","valor":10},{"palo":"Basto","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":6},{"palo":"Copa","valor":3},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":3},{"palo":"Espada","valor":11},{"palo":"Espada","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Oro","valor":1},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro envido")
  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  assert p.puntajes[Equipo.ROJO] == 3

  p.cmd("alvaro 6 espada")
  p.cmd("alvaro 6 espada")
  p.cmd("roro 5 espada")
  p.cmd("adolfo 10 oro")
  p.cmd("renzo 6 basto")
  p.cmd("andres 6 copa")
  p.cmd("richard 3 espada")
  p.cmd("adolfo 10 copa")
  p.cmd("renzo 10 espada")
  p.cmd("andres 3 copa")
  p.cmd("richard 11 espada")
  p.cmd("alvaro 12 basto")
  p.cmd("roro 10 basto")
  
  assert p.puntajes[Equipo.ROJO] == 3
  assert p.puntajes[Equipo.AZUL] == 1

def test_fix_flor_bucle():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Roro","Richard"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":6},{"palo":"Oro","valor":11},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Basto","valor":10},{"palo":"Basto","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":7},{"palo":"Oro","valor":5},{"palo":"Espada","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":12},{"palo":"Basto","valor":1},{"palo":"Copa","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Espada","valor":2},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":11},{"palo":"Espada","valor":12},{"palo":"Espada","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Copa","valor":10},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro mazo")
  p.cmd("roro flor")
  p.cmd("richard flor")
  
  assert p.puntajes[Equipo.ROJO] == 6

def test_fix_contra_flor():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Adolfo","Renzo"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":1},{"palo":"Espada","valor":1},{"palo":"Espada","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":4},{"palo":"Copa","valor":7},{"palo":"Oro","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":11},{"palo":"Copa","valor":11},{"palo":"Copa","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":12},{"palo":"Espada","valor":3},{"palo":"Espada","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":4},{"palo":"Oro","valor":1},{"palo":"Oro","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":6},{"palo":"Copa","valor":6},{"palo":"Espada","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":4},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 1 basto")
  p.cmd("roro 4 oro")
  p.cmd("adolfo flor")

  # no deberia dejarlo tirar xq el envite esta en juego
  # tampoco debio de haber pasado su turno
  p.cmd("adolfo 11 basto")

  assert p.ronda.get_el_turno().jugador.id == "Adolfo"

  # no deberia dejarlo tirar xq el envite esta en juego
  p.cmd("renzo 12 basto")

  assert p.ronda.manojos[2].get_cant_cartas_tiradas() == 0

  # no hay nada que querer
  p.cmd("renzo quiero")

  assert p.ronda.envite.estado == EstadoEnvite.FLOR

  p.cmd("renzo contra-flor")
  p.cmd("adolfo quiero")

  # renzo tiene 35 vs los 32 de adolfo
  # deberia ganar las 2 flores + x pts

  assert p.puntajes[Equipo.ROJO] > p.puntajes[Equipo.AZUL]
  
