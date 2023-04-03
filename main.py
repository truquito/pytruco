from pdt.jugador import Jugador

j1 = Jugador(id="Anna", equipo="Rojo")
j2 = Jugador(id="Bob", equipo="Azul")
js = [j1,j2]

print(js)

import jsonpickle
d = jsonpickle.encode(js, unpicklable=False)
print(d)