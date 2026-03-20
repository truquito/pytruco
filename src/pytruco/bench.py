import argparse
from multiprocessing import Process, Queue
import traceback
import sys
from datetime import datetime, timedelta

from pytruco.pdt.partida import Partida
from pytruco.pdt.chi import random_action, is_done

azules = ["Alice", "Ariana", "Annie"]
rojos = ["Bob", "Ben", "Bill"]


def parse_args():
  parser = argparse.ArgumentParser()
  parser.add_argument(
    "-n",
    type=int,
    choices=[2, 4, 6],
    default=2,
    help="total number of players (allowed: 2, 4, 6)")
  parser.add_argument(
    "-t",
    "--timeout",
    type=int,
    default=600,
    help="benchmark duration in seconds")
  parser.add_argument(
    "-p",
    type=int,
    default=16,
    help="number of parallel worker processes")
  return parser.parse_args()


def self_play(tic: datetime, running_time: timedelta, n: int) -> int:
  t = 0
  while datetime.now() - tic < running_time:
    p = Partida(20, azules[:n >> 1], rojos[:n >> 1], verbose=False)
    last_snapshot, actions = p.to_json(), []
    while not p.terminada():
      try:
        a = random_action(p, allow_mazo=False)
        actions += [str(a)]
        pkts = a.hacer(p)

        if is_done(pkts):
          last_snapshot = p.to_json()
          actions = []

      except Exception:
        print(last_snapshot)
        print(actions)
        traceback.print_exc()
        sys.exit(0)

      if p.terminada():
        t += 1
        break

  return t


def worker(ix: int, tic: datetime, running_time: timedelta, n: int, queue: Queue):
  res = self_play(tic, running_time, n)
  queue.put(res)


def main():
  args = parse_args()

  if args.p < 1:
    raise ValueError("-p must be >= 1")

  tic = datetime.now()
  running_time = timedelta(seconds=args.timeout)
  q = Queue()
  processes = []
  rets = []

  for ix in range(args.p):
    p = Process(target=worker, args=(ix, tic, running_time, args.n, q))
    processes += [p]
    p.start()

  print(f"Running {args.p} processes for {running_time} with n={args.n}...")

  for p in processes:
    ret = q.get()
    rets += [ret]

  for p in processes:
    p.join()

  total = sum(rets)
  print(f"total {total}", str(datetime.now() - tic)[:-7])


if __name__ == "__main__":
  main()
