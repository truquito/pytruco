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
OBERVACIONES:

2p -> 4p -> 6p :: go
iters: 100% -> 49% -> 32% 
ram: 100% -> 102% -> 102%

2p -> 4p -> 6p :: py
iters: 100% -> 54% -> 36% 
ram: 100% -> 100% -> 100%


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