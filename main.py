from pdt.jugador import Jugador
# import equipo from pdt
from pdt import equipo

j1 = Jugador(id="Anna", equipo=equipo.AZUL)
j2 = Jugador(id="Bob", equipo=equipo.ROJO)
js = [j1,j2]

print(js)

import jsonpickle
d = jsonpickle.encode(js, unpicklable=False)
print(d)