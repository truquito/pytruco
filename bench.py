from multiprocessing import Process, Queue
import traceback
import sys
from datetime import datetime, timedelta 

from pdt.partida import Partida
from pdt.chi import random_action, is_done

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

def worker(ix:int, tic: datetime, running_time: datetime, queue:Queue):
  res = self_play(tic, running_time)
  queue.put(res)

tic = datetime.now()
running_time = timedelta(minutes=10)
q = Queue()
processes = []
rets = []
t = 16

for ix in range(t):
  p = Process(target=worker, args=(ix,tic,running_time,q))
  processes += [p]
  p.start()

print(f"Running {t} processes for {running_time}...")

for p in processes:
  ret = q.get() # will block
  rets += [ret]

for p in processes:
  p.join()

total = sum(rets)
print(f"total {total}", str(datetime.now() - tic)[:-7])


"""
2p :: go (single)
809_434 10m0s
796_575 10m0s
795_242 10m0s
794_358 10m0s TIME:600.20 RAM:54256

2p :: py (single)
57_158 1000 0:10:00
56_540 1000 0:10:00
56_855 1000 0:10:00
55_796 1000 0:10:00 TIME:600.05 RAM:17488
56_582 0:10:00 TIME:600.07 RAM:17420 (sin el try)

----------------------

4p :: go (single)
398_415 10m0s TIME:600.21 RAM:55360

4p :: py (single)
30_500 1000 0:10:00 TIME:600.05 RAM:17376

----------------------

6p :: go (single)
262_517 10m0s TIME:600.22 RAM:55140

6p :: py (single)
20_695 1000 0:10:00 TIME:600.06 RAM:17464

========================

Observaciones:

2p -> 4p -> 6p :: go
iters: 100% -> 49% -> 32% 
ram: 100% -> 102% -> 102%

2p -> 4p -> 6p :: py
iters: 100% -> 54% -> 36% 
ram: 100% -> 100% -> 100%
"""

# ################################

"""
py_multithread vs py_multiprocessing:

  multithread:
    thread #0 did 921
    921 (0:00:10)

    thread #1 did 473
    thread #0 did 470
    total=943 (0:00:10)

  multiprocessing
    All 2 processes done
    1876 (0:00:10)
    TIME:10.06 RAM:18172

goroutines
  t=1 total 6874 5s
  t=2 total 9345 5s
  t=3 total 10309 5s
  t=4 total 10201 5s
  t=5 total 8971 5s
  t=6 total 8576 5s
  t=7 total 7880 5s
  t=8 total 7651 5s
  t=9 total 7625 5s
  TIME:45.25 RAM:54584
"""

# ################################

"""
2p :: go (16 GOROUTINES for 10m)
929_762 10m0s
938_311 10m0s

----------------------

2p :: go (3 GOROUTINES for 10m)
1_222_178 10m0s
 - Package id 0:  +30.0°C

----------------------

2p :: go (16 PROCS @ 12600k)
total 7_363_010 10m0s procs 600 (96% de cluster@24)
Package id 0:  +70.0°C
2p :: go (1 PROCS @ 12600k)
total 796_989 10m0s procs 600

----------------------

2p :: go (24 PROCS @ clusteruy)
total 7_662_908 10m4s procs 600
2p :: go (1 PROCS @ clusteruy)
total 356_081 10m0s procs 600
 
----------------------

2p :: py (16 processes for 10m)
435_739
 - Package id 0:  +75.0°C

"""

# ################################


"""
OBERVACIONES:

[rule-of-thumb] go single thread vs parallel:
 - actual: 7_363_010 / (795_242*16) = 58% vs 75% de una proyeccion lineal

[rule-of-thumb] python single thread vs parallel:
 - actual: 435_739/(56_540*16) = 48% vs 75% de una proyeccion lineal
 
conclusions:
  - single_py vs single_go = 56_855 / 795_242    = 7.15%
  - parall_py vs parall_go = 435_739 / 7_363_010 = 5.92%

  - multi3_go vs parall16_go = 1_222_178 / 7_363_010 = 17%
  - parall_py vs single_go = 435739 / 796575 = 54%

thumb-of-rule:
  - parall16_go vs single_go = 7_363_010 / 795242 = 9.25X (esperado 12x=75%16t)
  - parall16_py vs single_py = 435_739 / 56_855 = 7.66X (esperado 12x=75%16t)
"""