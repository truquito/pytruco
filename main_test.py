from multiprocessing import Process, Queue
import traceback
import sys
from datetime import datetime, timedelta 

from pdt.partida import Partida
from pdt.chi import random_action, is_done

n = 6 # <-- num. of players
azules = ["Alice", "Ariana", "Annie"]
rojos = ["Bob", "Ben", "Bill"]

tic = datetime.now()
running_time = timedelta(minutes=35)
t = 0

print(f"running for {running_time} starting at {str(tic)[:-10]}")

while datetime.now() - tic < running_time:
  p = Partida(20, azules[:n>>1], rojos[:n>>1], verbose=False)
  last_snapshot, actions  = p.to_json(), []
  while not p.terminada():
    try:
      a = random_action(p, allow_mazo=False)
      actions += [str(a)]
      pkts = a.hacer(p)
      
      if arranca_ronda_nueva := is_done(pkts):
        last_snapshot, actions = p.to_json(), []

    except Exception as e:
      print(last_snapshot)
      print(actions)
      traceback.print_exc()
      sys.exit(0)

    if p.terminada():
      t += 1
      break;

print(f"total {t}", str(datetime.now() - tic)[:-7])
