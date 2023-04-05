from pdt.equipo import Equipo
from pdt.jugador import Jugador
from pdt.carta import Carta, Palo
from pdt.manojo import Manojo
from pdt.ronda import Ronda

j1 = Jugador("Anna", Equipo.AZUL)
j2 = Jugador("Bob", Equipo.ROJO)
js = [j1,j2]

# print(js)

import jsonpickle
d = jsonpickle.encode(js, unpicklable=False)
print(d)

# cartas
c1 = Carta(12, Palo.BASTO)
c2 = Carta(7, Palo.COPA)
c3 = Carta(7, "oro")
cs = [c1, c2, c3]

# jugador
j1 = Jugador("Anna", Equipo.AZUL)
j2 = Jugador("Bob", Equipo.ROJO)

m1 = Manojo(j1)
m1.cartas = cs
print(m1)
print(m1.get_carta_idx(Carta(7, "oro")))

azules = ["alice", "ariana", "annie"]
rojos = ["bob", "ben", "bill"]
r = Ronda(azules, rojos)

from enco.message import Message
from enco.codmsg import CodMsg

m = Message(
    CodMsg.BYEBYE,
    data={"foo": 123, "bar": "el-pepe"}
)

d = jsonpickle.encode(m, unpicklable=False)
print(d)