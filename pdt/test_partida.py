import pytest
from .carta import Carta
from .equipo import Equipo
from .partida import Partida
from .envite import EstadoEnvite
from .truco import EstadoTruco
from .mano import NumMano, Resultado
from .printer import renderizar

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

  print(renderizar(p))

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
  
def test_partida_comandos_invalidos():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":2,"Rojo":2},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":5},{"palo":"Copa","valor":4},{"palo":"Copa","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Basto","valor":7},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Espada","valor":7},{"palo":"Oro","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Oro","valor":2},{"palo":"Espada","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":11},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)
  p.cmd("Alvaro Envido")

  with pytest.raises(Exception, match='comando invalido'):
    p.cmd("Quiero")

  assert p.ronda.envite.estado == EstadoEnvite.ENVIDO

  with pytest.raises(Exception, match='comando invalido'):
    p.cmd("Schumacher Flor")

  assert p.ronda.envite.estado == EstadoEnvite.ENVIDO

def test_fix_nacho():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Richard"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Copa","valor":7},{"palo":"Basto","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Copa","valor":6},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":11},{"palo":"Espada","valor":1},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":3},{"palo":"Basto","valor":7},{"palo":"Oro","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Basto","valor":12},{"palo":"Espada","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Espada","valor":5},{"palo":"Espada","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Espada","valor":3},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 6 basto")
  p.cmd("roro 2 basto")
  cantTiradasRoro = p.manojo("Roro").get_cant_cartas_tiradas()
  assert cantTiradasRoro == 1

  p.cmd("Adolfo 4 basto")
  p.cmd("renzo 7 basto")
  p.cmd("andres 10 espada")
  p.cmd("richard flor")
  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO

  p.cmd("richard 11 espada")
  assert p.ronda.get_el_turno().jugador.id == "Richard"

  p.cmd("richard truco")
  assert p.ronda.truco.estado == EstadoTruco.TRUCO

  p.cmd("roro quiero")
  assert p.ronda.truco.estado == EstadoTruco.TRUCO

  p.cmd("adolfo quiero")
  p.cmd("richard 5 espada")
  p.cmd("alvaro mazo")
  p.cmd("roro quiero")
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.id == "Adolfo"

  # syntaxis invalida
  with pytest.raises(Exception, match='comando invalido'):
    p.cmd("roro retruco")

  p.cmd("roro re-truco")
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.id == "Adolfo"

  p.cmd("alvaro re-truco")
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.id == "Adolfo"

  p.cmd("Adolfo re-truco")
  assert p.ronda.truco.estado == EstadoTruco.RETRUCO

  p.cmd("renzo quiero")
  assert p.ronda.truco.estado == EstadoTruco.RETRUCOQUERIDO
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.id == "Renzo"

  p.cmd("roro 6 copa")
  assert cantTiradasRoro == 1

  p.cmd("adolfo re-truco")
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.id == "Renzo"

  p.cmd("adolfo 1 espada")

  p.cmd("renzo 3 oro")
  assert p.ronda.get_el_turno().jugador.id == "Andres"

  p.cmd("andres mazo")

def test_fix_no_flor():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Andres","Richard"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Basto","valor":4},{"palo":"Espada","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":7},{"palo":"Basto","valor":11},{"palo":"Basto","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":12},{"palo":"Basto","valor":1},{"palo":"Copa","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Espada","valor":7},{"palo":"Oro","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":4},{"palo":"Basto","valor":6},{"palo":"Espada","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":11},{"palo":"Copa","valor":2},{"palo":"Espada","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Espada","valor":3},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 4 basto")
	# << Alvaro tira la carta 4 de pdt.Basto

  p.cmd("roro truco")

  # No es posible responder al truco ahora porque
  # "la flor esta primero":
  # el otro que tiene flor, pero se arruga
  p.cmd("richard no-quiero")

  assert p.ronda.truco.estado == EstadoTruco.NOCANTADO

  p.cmd("andres flor")
  p.cmd("richard flor")
  # << +6 puntos para el equipo pdt.Azul por las flores

  p.cmd("adolfo 12 oro")
  # No era su turno, no puede tirar la carta

  p.cmd("roro truco")
  # << Roro grita truco

  p.cmd("andres quiero")
  # << Andres responde quiero

  p.cmd("roro 7 copa")
  # << Roro tira la carta 7 de pdt.Copa

  p.cmd("adolfo 12 oro")
  # << Adolfo tira la carta 12 de pdt.Oro

  p.cmd("renzo 5 oro")
  # << Renzo tira la carta 5 de pdt.Oro

  p.cmd("andres flor")
  # No es posible cantar flor

  p.cmd("andres 6 basto")
  # << Andres tira la carta 6 de pdt.Basto

  p.cmd("richard flor")
  # no deberia dejarlo porque ya se jugo

  p.cmd("richard 11 copa")
  # << Richard tira la carta 11 de pdt.Copa

  """
  # << La Primera mano la gano Adolfo (equipo pdt.Azul)
  # << Es el turno de Adolfo
  """

  p.cmd("adolfo re-truco")
  # << Adolfo grita re-truco

  p.cmd("richard quiero")
  # << Richard responde quiero

  p.cmd("richard vale-4")
  # << Richard grita vale 4

  assert p.ronda.truco.estado == EstadoTruco.VALE4

  p.cmd("adolfo quiero")
  # << Adolfo responde quiero

  assert p.ronda.truco.estado == EstadoTruco.VALE4QUERIDO

  """
  # ACA EMPIEZAN A TIRAR CARTAS PARA LA SEGUNDA MANO
  # muesta: 3 espada
  """

  p.cmd("adolfo 1 basto")
  # << Adolfo tira la carta 1 de pdt.Basto

  p.cmd("renzo 7 espada")
  # << Renzo tira la carta 7 de pdt.Espada

  p.cmd("andres 4 espada")
  # << Andres tira la carta 4 de pdt.Espada

  p.cmd("richard 10 espada")
  # << Richard tira la carta 10 de pdt.Espada

  p.cmd("alvaro 6 espada")
  # << Alvaro tira la carta 6 de pdt.Espada

  p.cmd("roro re-truco")
  # << Alvaro tira la carta 6 de pdt.Espada

  p.cmd("roro mazo")
  # << Roro se va al mazo

  # era el ultimo que quedaba por tirar en esta mano
  # -> que evalue la mano

  # << +4 puntos para el equipo pdt.Azul por el vale4Querido no querido por Roro
  # << Empieza una nueva ronda
  # << Empieza una nueva ronda

  """6 de las 2 flores"""
  # assert p.GetMaxPuntaje() == 6+4

def test_fix_panic():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Richard"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Copa","valor":7},{"palo":"Basto","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Copa","valor":6},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":11},{"palo":"Espada","valor":1},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":3},{"palo":"Basto","valor":7},{"palo":"Oro","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Basto","valor":12},{"palo":"Espada","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Espada","valor":5},{"palo":"Espada","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Espada","valor":3},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 6 basto")
  # << Alvaro tira la carta 6 de pdt.Basto
  p.cmd("roro 2 basto")
  # << Roro tira la carta 2 de pdt.Basto
  p.cmd("Adolfo 4 basto")
  # << Adolfo tira la carta 4 de pdt.Basto
  p.cmd("renzo 7 basto")
  # << Renzo tira la carta 7 de pdt.Basto
  p.cmd("andres 10 espada")
  # << Andres tira la carta 10 de pdt.Espada
  p.cmd("richard flor")
  # << Richard canta flor
  # << +3 puntos para el equipo pdt.Rojo (por ser la unica flor de esta ronda)
  p.cmd("richard 11 espada")
  # << Richard tira la carta 11 de pdt.Espada
  """
    # << La Mano resulta parda
    # << Es el turno de Richard
  """
  # ERROR: no la deberia ganar andres porque es mano (DUDA)
  p.cmd("richard truco")
  # << Richard grita truco
  p.cmd("roro quiero")
  # (Para Roro) No hay nada "que querer"; ya que: el estado del envido no es "envido" (o mayor) y el estado del truco no es "truco" (o mayor) o bien fue cantado por uno de su equipo
  p.cmd("adolfo quiero")
  # << Adolfo responde quiero
  p.cmd("richard 5 espada")
  # << Richard tira la carta 5 de pdt.Espada
  p.cmd("alvaro mazo")
  # << Alvaro se va al mazo
  p.cmd("roro quiero")
  # (Para Roro) No hay nada "que querer"; ya que: el estado del envido no es "envido" (o mayor) y el estado del truco no es "truco" (o mayor) o bien fue cantado por uno de su equipo
  with pytest.raises(Exception, match='comando invalido'):
    p.cmd("roro retruco")
    # << No esxiste esa jugada
  p.cmd("roro re-truco")
  # No es posible cantar re-truco ahora
  p.cmd("alvaro re-truco") # ya que se fue al mazo
  # No es posible cantar re-truco ahora
  p.cmd("Adolfo re-truco") # no es su turno ni el de su equipo
  # No es posible cantar re-truco ahora
  p.cmd("roro 6 copa")
  # << Roro tira la carta 6 de pdt.Copa
  p.cmd("adolfo re-truco")
  # << Adolfo grita re-truco
  p.cmd("adolfo 1 espada")
  # << Adolfo tira la carta 1 de pdt.Espada
  with pytest.raises(Exception, match='comando invalido'):
    p.cmd("renzo retruco")
  # << No esxiste esa jugada
  p.cmd("renzo re-truco") # ya que ya lo canto adolfo
  # No es posible cantar re-truco ahora
  p.cmd("renzo mazo")
  # << Renzo se va al mazo

  p.cmd("andres mazo")

def test_fix_bocha():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Espada","valor":7},{"palo":"Basto","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":12},{"palo":"Espada","valor":11},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":12},{"palo":"Oro","valor":6},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":7},{"palo":"Basto","valor":10},{"palo":"Copa","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":2},{"palo":"Copa","valor":3},{"palo":"Oro","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":10},{"palo":"Oro","valor":2},{"palo":"Copa","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Copa","valor":6},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro mazo")
  # << Alvaro se va al mazo
  p.cmd("adolfo mazo")
  # << Adolfo se va al mazo
  p.cmd("andres mazo")
  # << Andres se va al mazo

  assert p.puntajes[Equipo.ROJO] == 1 and p.puntajes[Equipo.AZUL] == 0
  assert p.ronda.get_el_mano().jugador.equipo == Equipo.ROJO

def test_fix_bocha_parte2():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Espada","valor":7},{"palo":"Basto","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":12},{"palo":"Espada","valor":11},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":12},{"palo":"Oro","valor":6},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":7},{"palo":"Basto","valor":10},{"palo":"Copa","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":2},{"palo":"Copa","valor":3},{"palo":"Oro","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":10},{"palo":"Oro","valor":2},{"palo":"Copa","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Copa","valor":6},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("roro envido")
  # No es posible cantar 'Envido'
  p.cmd("andres quiero")
  # (Para Andres) No hay nada "que querer"; ya que: el estado del envido no es "envido" (o mayor) y el estado del truco no es "truco" (o mayor) o bien fue cantado por uno de su equipo
  p.cmd("andres quiero")
  # (Para Andres) No hay nada "que querer"; ya que: el estado del envido no es "envido" (o mayor) y el estado del truco no es "truco" (o mayor) o bien fue cantado por uno de su equipo
  p.cmd("alvaro mazo")
  # << Alvaro se va al mazo
  with pytest.raises(Exception):
    p.cmd("adolfo 1 copa")
  # Esa carta no se encuentra en este manojo
  p.cmd("adolfo mazo")
  # << Adolfo se va al mazo
  p.cmd("andres mazo")
  # << Andres se va al mazo

  assert p.puntajes[Equipo.ROJO] == 1 and p.puntajes[Equipo.AZUL] == 0

def test_fix_bocha_parte3():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Espada","valor":7},{"palo":"Basto","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":12},{"palo":"Espada","valor":11},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":12},{"palo":"Oro","valor":6},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":7},{"palo":"Basto","valor":10},{"palo":"Copa","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":2},{"palo":"Copa","valor":3},{"palo":"Oro","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":10},{"palo":"Oro","valor":2},{"palo":"Copa","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Copa","valor":6},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("richard flor")
  assert p.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN

  # (Para Andres) No hay nada "que querer"; ya que: el estado del envido no
  # es "envido" (o mayor) y el estado del truco no es "truco" (o mayor) o
  # bien fue cantado por uno de su equipo
  p.cmd("andres quiero")
  assert p.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN and \
    p.ronda.truco.estado == EstadoTruco.NOCANTADO

  # No es posible cantar contra flor
  p.cmd("andres contra-flor")
  assert p.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN

  # No es posible cantar contra flor
  p.cmd("richard contra-flor")
  assert p.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN

  # (Para Richard) No hay nada "que querer"; ya que: el estado del envido no
  # es "envido" (o mayor) y el estado del truco no es "truco" (o mayor) o
  # bien fue cantado por uno de su equipo
  p.cmd("richard quiero")
  assert p.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN and \
    p.ronda.truco.estado == EstadoTruco.NOCANTADO


def test_fix_auto_querer():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Espada","valor":7},{"palo":"Basto","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":12},{"palo":"Espada","valor":11},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":12},{"palo":"Oro","valor":6},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":7},{"palo":"Basto","valor":10},{"palo":"Copa","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":2},{"palo":"Copa","valor":3},{"palo":"Oro","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":10},{"palo":"Oro","valor":2},{"palo":"Copa","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Copa","valor":6},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro envido")
  assert p.ronda.envite.estado == EstadoEnvite.ENVIDO

  p.cmd("alvaro quiero")
  assert p.ronda.envite.estado == EstadoEnvite.ENVIDO

  p.cmd("adolfo quiero")
  assert p.ronda.envite.estado == EstadoEnvite.ENVIDO


def test_fix_nil_pointer():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Renzo"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":11},{"palo":"Espada","valor":10},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":12},{"palo":"Copa","valor":5},{"palo":"Copa","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":3},{"palo":"Copa","valor":7},{"palo":"Basto","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":6},{"palo":"Basto","valor":1},{"palo":"Copa","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":3},{"palo":"Copa","valor":6},{"palo":"Copa","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":4},{"palo":"Basto","valor":10},{"palo":"Copa","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Copa","valor":6},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)
  p.ronda.turno = 3 # es el turno de renzo

  with pytest.raises(Exception):
    p.cmd("renzo6 basto")
  p.cmd("renzo 6 basto")
  p.cmd("andres truco")
  p.cmd("renzo quiero")
  p.cmd("andres re-truco")
  p.cmd("andres 3 oro")
  p.cmd("richard vale-4")
  p.cmd("richard re-truco")
  p.cmd("andres quiero")
  p.cmd("richard mazo")
  p.cmd("alvaro vale-4")
  p.cmd("andres quiero")
  p.cmd("roro quiero")
  p.cmd("alvaro mazo")
  p.cmd("roro mazo")
  p.cmd("roro 12 oro")
  p.cmd("adolfo mazo")
  p.cmd("Renzo flor")


def test_fix_no_deja_irse_al_mazo():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Renzo"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":11},{"palo":"Oro","valor":7},{"palo":"Oro","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":6},{"palo":"Copa","valor":2},{"palo":"Espada","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":12},{"palo":"Oro","valor":4},{"palo":"Oro","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":2},{"palo":"Espada","valor":10},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":6},{"palo":"Copa","valor":7},{"palo":"Basto","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":2},{"palo":"Basto","valor":2},{"palo":"Copa","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":3},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 11 copa")
  p.cmd("roro 6 basto")
  p.cmd("adolfo 12 espada")
  p.cmd("renzo 2 espada")
  p.cmd("renzo flor")
  p.cmd("andres 6 oro")
  p.cmd("richard truco")
  p.cmd("andres quiero")
  p.cmd("alvaro 7 oro")
  p.cmd("roro 2 copa")
  p.cmd("richard 2 oro")
  p.cmd("renzo mazo")

  assert p.ronda.manojos[3].se_fue_al_mazo == True
  p.cmd("andres mazo")

  assert p.ronda.manojos[4].se_fue_al_mazo == True
  p.cmd("andres mazo")


def test_fix_flor_obligatoria():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Alvaro"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Oro","valor":6},{"palo":"Oro","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":5},{"palo":"Basto","valor":12},{"palo":"Espada","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":7},{"palo":"Basto","valor":5},{"palo":"Oro","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":1},{"palo":"Copa","valor":11},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":10},{"palo":"Oro","valor":2},{"palo":"Oro","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Basto","valor":3},{"palo":"Espada","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":6},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 2 basto") # alvaro deberia primero cantar flor
  # p.cmd("alvaro flor")
  p.cmd("roro 5 copa")
  p.cmd("adolfo 7 espada")
  p.cmd("renzo 1 espada")
  p.cmd("andres 10 espada")
  p.cmd("richard 3 basto")
  p.cmd("alvaro envido")
  p.cmd("alvaro 1 oro")
  p.cmd("roro 2 espada")
  p.cmd("adolfo truco")
  p.cmd("roro quiero")
  p.cmd("renzo quiero")
  p.cmd("adolfo 5 basto")
  p.cmd("renzo quiero")
  p.cmd("renzo 11 copa")
  p.cmd("andres 2 oro")
  p.cmd("richard 10 oro")

  with pytest.raises(Exception):
    p.cmd("roro 1 oro")


def test_fix_no_permite_contra_flor():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Adolfo","Renzo"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":1},{"palo":"Espada","valor":1},{"palo":"Espada","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":4},{"palo":"Copa","valor":7},{"palo":"Oro","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":11},{"palo":"Copa","valor":11},{"palo":"Copa","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":12},{"palo":"Espada","valor":3},{"palo":"Espada","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":4},{"palo":"Oro","valor":1},{"palo":"Oro","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":6},{"palo":"Copa","valor":6},{"palo":"Espada","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":4},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 1 basto")
  p.cmd("roro 4 oro")

  p.cmd("adolfo flor")
  assert p.ronda.envite.estado == EstadoEnvite.FLOR

  p.cmd("adolfo 11 basto")
  p.cmd("renzo 12 basto")

  p.cmd("renzo quiero")
  assert p.ronda.envite.estado == EstadoEnvite.FLOR

  p.cmd("renzo contra-flor")
  assert p.ronda.envite.estado == EstadoEnvite.CONTRAFLOR


def test_fix_deberia_ganar_azul():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":2,"Rojo":2},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Espada","valor":10},{"palo":"Oro","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":10},{"palo":"Oro","valor":5},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Espada","valor":3},{"palo":"Basto","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":4},{"palo":"Espada","valor":6},{"palo":"Copa","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":12},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 10 oro")
  p.cmd("roro 10 copa")
  p.cmd("adolfo 2 copa")
  p.cmd("renzo 4 basto")
  p.cmd("renzo mazo")
  p.cmd("alvaro mazo")

  p.cmd("roro mazo")
  assert p.puntajes[Equipo.ROJO] == 0 and p.puntajes[Equipo.AZUL] > 0

def test_fix_pierde_turno():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":2,"Rojo":2},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":5},{"palo":"Copa","valor":4},{"palo":"Copa","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Basto","valor":7},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Espada","valor":7},{"palo":"Oro","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Oro","valor":2},{"palo":"Espada","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":11},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 5 espada")

  p.cmd("adolfo mazo")
  assert p.ronda.get_el_turno().jugador.id == "Roro"


def test_fix_tiene_flor():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":2,"Rojo":2},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Alvaro"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":5},{"palo":"Copa","valor":4},{"palo":"Copa","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Basto","valor":7},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Espada","valor":7},{"palo":"Oro","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Oro","valor":2},{"palo":"Espada","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":11},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  # no deberia dejarlo jugar porque tiene flor
  p.cmd("alvaro 5 copa")
  assert p.ronda.get_el_turno().jugador.id == "Alvaro"

def test_flores_se_va_al_mazo2():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Alvaro","Richard"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Copa","valor":7},{"palo":"Copa","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Copa","valor":6},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":11},{"palo":"Espada","valor":1},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":3},{"palo":"Basto","valor":7},{"palo":"Oro","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Basto","valor":12},{"palo":"Espada","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Espada","valor":5},{"palo":"Espada","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Espada","valor":3},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 1 copa") # no deberia dejarlo porque tiene flor
  p.cmd("alvaro envido") # no deberia dejarlo porque tiene flor
  p.cmd("alvaro flor")
  
  p.cmd("richard mazo") # lo deja que se vaya
  assert p.ronda.manojos[5].se_fue_al_mazo == True

def test_todo_tienen_flor():

  p = Partida(20, ["Alvaro", "Adolfo", "Andres"], ["Roro", "Renzo", "Richard"])  
  mu = Carta(3, "oro")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(2, "Oro"), Carta(6, "Basto"), Carta(7, "Basto") ], # Alvaro tiene flor
    [ Carta(5, "Oro"), Carta(5, "Espada"), Carta(5, "Basto") ], # Roro no tiene flor
    [ Carta(1, "Copa"), Carta(2, "Copa"), Carta(3, "Copa") ], # Adolfo tiene flor
    [ Carta(1, "Copa"), Carta(7, "Oro"), Carta(1, "Basto") ], # Renzo no tiene flor
    [ Carta(4, "Oro"), Carta(4, "Espada"), Carta(1, "Espada") ], # Andres tiene  flor
    [ Carta(1, "Copa"), Carta(2, "Oro"), Carta(1, "Basto") ], # Richard no tiene flor
  ])

  p.cmd("Alvaro Envido")
  assert p.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN

  p.cmd("Alvaro Flor")
  p.cmd("Roro Mazo")
  p.cmd("Adolfo Flor")

def test_fix_tope_envido():
  data = '{"puntuacion":20,"puntajes":{"Azul":10,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Basto","valor":1},{"palo":"Basto","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":11},{"palo":"Basto","valor":3},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":1},{"palo":"Espada","valor":10},{"palo":"Basto","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":4},{"palo":"Copa","valor":12},{"palo":"Basto","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":10},{"palo":"Copa","valor":7},{"palo":"Espada","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Copa","valor":1},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":4},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  # azul va 10 pts de 20,
  # asi que el maximo permitido de envite deberia ser 10
  # ~ 5 envidos
  # al 6to saltar error

  p.cmd("alvaro envido")
  p.cmd("Roro envido")
  p.cmd("alvaro envido")
  p.cmd("Roro envido")
  p.cmd("alvaro envido")
  pts = p.ronda.envite.puntaje

  p.cmd("Roro envido") # debe retornar error
  assert p.ronda.envite.puntaje == pts

  p.cmd("Roro quiero")


def test_auto_quererse():
  data = '{"puntuacion":20,"puntajes":{"Azul":10,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Basto","valor":1},{"palo":"Basto","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":11},{"palo":"Basto","valor":3},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":1},{"palo":"Espada","valor":10},{"palo":"Basto","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":4},{"palo":"Copa","valor":12},{"palo":"Basto","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":10},{"palo":"Copa","valor":7},{"palo":"Espada","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Copa","valor":1},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":4},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  # no deberia poder auto quererse **ni auto no-quererse**
  p.cmd("Alvaro Envido")
  p.cmd("Roro Envido")
  p.cmd("Alvaro Real-Envido")
  p.cmd("Roro Falta-Envido")

  p.cmd("Roro Quiero")
  assert p.ronda.envite.estado == EstadoEnvite.FALTAENVIDO

  p.cmd("Roro no-quiero")
  assert p.ronda.envite.estado == EstadoEnvite.FALTAENVIDO

  p.cmd("Renzo Quiero")
  assert p.ronda.envite.estado == EstadoEnvite.FALTAENVIDO

  p.cmd("Renzo no-quiero")
  assert p.ronda.envite.estado == EstadoEnvite.FALTAENVIDO

def test_json_sin_flores():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Alvaro","Adolfo","Renzo","Richard"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":2},{"palo":"Basto","valor":6},{"palo":"Basto","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Espada","valor":5},{"palo":"Basto","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":1},{"palo":"Copa","valor":2},{"palo":"Copa","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":4},{"palo":"Espada","valor":4},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":10},{"palo":"Oro","valor":7},{"palo":"Basto","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Oro","valor":2},{"palo":"Basto","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Oro","valor":3},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)
  # los metodos de las flores son privados
  # deberia testearse en pdt

def test_fix_envido_mano_es_el_ultimo():
  data = '{"puntuacion":20,"puntajes":{"Azul":10,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":5,"turno":3,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Basto","valor":1},{"palo":"Basto","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":11},{"palo":"Basto","valor":3},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":1},{"palo":"Espada","valor":10},{"palo":"Basto","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":4},{"palo":"Copa","valor":12},{"palo":"Basto","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":10},{"palo":"Copa","valor":7},{"palo":"Espada","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Copa","valor":1},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":4},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("renzo Envido")
  p.cmd("andres Envido")

  p.cmd("richard quiero")
  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO

def test_envido_mano_se_fue():
  data = '{"puntuacion":20,"puntajes":{"Azul":10,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":5,"turno":3,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Basto","valor":1},{"palo":"Basto","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":11},{"palo":"Basto","valor":3},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":1},{"palo":"Espada","valor":10},{"palo":"Basto","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Copa","valor":1},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":10},{"palo":"Copa","valor":7},{"palo":"Espada","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":4},{"palo":"Copa","valor":12},{"palo":"Basto","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":4},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("renzo Envido")
  p.cmd("andres Envido")
  p.cmd("richard mazo")
  p.cmd("renzo quiero")

  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO

def test_flor_blucle():
  p = Partida(20, ["Alvaro"], ["Roro"])  
  mu = Carta(3, "oro")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(2, "Oro"), Carta(6, "Basto"), Carta(7, "Basto") ], # Alvaro tiene flor
    [ Carta(5, "Oro"), Carta(5, "Espada"), Carta(5, "Espada") ], # Roro
  ])

  p.cmd("alvaro flor")

  p.cmd("roro flor")
  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO

def test_quiero_contraflor_desde_mazo():

  p = Partida(20, ["Alvaro", "Adolfo", "Andres"], ["Roro", "Renzo", "Richard"])  
  mu = Carta(3, "oro")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(2, "Oro"), Carta(6, "Basto"), Carta(7, "Basto") ], # Alvaro tiene flor
    [ Carta(5, "Oro"), Carta(5, "Espada"), Carta(5, "Basto") ], # Roro no tiene flor
    [ Carta(1, "Copa"), Carta(2, "Copa"), Carta(3, "Copa") ], # Adolfo tiene flor
    [ Carta(10, "Copa"), Carta(4, "Copa"), Carta(11, "Copa") ], # Renzo no tiene flor
    [ Carta(4, "Oro"), Carta(4, "Espada"), Carta(1, "Espada") ], # Andres tiene  flor
    [ Carta(12, "Copa"), Carta(2, "Oro"), Carta(1, "Basto") ], # Richard no tiene flor
  ])

  p.cmd("alvaro flor")
  p.cmd("andres mazo")

  assert p.ronda.manojos[4].se_fue_al_mazo == True
  p.cmd("renzo contra-flor")

  p.cmd("andres quiero")
  assert p.ronda.envite.cantado_por == "Renzo"
  assert p.ronda.envite.estado == EstadoEnvite.CONTRAFLOR

def test_fix_se_va_al_mazo_y_tenia_flor():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Alvaro"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":6},{"palo":"Espada","valor":10},{"palo":"Espada","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":11},{"palo":"Espada","valor":7},{"palo":"Basto","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":12},{"palo":"Basto","valor":3},{"palo":"Espada","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":7},{"palo":"Oro","valor":7},{"palo":"Basto","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":5},{"palo":"Basto","valor":11},{"palo":"Copa","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":6},{"palo":"Oro","valor":5},{"palo":"Oro","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Espada","valor":5},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  ptsAzul = p.puntajes[Equipo.AZUL]

  p.cmd("alvaro mazo")
  assert p.ronda.manojos[0].se_fue_al_mazo == True
  assert ptsAzul == p.puntajes[Equipo.AZUL]

  p.cmd("roro truco")
  assert p.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN # ??????????

def test_fix_desconcertante():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Alvaro","Renzo"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":3},{"palo":"Espada","valor":2},{"palo":"Espada","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":3},{"palo":"Espada","valor":11},{"palo":"Copa","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":7},{"palo":"Copa","valor":10},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":11},{"palo":"Espada","valor":4},{"palo":"Oro","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":12},{"palo":"Oro","valor":7},{"palo":"Copa","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":6},{"palo":"Oro","valor":3},{"palo":"Copa","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Oro","valor":4},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro flor")
  
  p.cmd("alvaro mazo")
  assert p.ronda.manojos[0].se_fue_al_mazo == False
  
  p.cmd("roro truco")

def test_mala_asignacion_pts():

  p = Partida(20, ["Alvaro"], ["Roro"])  
  mu = Carta(12, "Basto")
  p.ronda.muestra = mu
  p.puntajes[Equipo.ROJO] = 3
  p.puntajes[Equipo.AZUL] = 2
  p.ronda.turno = 1
  p.ronda.el_mano = 1
  p.ronda.set_cartas([
    [ Carta(10, "Oro"), Carta(12, "Oro"), Carta(5, "Espada") ], # Alvaro
    [ Carta(1, "Oro"), Carta(1, "Espada"), Carta(11, "Espada") ], # Roro
  ])

  p.ronda.cachear_flores(True)

  p.cmd("alvaro vale-4")
  p.cmd("alvaro truco") # vigente
  p.cmd("roro truco")
  p.cmd("alvaro re-truco")
  p.cmd("roro vale-4")
  p.cmd("alvaro quiero")
  p.cmd("roro quiero") # <- no hay nada que querer
  p.cmd("roro 1 espada") # <- gana roro
  p.cmd("alvaro 12 oro")
  p.cmd("roro 1 oro") # <- gana roro
  
  p.cmd("alvaro 5 espada")
  # pts Vale4 Ganado = 4
  # puntaje de Rojo deberia ser = 3 + 4
  # puntaje de Azul deberia ser = 2
  assert p.puntajes[Equipo.ROJO] == 3+4 and p.puntajes[Equipo.AZUL] == 2

def test_fix_ronda_nueva():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Renzo"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":3},{"palo":"Copa","valor":1},{"palo":"Espada","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Espada","valor":4},{"palo":"Basto","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Basto","valor":6},{"palo":"Oro","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":11},{"palo":"Oro","valor":10},{"palo":"Oro","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":4},{"palo":"Basto","valor":7},{"palo":"Espada","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":12},{"palo":"Espada","valor":10},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Espada","valor":6},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("renzo flor")
  assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO

  p.cmd("alvaro 1 copa")
  assert p.ronda.manojos[0].get_cant_cartas_tiradas() == 1

  p.cmd("roro truco")
  assert p.ronda.truco.estado == EstadoTruco.TRUCO
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo == Equipo.ROJO

  p.cmd("adolfo re-truco")
  assert p.ronda.truco.estado == EstadoTruco.RETRUCO
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo == Equipo.AZUL

  p.cmd("renzo vale-4")
  assert p.ronda.truco.estado == EstadoTruco.VALE4
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo == Equipo.ROJO

  p.cmd("adolfo quiero")
  assert p.ronda.truco.estado == EstadoTruco.VALE4QUERIDO
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo == Equipo.AZUL

  p.cmd("roro 5 oro")
  assert p.ronda.manojos[1].get_cant_cartas_tiradas() == 1

  p.cmd("adolfo 6 basto")
  assert p.ronda.manojos[2].get_cant_cartas_tiradas() == 1

  with pytest.raises(Exception):
    p.cmd("renzo 19 oro")
  assert p.ronda.manojos[3].get_cant_cartas_tiradas() == 0

  p.cmd("renzo 10 oro")
  assert p.ronda.manojos[3].get_cant_cartas_tiradas() == 1

  p.cmd("andres 4 copa")
  assert p.ronda.manojos[4].get_cant_cartas_tiradas() == 1

  p.cmd("richard 10 espada")
  assert p.ronda.manojos[5].get_cant_cartas_tiradas() == 1
  assert p.ronda.manojo(p.ronda.manos[0].ganador).jugador.equipo == Equipo.ROJO

  # segunda mano
  p.cmd("renzo 10 oro")
  assert p.ronda.manojos[3].get_cant_cartas_tiradas() == 1

  p.cmd("andres 7 basto")
  assert p.ronda.manojos[4].get_cant_cartas_tiradas() == 1

  p.cmd("richard 10 espada")
  assert p.ronda.manojos[5].get_cant_cartas_tiradas() == 1

  p.cmd("richard 12 copa")
  assert p.ronda.manojos[5].get_cant_cartas_tiradas() == 2

  p.cmd("alvaro 3 espada")
  assert p.ronda.manojos[0].get_cant_cartas_tiradas() == 2

  p.cmd("roro 4 espada")
  assert p.ronda.manojos[1].get_cant_cartas_tiradas() == 2

  p.cmd("adolfo 2 copa")
  assert p.ronda.manojos[2].get_cant_cartas_tiradas() == 2

  p.cmd("renzo 4 oro")
  assert p.ronda.manojos[3].get_cant_cartas_tiradas() == 2

  p.cmd("andres 5 espada")
  assert p.ronda.manojos[4].get_cant_cartas_tiradas() == 0

  """ 3:flor + 4:vale4 """
  assert p.puntajes[Equipo.ROJO] == 3+4
  assert p.puntajes[Equipo.AZUL] == 0

def test_fix_irse_al_mazo2():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":6},{"palo":"Espada","valor":7},{"palo":"Basto","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":11},{"palo":"Espada","valor":3},{"palo":"Copa","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Oro","valor":5},{"palo":"Espada","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":12},{"palo":"Oro","valor":2},{"palo":"Copa","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":7},{"palo":"Basto","valor":7},{"palo":"Oro","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":12},{"palo":"Copa","valor":3},{"palo":"Espada","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Oro","valor":6},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("renzo flor")
  assert p.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN

  # mano 1
  p.cmd("alvaro envido")
  assert p.ronda.envite.estado == EstadoEnvite.ENVIDO

  p.cmd("alvaro 6 basto")
  assert p.ronda.manojos[0].get_cant_cartas_tiradas() == 0

  p.cmd("roro 11 oro")
  assert p.ronda.manojos[1].get_cant_cartas_tiradas() == 0

  p.cmd("adolfo 2 basto")
  assert p.ronda.manojos[2].get_cant_cartas_tiradas() == 0

  p.cmd("renzo 12 oro")
  assert p.ronda.manojos[3].get_cant_cartas_tiradas() == 0

  p.cmd("andres 7 copa")
  assert p.ronda.manojos[4].get_cant_cartas_tiradas() == 0

  p.cmd("richard 12 basto")
  assert p.ronda.manojos[5].get_cant_cartas_tiradas() == 0

  # mano 2
  p.cmd("roro 3 espada")
  p.cmd("adolfo 5 oro")
  p.cmd("renzo 2 oro")
  p.cmd("andres 7 basto")
  p.cmd("richard truco")
  p.cmd("renzo quiero")
  p.cmd("andres re-truco")
  p.cmd("richard vale-4")
  p.cmd("alvaro quiero")

  p.cmd("roro mazo")
  assert p.ronda.manojos[1].se_fue_al_mazo == True

def test_fix_decir_quiero():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Renzo"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":1},{"palo":"Copa","valor":6},{"palo":"Oro","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":7},{"palo":"Copa","valor":12},{"palo":"Oro","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":11},{"palo":"Espada","valor":2},{"palo":"Espada","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":10},{"palo":"Espada","valor":12},{"palo":"Basto","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Basto","valor":3},{"palo":"Basto","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":2},{"palo":"Basto","valor":6},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":2},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("renzo flor")

  p.cmd("alvaro truco")
  assert p.ronda.truco.estado == EstadoTruco.TRUCO

  p.cmd("renzo quiero")
  assert p.ronda.truco.estado == EstadoTruco.TRUCOQUERIDO

  p.cmd("alvaro re-truco")
  assert p.ronda.truco.estado == EstadoTruco.TRUCOQUERIDO
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo == Equipo.ROJO

  p.cmd("renzo re-truco")

  p.cmd("alvaro vale-4")
  assert p.ronda.truco.estado == EstadoTruco.VALE4

  p.cmd("alvaro quiero")
  assert p.ronda.truco.estado == EstadoTruco.VALE4
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo == Equipo.AZUL

  p.cmd("renzo re-truco")
  assert p.ronda.truco.estado == EstadoTruco.VALE4
  assert p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo == Equipo.AZUL

def test_fix_panic_no_quiero():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Alvaro","Renzo"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":1},{"palo":"Basto","valor":10},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":4},{"palo":"Espada","valor":6},{"palo":"Basto","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":2},{"palo":"Copa","valor":5},{"palo":"Basto","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":4},{"palo":"Oro","valor":12},{"palo":"Oro","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":7},{"palo":"Oro","valor":11},{"palo":"Oro","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":10},{"palo":"Copa","valor":2},{"palo":"Basto","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Oro","valor":1},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro flor")
  p.cmd("alvaro 1 basto")
  p.cmd("renzo flor")
  ptsPostFlor = p.puntajes[Equipo.ROJO]
  p.cmd("alvaro 1 basto")
  p.cmd("roro 4 copa")
  p.cmd("adolfo 2 espada")
  p.cmd("renzo 4 oro") # la Primera mano la gana renzo
  p.cmd("andres 7 espada")
  
  p.cmd("richard 10 copa")
  assert p.ronda.manojo(p.ronda.manos[0].ganador).jugador.equipo == Equipo.ROJO

  p.cmd("renzo 12 oro")
  p.cmd("andres 11 oro") # la seguna mano la gana andres
  p.cmd("richard 2 copa")
  p.cmd("alvaro 10 basto")
  p.cmd("roro 6 espada")

  p.cmd("adolfo 5 copa")
  assert p.ronda.manojo(p.ronda.manos[1].ganador).jugador.equipo == Equipo.AZUL

  p.cmd("andres 3 oro")
  p.cmd("richard truco")
  p.cmd("richard mazo")
  p.cmd("alvaro quiero")
  p.cmd("alvaro re-truco")
  p.cmd("renzo quiero")
  p.cmd("roro vale-4")

  p.cmd("andres no-quiero")
  assert p.puntajes[Equipo.ROJO] == ptsPostFlor+3

def test_fix_carta_ya_jugada():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Richard"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":2},{"palo":"Oro","valor":4},{"palo":"Basto","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":4},{"palo":"Espada","valor":5},{"palo":"Basto","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":10},{"palo":"Espada","valor":3},{"palo":"Oro","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":6},{"palo":"Oro","valor":2},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":7},{"palo":"Basto","valor":3},{"palo":"Copa","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Oro","valor":6},{"palo":"Oro","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Oro","valor":11},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro 2 espada")
  p.cmd("roro 4 copa")
  p.cmd("adolfo 10 copa")
  p.cmd("renzo 6 copa")
  p.cmd("andres 7 copa")
  p.cmd("richard flor")
  p.cmd("richard 5 oro")

  p.cmd("richard 5 oro")
  assert p.ronda.get_el_turno().jugador.id == "Richard"

def test_fix_truco_no_quiero():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":3},{"palo":"Copa","valor":7},{"palo":"Espada","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":12},{"palo":"Basto","valor":2},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":4},{"palo":"Copa","valor":5},{"palo":"Copa","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":7},{"palo":"Espada","valor":3},{"palo":"Espada","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":10},{"palo":"Espada","valor":2},{"palo":"Copa","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":11},{"palo":"Espada","valor":7},{"palo":"Oro","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Espada","valor":10},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro truco")

  p.cmd("roro no-quiero")
  assert p.puntajes[Equipo.AZUL] > 0

def test_perspectiva():
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Richard"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Copa","valor":7},{"palo":"Basto","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Copa","valor":6},{"palo":"Oro","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":11},{"palo":"Espada","valor":1},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":3},{"palo":"Basto","valor":7},{"palo":"Oro","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Basto","valor":12},{"palo":"Espada","valor":10}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Espada","valor":5},{"palo":"Espada","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Espada","valor":3},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)
  # per, _ = p.Perspectiva("Alvaro")

def test_parda_sig_turno1():
  # si va parda, el siguiente turno deberia ser del mano
  # o del mas cercano a este
  p = Partida(20, ["Alvaro", "Adolfo", "Andres"], ["Roro", "Renzo", "Richard"])  
  mu = Carta(1, "Espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "Copa"), Carta(12, "Oro"), Carta(5, "Copa") ], # Alvaro envido: 26
    [ Carta(3, "Copa"), Carta(4, "Copa"), Carta(4, "Oro") ], # Roro envido: 27
    [ Carta(2, "Copa"), Carta(1, "Copa"), Carta(6, "Espada") ], # Adolfo envido: 28
    [ Carta(2, "Basto"), Carta(3, "Oro"), Carta(6, "Oro") ], # Renzo envido: 25
    [ Carta(3, "Basto"), Carta(7, "Basto"), Carta(6, "Copa") ], # Andres envido: 33
    [ Carta(12, "Copa"), Carta(11, "Copa"), Carta(6, "Basto") ], # Richard envido: 20
  ])
  p.ronda.cachear_flores(True)

  p.cmd("Alvaro 5 Copa")
  p.cmd("Roro 4 Copa")
  # los siguientes 4: todos tiran 6 -> resulta mano parda
  p.cmd("Adolfo 6 Espada")
  p.cmd("Renzo 6 Oro")
  p.cmd("Andres 6 Copa")
  p.cmd("Richard 6 Basto")


  assert p.ronda.manos[0].resultado == Resultado.EMPARDADA

  assert p.ronda.get_el_turno().jugador.id == "Adolfo"

def test_parda_sig_turno2():
  # igual que el anterior pero ahora adolfo se va al mazo
  # si va parda, el siguiente turno deberia ser del mano
  # o del mas cercano a este
  p = Partida(20, ["Alvaro", "Adolfo", "Andres"], ["Roro", "Renzo", "Richard"])  
  mu = Carta(1, "Espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "Copa"), Carta(12, "Oro"), Carta(5, "Copa") ], # Alvaro envido: 26
    [ Carta(3, "Copa"), Carta(4, "Copa"), Carta(4, "Oro") ], # Roro envido: 27
    [ Carta(2, "Copa"), Carta(1, "Copa"), Carta(6, "Espada") ], # Adolfo envido: 28
    [ Carta(2, "Basto"), Carta(3, "Oro"), Carta(6, "Oro") ], # Renzo envido: 25
    [ Carta(3, "Basto"), Carta(7, "Basto"), Carta(6, "Copa") ], # Andres envido: 33
    [ Carta(12, "Copa"), Carta(11, "Copa"), Carta(6, "Basto") ], # Richard envido: 20
  ])
  p.ronda.cachear_flores(True)

  p.cmd("Alvaro 5 Copa")
  p.cmd("Roro 4 Copa")
  # los siguientes 4: todos tiran 6 -> resulta mano parda
  p.cmd("Adolfo 6 Espada")
  p.cmd("Adolfo mazo")
  p.cmd("Renzo 6 Oro")
  p.cmd("Andres 6 Copa")

  p.cmd("Richard 6 Basto")
  assert p.ronda.manos[0].resultado == Resultado.EMPARDADA
  assert p.ronda.get_el_turno().jugador.id == "Renzo"

def test_parda_sig_turno3():
  # igual que el anterior pero ahora todos los que empardaron se van al mazo
  # si va parda, el siguiente turno deberia ser del mano
  # o del mas cercano a este
  p = Partida(20, ["Alvaro", "Adolfo", "Andres"], ["Roro", "Renzo", "Richard"])  
  mu = Carta(1, "Espada")
  p.ronda.muestra = mu
  p.ronda.set_cartas([
    [ Carta(7, "Copa"), Carta(12, "Oro"), Carta(5, "Copa") ], # Alvaro envido: 26
    [ Carta(3, "Copa"), Carta(4, "Copa"), Carta(4, "Oro") ], # Roro envido: 27
    [ Carta(2, "Copa"), Carta(1, "Copa"), Carta(6, "Espada") ], # Adolfo envido: 28
    [ Carta(2, "Basto"), Carta(3, "Oro"), Carta(6, "Oro") ], # Renzo envido: 25
    [ Carta(3, "Basto"), Carta(7, "Basto"), Carta(6, "Copa") ], # Andres envido: 33
    [ Carta(4, "Basto"), Carta(11, "Copa"), Carta(6, "Basto") ], # Richard envido: 20
  ])

  p.cmd("Alvaro 5 Copa")
  # assert enco.Contains(enco.Collect(out), enco.TirarCarta) # ??????????
  p.cmd("Roro 4 Copa")
  # los siguientes 4: todos tiran 6 -> resulta mano parda
  p.cmd("Adolfo 6 Espada")
  p.cmd("Adolfo mazo")
  p.cmd("Renzo 6 Oro")
  p.cmd("Renzo mazo")
  p.cmd("Andres 6 Copa")
  p.cmd("Andres mazo")
  p.cmd("Richard 4 Basto")
  
  # ojo no imprime nada porque la aterior ya consumio el out
  p.cmd("Richard mazo")
  assert p.ronda.manos[0].resultado == Resultado.EMPARDADA
  assert p.ronda.get_el_turno().jugador.id == "Roro"
  assert p.ronda.manojos[5].se_fue_al_mazo == True

def test_fix_truco_deshabilita_envido():
  # cantar truco (sin siquiera ser querido) deshabilita el envido
  # cuando en la vida real es posible tocar "el envido esta primero"
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":2,"Rojo":2},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":5},{"palo":"Copa","valor":4},{"palo":"Copa","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Basto","valor":7},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Espada","valor":7},{"palo":"Oro","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Oro","valor":2},{"palo":"Espada","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":11},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("Alvaro truco")
  assert p.ronda.truco.estado == EstadoTruco.TRUCO

  # el envido esta primero!!
  p.cmd("Roro envido")
  # assert !enco.Contains(enco.Collect(out), enco.Error) # ??????????
  assert p.ronda.envite.estado == EstadoEnvite.ENVIDO

def test_abandono():
  # simulacro de un jugador abandonando
  data = '{"puntuacion":20,"puntajes":{"Azul":2,"Rojo":3},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":2,"Rojo":2},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":5},{"palo":"Copa","valor":4},{"palo":"Copa","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Basto","valor":7},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Espada","valor":7},{"palo":"Oro","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":2},{"palo":"Oro","valor":2},{"palo":"Espada","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":11},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("Alvaro truco")
  assert p.ronda.truco.estado == EstadoTruco.TRUCO

  # el envido esta primero!!
  p.abandono("Adolfo")
  assert p.terminada()
  assert p.puntajes[Equipo.ROJO] == p.puntuacion

def test_fix_orden_canto_flor():
  # simulacro de un jugador abandonando
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Alvaro","Renzo","Andres"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":12},{"palo":"Espada","valor":7},{"palo":"Espada","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":11},{"palo":"Espada","valor":11},{"palo":"Espada","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":6},{"palo":"Oro","valor":10},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":11},{"palo":"Oro","valor":3},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":4},{"palo":"Copa","valor":3},{"palo":"Copa","valor":6}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":4},{"palo":"Copa","valor":12},{"palo":"Basto","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":7},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("alvaro flor")
  p.cmd("renzo flor")
  p.cmd("andres flor")
  # assert enco.Contains(enco.Collect(out), enco.DiceSonBuenas) # ?????????

def test_fix_tester2():
  # simulacro de un jugador abandonando
  data = '{"puntuacion":30,"puntajes":{"Azul":27,"Rojo":23},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":2,"Rojo":2},"elMano":2,"turno":3,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Alvaro"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":12},{"palo":"Basto","valor":5},{"palo":"Basto","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":3},{"palo":"Espada","valor":1},{"palo":"Oro","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":6},{"palo":"Copa","valor":7},{"palo":"Espada","valor":12}],"tiradas":[false,true,false],"ultimaTirada":1,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":3},{"palo":"Copa","valor":12},{"palo":"Basto","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}}],"muestra":{"palo":"Oro","valor":5},"manos":[{"resultado":"ganoRojo","ganador":"","cartasTiradas":[{"jugador":"Adolfo","carta":{"palo":"Copa","valor":7}}]},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  from .printer import renderizar
  print(renderizar(p))

  p.cmd("Adolfo no-quiero")
  p.cmd("Adolfo 7 Copa")
  p.cmd("Roro 3 Oro")
  p.cmd("Renzo contra-flor-al-resto")
  p.cmd("Roro 7 Oro")
  p.cmd("Alvaro flor")

def test_fix_flor_no_cantada():
  # Roro tiene flor y aun asi es capaz de tira carta sin cantarla
  # no deberia ser posible; primero debe cantar la flor
  data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":2,"Rojo":2},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Roro"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":4},{"palo":"Espada","valor":2},{"palo":"Basto","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":1},{"palo":"Basto","valor":10},{"palo":"Basto","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":1},{"palo":"Basto","valor":5},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":5},{"palo":"Basto","valor":6},{"palo":"Copa","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}}],"muestra":{"palo":"Basto","valor":12},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
  p = Partida.parse(data)

  p.cmd("Alvaro 2 Basto")
  roro = p.manojo("Roro")

  # aa = pdt.Chi(p.Partida, roro) # ?????????????
  # p.cmd("Roro 4 Basto")

