from pytruco.enco.codmsg import CodMsg
from pytruco.enco.message import Message
from pytruco.pdt.equipo import Equipo
from pytruco.pdt.jugada import ResponderQuiero, ResponderNoQuiero
from pytruco.perspectiva.perspectiva import Perspectiva

# 4p: "activer1" (seat 0, azul) holds a real flor (three espada); "activer3"
# (seat 2, azul) doesn't; the opponents' hands are masked.
PERS_4P = '{"puntuacion":20,"puntajes":{"azul":0,"rojo":0},"ronda":{"manoEnJuego":0,"cantJugadoresEnJuego":{"azul":2,"rojo":2},"elMano":0,"turno":0,"envite":{"estado":"noCantadoAun","puntaje":0,"cantadoPor":"","sinCantar":[]},"truco":{"cantadoPor":"","estado":"noGritadoAun"},"manojos":[{"seFueAlMazo":false,"cartas":[{"palo":"espada","valor":3},{"palo":"espada","valor":4},{"palo":"espada","valor":5}],"tiradas":[false,false,false],"ultimaTirada":-1,"jugador":{"id":"activer1","equipo":"azul"}},{"seFueAlMazo":false,"cartas":[null,null,null],"tiradas":[false,false,false],"ultimaTirada":-1,"jugador":{"id":"opp2","equipo":"rojo"}},{"seFueAlMazo":false,"cartas":[{"palo":"oro","valor":2},{"palo":"basto","valor":4},{"palo":"copa","valor":10}],"tiradas":[false,false,false],"ultimaTirada":-1,"jugador":{"id":"activer3","equipo":"azul"}},{"seFueAlMazo":false,"cartas":[null,null,null],"tiradas":[false,false,false],"ultimaTirada":-1,"jugador":{"id":"opp4","equipo":"rojo"}}],"mixs":{"activer1":0,"opp2":1,"activer3":2,"opp4":3},"muestra":{"palo":"copa","valor":3},"manos":[{"resultado":"indeterminado","ganador":"","cartasTiradas":[]},{"resultado":"indeterminado","ganador":"","cartasTiradas":[]},{"resultado":"indeterminado","ganador":"","cartasTiradas":[]}]},"limiteEnvido":1}'


def test_mazo_folded_florero_no_longer_blocks_teammate():
  # The server's fold drops the folding player from sin_cantar /
  # jugadores_con_flor and decrements cant_jugadores_en_juego; Perspectiva
  # used to only set se_fue_al_mazo, so a folded teammate's unsung flor kept
  # blocking my quiero/no-quiero (possibly leaving no legal action at all).
  pers = Perspectiva("activer1", PERS_4P)
  assert pers.p.ronda.envite.sin_cantar == ["activer1"]

  pers.aplicar(Message(CodMsg.MAZO, "activer1"))

  assert pers.p.manojo("activer1").se_fue_al_mazo
  assert pers.p.ronda.envite.sin_cantar == []
  assert all(m.jugador.id != "activer1" for m in pers.p.ronda.envite.jugadores_con_flor)
  assert pers.p.ronda.cant_jugadores_en_juego[Equipo.AZUL] == 1

  # the opponents call truco: activer3 must be able to answer
  pers.aplicar(Message(CodMsg.GRITAR_TRUCO, "opp2"))
  _, ok_quiero = ResponderQuiero("activer3").ok(pers.p)
  _, ok_no_quiero = ResponderNoQuiero("activer3").ok(pers.p)
  assert ok_quiero
  assert ok_no_quiero
