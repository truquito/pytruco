# pytruco

`pytruco` is a pure Python Uruguayan Truco engine, simulator, and library.

## Install

```sh
pip install pytruco
```

### Example

```py
from pytruco.pdt.partida import Partida

p = Partida(
    puntuacion    = 20,
    azules        = ["Alice", "Ariana"],
    rojos         = ["Bob", "Ben"],
    verbose       = True,
    limite_envido = 4
)

print(p)

print(p.cmd("alice envido"))
print(p.cmd("bob quiero"))
print(p.cmd("ariana truco"))
print(p.cmd("ben quiero"))
```

### Random walker example

```py
from pytruco.pdt.partida import Partida
from pytruco.pdt.chi import chis
import random

def random_action(p:Partida, allow_mazo=True):
  aas = chis(p, allow_mazo)
  aas = [aa for aa in aas if len(aa) > 0]
  aa = random.choice(aas)
  return random.choice(aa)

p = Partida(
    puntuacion    = 20,
    azules        = ["Alice", "Ariana"],
    rojos         = ["Bob", "Ben"],
    verbose       = True,
    limite_envido = 4
)

print(p)

while not p.terminada():
    a = random_action(p, allow_mazo=False)
    pkts = a.hacer(p)
    print(f"{a} -> {pkts}")
```