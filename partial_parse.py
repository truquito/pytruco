from pdt.partida import Partida
from pdt.chi import random_action, is_done, chis, chi


from enco.razon import Razon
from enco.message import Message
from enco.codmsg import CodMsg
from pdt.partida import Partida, CartaTirada
from pdt.envite import EstadoEnvite
from pdt.truco import EstadoTruco
from pdt.mano import NumMano, Resultado
from pdt.carta import Carta
import json

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", 
                    help="increase output verbosity", 
                    action="store_true")
args = parser.parse_args()


def aplicar(minombre :str, msg :Message, p :Partida):
  # if msg.cod == CodMsg.ABANDONO:
  #   pass
  # if msg.cod == CodMsg.TIMEOUT:
  #   pass
  # if msg.cod == CodMsg.BYEBYE:
  #   pass
  if msg.cod == CodMsg.DICE_SON_BUENAS:
    # sé qué equipo ganó el envite
    p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
  if msg.cod == CodMsg.CANTAR_FLOR:
    p.ronda.envite.estado = EstadoEnvite.FLOR
    p.ronda.envite.cantado_por = msg.cont
  if msg.cod == CodMsg.CANTAR_CONTRAFLOR:
    p.ronda.envite.estado = EstadoEnvite.CONTRAFLOR
    p.ronda.envite.cantado_por = msg.cont
  if msg.cod == CodMsg.CANTAR_CONTRAFLOR_AL_RESTO:
    p.ronda.envite.estado = EstadoEnvite.CONTRAFLORALRESTO
    p.ronda.envite.cantado_por = msg.cont
  if msg.cod == CodMsg.TOCAR_ENVIDO:
    p.ronda.envite.estado = EstadoEnvite.ENVIDO
    p.ronda.envite.cantado_por = msg.cont
  if msg.cod == CodMsg.TOCAR_REALENVIDO:
    p.ronda.envite.estado = EstadoEnvite.REALENVIDO
    p.ronda.envite.cantado_por = msg.cont
  if msg.cod == CodMsg.TOCAR_FALTAENVIDO:
    p.ronda.envite.estado = EstadoEnvite.FALTAENVIDO
    p.ronda.envite.cantado_por = msg.cont
  if msg.cod == CodMsg.GRITAR_TRUCO:
    p.ronda.truco.estado = EstadoTruco.TRUCO
    p.ronda.truco.cantado_por = msg.cont
  if msg.cod == CodMsg.GRITAR_RETRUCO:
    p.ronda.truco.estado = EstadoTruco.RETRUCO
    p.ronda.truco.cantado_por = msg.cont
  if msg.cod == CodMsg.GRITAR_VALE4:
    p.ronda.truco.estado = EstadoTruco.VALE4
    p.ronda.truco.cantado_por = msg.cont
  if msg.cod == CodMsg.NO_QUIERO:
    if p.ronda.envite.estado != EstadoEnvite.DESHABILITADO:
      p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
    else:
      # si es al truco al que le esta diciendo `NO_QUIERO` entonces deberia de
      # empezar una nueva ronda.
      # enotnces antes de tomar una accion deberia esperar un tiempo asi le doy
      # tiempo a que lleguen los otros mensajes 
      pass
  if msg.cod == CodMsg.CON_FLOR_ME_ACHICO:
    p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
  if msg.cod == CodMsg.QUIERO_TRUCO:
    if p.ronda.truco.estado == EstadoTruco.TRUCO:
      p.ronda.truco.estado = EstadoTruco.TRUCOQUERIDO
    elif p.ronda.truco.estado == EstadoTruco.RETRUCO:
      p.ronda.truco.estado = EstadoTruco.RETRUCOQUERIDO
    elif p.ronda.truco.estado == EstadoTruco.VALE4:
      p.ronda.truco.estado = EstadoTruco.VALE4QUERIDO
    p.ronda.truco.cantado_por = msg.cont # <--- que tipo de cont
  if msg.cod == CodMsg.QUIERO_ENVITE:
    # p.ronda.envite.estado = # el estado queda igual ?
    # se pasaria a evaluar
    p.ronda.envite.cantado_por = msg.cont
    p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
  if msg.cod == CodMsg.SIG_TURNO:
    p.ronda.turno = msg.cont
  if msg.cod == CodMsg.SIG_TURNO_POSMANO:
    p.ronda.mano_en_juego = NumMano.inc(p.ronda.mano_en_juego)
    p.ronda.turno = msg.cont
  # if msg.cod == CodMsg.DICE_TENGO:
  #   pass
  if msg.cod == CodMsg.DICE_SON_MEJORES:
    # doy por ganado el envite
    p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
    p.ronda.envite.cantado_por = msg.cont["autor"]
  if msg.cod == CodMsg.NUEVA_PARTIDA:
    data = json.dumps(msg.cont) # me viene un dict
    p = Partida.parse(data)
  if msg.cod == CodMsg.NUEVA_RONDA:
    data = json.dumps(msg.cont) # me viene un dict
    p = Partida.parse(data)
  if msg.cod == CodMsg.TIRAR_CARTA:
    jid, palo, valor = msg.cont["autor"], msg.cont["palo"], msg.cont["valor"]
    m = p.ronda.manojo(jid)
    c = Carta(valor, palo)
    # si no es de mi equipo, entonces supongo que la carta es desconocida
    # le asigno cualquier slot
    es_de_equipo_contrario = m.jugador.equipo != p.manojo(minombre).jugador.equipo
    if es_de_equipo_contrario:
      # entonces uso el primer slot
      for i,x in enumerate(m.cartas):
        if x == None:
          m.ultima_tirada = i
          m.tiradas[i] = True
          m.cartas[i] = c
          break
    else:
      for i,x in enumerate(m.cartas):
        if x == c:
          m.ultima_tirada = i
          m.tiradas[i] = True
          break
    # tambien la agrego a la mano/tiradas
    p.ronda.get_mano_actual().agregar_tirada(CartaTirada(jid, c))
  if msg.cod == CodMsg.SUMA_PTS:
    jid, pts = msg.cont["autor"], msg.cont["valor"]
    p.puntajes[p.ronda.manojo(jid).jugador.equipo] += pts
    # ahora la razon pude contener info importante:
    
    if msg.cont["razon"] in [Razon.ENVIDO_GANADO, Razon.REALENVIDO_GANADO, 
                             Razon.FALTA_ENVIDO_GANADO, Razon.ENVITE_NO_QUERIDO, 
                             Razon.FLOR_ACHICADA, Razon.LA_UNICA_FLOR, 
                             Razon.LAS_FLORES, Razon.LA_FLOR_MASALTA, 
                             Razon.CONTRAFLOR_GANADA, 
                             Razon.CONTRAFLOR_AL_RESTO_GANADA]:
      p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
    if msg.cont["razon"] == [Razon.TRUCO_NO_QUERIDO, Razon.TRUCO_QUERIDO, 
                             Razon.SE_FUERON_AL_MAZO]:
      # no hago nada
      pass
  if msg.cod == CodMsg.MAZO:
    p.ronda.manojo(msg.cont).se_fue_al_mazo = True
  if msg.cod == CodMsg.EL_ENVIDO_ESTA_PRIMERO:
    p.ronda.envite.estado = EstadoEnvite.ENVIDO
    p.ronda.envite.cantado_por = msg.cont
    p.ronda.truco.estado = EstadoTruco.NOCANTADO
  if msg.cod == CodMsg.LA_MANO_RESULTA_PARDA:
    p.ronda.get_mano_actual().resultado = Resultado.EMPARDADA
  if msg.cod == CodMsg.MANO_GANADA:
    p.ronda.get_mano_actual().ganador = msg.cont["autor"]
  if msg.cod == CodMsg.RONDA_GANADA:
    # ???? que voy a hacer
    pass

# original
data_orig = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":3},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":1,"Rojo":1},"elMano":0,"turno":0,"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["annon#1025"]},"truco":{"cantadoPor":"","estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":5},{"palo":"Copa","valor":12},{"palo":"Oro","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"juampi","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":10},{"palo":"Basto","valor":5},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"annon#1025","equipo":"Rojo"}}],"mixs":{"annon#1025":1,"juampi":0},"muestra":{"palo":"Basto","valor":12},"manos":[{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null}]}}'
# partial jp #2
data_jp = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":3},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":1,"Rojo":1},"elMano":0,"turno":0,"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["annon#1025"]},"truco":{"cantadoPor":"","estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":5},{"palo":"Copa","valor":12},{"palo":"Oro","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"juampi","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[null,null,null],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"annon#1025","equipo":"Rojo"}}],"mixs":{"annon#1025":1,"juampi":0},"muestra":{"palo":"Basto","valor":12},"manos":[{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null}]}}'
# partial annon #2
data_annon = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":3},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":1,"Rojo":1},"elMano":0,"turno":0,"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["annon#1025"]},"truco":{"cantadoPor":"","estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[null,null,null],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"juampi","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":10},{"palo":"Basto","valor":5},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"annon#1025","equipo":"Rojo"}}],"mixs":{"annon#1025":1,"juampi":0},"muestra":{"palo":"Basto","valor":12},"manos":[{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null}]}}'

jug0 = "juampi"
jug1 = "annon#1025"
names = [jug0, jug1]

# parse ?
# p = Partida.parse(data_orig)
# p0 = Partida.parse(data_jp)
# p1 = Partida.parse(data_annon)

# if args.verbose: print("orig")
# if args.verbose: print(p)
# if args.verbose: print("="*80)
# if args.verbose: print("jp")
# if args.verbose: print(p0)
# if args.verbose: print("="*80)
# if args.verbose: print("annon")
# if args.verbose: print(p1)
# if args.verbose: print("="*80)
for _ in range(1000):
  p = Partida(puntuacion=20,
              azules=[jug0], 
              rojos=[jug1], 
              dummy=False, 
              verbose=True)
  p0 = Partida.parse(p.perspectiva(jug0).to_json())
  p1 = Partida.parse(p.perspectiva(jug1).to_json())

  actions = []

  import random

  wtf = False

  # random.seed(42)

  num_jugadas = 0

  while not p.terminada():
    try:

      if num_jugadas == 30: # 30
        if args.verbose: print("reaching")

      # supongo que ambas son analogas, a menos de la info privada
      # tomo como rho al que tenga la mayor cantidad de acciones a tomar

      # ANTES:
      # aas = chis(p_jp, allow_mazo=False)
      # lens = [len(aa) for aa in aas]
      # mayor_idx = lens.index(max(lens))
      # a = random.choice(aas[mayor_idx])

      # AHORA:
      aa0 = chi(p0, p0.manojo(jug0), allow_mazo=False)
      aa1 = chi(p1, p1.manojo(jug1), allow_mazo=False)
      # quien tiene mas opciones de jugada?
      aa = aa0 if len(aa0) >= len(aa1) else aa1
      jug_idx = 0 if len(aa0) >= len(aa1) else 1
      jug_name = jug0 if jug_idx == 0 else jug1
      alt_name = jug1 if jug_idx == 0 else jug0
      p_chosen = p0 if jug_idx == 0 else p1
      p_alt = p1 if jug_idx == 0 else p0
      # elijo una accion al azar
      a = random.choice(aa)

      # esta accion la ejecuto donde corresponde, en p
      actions += [str(a)]
      if args.verbose: print(a)

      try:
        pkts = a.hacer(p)
        num_jugadas += 1
      except Exception as e:
        if args.verbose: print(e)
        pkts = a.hacer(p_chosen)

      # ahora tengo que aplicar estos `Envelopes` a los otros
      for env in pkts:
        for dest in env.destination:
          # si esta destinado a "TODOS" o al usuario "alt", entonces le actualizo su perspectiva
          if env.message.cod == CodMsg.NUEVA_PARTIDA:
            import sys
            if args.verbose: print("se termino !!!!!!!!!!!")
            sys.exit(0)
          if env.message.cod in [CodMsg.NUEVA_RONDA, CodMsg.NUEVA_PARTIDA]:
            aux = Partida.parse(json.dumps(env.message.cont))
            if dest == jug0:
              p0 = aux
            else:
              p1 = aux
          else: 
            if dest in ["ALL", jug_name]:
              aplicar(jug_name, env.message, p_chosen)
            if dest in ["ALL", alt_name]:
              aplicar(alt_name, env.message, p_alt)

      # vuelvo a castear los punteros p y p_alt por si los originales (p0 y p1) hayan cambiado
      p_chosen = p0 if jug_idx == 0 else p1
      p_alt = p1 if jug_idx == 0 else p0 

      if args.verbose: print(f"como quedo la perspectiva de original (num_jugadas:{num_jugadas})")
      if args.verbose: print(p)
      # if args.verbose: print(p.to_json())
      if args.verbose: print("="*80)
      if args.verbose: print(f"como quedo la perspectiva de {jug_name}")
      if args.verbose: print(p_chosen)
      # if args.verbose: print(p_chosen.to_json())
      if args.verbose: print("="*80)
      if args.verbose: print(f"como quedo la perspectiva de {alt_name}")
      if args.verbose: print(p_alt)
      # if args.verbose: print(p_alt.to_json())
      if args.verbose: print("="*80)
      if args.verbose: print("="*80)
      if args.verbose: print("="*80)
      # import sys
      # sys.exit(0)


      
      if arranca_ronda_nueva := is_done(pkts):
        actions = []

    except Exception as e:
      import traceback
      if args.verbose: print("="*80)
      if args.verbose: print(actions)
      if args.verbose: print("="*80)
      traceback.print_exc()
      import sys
      sys.exit(0)

    if p0.terminada():
      break;

print("ce fini")