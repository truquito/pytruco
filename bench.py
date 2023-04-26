from pdt.partida import Partida
import traceback
import sys
from pdt.chi import random_action, is_done
from datetime import datetime, timedelta 

n = 2 # <-- num. of players
azules = ["Alice", "Ariana", "Annie"]
rojos = ["Bob", "Ben", "Bill"]

def self_play(tic: datetime, running_time: datetime) -> int:
  t = 0
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
        print(last_snapshot)
        print(actions)
        traceback.print_exc()
        sys.exit(0)

      if p.terminada():
        t += 1
        break;
  
  return t

def worker(ix:int, tic: datetime, running_time: datetime, outs):
  res = self_play(tic, running_time)
  print(f"thread #{ix} did {res}")
  outs[ix] = res

"""
tiempos
"""
tic = datetime.now()
running_time = timedelta(seconds=10)

import threading
t = 2
threads = list()
outs = [0 for _ in range(t)]

for ix in range(t):
  x = threading.Thread(target=worker, args=(ix,tic,running_time,outs))
  threads.append(x)
  x.start()

print(f"Running {t} threads...")

for ix, thread in enumerate(threads):
  thread.join()

print(f"All {t} threads done")
total = sum(outs)
print(total, str(datetime.now() - tic)[:-7])


"""
2p :: go
809_434 10m0s
796_575 10m0s
795_242 10m0s
794_358 10m0s TIME:600.20 RAM:54256

2p :: py
57_158 1000 0:10:00
56_540 1000 0:10:00
56_855 1000 0:10:00
55_796 1000 0:10:00 TIME:600.05 RAM:17488
56_582 0:10:00 TIME:600.07 RAM:17420 (sin el try)

----------------------

4p :: go
398_415 10m0s TIME:600.21 RAM:55360

4p :: py
30_500 1000 0:10:00 TIME:600.05 RAM:17376

----------------------

6p :: go
262_517 10m0s TIME:600.22 RAM:55140

6p :: py
20_695 1000 0:10:00 TIME:600.06 RAM:17464

========================

2p -> 4p -> 6p :: go
iters: 100% -> 49% -> 32% 
ram: 100% -> 102% -> 102%

2p -> 4p -> 6p :: py
iters: 100% -> 54% -> 36% 
ram: 100% -> 100% -> 100%
"""


"""
multithread vs single thead:

thread #1 did 473
thread #0 did 470
943 0:00:10

thread #0 did 921
921 0:00:10
"""