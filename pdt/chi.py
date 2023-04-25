import random

from enco.packet import Packet
from enco.codmsg import CodMsg
from .partida import IJugada, Partida
from .manojo import Manojo
from .jugada import TirarCarta, TocarEnvido, TocarRealEnvido, TocarFaltaEnvido, \
CantarFlor, CantarContraFlor, CantarContraFlorAlResto, GritarTruco, \
GritarReTruco, GritarVale4, ResponderQuiero, ResponderNoQuiero, IrseAlMazo

""" retorna `True` si una ronda ha terminado segun una lista de `Packet`"""
def is_done(pkts:list[Packet]) -> bool:
  dones = [CodMsg.NUEVA_PARTIDA, CodMsg.NUEVA_RONDA, CodMsg.RONDA_GANADA]
  return any(pkt.message.codmsg in dones for pkt in pkts)

def random_action_chi(chi:list[IJugada]) -> int:
  return random.randrange(len(chi))

"""
en el primer parametro de salida retorna un indice de manojo random
en el segundo retorna una jugada random de este manojo
"""
def random_action_chis(chis:list[list[IJugada]]) -> tuple[int, int]:
  # hago un cambio de variable:
  # tomo en cuenta solo aquellos chi's que tengan al menos una accion habilitada
  # lo almaceno como un slice de mix's
  habilitados = [mix for mix, chi in enumerate(chis) if len(chi) > 0]
  r_habilitado_ix = random.randrange(len(habilitados))
  rmix = habilitados[r_habilitado_ix]
  raix = random.randrange(len(chis[rmix]))
  return rmix, raix

# Retorna todas las acciones posibles para un jugador `m` dado
def chi(p:Partida, m:Manojo, allow_mazo=True) -> list[IJugada]:

  res :list[IJugada] = []

  # tirada de cartas
  res += [t for c in m.cartas if (t := TirarCarta(m.jugador.id, c)).ok(p)[1]]

  # jugadas "simples"
  simples :list[IJugada] = [
    TocarEnvido(m.jugador.id),
    TocarRealEnvido(m.jugador.id),
    TocarFaltaEnvido(m.jugador.id),
    CantarFlor(m.jugador.id),
    CantarContraFlor(m.jugador.id),
    CantarContraFlorAlResto(m.jugador.id),
    GritarTruco(m.jugador.id),
    GritarReTruco(m.jugador.id),
    GritarVale4(m.jugador.id),
    ResponderQuiero(m.jugador.id),
    ResponderNoQuiero(m.jugador.id),
    IrseAlMazo(m.jugador.id),
  ]

  if not allow_mazo:
    simples = simples[:-1]

  res += [j for j in simples if (valid := j.ok(p)[1])]

  return res

""" Retorna TODAS las jugadas posibles de cada jugador """
""" OJO: puede haber jugadores con vectore chi vacios """
def chis(p:Partida, allow_mazo=True) -> list[list[IJugada]]:
  return [chi(p, m, allow_mazo) for m in p.ronda.manojos]

def random_action(p:Partida, allow_mazo=True):
  aas = chis(p, allow_mazo)
  aas = [aa for aa in aas if len(aa) > 0]
  aa = random.choice(aas)
  return random.choice(aa)