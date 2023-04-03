from pdt.jugador import Jugador
# import equipo from pdt
from pdt import equipo

j1 = Jugador(id="Anna", equipo=equipo.Equipo.AZUL)
j2 = Jugador(id="Bob", equipo=equipo.Equipo.ROJO)
js = [j1,j2]

# print(js)

import jsonpickle
d = jsonpickle.encode(js, unpicklable=False, make_refs=False)
print(d)