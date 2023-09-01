import json
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-v", "--verbose", 
                    help="increase output verbosity", 
                    action="store_true")
args = parser.parse_args()

from pdt.partida import Partida
from pdt.chi import is_done, chi, chis
from enco.codmsg import CodMsg
from pdt.partida import Partida


from perspectiva.perspectiva import Perspectiva

# parse ?
# original
# data_orig = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":3},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":1,"Rojo":1},"elMano":0,"turno":0,"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["annon#1025"]},"truco":{"cantadoPor":"","estado":"noGritadoAun"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":5},{"palo":"Copa","valor":12},{"palo":"Oro","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"juampi","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":10},{"palo":"Basto","valor":5},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"annon#1025","equipo":"Rojo"}}],"mixs":{"annon#1025":1,"juampi":0},"muestra":{"palo":"Basto","valor":12},"manos":[{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null}]}}'
# partial jp #2
# data_jp = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":3},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":1,"Rojo":1},"elMano":0,"turno":0,"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["annon#1025"]},"truco":{"cantadoPor":"","estado":"noGritadoAun"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":5},{"palo":"Copa","valor":12},{"palo":"Oro","valor":5}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"juampi","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[null,null,null],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"annon#1025","equipo":"Rojo"}}],"mixs":{"annon#1025":1,"juampi":0},"muestra":{"palo":"Basto","valor":12},"manos":[{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null}]}}'
# partial annon #2
# data_annon = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":3},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":1,"Rojo":1},"elMano":0,"turno":0,"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["annon#1025"]},"truco":{"cantadoPor":"","estado":"noGritadoAun"},"manojos":[{"seFueAlMazo":false,"cartas":[null,null,null],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"juampi","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":10},{"palo":"Basto","valor":5},{"palo":"Oro","valor":12}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"annon#1025","equipo":"Rojo"}}],"mixs":{"annon#1025":1,"juampi":0},"muestra":{"palo":"Basto","valor":12},"manos":[{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null}]}}'

# data_orig = '{"puntuacion": 20, "puntajes": {"Azul": 0, "Rojo": 0}, "ronda": {"manoEnJuego": 0, "cantJugadoresEnJuego": {"Rojo": 1, "Azul": 1}, "elMano": 0, "turno": 0, "envite": {"estado": "noCantadoAun", "puntaje": 0, "cantadoPor": "", "sinCantar": []}, "truco": {"cantadoPor": "", "estado": "noGritadoAun"}, "manojos": [{"seFueAlMazo": false, "cartas": [{"palo": "Oro", "valor": 12}, {"palo": "Espada", "valor": 6}, {"palo": "Espada", "valor": 7}], "tiradas": [false, false, false], "ultimaTirada": -1, "jugador": {"id": "juampi", "equipo": "Azul"}}, {"seFueAlMazo": false, "cartas": [{"palo": "Oro", "valor": 6}, {"palo": "Espada", "valor": 3}, {"palo": "Oro", "valor": 5}], "tiradas": [false, false, false], "ultimaTirada": -1, "jugador": {"id": "annon#1025", "equipo": "Rojo"}}], "mixs": {"juampi": 0, "annon#1025": 1}, "muestra": {"palo": "Copa", "valor": 7}, "manos": [{"resultado": "ganoRojo", "ganador": "", "cartasTiradas": null}, {"resultado": "ganoRojo", "ganador": "", "cartasTiradas": null}, {"resultado": "ganoRojo", "ganador": "", "cartasTiradas": null}]}}'

jug0 = "juampi"
jug1 = "annon#1025"

# p = Partida.parse(data_orig)
# p0 = Partida.parse(data_jp)
# p1 = Partida.parse(data_annon)

def print_every_p(p :Partida, p_chosen :Perspectiva, p_alt :Perspectiva):
  print("orig")
  print(p)
  print(p.to_json())
  print("="*80)
  print(f"perspectiva de {p.ronda.manojos[0].jugador.id}")
  print(p_chosen.p)
  print(p_chosen.p.to_json())
  print("="*80)
  print(f"perspectiva de {p.ronda.manojos[1].jugador.id}")
  print(p_alt.p)
  print(p_alt.p.to_json())
  print("="*80)

# random.seed(42)

total = 1_000
next_hit = 0

for i in range(total+1):

  if i == next_hit:
    next_hit += total / 10
    progres_pct = round((i / total) * 100)
    print(f"{progres_pct}%")

  p = Partida(puntuacion=20, azules=[jug0], rojos=[jug1], dummy=False, verbose=True)
  p0 = Perspectiva(jug0, p.perspectiva(jug0).to_json())
  p1 = Perspectiva(jug1, p.perspectiva(jug1).to_json())

  last_snap = p.to_json()
  actions = []
  num_jugadas = 0

  while not p.terminada():
    try:

      # if num_jugadas == 30: # 30
      #   if args.verbose: print("reaching")

      # AHORA:
      aa0 = p0.chi(allow_mazo=False)
      aa1 = p1.chi(allow_mazo=False)
      aas = chis(p, allow_mazo=False)
      # checkeo de correctitud
      ok = len(aas[0]) == len(aa0) and len(aas[1]) == len(aa1)
      if not ok:
        print("los chis no coinciden")
        print(last_snap)
        print(actions)
        print(p)
        print(f"chis: {aas}")
        print(f"chi jug0: {aa0}")
        print(f"chi jug1: {aa1}")
        chis(p, allow_mazo=False)
        p0.chi(allow_mazo=False)
        p1.chi(allow_mazo=False)
        raise Exception("los chis no coinciden")
      # quien tiene mas opciones de jugada?
      aa = aa0 if len(aa0) >= len(aa1) else aa1
      jug_idx = 0 if len(aa0) >= len(aa1) else 1
      jug_name,alt_name = (jug0,jug1) if jug_idx == 0 else (jug1,jug0)
      p_chosen, p_alt = (p0,p1) if jug_idx == 0 else (p1,p0)
      # elijo una accion al azar
      a = random.choice(aa)

      # esta accion la ejecuto donde corresponde, en p
      actions += [str(a)]
      if args.verbose: print(a)

      pkts = a.hacer(p)
      num_jugadas += 1

      # ahora tengo que aplicar estos `Envelopes` a los otros
      for env in pkts:
        for dest in env.destination:
          # si esta destinado a "TODOS" o al usuario "alt", entonces le actualizo su perspectiva
          if env.message.cod == CodMsg.NUEVA_PARTIDA:
            raise Exception("nueva partida")
          if env.message.cod in [CodMsg.NUEVA_RONDA, CodMsg.NUEVA_PARTIDA]:
            last_snap = p.to_json()
            # aux = Partida.parse(json.dumps(env.message.cont))
            if dest == jug0:
              p0.p = Partida.parse(json.dumps(env.message.cont))
            else:
              p1.p = Partida.parse(json.dumps(env.message.cont))
          else: 
            if dest in ["ALL", jug_name]:
              p_chosen.aplicar(env.message)
            if dest in ["ALL", alt_name]:
              p_alt.aplicar(env.message)

      # vuelvo a castear los punteros p y p_alt por si los originales (p0 y p1) hayan cambiado
      p_chosen = p0 if jug_idx == 0 else p1
      p_alt = p1 if jug_idx == 0 else p0 

      if args.verbose: print(f"(num_jugadas:{num_jugadas})")
      if args.verbose: print_every_p(p, p_chosen, p_alt)
      
      if arranca_ronda_nueva := is_done(pkts):
        actions = []

    except Exception as e:
      import traceback
      print("="*80)
      print(last_snap)
      print(actions)
      print("="*80)
      traceback.print_exc()
      import sys
      sys.exit(0)

    if p.terminada():
      break;

print("ce fini")