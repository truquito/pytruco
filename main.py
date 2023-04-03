from pdt.jugador import Jugador
from pdt.carta import Carta, Palo
# import equipo from pdt
from pdt import equipo

j1 = Jugador(id="Anna", equipo=equipo.Equipo.AZUL)
j2 = Jugador(id="Bob", equipo=equipo.Equipo.ROJO)
js = [j1,j2]

# print(js)

import jsonpickle
d = jsonpickle.encode(js, unpicklable=False, make_refs=False)
print(d)

c1 = Carta(12, Palo.BASTO)
c2 = Carta(7, Palo.ORO)
c3 = Carta(7, "oro")

