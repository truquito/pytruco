from pdt.partida import Partida
from pdt.chi import random_action, is_done
from datetime import datetime, timedelta 

n = 2 # <-- num. of players
azules = ["Alice", "Ariana", "Annie"]
rojos = ["Bob", "Ben", "Bill"]
# p = Partida(20, azules[:n>>1], rojos[:n>>1], verbose=False)
# p = Partida.parse('{"puntuacion": 20, "puntajes": {"Azul": 0, "Rojo": 0}, "ronda": {"manoEnJuego": 0, "cantJugadoresEnJuego": {"Rojo": 1, "Azul": 1}, "elMano": 0, "turno": 0, "envite": {"estado": "noCantadoAun", "puntaje": 0, "cantadoPor": "", "sinCantar": []}, "truco": {"cantadoPor": "", "estado": "noGritadoAun"}, "manojos": [{"seFueAlMazo": false, "cartas": [{"palo": "Espada", "valor": 10}, {"palo": "Basto", "valor": 5}, {"palo": "Copa", "valor": 5}], "tiradas": [false, false, false], "ultimaTirada": -1, "jugador": {"id": "Alice", "equipo": "Azul"}}, {"seFueAlMazo": false, "cartas": [{"palo": "Oro", "valor": 11}, {"palo": "Espada", "valor": 4}, {"palo": "Oro", "valor": 4}], "tiradas": [false, false, false], "ultimaTirada": -1, "jugador": {"id": "Bob", "equipo": "Rojo"}}], "mixs": {"Alice": 0, "Bob": 1}, "muestra": {"palo": "Basto", "valor": 4}, "manos": [{"resultado": "ganoRojo", "ganador": "", "cartasTiradas": null}, {"resultado": "ganoRojo", "ganador": "", "cartasTiradas": null}, {"resultado": "ganoRojo", "ganador": "", "cartasTiradas": null}]}}')
# print(p)
# print(p.to_json(), end="\n\n")

tic = datetime.now()
t = 0
running_time = timedelta(seconds=10)

while datetime.now() - tic < running_time:
  p = Partida(20, azules[:n>>1], rojos[:n>>1], verbose=False)
  last_snapshot, actions  = p.to_json(), []
  while not p.terminada():
    try:
      a = random_action(p, allow_mazo=False)
      actions += [str(a)]
      pkts = a.hacer(p)
      
      if arranca_ronda_nueva := is_done(pkts):
        last_snapshot = p.to_json()
        actions = []

    except Exception as e:
      import traceback
      print("="*80)
      print(last_snapshot)
      print("="*80)
      print(actions)
      print("="*80)
      traceback.print_exc()
      import sys
      sys.exit(0)

    if p.terminada():
      t += 1
      break;

print(t, str(datetime.now() - tic)[:-7])

