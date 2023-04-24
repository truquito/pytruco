from pdt.equipo import Equipo
from pdt.jugador import Jugador
from pdt.carta import Carta, Palo
from pdt.manojo import Manojo
from pdt.ronda import Ronda
from pdt.partida import Partida
from pdt.envite import EstadoEnvite
from pdt.mano import NumMano, Resultado
from pdt.printer import renderizar

p = Partida(20, ["Alice"], ["Bob"])
print(renderizar(p))