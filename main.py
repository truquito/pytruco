from pdt.equipo import Equipo
from pdt.jugador import Jugador
from pdt.carta import Carta, Palo
from pdt.manojo import Manojo
from pdt.ronda import Ronda
from pdt.partida import Partida
from pdt.envite import EstadoEnvite
from pdt.mano import NumMano, Resultado

# j1 = Jugador("Anna", Equipo.AZUL)
# j2 = Jugador("Bob", Equipo.ROJO)
# js = [j1,j2]

# print(js)

# import jsonpickle
# d = jsonpickle.encode(js, unpicklable=False)
# print(d)

# # cartas
# c1 = Carta(12, Palo.BASTO)
# c2 = Carta(7, Palo.COPA)
# c3 = Carta(7, "oro")
# cs = [c1, c2, c3]

# # jugador
# j1 = Jugador("Anna", Equipo.AZUL)
# j2 = Jugador("Bob", Equipo.ROJO)

# m1 = Manojo(j1)
# m1.cartas = cs
# print(m1)
# print(m1.get_carta_idx(Carta(7, "oro")))

# azules = ["alice", "ariana", "annie"]
# rojos = ["bob", "ben", "bill"]
# r = Ronda(azules, rojos)

# from enco.message import Message
# from enco.codmsg import CodMsg

# m = Message(
#     CodMsg.BYEBYE,
#     data={"foo": 123, "bar": "el-pepe"}
# )

# d = jsonpickle.encode(m, unpicklable=False)
# print(d)

# p = Partida(20, ["alice"], ["bob"])
  
# muestra = Carta(1, "espada")
# p.ronda.muestra = muestra
# p.ronda.set_cartas([
#     [ Carta(7, "oro"), Carta(6, "oro"), Carta(5, "copa") ],
#     [ Carta(1, "copa"), Carta(2, "oro"), Carta(3, "basto") ],
# ])

# print(p.manojo("alice").calcular_envido(muestra))
# print(p.manojo("bob").calcular_envido(muestra))

# p.cmd("alice envido")
# p.cmd("bob quiero")

""""""
# et = Partida(20, ["Alvaro", "Adolfo", "Andres"], ["Roro", "Renzo", "Richard"])  
# mu = Carta(3, "oro")
# et.ronda.muestra = mu
# et.ronda.set_cartas([
#   [ Carta(2, "Oro"), Carta(6, "Basto"), Carta(7, "Basto") ], # Alvaro tiene flor
#   [ Carta(5, "Oro"), Carta(5, "Espada"), Carta(5, "Basto") ], # Roro no tiene flor
#   [ Carta(1, "Copa"), Carta(2, "Copa"), Carta(3, "Copa") ], # Adolfo tiene flor
#   [ Carta(4, "Oro"), Carta(4, "Espada"), Carta(1, "Espada") ], # Renzo tiene flor
#   [ Carta(10, "Copa"), Carta(7, "Oro"), Carta(11, "Basto") ], # Andres no tiene  flor
#   [ Carta(10, "Oro"), Carta(2, "Oro"), Carta(1, "Basto") ], # Richard tiene flor
# ])

# # print(p)

# # no deberia dejarlo cantar envido xq tiene flor
# et.cmd("Alvaro Envido")
# assert et.ronda.envite.estado != EstadoEnvite.ENVIDO

# # deberia retornar un error debido a que ya canto flor
# pkts = et.cmd("Alvaro Flor")
# for pkt in pkts:
#   print(pkt)

# # deberia dejarlo irse al mazo
# et.cmd("Roro Mazo")
# assert et.ronda.manojos[1].se_fue_al_mazo == True

# # deberia retornar un error debido a que ya canto flor
# et.cmd("Adolfo Flor")

# # deberia aumentar la apuesta
# et.cmd("Renzo Contra-flor")
# assert et.ronda.envite.estado == EstadoEnvite.CONTRAFLOR

# et.cmd("Alvaro Quiero")

# data = '{"puntuacion":20,"puntajes":{"Azul":3,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":2,"Rojo":2},"elMano":1,"turno":2,"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Ariana"]},"truco":{"cantadoPor":"","estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":4},{"palo":"Basto","valor":1},{"palo":"Basto","valor":11}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alice","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":2},{"palo":"Copa","valor":5},{"palo":"Copa","valor":7}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Bob","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":3},{"palo":"Oro","valor":7},{"palo":"Oro","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Ariana","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":11},{"palo":"Basto","valor":6},{"palo":"Copa","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Ben","equipo":"Rojo"}}],"mixs":{"Alice":0,"Ariana":2,"Ben":3,"Bob":1},"muestra":{"palo":"Oro","valor":5},"manos":[{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null},{"resultado":"ganoRojo","ganador":"","cartasTiradas":null}]}}'
# p = Partida.parse(data)

data = '{"puntuacion":20,"puntajes":{"Azul":0,"Rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"Azul":3,"Rojo":3},"elMano":0,"turno":0,"pies":[0,0],"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":["Richard"]},"truco":{"cantadoPor":null,"estado":"noCantado"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":6},{"palo":"Basto","valor":12},{"palo":"Oro","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Alvaro","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":5},{"palo":"Basto","valor":10},{"palo":"Oro","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Roro","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Oro","valor":10},{"palo":"Copa","valor":10},{"palo":"Basto","valor":2}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Adolfo","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Basto","valor":6},{"palo":"Espada","valor":10},{"palo":"Basto","valor":3}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Renzo","equipo":"Rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"Copa","valor":6},{"palo":"Copa","valor":3},{"palo":"Espada","valor":1}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Andres","equipo":"Azul"}},{"seFueAlMazo":false,"cartas":[{"palo":"Espada","valor":3},{"palo":"Espada","valor":11},{"palo":"Espada","valor":4}],"tiradas":[false,false,false],"ultimaTirada":0,"jugador":{"id":"Richard","equipo":"Rojo"}}],"muestra":{"palo":"Oro","valor":1},"manos":[{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null},{"resultado":"ganoRojo","ganador": "","cartasTiradas":null}]}}'
p = Partida.parse(data)

p.cmd("alvaro envido")
# assert p.ronda.envite.estado == EstadoEnvite.DESHABILITADO
# assert p.puntajes[Equipo.ROJO] == 3

p.cmd("alvaro 6 espada")
p.cmd("alvaro 6 espada")
p.cmd("roro 5 espada")
p.cmd("adolfo 10 oro")
p.cmd("renzo 6 basto")
p.cmd("andres 6 copa")
p.cmd("richard 3 espada")
p.cmd("adolfo 10 copa")
p.cmd("renzo 10 espada")
p.cmd("andres 3 copa")
p.cmd("richard 11 espada")
p.cmd("alvaro 12 basto")
p.cmd("roro 10 basto")