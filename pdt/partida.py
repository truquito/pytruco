from __future__ import annotations
from typing import Dict
import re
import json

from .equipo import Equipo
from .ronda import Ronda
from .jugador import Jugador
from .manojo import Manojo
from .envite import EstadoEnvite
from .truco import EstadoTruco
from .mano import NumMano, Resultado, CartaTirada
from .carta import Carta
from .jugadas import IJUGADA_ID

from enco.packet import Packet
from enco.message import Message
from enco.codmsg import CodMsg
from enco.razon import Razon

# IJugada Interface para las jugadas
class IJugada():
  def id() -> IJUGADA_ID:
    pass
  """retorna `True` si la jugada es valida"""
  def ok(self,p:Partida) -> tuple[list[Packet], bool]:
    pass
  def hacer(self, p:Partida) -> list[Packet]:
    pass
  def __str__(self) -> str:
    pass
  def __repr__(self) -> str:
    return str(self)
  
class Partida():
  def __init__(self, puntuacion:int, azules:list[str], rojos:list[str], dummy=False):
    if puntuacion not in [20,30,40]:
      raise Exception("el valor de la partida no es valido")

    misma_cant_de_jugadores = len(azules) == len(rojos)
    cant_jugadores = len(azules) + len(rojos)
    cant_correcta = cant_jugadores in [2,4,6]
    ok = misma_cant_de_jugadores and cant_correcta
    if not ok:
      raise Exception("la cantidad de jguadores no es correcta")

    self.puntuacion:int = puntuacion
    self.puntajes :Dict[Equipo, int] = {
      Equipo.AZUL: 0,
      Equipo.ROJO: 0,
    }

    self.ronda = Ronda(azules, rojos, dummy)

  """
  
  GETTERs
  
  """
  def manojo(self, jid:str) -> Manojo:
    # primer intento
    m = self.ronda.manojo(jid)
    return m if m is not None else self.ronda.manojo(jid.capitalize())

  def get_max_puntaje(self) -> int:
    return max(self.puntajes.values())

  """retorna el equipo que va ganando"""
  def el_que_va_ganando(self) -> Equipo:
    va_ganando_rojo = self.puntajes[Equipo.ROJO] > self.puntajes[Equipo.AZUL]
    return Equipo.ROJO if va_ganando_rojo else Equipo.AZUL

  """devuelve la mitad de la puntuacion total jugable durante toda la partida"""
  def get_puntuacion_malas(self) -> int:
    return int(self.puntuacion / 2)

  """retorna `True` sii la partida consta de exactamente 2 jugadores"""
  def es_mano_a_mano(self) -> bool:
    return len(self.ronda.manojos) == 2

  """retorna `True` si la partida acabo"""
  def terminada(self) -> bool:
    return self.get_max_puntaje() >= self.puntuacion

  def el_chico(self) -> int:
    return int(self.puntuacion / 2)

  """retorna `True` si `e` esta en malas"""
  def esta_en_malas(self, e:Equipo) -> bool:
    return self.puntajes[e] < self.el_chico()

  """retorna la cantidad de puntos que le falta para ganar al que va ganando"""
  def calc_pts_falta(self) -> int:
    return self.puntuacion - self.puntajes[self.el_que_va_ganando()]

  """retorna la cantidad de puntos que corresponden al Falta-Envido"""
  def calc_pts_falta_envido(self, ganador_del_envite:Equipo) -> int:
    if self.esta_en_malas(self.el_que_va_ganando()):
      lo_que_le_falta_al_GANADOR_para_ganar_el_chico = \
        self.el_chico() - self.puntajes[ganador_del_envite]
      return lo_que_le_falta_al_GANADOR_para_ganar_el_chico

    lo_Que_Le_Falta_Al_QUE_va_GANANDO_para_Ganar_El_Chico = self.calc_pts_falta()
    return lo_Que_Le_Falta_Al_QUE_va_GANANDO_para_Ganar_El_Chico

  """retorna la cantidad de puntos que le corresponderian
  a `ganadorDelEnvite` si hubiese ganado un "Contra flor al resto"
  sin tener en cuenta los puntos acumulados de envites anteriores"""
  def calc_pts_contraflor_al_resto(self, ganadorDelEnvite:Equipo) -> int:
    return self.calc_pts_falta_envido(ganadorDelEnvite)

  """suma pts y ademas retorna true si termino la partida"""
  def suma_puntos(self, e:Equipo, total_pts:int) -> bool:
    self.puntajes[e] += total_pts
    return self.terminada()

  def tocar_envido(self, m:Manojo) -> None:
    # 2 opciones: o bien no se jugo aun
	  # o bien ya estabamos en envido
    ya_Se_Habia_Cantado_El_Envido = self.ronda.envite.estado == EstadoEnvite.ENVIDO
    if ya_Se_Habia_Cantado_El_Envido:
      # se aumenta el puntaje del envido en +2
      self.ronda.envite.puntaje += 2
      self.ronda.envite.cantado_por = m.jugador.id

    else: # no se habia jugado aun
      self.ronda.envite.cantado_por = m.jugador.id
      self.ronda.envite.estado = EstadoEnvite.ENVIDO
      self.ronda.envite.puntaje = 2

  def tocar_real_envido(self, m:Manojo) -> None:
    self.ronda.envite.cantado_por = m.jugador.id
    # 2 opciones:
    # o bien el envido no se jugo aun,
    # o bien ya estabamos en envido
    if self.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN: # no se habia jugado aun
      self.ronda.envite.puntaje = 3
    else: # ya se habia cantado ENVIDO x cantidad de veces
      self.ronda.envite.puntaje += 3
    self.ronda.envite.estado = EstadoEnvite.REALENVIDO

  def tocar_falta_envido(self, m:Manojo) -> None:
    self.ronda.envite.estado = EstadoEnvite.FALTAENVIDO
    self.ronda.envite.cantado_por = m.jugador.id
  
  def cantar_flor(self, m:Manojo) -> None:
    ya_estabamos_en_flor = self.ronda.envite.estado >= EstadoEnvite.FLOR
    if ya_estabamos_en_flor:
      self.ronda.envite.puntaje += 3
      # si estabamos en algo mas grande que `FLOR` -> no lo aumenta
      if self.ronda.envite.estado == EstadoEnvite.FLOR:
        self.ronda.envite.cantado_por = m.jugador.id
        self.ronda.envite.estado = EstadoEnvite.FLOR
    else:
      # se usa por si dicen "no quiero" -> se obtiene el equipo
      # al que pertenece el que la canto en un principio para
      # poder sumarle los puntos correspondientes
      self.ronda.envite.puntaje = 3
      self.ronda.envite.cantado_por = m.jugador.id
      self.ronda.envite.estado = EstadoEnvite.FLOR

  def cantar_contra_flor(self, m:Manojo) -> None:
    self.ronda.envite.estado = EstadoEnvite.CONTRAFLOR
    self.ronda.envite.cantado_por = m.jugador.id
    # ahora la flor pasa a jugarse por 4 puntos
    self.ronda.envite.puntaje = 4
  
  def cantar_contra_flor_al_resto(self, m:Manojo) -> None:
    self.ronda.envite.estado = EstadoEnvite.CONTRAFLORALRESTO
    self.ronda.envite.cantado_por = m.jugador.id
    # ahora la flor pasa a jugarse por 4 puntos
    self.ronda.envite.puntaje = 4 # <- eso es al pedo, es independiente
  
  def gritar_truco(self, m:Manojo) -> None:
    self.ronda.truco.cantado_por = m.jugador.id
    self.ronda.truco.estado = EstadoTruco.TRUCO

  def querer_truco(self, m:Manojo) -> None:
    self.ronda.truco.cantado_por = m.jugador.id
    if self.ronda.truco.estado == EstadoTruco.TRUCO:
      self.ronda.truco.estado = EstadoTruco.TRUCOQUERIDO
    elif self.ronda.truco.estado == EstadoTruco.RETRUCO:
      self.ronda.truco.estado = EstadoTruco.RETRUCOQUERIDO
    elif self.ronda.truco.estado == EstadoTruco.VALE4:
      self.ronda.truco.estado = EstadoTruco.VALE4QUERIDO

  def gritar_retruco(self, m:Manojo) -> None:
    self.ronda.truco.cantado_por = m.jugador.id
    self.ronda.truco.estado = EstadoTruco.RETRUCO
  
  def gritar_retruco(self, m:Manojo) -> None:
      self.ronda.truco.cantado_por = m.jugador.id
      self.ronda.truco.estado = EstadoTruco.RETRUCO

  """manda el manojo al mazo
  todo: esto podria ser un metodo de Ronda, no de partida"""
  def ir_al_mazo(self, m:Manojo) -> None:
    m.se_fue_al_mazo = True
    equipoDelJugador = m.jugador.equipo
    self.ronda.cant_jugadores_en_juego[equipoDelJugador] -= 1
    # lo elimino de los jugadores que tenian flor (si es que tenia)
    if m.jugador.id in self.ronda.envite.sin_cantar:
      self.ronda.envite.sin_cantar.remove(m.jugador.id)
  
  def tirar_carta(self, manojo:Manojo, idx:int) -> None:
    manojo.tiradas[idx] = True
    manojo.ultima_tirada = idx
    carta = manojo.cartas[idx]
    tirada = CartaTirada(manojo.jugador.id, carta)
    self.ronda.get_mano_actual().agregar_tirada(tirada)

  """EvaluarRonda tener siempre en cuenta que evaluar la ronda es sinonimo de
  evaluar el truco
  se acabo la ronda?
  si se empieza una ronda nueva -> retorna true
  si no se termino la ronda 	 -> retorna false"""
  def evaluar_ronda(self) -> tuple[bool, list[Packet]]:
    """
		TENER EN CUENTA:
		===============
		el enum self.ronda.Mano.Resultado \\in {GanoRojo,GanoAzul,Empardada}
		no me dice el resultado per se,
		sino:
			noSeSabe sii (no esta empardada) & (ganador == nil)
		por default dice "ganoRojo"
    """
    pkts:list[Packet] = []

    # A MENOS QUE SE HAYAN IDO TODOS EN LA PRIMERA MANO!!!
    hayJugadoresRojo = self.ronda.cant_jugadores_en_juego[Equipo.ROJO] > 0
    hayJugadoresAzul = self.ronda.cant_jugadores_en_juego[Equipo.AZUL] > 0
    hayJugadoresEnAmbos = hayJugadoresRojo and hayJugadoresAzul
    primeraMano = self.ronda.mano_en_juego == NumMano.PRIMERA

    # o bien que en la primera mano hayan cantado truco y uno no lo quizo
    manoActual = self.ronda.mano_en_juego.to_ix()
    elTrucoNoTuvoRespuesta = self.ronda.truco.estado.es_truco_respondible()
    noFueParda = self.ronda.manos[manoActual].resultado != Resultado.EMPARDADA
    estaManoYaTieneGanador = noFueParda and self.ronda.manos[manoActual].ganador != ""
    elTrucoFueNoQuerido = elTrucoNoTuvoRespuesta and estaManoYaTieneGanador

    elTrucoFueQuerido = not elTrucoFueNoQuerido

    noSeAcabo = (primeraMano and hayJugadoresEnAmbos and elTrucoFueQuerido)
    if noSeAcabo:
      return False, []

    # de aca en mas ya se que hay al menos 2 manos jugadas
    # (excepto el caso en que un equipo haya abandonado)
    # asi que es seguro acceder a los indices 0 y 1 en:
    # self.ronda.manos[0] & self.ronda.manos[1]

    cantManosGanadas :Dict[Equipo,int] = { Equipo.ROJO: 0, Equipo.AZUL: 0 }
    n = self.ronda.mano_en_juego.to_ix()
    for i in range(manoActual+1):
      mano = self.ronda.manos[i]
      if mano.resultado != Resultado.EMPARDADA:
        cantManosGanadas[self.ronda.manojo(mano.ganador).jugador.equipo] += 1

    hayEmpate = cantManosGanadas[Equipo.ROJO] == cantManosGanadas[Equipo.AZUL]
    pardaPrimera = self.ronda.manos[0].resultado == Resultado.EMPARDADA
    pardaSegunda = self.ronda.manos[1].resultado == Resultado.EMPARDADA
    pardaTercera = self.ronda.manos[2].resultado == Resultado.EMPARDADA
    seEstaJugandoLaSegunda = self.ronda.mano_en_juego == NumMano.SEGUNDA

    noSeAcaboAun = seEstaJugandoLaSegunda and hayEmpate and \
      hayJugadoresEnAmbos and not elTrucoFueNoQuerido

    if noSeAcaboAun:
      return False, []
    
    # caso particular:
    # no puedo definir quien gano si la seguna mano no tiene definido un resultado
    segunda = 1
    noEstaEmpardada = self.ronda.manos[segunda].resultado != Resultado.EMPARDADA
    noTieneGanador = self.ronda.manos[segunda].ganador == ""
    segundaManoIndefinida = noEstaEmpardada and noTieneGanador
    # tengo que diferenciar si vengo de: TirarCarta o si vengo de un no quiero:
    # si viniera de un TirarCarta -> en la mano actual (o la anterior)? la ultima carta tirada pertenece al turno actual
    ix_mano_en_juego = self.ronda.mano_en_juego.to_ix()
    n = len(self.ronda.manos[ix_mano_en_juego].cartas_tiradas)
    actual = self.ronda.get_el_turno().jugador.id
    mix = self.ronda.mano_en_juego.to_ix()
    ultimaCartaTiradaPerteneceAlTurnoActual = n > 0 and \
      self.ronda.manos[mix].cartas_tiradas[n-1].jugador == actual
    vengoDeTirarCarta = ultimaCartaTiradaPerteneceAlTurnoActual
    if segundaManoIndefinida and hayJugadoresEnAmbos and vengoDeTirarCarta:
      return False, []

    # hay ganador -> ya se que al final voy a retornar un true
    ganador:str = ""
    
    if not hayJugadoresEnAmbos: # caso particular: todos abandonaron
      # enonces como antes paso por evaluar mano
      # y seteo a ganador de la ultima mano jugada (la "actual")
      # al equipo que no abandono -> lo sacao de ahi
      # caso particular: la mano resulto "empardada pero uno abandono"
      if noFueParda and estaManoYaTieneGanador:
        ganador = self.ronda.get_mano_actual().ganador
      else:
        # el ganador es el primer jugador que no se haya ido al mazo del equipo
        # que sigue en pie
        equipoGanador = Equipo.AZUL if hayJugadoresAzul else Equipo.ROJO
        for m in self.ronda.manojos:
          if (not m.se_fue_al_mazo) and m.jugador.equipo == equipoGanador:
            ganador = m.jugador.id
            break

    # primero el caso clasico: un equipo gano 2 o mas manos
    elif cantManosGanadas[Equipo.ROJO] >= 2:
      # agarro cualquier manojo de los rojos
      # o bien es la Primera o bien la Segunda
      if self.ronda.manojo(self.ronda.manos[0].ganador).jugador.equipo == Equipo.ROJO:
        ganador = self.ronda.manos[0].ganador
      else:
        ganador = self.ronda.manos[1].ganador
      
    elif cantManosGanadas[Equipo.AZUL] >= 2:
      # agarro cualquier manojo de los azules
      # o bien es la Primera o bien la Segunda
      if self.ronda.manojo(self.ronda.manos[0].ganador).jugador.equipo == Equipo.AZUL:
        ganador = self.ronda.manos[0].ganador
      else:
        ganador = self.ronda.manos[1].ganador

    else:

      # si llego aca es porque recae en uno de los
      # siguientes casos: (Obs: se jugo la Tercera)

      # CASO 1. parda Primera -> gana Segunda
      # CASO 2. parda Segunda -> gana Primera
      # CASO 3. parda Tercera -> gana Primera
      # CASO 4. parda Primera & Segunda -> gana Tercera
      # CASO 5. parda Primera, Segunda & Tercera -> gana la mano

      caso1 = pardaPrimera and (not pardaSegunda) and (not pardaTercera)
      caso2 = (not pardaPrimera) and pardaSegunda and (not pardaTercera)
      caso3 = (not pardaPrimera) and (not pardaSegunda) and pardaTercera
      caso4 = pardaPrimera and pardaSegunda and (not pardaTercera)
      caso5 = pardaPrimera and pardaSegunda and pardaTercera

      if caso1:
        ganador = self.ronda.manos[NumMano.to_int(NumMano.SEGUNDA) -1].ganador
      elif caso2:
        ganador = self.ronda.manos[NumMano.to_int(NumMano.PRIMERA) -1].ganador
      elif caso3:
        ganador = self.ronda.manos[NumMano.to_int(NumMano.PRIMERA) -1].ganador
      elif caso4:
        ganador = self.ronda.manos[NumMano.to_int(NumMano.TERCERA) -1].ganador
      elif caso5:
        ganador = self.ronda.get_el_mano().jugador.id

    # ya sabemos el ganador ahora es el
    # momento de sumar los puntos del truco
    totalPts :int = 0

    if self.ronda.truco.estado in [EstadoTruco.NOCANTADO, EstadoTruco.TRUCO]:
      totalPts = 1
    elif self.ronda.truco.estado in [EstadoTruco.TRUCOQUERIDO, EstadoTruco.RETRUCO]:
      totalPts = 2
    elif self.ronda.truco.estado in [EstadoTruco.RETRUCOQUERIDO, EstadoTruco.VALE4]:
      totalPts = 3
    elif self.ronda.truco.estado == EstadoTruco.VALE4QUERIDO:
      totalPts = 4

    
    if not hayJugadoresEnAmbos:

      # `La ronda ha sido ganada por el equipo %s. +%v puntos para el equipo %s 
      # por el %s ganado`
      pkts += [Packet(
        ["ALL"],
        Message(
          CodMsg.RONDA_GANADA,
          data={
            "autor": ganador,
            "razon": Razon.SE_FUERON_AL_MAZO
          })
      )]

    elif elTrucoNoTuvoRespuesta:

      ganador = self.ronda.truco.cantado_por
      razon :Razon = None
      if self.ronda.truco.estado == EstadoTruco.TRUCO:
        razon = Razon.TRUCO_NO_QUERIDO
      elif self.ronda.truco.estado == EstadoTruco.RETRUCO:
        razon = Razon.TRUCO_NO_QUERIDO
      elif self.ronda.truco.estado == EstadoTruco.VALE4:
        razon = Razon.TRUCO_NO_QUERIDO

      # `La ronda ha sido ganada por el equipo %s. +%v puntos para el equipo %s 
      # por el %s no querido`
      pkts += [Packet(
        ["ALL"],
        Message(
          CodMsg.RONDA_GANADA,
          data={
            "autor": ganador,
            "razon": razon
          })
      )]

    else:

      razon :Razon = None
      if self.ronda.truco.estado == EstadoTruco.TRUCO:
        razon = Razon.TRUCO_QUERIDO
      if self.ronda.truco.estado == EstadoTruco.RETRUCO:
        razon = Razon.TRUCO_QUERIDO
      if self.ronda.truco.estado == EstadoTruco.VALE4:
        razon = Razon.TRUCO_QUERIDO

      # `La ronda ha sido ganada por el equipo %s. +%v puntos para el equipo %s 
      # por el %s ganado`
      pkts += [Packet(
        ["ALL"],
        Message(
          CodMsg.RONDA_GANADA,
          data={
            "autor": ganador,
            "razon": razon
          })
      )]

    self.suma_puntos(self.ronda.manojo(ganador).jugador.equipo, totalPts)

    pkts += [Packet(
      ["ALL"],
      Message(
        CodMsg.SUMA_PTS,
        data={
          "autor": ganador,
          "razon": Razon.TRUCO_QUERIDO,
          "valor": totalPts
        })
    )]

    return True, pkts # porque se empezo una nueva ronda

  def evaluar_mano(self) -> tuple[bool, list[Packet]]:
    pkts:list[Packet] = []
    
    # cual es la tirada-carta que gano la mano?
    # ojo que puede salir parda
    # para ello primero busco las maximas de cada equipo
    # y luego comparo entre estas para simplificar
    # Obs: en caso de 2 jugadores del mismo que tiraron
    # una carta con el mismo poder -> se queda con la Primera
    # es decir, la que "gana de mano"
    maxPoder :Dict[Equipo,int] = { Equipo.ROJO: -1, Equipo.AZUL: -1 }
    max :Dict[Equipo,CartaTirada] = { Equipo.ROJO: None, Equipo.AZUL: None }
    tiradas = self.ronda.get_mano_actual().cartas_tiradas

    for i,tirada in enumerate(tiradas):
      poder = tirada.carta.calc_poder(self.ronda.muestra)
      equipo = self.ronda.manojo(tirada.jugador).jugador.equipo
      if poder > maxPoder[equipo]:
        maxPoder[equipo] = poder
        max[equipo] = tiradas[i]

    mano = self.ronda.get_mano_actual()
    esParda = maxPoder[Equipo.ROJO] == maxPoder[Equipo.AZUL]

    # caso particular de parda:
    # cuando nadie llego a tirar ninguna carta y se fueron todos los de 1 equipo
    # entonces la mano es ganada por el equipo contrario al ultimo que se fue

    # FIX: o simplemente cuando un equipo entero quedo con 0 jugadores "en pie"
    noSeLlegoATirarNingunaCarta = len(self.ronda.get_mano_actual().cartas_tiradas) == 0
    seFueronTodos = self.ronda.cant_jugadores_en_juego[Equipo.ROJO] == 0 or \
      self.ronda.cant_jugadores_en_juego[Equipo.AZUL] == 0
    
    if noSeLlegoATirarNingunaCarta or seFueronTodos:

      equipoGanador :Equipo = None
      quedanJugadoresDelRojo = self.ronda.cant_jugadores_en_juego[Equipo.ROJO] > 0
      if quedanJugadoresDelRojo:
        equipoGanador = Equipo.ROJO
        mano.resultado = Resultado.GANO_ROJO
      else:
        equipoGanador = Equipo.AZUL
        mano.resultado = Resultado.GANO_AZUL
      

      # aca le tengo que poner un ganador para despues sacarle el equipo
      # le asigno el primero que encuentre del equipo ganador
      if self.ronda.manojos[0].jugador.equipo == equipoGanador:
        mano.ganador = self.ronda.manojos[0].jugador.id
      else:
        mano.ganador = self.ronda.manojos[1].jugador.id
      

      # todo: MENSAJE ACAAAAAAA!!!

      # fmt.Printf("La %s mano la gano el equipo %s\n",
      # 	strings.ToLower(p.Ronda.ManoEnJuego.String()),
      # 	equipoGanador.String())

    elif esParda:
      mano.resultado = Resultado.EMPARDADA
      mano.ganador = ""
      
      pkts += [Packet(
        ["ALL"],
        Message(
          CodMsg.LA_MANO_RESULTA_PARDA,
          data=None)
      )]

      # no se cambia el turno

    else:

      # esto quedo arreglado en la funcion IrseAlMazo.Ok para evitar que pueda
      # llegar hasta aca

      """
      caso especial:
        2 jugadores, 1 tiro carta y enseguida se fue al mazo

      para 4 o 6 jugadores:
        si era el primero de mi equipo y de todos en tirar:
        todos los de mi equipo se van
        yo tiro y me voy (sin dejar chance que los otros tiren)
        gana mi equipo

      -> no se puede ir al mazo si mi equipo llego a tirar carta y los otros no llegaron a tirar al menos una carta
      """

      tiradaGanadora :CartaTirada = None

      if maxPoder[Equipo.ROJO] > maxPoder[Equipo.AZUL]:
        tiradaGanadora = max[Equipo.ROJO]
        mano.resultado = Resultado.GANO_ROJO
      else:
        tiradaGanadora = max[Equipo.AZUL]
        mano.resultado = Resultado.GANO_AZUL
      

      # el turno pasa a ser el del mano.ganador
      # pero se setea despues de evaluar la ronda
      mano.ganador = self.ronda.manojo(tiradaGanadora.jugador).jugador.id

      pkts += [Packet(
        ["ALL"],
        Message(
          CodMsg.MANO_GANADA,
          data={
          "autor": mano.ganador,
          "valor": self.ronda.mano_en_juego # ?????? <-- en go devuelve `mano_en_juego - 1`
          })
      )]

    # se termino la ronda?
    empiezaNuevaRonda, pkt2 = self.evaluar_ronda()

    pkts += pkt2

    # cuando termina la mano (y no se empieza una ronda) -> cambia de TRUNO
    # cuando termina la ronda -> cambia de MANO
    # para usar esto, antes se debe primero incrementar el turno
    # incremento solo si no se empezo una nueva ronda

    return empiezaNuevaRonda, pkts

  def nueva_ronda(self, el_mano:int) -> None:
    self.ronda.nueva_ronda(el_mano)


  """
  
  perspectivas para los mensajes/Packets
  
  """

  """retorna una representacion en json de la PerspectivaCacheFlor que tiene
  el jugador `j` de la partida. (no re-calcula las flores)
  """
  def perspectiva(self, jid:str) -> Partida:
    import copy
    copia = copy.deepcopy(self)
    # oculto las caras no tiradas de los manojos que no son de su equipo
    manojo = self.ronda.manojo(jid)
    for m in copia.ronda.manojos:
      noEsDeSuEquipo = m.jugador.equipo != manojo.jugador.equipo
      if noEsDeSuEquipo:
        # oculto solo las cartas que no tiro
        m.cartas = [None if not m.tiradas[j] else c
            for j,c in enumerate(m.cartas)]
        
    return copia
  
  """
  
  parser
  
  """

  def byeBye(self) -> list[Packet]:
    pkts:list[Packet] = []
    if self.terminada():

      s :str = self.ronda.manojos[0].jugador.id \
        if self.ronda.manojos[0].jugador.equipo == self.el_que_va_ganando() \
        else self.ronda.manojos[1].jugador.id  

      pkts += [Packet(
        ["ALL"],
        Message(
          CodMsg.BYEBYE,
          data=s)
      )]    

    return pkts
  
  def parse_jugada(self, cmd:str) -> IJugada:
    from .jugada import TocarEnvido, TocarRealEnvido, TocarFaltaEnvido, \
      CantarFlor, CantarContraFlor, CantarContraFlorAlResto, GritarTruco, \
      GritarReTruco, GritarVale4, ResponderQuiero, ResponderNoQuiero, \
      IrseAlMazo, TirarCarta
    
    # jugada simple?
    m = re.search("(?i)^([a-zA-Z0-9_-]+) ([a-zA-Z0-9_-]+)$", cmd)
    if m is not None:
      jugadorStr, j = m[1], m[2].lower()
      # jugador
      manojo = self.manojo(jugadorStr)
      if manojo is None: raise Exception("comando invalido")
      # jugada
      x :IJugada = TocarEnvido(manojo.jugador.id) if j == "envido" \
              else TocarRealEnvido(manojo.jugador.id) if j == "real-envido" \
              else TocarFaltaEnvido(manojo.jugador.id) if j == "falta-envido" \
              else CantarFlor(manojo.jugador.id) if j == "flor" \
              else CantarContraFlor(manojo.jugador.id) if j == "contra-flor" \
              else CantarContraFlorAlResto(manojo.jugador.id) if j == "contra-flor-al-resto" \
              else GritarTruco(manojo.jugador.id) if j == "truco" \
              else GritarReTruco(manojo.jugador.id) if j == "re-truco" \
              else GritarVale4(manojo.jugador.id) if j == "vale-4" \
              else ResponderQuiero(manojo.jugador.id) if j == "quiero" \
              else ResponderNoQuiero(manojo.jugador.id) if j == "no-quiero" \
              else IrseAlMazo(manojo.jugador.id) if j == "mazo" \
              else None
      
      if x is None: raise Exception("comando invalido")
      return x
    
    # jugada de tipo tirar-carta ?
    m = re.search("(?i)^([a-zA-Z0-9_-]+) (1|2|3|4|5|6|7|10|11|12) (oro|copa|basto|espada)$", cmd)
    if m is not None:
      jugadorStr, valorStr, paloStr = m[1], m[2].lower(), m[3].lower()
      # jugador
      manojo = self.manojo(jugadorStr)
      if manojo is None: raise Exception("comando invalido")
      # jugada
      carta = Carta(int(valorStr), paloStr)
      return TirarCarta(jugadorStr, carta)

    # sino
    raise Exception("comando invalido")

  """nexo capa presentacion con capa logica"""
  def cmd(self, cmd:str) -> list[Packet]:
    pkts:list[Packet] = []

    # checkeo semantico
    jugada = self.parse_jugada(cmd)
    jugada.hacer(self)

    if self.terminada():
      pkts += self.byeBye()

    return pkts

  """
  
  metodos de parseo y dumpeo JSON .to_json(...) .parse(...)
  
  """

  def to_json(self) -> any:
    pass

  @staticmethod
  def parse(data:str) -> Partida:
    if not isinstance(data, str):
      raise Exception("el valor de la partida no es valido")
    
    d: Dict[str,any] = json.loads(data)

    equipos = list(d["puntajes"].keys())
    e1 = equipos[0]
    e2 = equipos[1]
    jugadores = [m["jugador"]["id"] for m in d["ronda"]["manojos"]]

    p = Partida(
      puntuacion=int(d["puntuacion"]),
      azules=jugadores[0::2],
      rojos=jugadores[1::2],
      dummy=True
    )

    p.puntajes[Equipo.AZUL] = int(d["puntajes"][e1])
    p.puntajes[Equipo.ROJO] = int(d["puntajes"][e2])

    # setea el numero de mano
    p.ronda.mano_en_juego = NumMano.parse_int(int(d["ronda"]["manoEnJuego"]))

    # setea el numero de jugadores en juego
    p.ronda.cant_jugadores_en_juego[Equipo.AZUL] = int(d["ronda"]["cantJugadoresEnJuego"][e1])
    p.ronda.cant_jugadores_en_juego[Equipo.ROJO] = int(d["ronda"]["cantJugadoresEnJuego"][e2])

    # setea mano, turno
    p.ronda.el_mano = int(d["ronda"]["elMano"])
    p.ronda.turno = int(d["ronda"]["turno"])
    
    # carga Envite
    p.ronda.envite.cantado_por = d["ronda"]["envite"]["cantadoPor"]
    p.ronda.envite.puntaje = int(d["ronda"]["envite"]["puntaje"])
    p.ronda.envite.estado = EstadoEnvite.parse(d["ronda"]["envite"]["estado"])
    p.ronda.envite.sin_cantar = d["ronda"]["envite"]["sinCantar"]
    
    # carga Truco
    p.ronda.truco.cantado_por = d["ronda"]["truco"]["cantadoPor"]
    p.ronda.truco.estado = EstadoTruco.parse(d["ronda"]["truco"]["estado"])

    # crea manojos linkeados a los jugadores
    p.ronda.manojos = [
      Manojo(
        Jugador(
          id=m["jugador"]["id"],
          equipo=Equipo.AZUL if jid % 2 == 0 else Equipo.ROJO
        )
      ) for jid,m in enumerate(d["ronda"]["manojos"])
    ]

    # carga cartas de manojos
    for ix, m in enumerate(p.ronda.manojos):
      m.ultima_tirada = int(d["ronda"]["manojos"][ix]["ultimaTirada"])
      m.tiradas = d["ronda"]["manojos"][ix]["tiradas"]
      m.se_fue_al_mazo = d["ronda"]["manojos"][ix]["seFueAlMazo"]
      m.cartas = [
        Carta(int(c["valor"]), c["palo"]) \
        for c in d["ronda"]["manojos"][ix]["cartas"]
      ]

    # crea el mapping MIXS: str -> int
    if d["ronda"].get("mixs") is not None:
      p.ronda.MIXS = d["ronda"]["mixs"]
    else:
      p.ronda.indexar_manojos()

    # carga muestras
    p.ronda.muestra = Carta(
      valor=int(d["ronda"]["muestra"]["valor"]),
      palo=d["ronda"]["muestra"]["palo"]
    )

    # carga manos + cartas tiradas
    for ix, m in enumerate(p.ronda.manos):
      # ojo, en una version mas nueva del protocolo de codificacion puede que
      # no existan TODAS las manos en el JSON.
      m.resultado = Resultado.parse(d["ronda"]["manos"][ix]["resultado"])
      m.ganador = d["ronda"]["manos"][ix]["ganador"]
      if d["ronda"]["manos"][ix]["cartasTiradas"] is not None:
        m.cartas_tiradas = [
          CartaTirada(
            jugador=t["jugador"],
            carta=Carta(
              valor=int(t["carta"]["valor"]),
              palo=t["carta"]["palo"]
            )
          ) for t in d["ronda"]["manos"][ix]["cartasTiradas"]
        ]

    # cachea flores, SIN RESET
    p.ronda.cachear_flores(reset=False)

    return p


    




