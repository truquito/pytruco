from .partida import Partida, IJugada
from .jugadas import IJUGADA_ID
from .carta import Carta
from .envite import EstadoEnvite
from .mano import NumMano, Resultado
from .truco import EstadoTruco
from .equipo import Equipo

from enco.envelope import Envelope
from enco.message import Message
from enco.codmsg import CodMsg
from enco.razon import Razon
  
class TirarCarta(IJugada):
  def __init__(self, jid:str, carta:Carta):
    self.jid   :str   = jid
    self.carta :Carta = carta
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_TIRAR_CARTA
  
  def __str__(self) -> str:
    return f"{self.jid} {self.carta.valor} {self.carta.palo}"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []
    # checkeo si se fue al mazo
    noSeFueAlMazo = not p.manojo(self.jid).se_fue_al_mazo
    ok = noSeFueAlMazo
    if not ok:
      pkts += [Envelope(
        ["ALL"],
        Message(
          CodMsg.ERROR,
          data="No es posible tirar una carta porque ya te fuiste al mazo")
      )] if p.verbose else []
      return pkts, False
    
    # esto es un tanto redundante porque es imposible que no sea su turno
    # (checkeado mas adelante) y que al mismo tiempo tenga algo para tirar
    # luego de haber jugado sus 3 cartas; aun asi lo dejo
    yaTiroTodasSusCartas = p.manojo(self.jid).get_cant_cartas_tiradas() == 3
    if yaTiroTodasSusCartas:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tirar una carta porque ya las tiraste todas")
      )] if p.verbose else []
      return pkts, False
    
    # checkeo flor en juego
    enviteEnJuego = p.ronda.envite.estado >= EstadoEnvite.ENVIDO
    if enviteEnJuego:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tirar una carta ahora porque el envite esta en juego")
      )] if p.verbose else []
      return pkts, False
    
    # primero que nada: tiene esa carta?
    idx = p.manojo(self.jid).get_carta_idx(self.carta)
    if idx is None:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No tienes esa carta en tu manojo")
      )] if p.verbose else []
      return pkts, False
    
    # ya jugo esa carta?
    todaviaNoLaTiro = not p.manojo(self.jid).tiradas[idx]
    if not todaviaNoLaTiro:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="Ya tiraste esa carta")
      )] if p.verbose else []
      return pkts, False
    
    # luego, era su turno?
    eraSuTurno = p.ronda.get_el_turno().jugador.id == p.manojo(self.jid).jugador.id
    if not eraSuTurno:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No era su turno, no puede tirar la carta")
      )] if p.verbose else []
      return pkts, False
    
    # checkeo si tiene flor
    florHabilitada = (p.ronda.envite.estado >= EstadoEnvite.NOGRITADOAUNAUN and \
                      p.ronda.envite.estado <= EstadoEnvite.FLOR) and \
                      p.ronda.mano_en_juego == NumMano.PRIMERA
    tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
    noCantoFlorAun = p.ronda.envite.no_canto_flor_aun(p.manojo(self.jid).jugador.id)
    noPuedeTirar = florHabilitada and tieneFlor and noCantoFlorAun
    if noPuedeTirar:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tirar una carta sin antes cantar la flor")
      )] if p.verbose else []
      return pkts, False
    
    # cambio: ahora no puede tirar carta si el grito truco
    trucoGritado = p.ronda.truco.estado.es_truco_respondible()
    unoDelEquipoContrarioGritoTruco = trucoGritado and p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    yoGiteElTruco = trucoGritado and p.manojo(self.jid).jugador.id == p.ronda.truco.cantado_por
    elTrucoEsRespondible = trucoGritado and unoDelEquipoContrarioGritoTruco and not yoGiteElTruco
    if elTrucoEsRespondible:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tirar una carta porque tu equipo debe responder \
            la propuesta del truco")
      )] if p.verbose else []
      return pkts, False

    return pkts, True   

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    # ok la tiene y era su turno -> la juega
    pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.TIRAR_CARTA,
          data={
            "autor": p.manojo(self.jid).jugador.id,
            "palo": str(self.carta.palo),
            "valor": self.carta.valor })
      )] if p.verbose else []

    idx = p.manojo(self.jid).get_carta_idx(self.carta)

    p.tirar_carta(p.manojo(self.jid), idx)

    # era el ultimo en tirar de esta mano?
    eraElUltimoEnTirar = p.ronda.get_sig_habilitado(p.manojo(self.jid)) == None
    if eraElUltimoEnTirar:
      # de ser asi tengo que checkear el resultado de la mano
      empiezaNuevaRonda, res = p.evaluar_mano()

      pkts += res

      if not empiezaNuevaRonda:

        seTerminoLaPrimeraMano = p.ronda.mano_en_juego == NumMano.PRIMERA
        nadieCantoEnvite = p.ronda.envite.estado == EstadoEnvite.NOGRITADOAUNAUN
        if seTerminoLaPrimeraMano and nadieCantoEnvite:
          p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
          p.ronda.envite.sin_cantar = []
        
        # actualizo el mano
        p.ronda.mano_en_juego = NumMano.inc(p.ronda.mano_en_juego)
        p.ronda.set_next_turno_pos_mano()
        # lo envio
        pkts += [Envelope(
          dest=["ALL"],
          m=Message(
            CodMsg.SIG_TURNO_POSMANO,
            data=p.ronda.turno)
        )] if p.verbose else []

      else:
        if not p.terminada():
          # ahora se deberia de incrementar el mano
          # y ser el turno de este
          sigMano = p.ronda.get_sig_el_mano()
          p.nueva_ronda(sigMano) # todo: el tema es que cuando llama aca
          # no manda mensaje de que arranco nueva ronda
          # falso: el padre que llama a .EvaluarRonda tiene que fijarse si
          # retorno true
          # entonces debe crearla el
          # no es responsabilidad de EvaluarRonda arrancar una ronda nueva!!
          # de hecho, si una ronda es terminable y se llama 2 veces consecutivas
          # al mismo metodo booleano, en ambas oportunidades retorna diferente
          # ridiculo

          pkts += [
            Envelope(
              dest=[m.jugador.id],
              m=Message(
                CodMsg.NUEVA_RONDA,
                data=p.perspectiva(m.jugador.id).to_dict())
            ) for m in p.ronda.manojos ] if p.verbose else []

      # el turno del siguiente queda dado por el ganador de esta
    else:
      p.ronda.set_next_turno()
      pkts += [Envelope(
          dest=["ALL"],
          m=Message(
            CodMsg.SIG_TURNO,
            data=p.ronda.turno)
        )] if p.verbose else []    

    return pkts


class TocarEnvido(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_ENVIDO
  
  def __str__(self) -> str:
    return f"{self.jid} envido"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []
    # checkeo flor en juego
    florEnJuego = p.ronda.envite.estado >= EstadoEnvite.FLOR
    if florEnJuego:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tocar el envido ahora porque la flor esta en juego")
      )] if p.verbose else []
      return pkts, False
    
    seFueAlMazo = p.manojo(self.jid).se_fue_al_mazo
    esPrimeraMano = p.ronda.mano_en_juego == NumMano.PRIMERA
    esSuTurno = p.ronda.get_el_turno().jugador.id == p.manojo(self.jid).jugador.id
    tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
    envidoHabilitado = (p.ronda.envite.estado == EstadoEnvite.NOGRITADOAUNAUN or p.ronda.envite.estado == EstadoEnvite.ENVIDO)

    if not envidoHabilitado:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tocar envido ahora")
      )] if p.verbose else []

      return pkts, False
    
    esDelEquipoContrario = p.ronda.envite.estado == EstadoEnvite.NOGRITADOAUNAUN or p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    yaEstabamosEnEnvido = p.ronda.envite.estado == EstadoEnvite.ENVIDO
    # apuestaSaturada = p.ronda.envite.Puntaje >= p.CalcPtsFalta()
    apuestaSaturada = p.ronda.envite.puntaje >= 4
    trucoNoCantado = p.ronda.truco.estado == EstadoTruco.NOGRITADOAUN

    estaIniciandoPorPrimeraVezElEnvido = esSuTurno and p.ronda.envite.estado == EstadoEnvite.NOGRITADOAUNAUN and trucoNoCantado
    estaRedoblandoLaApuesta = p.ronda.envite.estado == EstadoEnvite.ENVIDO and esDelEquipoContrario # cuando redobla una apuesta puede o no ser su turno
    elEnvidoEstaPrimero = (not esSuTurno) and p.ronda.truco.estado == EstadoTruco.TRUCO and (not yaEstabamosEnEnvido) and esPrimeraMano

    puedeTocarEnvido = estaIniciandoPorPrimeraVezElEnvido or estaRedoblandoLaApuesta or elEnvidoEstaPrimero

    ok = (not seFueAlMazo) and (envidoHabilitado and esPrimeraMano and (not tieneFlor) and esDelEquipoContrario) and puedeTocarEnvido and (not apuestaSaturada)

    if not ok:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible cantar 'Envido'")
      )] if p.verbose else []
      return pkts, False
    
    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    esPrimeraMano = p.ronda.mano_en_juego == NumMano.PRIMERA
    yaEstabamosEnEnvido = p.ronda.envite.estado == EstadoEnvite.ENVIDO
    elEnvidoEstaPrimero = p.ronda.truco.estado == EstadoTruco.TRUCO and (not yaEstabamosEnEnvido) and esPrimeraMano

    if elEnvidoEstaPrimero:
      # actualizacion 23/9/23: se desactiva este comportamiento debido a inconsistencias
	    # con el simulador-parcial (a.k.a., la `Perspectiva`)
  
      # deshabilito el truco
      # p.ronda.truco.estado = EstadoTruco.NOGRITADOAUN
      # p.ronda.truco.cantado_por = ""
      
      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.EL_ENVIDO_ESTA_PRIMERO,
          data=p.manojo(self.jid).jugador.id)
      )] if p.verbose else []

    pkts += [Envelope(
      dest=["ALL"],
      m=Message(
        CodMsg.TOCAR_ENVIDO,
        data=p.manojo(self.jid).jugador.id)
    )] if p.verbose else []

    # ahora checkeo si alguien tiene flor
    hayFlor = len(p.ronda.envite.sin_cantar) > 0
    if hayFlor:
      # todo: deberia ir al estado magico en el que espera
      # solo por jugadas de tipo flor-related
      # lo mismo para el real-envido; falta-envido
      jid = p.ronda.envite.sin_cantar[0]
      # j = p.ronda.Manojo(jid)
      siguienteJugada = CantarFlor(jid)
      res = siguienteJugada.hacer(p)
      pkts += res
    else:
      p.tocar_envido(p.manojo(self.jid))

    return pkts
  
  """
  
  metodo particular. lo tiene tanto el tocarenvido como el tocarflataenvido.
  el problema de esta funcion es que esta mas relacionada con el `quiero`
  que con el envido. Deberia formar parte del eval del quiero.
  
  @param 'j' el jugador que dijo 'quiero' al 'envido'/'real envido'
  """
  def eval(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
    p.ronda.envite.sin_cantar = []
    jIdx, _, res = p.ronda.exec_el_envido(verbose=p.verbose)

    pkts += res if p.verbose else []
    jug = p.ronda.manojos[jIdx].jugador

    pkts += [Envelope(
      dest=["ALL"],
      m=Message(
        CodMsg.SUMA_PTS,
        data={
          "autor": jug.id,
          "razon": Razon.ENVIDO_GANADO,
          "puntos": p.ronda.envite.puntaje,
        })
    )] if p.verbose else []

    p.suma_puntos(jug.equipo, p.ronda.envite.puntaje)
    return pkts  



class TocarRealEnvido(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_REAL_ENVIDO
  
  def __str__(self) -> str:
    return f"{self.jid} real-envido"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []

    # checkeo flor en juego
    florEnJuego = p.ronda.envite.estado >= EstadoEnvite.FLOR
    if florEnJuego:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tocar real envido ahora porque la flor esta en juego")
      )] if p.verbose else []
      return pkts, False
    
    seFueAlMazo = p.manojo(self.jid).se_fue_al_mazo
    esPrimeraMano = p.ronda.mano_en_juego == NumMano.PRIMERA
    esSuTurno = p.ronda.get_el_turno().jugador.id == p.manojo(self.jid).jugador.id
    tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
    realEnvidoHabilitado = (p.ronda.envite.estado == EstadoEnvite.NOGRITADOAUNAUN \
                            or p.ronda.envite.estado == EstadoEnvite.ENVIDO)
    if not realEnvidoHabilitado:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tocar real-envido ahora")
      )] if p.verbose else []
      return pkts, False
    
    esDelEquipoContrario = p.ronda.envite.estado == EstadoEnvite.NOGRITADOAUNAUN or \
      p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    yaEstabamosEnEnvido = p.ronda.envite.estado == EstadoEnvite.ENVIDO
    trucoNoCantado = p.ronda.truco.estado == EstadoTruco.NOGRITADOAUN

    estaIniciandoPorPrimeraVezElEnvido = esSuTurno and p.ronda.envite.estado == EstadoEnvite.NOGRITADOAUNAUN and trucoNoCantado
    estaRedoblandoLaApuesta = p.ronda.envite.estado == EstadoEnvite.ENVIDO and esDelEquipoContrario # cuando redobla una apuesta puede o no ser su turno
    elEnvidoEstaPrimero = (not esSuTurno) and p.ronda.truco.estado == EstadoTruco.TRUCO and (not yaEstabamosEnEnvido) and esPrimeraMano

    puedeTocarRealEnvido = estaIniciandoPorPrimeraVezElEnvido or estaRedoblandoLaApuesta or elEnvidoEstaPrimero
    ok = (not seFueAlMazo) and (realEnvidoHabilitado and esPrimeraMano and (not tieneFlor) and esDelEquipoContrario) and puedeTocarRealEnvido

    if not ok:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible cantar 'Real Envido'")
      )] if p.verbose else []
      return pkts, False
    
    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    esPrimeraMano = p.ronda.mano_en_juego == NumMano.PRIMERA
    yaEstabamosEnEnvido = p.ronda.envite.estado == EstadoEnvite.ENVIDO
    elEnvidoEstaPrimero = p.ronda.truco.estado == EstadoTruco.TRUCO and (not yaEstabamosEnEnvido) and esPrimeraMano

    if elEnvidoEstaPrimero:
      # actualizacion 23/9/23: se desactiva este comportamiento debido a inconsistencias
	    # con el simulador-parcial (a.k.a., la `Perspectiva`)

      # deshabilito el truco
      # p.ronda.truco.estado = EstadoTruco.NOGRITADOAUN
      # p.ronda.truco.cantado_por = ""

      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.EL_ENVIDO_ESTA_PRIMERO,
          data=p.manojo(self.jid).jugador.id)
      )] if p.verbose else []

    pkts += [Envelope(
      dest=["ALL"],
      m=Message(
        CodMsg.TOCAR_REALENVIDO,
        data=p.manojo(self.jid).jugador.id)
    )] if p.verbose else []

    p.tocar_real_envido(p.manojo(self.jid))

    # ahora checkeo si alguien tiene flor
    hayFlor = len(p.ronda.envite.sin_cantar) > 0

    if hayFlor:
      jid = p.ronda.envite.sin_cantar[0]
      # j = p.Ronda.Manojo(jid)
      siguienteJugada = CantarFlor(jid)
      res = siguienteJugada.hacer(p)
      pkts += res
    
    return pkts   



class TocarFaltaEnvido(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_FALTA_ENVIDO
  
  def __str__(self) -> str:
    return f"{self.jid} falta-envido"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []

    # checkeo flor en juego
    florEnJuego = p.ronda.envite.estado >= EstadoEnvite.FLOR
    if florEnJuego:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tocar falta envido ahora porque la flor esta en juego")
      )] if p.verbose else []
      return pkts, False

    seFueAlMazo = p.manojo(self.jid).se_fue_al_mazo
    esSuTurno = p.ronda.get_el_turno().jugador.id == p.manojo(self.jid).jugador.id
    esPrimeraMano = p.ronda.mano_en_juego == NumMano.PRIMERA
    tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
    faltaEnvidoHabilitado = p.ronda.envite.estado >= EstadoEnvite.NOGRITADOAUNAUN \
      and p.ronda.envite.estado < EstadoEnvite.FALTAENVIDO
    
    if (not faltaEnvidoHabilitado):
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tocar real-envido ahora")
      )] if p.verbose else []
      return pkts, False
    
    esDelEquipoContrario = p.ronda.envite.estado == EstadoEnvite.NOGRITADOAUNAUN or p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    yaEstabamosEnEnvido = p.ronda.envite.estado >= EstadoEnvite.ENVIDO
    trucoNoCantado = p.ronda.truco.estado == EstadoTruco.NOGRITADOAUN

    estaIniciandoPorPrimeraVezElEnvido = esSuTurno and p.ronda.envite.estado == EstadoEnvite.NOGRITADOAUNAUN and trucoNoCantado
    estaRedoblandoLaApuesta = p.ronda.envite.estado >= EstadoEnvite.ENVIDO and p.ronda.envite.estado < EstadoEnvite.FALTAENVIDO and esDelEquipoContrario # cuando redobla una apuesta puede o no ser su turno
    elEnvidoEstaPrimero = (not esSuTurno) and p.ronda.truco.estado == EstadoTruco.TRUCO and (not yaEstabamosEnEnvido) and esPrimeraMano

    puedeTocarFaltaEnvido = estaIniciandoPorPrimeraVezElEnvido or estaRedoblandoLaApuesta or elEnvidoEstaPrimero
    ok = (not seFueAlMazo) and (faltaEnvidoHabilitado and esPrimeraMano and (not tieneFlor) and esDelEquipoContrario) and puedeTocarFaltaEnvido

    if not ok:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible cantar 'Falta Envido'")
      )] if p.verbose else []
      return pkts, False
        
    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    esPrimeraMano = p.ronda.mano_en_juego == NumMano.PRIMERA
    yaEstabamosEnEnvido = p.ronda.envite.estado == EstadoEnvite.ENVIDO or p.ronda.envite.estado == EstadoEnvite.REALENVIDO
    elEnvidoEstaPrimero = p.ronda.truco.estado == EstadoTruco.TRUCO and (not yaEstabamosEnEnvido) and esPrimeraMano

    if elEnvidoEstaPrimero:
      # actualizacion 23/9/23: se desactiva este comportamiento debido a inconsistencias
	    # con el simulador-parcial (a.k.a., la `Perspectiva`)

      # deshabilito el truco
      # p.ronda.truco.estado = EstadoTruco.NOGRITADOAUN
      # p.ronda.truco.cantado_por = ""
      
      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.EL_ENVIDO_ESTA_PRIMERO,
          data=p.manojo(self.jid).jugador.id)
      )] if p.verbose else []

    pkts += [Envelope(
      dest=["ALL"],
      m=Message(
        CodMsg.TOCAR_FALTAENVIDO,
        data=p.manojo(self.jid).jugador.id)
    )] if p.verbose else []

    p.tocar_falta_envido(p.manojo(self.jid))

    # ahora checkeo si alguien tiene flor
    hayFlor = len(p.ronda.envite.sin_cantar) > 0
    if hayFlor:
      jid = p.ronda.envite.sin_cantar[0]
      # j = p.Ronda.Manojo(jid)
      siguienteJugada = CantarFlor(jid)
      res = siguienteJugada.hacer(p)
      pkts += res

    return pkts  

  """
  forma actual de jugar:
 		si estan en malas: el que gana el envido gana la partida.
				terminando asi la partida.
 		si no: se juega por el resto del maximo puntaje
				no necesariamente terminando asi la partida.
  forma alternativa:
 		si estan en malas: se juega por completar las malas
 		si no: se juega por el resto del maximo puntaje
  """
  def eval(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
    p.ronda.envite.sin_cantar = []

    # computar envidos
    jIdx, _, res = p.ronda.exec_el_envido(verbose=p.verbose)

    pkts += res if p.verbose else []

    # jug es el que gano el (falta) envido
    jug = p.ronda.manojos[jIdx].jugador

    pts = p.calc_pts_falta_envido(jug.equipo)

    p.ronda.envite.puntaje += pts

    pkts += [Envelope(
      dest=["ALL"],
      m=Message(
        CodMsg.SUMA_PTS,
        data={
          "autor": jug.id,
          "razon": Razon.FALTA_ENVIDO_GANADO,
          "puntos": p.ronda.envite.puntaje,
        })
    )] if p.verbose else []

    p.suma_puntos(jug.equipo, p.ronda.envite.puntaje)

    return pkts 


class CantarFlor(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_FLOR
  
  def __str__(self) -> str:
    return f"{self.jid} flor"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []

    # manojo dice que puede cantar flor;
    # es esto verdad?
    seFueAlMazo = p.manojo(self.jid).se_fue_al_mazo
    florHabilitada = (p.ronda.envite.estado >= EstadoEnvite.NOGRITADOAUNAUN) and p.ronda.mano_en_juego == NumMano.PRIMERA
    tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
    noCantoFlorAun = p.ronda.envite.no_canto_flor_aun(p.manojo(self.jid).jugador.id)
    
    # caso especial:
    # tienen flor: alice bob ben.
    # alice:flor -> bob:contra-flor -> alice:mazo => ben ??? no canto su flor
    # entonces, puede cantar flor, (SIN disminuir su estado) si tiene flor Y NO CANTO AUN
    # por eso le elimino la clausura:
    # `p.Ronda.Envite.Estado <= FLOR` en la variable `florHabilitada`

    ok = (not seFueAlMazo) and florHabilitada and tieneFlor and noCantoFlorAun

    if not ok:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible cantar flor")
      )] if p.verbose else []
      return pkts, False
      
    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    # yo canto
    pkts += [Envelope(
      ["ALL"],
      Message(
        CodMsg.CANTAR_FLOR,
        data=p.manojo(self.jid).jugador.id)
    )] if p.verbose else []

    # actualizacion 23/9/23: se desactiva este comportamiento debido a inconsistencias
	  # con el simulador-parcial (a.k.a., la `Perspectiva`)
    
    # corresponde que desactive el truco?
    # si lo desactivo: es medio tedioso para el usuario tener q volver a gritar
    # si no lo desacivo: medio como que se olvida
    # QUEDA CONSISTENTE CON "EL ENVIDO ESTA PRIMERO"!

    # p.ronda.truco.cantado_por = ""
    # p.ronda.truco.estado = EstadoTruco.NOGRITADOAUN
    
    pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.EL_ENVIDO_ESTA_PRIMERO,
          data=p.manojo(self.jid).jugador.id)
      )] if p.verbose else []

    # y me elimino de los que no-cantaron
    p.ronda.envite.canto_flor(p.manojo(self.jid).jugador.id)

    p.cantar_flor(p.manojo(self.jid))

    # es el ultimo en cantar flor que faltaba?
    # o simplemente es el unico que tiene flor (caso particular)

    todosLosJugadoresConFlorCantaron = len(p.ronda.envite.sin_cantar) == 0
    if todosLosJugadoresConFlorCantaron:
      pkts += CantarFlor.eval(p)
    else:
      # cachear esto
      # solos los de su equipo tienen flor?
      # si solos los de su equipo tienen flor (y los otros no) -> las canto todas
      soloLosDeSuEquipoTienenFlor = True
      for m in p.ronda.envite.jugadores_con_flor:
        if m.jugador.equipo != p.manojo(self.jid).jugador.equipo:
          soloLosDeSuEquipoTienenFlor = False
          break

      if soloLosDeSuEquipoTienenFlor:
        # los quiero llamar a todos, pero no quiero Hacer llamadas al pedo
        # entonces: llamo al primero sin cantar, y que este llame al proximo
        # y que el proximo llame al siguiente, y asi...
        jid = p.ronda.envite.sin_cantar[0]
        # j = p.Ronda.Manojo(jid)
        siguienteJugada = CantarFlor(jid)
        res = siguienteJugada.hacer(p)
        pkts += res
    
    return pkts   


  def eval(p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    
    florEnJuego = p.ronda.envite.estado >= EstadoEnvite.FLOR
    todosLosJugadoresConFlorCantaron = len(p.ronda.envite.sin_cantar) == 0
    ok = todosLosJugadoresConFlorCantaron and florEnJuego
    if not ok:
      return pkts
    
    # cual es la flor ganadora?
    # empieza cantando el autor del envite no el que "quizo"
    autorIdx = p.ronda.JIX(p.ronda.manojo(p.ronda.envite.cantado_por).jugador.id)
    manojoConLaFlorMasAlta, _, res = p.ronda.exec_las_flores(autorIdx, verbose=p.verbose)
    pkts += res if p.verbose else []
    equipoGanador = manojoConLaFlorMasAlta.jugador.equipo

    # que estaba en juego?
    # switch p.Ronda.Envite.Estado {
    # case FLOR:
    # ahora se quien es el ganador; necesito saber cuantos puntos
    # se le va a sumar a ese equipo:
    # los acumulados del envite hasta ahora
    puntosASumar = p.ronda.envite.puntaje
    p.suma_puntos(equipoGanador, puntosASumar)
    habiaSolo1JugadorConFlor = len(p.ronda.envite.jugadores_con_flor) == 1
    if habiaSolo1JugadorConFlor:
      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.SUMA_PTS,
          data={
            "autor": manojoConLaFlorMasAlta.jugador.id,
            "razon": Razon.LA_UNICA_FLOR,
            "puntos": puntosASumar,
          })
      )] if p.verbose else []
    else:
      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.SUMA_PTS,
          data={
            "autor": manojoConLaFlorMasAlta.jugador.id,
            "razon": Razon.LA_FLOR_MASALTA,
            "puntos": puntosASumar,
          })
      )] if p.verbose else []

    p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
    p.ronda.envite.sin_cantar = []

    return pkts

class CantarContraFlor(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_CONTRA_FLOR
  
  def __str__(self) -> str:
    return f"{self.jid} contra-flor"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []
    # manojo dice que puede cantar flor;
    # es esto verdad?
    seFueAlMazo = p.manojo(self.jid).se_fue_al_mazo
    contraFlorHabilitada = p.ronda.envite.estado == EstadoEnvite.FLOR and p.ronda.mano_en_juego == NumMano.PRIMERA
    esDelEquipoContrario = contraFlorHabilitada and p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
    noCantoFlorAun = p.ronda.envite.no_canto_flor_aun(p.manojo(self.jid).jugador.id)
    ok = (not seFueAlMazo) and contraFlorHabilitada and tieneFlor and esDelEquipoContrario and noCantoFlorAun
    if not ok:
      pkts += [Envelope(
        ["ALL"],
        Message(
          CodMsg.ERROR,
          data="No es posible cantar contra flor")
      )] if p.verbose else []
      return pkts, False

    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    # la canta
    pkts += [Envelope(
      ["ALL"],
      Message(
        CodMsg.CANTAR_CONTRAFLOR,
        data=p.manojo(self.jid).jugador.id)
    )] if p.verbose else []

    p.cantar_contra_flor(p.manojo(self.jid))
    # y ahora tengo que esperar por la respuesta de la nueva
    # propuesta de todos menos de el que canto la contraflor
    # restauro la copia
    p.ronda.envite.canto_flor(p.manojo(self.jid).jugador.id)
    
    return pkts

class CantarContraFlorAlResto(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_CONTRA_FLOR_AL_RESTO
  
  def __str__(self) -> str:
    return f"{self.jid} contra-flor-al-resto"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []

    # manojo dice que puede cantar flor;
    # es esto verdad?
    seFueAlMazo = p.manojo(self.jid).se_fue_al_mazo
    contraFlorHabilitada = (p.ronda.envite.estado == EstadoEnvite.FLOR or \
                            p.ronda.envite.estado == EstadoEnvite.CONTRAFLOR) \
                              and p.ronda.mano_en_juego == NumMano.PRIMERA
    esDelEquipoContrario = contraFlorHabilitada and p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
    noCantoFlorAun = p.ronda.envite.no_canto_flor_aun(p.manojo(self.jid).jugador.id)
    ok = (not seFueAlMazo) and contraFlorHabilitada and tieneFlor and esDelEquipoContrario and noCantoFlorAun
    if not ok:
      pkts += [Envelope(
        ["ALL"],
        Message(
          CodMsg.ERROR,
          data="No es posible cantar contra flor al resto")
      )] if p.verbose else []
      return pkts, False
        
    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    # la canta
    pkts += [Envelope(
      ["ALL"],
      Message(
        CodMsg.CANTAR_CONTRAFLOR_AL_RESTO,
        data=p.manojo(self.jid).jugador.id)
    )] if p.verbose else []

    p.cantar_contra_flor_al_resto(p.manojo(self.jid))
    # y ahora tengo que esperar por la respuesta de la nueva
    # propuesta de todos menos de el que canto la contraflor
    # restauro la copia
    p.ronda.envite.canto_flor(p.manojo(self.jid).jugador.id)
    
    return pkts
  
# class CantarConFlorMeAchico(IJugada):
#   def __init__(self, jid:str):
#     self.jid   :str   = jid
  
#   def id() -> IJUGADA_ID:
#     return IJUGADA_ID.FOO
  
#   def __str__(self) -> str:
#     return f"{self.jid} foo"

#   # Retorna true si la jugada es valida
#   def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
#     pkts :list[Envelope] = []
#     return pkts, True

#   def hacer(self, p:Partida) -> list[Envelope]:
#     pkts :list[Envelope] = []
#     pre, ok = self.ok(p)
#     pkts += pre

#     if not ok:
#       return pkts
    
#     return pkts   

class GritarTruco(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_TRUCO
  
  def __str__(self) -> str:
    return f"{self.jid} truco"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []

    # checkeos:
    noSeFueAlMazo = not p.manojo(self.jid).se_fue_al_mazo
    noSeEstaJugandoElEnvite = p.ronda.envite.estado <= EstadoEnvite.NOGRITADOAUNAUN

    yoOUnoDeMisCompasTieneFlorYAunNoCanto = p.ronda.hay_equipos_sin_cantar(p.manojo(self.jid).jugador.equipo)

    laFlorEstaPrimero = yoOUnoDeMisCompasTieneFlorYAunNoCanto
    trucoNoSeJugoAun = p.ronda.truco.estado == EstadoTruco.NOGRITADOAUN
    esSuTurno = p.ronda.get_el_turno().jugador.id == p.manojo(self.jid).jugador.id
    trucoHabilitado = noSeFueAlMazo and trucoNoSeJugoAun and noSeEstaJugandoElEnvite and (not laFlorEstaPrimero) and esSuTurno

    if not trucoHabilitado:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible cantar truco ahora")
      )] if p.verbose else []
      return pkts, False
      
    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    pkts += [Envelope(
      dest=["ALL"],
      m=Message(
        CodMsg.GRITAR_TRUCO,
        data=p.manojo(self.jid).jugador.id)
    )] if p.verbose else []

    p.gritar_truco(p.manojo(self.jid))
    return pkts

class GritarReTruco(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_RE_TRUCO
  
  def __str__(self) -> str:
    return f"{self.jid} re-truco"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []

    # checkeos generales:
    noSeFueAlMazo = not p.manojo(self.jid).se_fue_al_mazo
    noSeEstaJugandoElEnvite = p.ronda.envite.estado <= EstadoEnvite.NOGRITADOAUNAUN

    yoOUnoDeMisCompasTieneFlorYAunNoCanto = p.ronda.hay_equipos_sin_cantar(p.manojo(self.jid).jugador.equipo)

    laFlorEstaPrimero = yoOUnoDeMisCompasTieneFlorYAunNoCanto

    """
      Hay 2 casos para cantar rectruco:
          - CASO I: Uno del equipo contrario grito el truco
        - CASO II: Uno de su equipo posee el quiero
    """

    # CASO I:
    trucoGritado = p.ronda.truco.estado == EstadoTruco.TRUCO
    unoDelEquipoContrarioGritoTruco = trucoGritado and p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    casoI = trucoGritado and unoDelEquipoContrarioGritoTruco

    # CASO II:
    trucoYaQuerido = p.ronda.truco.estado == EstadoTruco.TRUCOQUERIDO
    unoDeMiEquipoQuizo = trucoYaQuerido and p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo == p.manojo(self.jid).jugador.equipo
    # esTurnoDeMiEquipo = p.Ronda.GetElTurno().jugador.equipo == p.manojo(self.jid).jugador.equipo
    casoII = trucoYaQuerido and unoDeMiEquipoQuizo # and esTurnoDeMiEquipo

    reTrucoHabilitado = noSeFueAlMazo and noSeEstaJugandoElEnvite and (casoI or casoII) and (not laFlorEstaPrimero)

    if not reTrucoHabilitado:
      pkts += [Envelope(
        ["ALL"],
        Message(
          CodMsg.ERROR,
          data="No es posible cantar re-truco ahora")
      )] if p.verbose else []
      return pkts, False

    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    pkts += [Envelope(
      dest=["ALL"],
      m=Message(
        CodMsg.GRITAR_RETRUCO,
        data=p.manojo(self.jid).jugador.id)
    )] if p.verbose else []
    p.gritar_retruco(p.manojo(self.jid))
    return pkts   
  
class GritarVale4(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_VALE_4
  
  def __str__(self) -> str:
    return f"{self.jid} vale-4"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []

    # checkeos:
    noSeFueAlMazo = not p.manojo(self.jid).se_fue_al_mazo

    noSeEstaJugandoElEnvite = p.ronda.envite.estado <= EstadoEnvite.NOGRITADOAUNAUN

    yoOUnoDeMisCompasTieneFlorYAunNoCanto = p.ronda.hay_equipos_sin_cantar(p.manojo(self.jid).jugador.equipo)

    laFlorEstaPrimero = yoOUnoDeMisCompasTieneFlorYAunNoCanto

    """
      Hay 2 casos para cantar rectruco:
          - CASO I: Uno del equipo contrario grito el re-truco
        - CASO II: Uno de su equipo posee el quiero
    """

    # CASO I:
    reTrucoGritado = p.ronda.truco.estado == EstadoTruco.RETRUCO
    # para eviat el nil primero checkeo que haya sido gritado reTrucoGritado and
    unoDelEquipoContrarioGritoReTruco = reTrucoGritado and p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    casoI = reTrucoGritado and unoDelEquipoContrarioGritoReTruco

    # CASO I:
    retrucoYaQuerido = p.ronda.truco.estado == EstadoTruco.RETRUCOQUERIDO
    # para eviat el nil primero checkeo que haya sido gritado reTrucoGritado and
    suEquipotieneElQuiero = retrucoYaQuerido and p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo == p.manojo(self.jid).jugador.equipo
    casoII = retrucoYaQuerido and suEquipotieneElQuiero

    vale4Habilitado = noSeFueAlMazo and (casoI or casoII) and noSeEstaJugandoElEnvite and not laFlorEstaPrimero

    if not vale4Habilitado:
      pkts += [Envelope(
        ["ALL"],
        Message(
          CodMsg.ERROR,
          data="No es posible cantar vale-4 ahora")
      )] if p.verbose else []
      return pkts, False

    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    pkts += [Envelope(
      dest=["ALL"],
      m=Message(
        CodMsg.GRITAR_VALE4,
        data=p.manojo(self.jid).jugador.id)
    )] if p.verbose else []
    p.gritar_vale4(p.manojo(self.jid))

    return pkts   

class ResponderQuiero(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_QUIERO
  
  def __str__(self) -> str:
    return f"{self.jid} quiero"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []

    seFueAlMazo = p.manojo(self.jid).se_fue_al_mazo
    if seFueAlMazo:
      pkts += [Envelope(
        ["ALL"],
        Message(
          CodMsg.ERROR,
          data="Te fuiste al mazo; no podes Hacer esta jugada")
      )] if p.verbose else []
      return pkts, False
    
    # checkeo flor en juego
    # caso particular del checkeo:
    # no se le puede decir quiero ni al envido* ni al truco si se esta jugando la flor
    # no se le puede decir quiero a la flor -> si la flor esta en juego -> error
    # pero si a la contra flor o contra flor al resto
    # casos posibles:
    # alguien dijo envido/truco, otro responde quiero, pero hay uno que tiene flor que todavia no la jugo -> deberia saltar error: "alguien tiene flor y no la jugo aun"
    # alguien tiene flor, uno dice quiero -> no deberia dejarlo porque la flor no se responde con quiero
    # se esta jugando la contra-flor/CFAR -> ok

    florEnJuego = p.ronda.envite.estado == EstadoEnvite.FLOR
    if florEnJuego:
      pkts += [Envelope(
        ["ALL"],
        Message(
          CodMsg.ERROR,
          data="No es posible responder quiero ahora")
      )] if p.verbose else []
      return pkts, False

    noHanCantadoLaFlorAun = p.ronda.envite.estado < EstadoEnvite.FLOR
    yoOUnoDeMisCompasTieneFlorYAunNoCanto = p.ronda.hay_equipos_sin_cantar(p.manojo(self.jid).jugador.equipo)
    if noHanCantadoLaFlorAun and yoOUnoDeMisCompasTieneFlorYAunNoCanto:
      pkts += [Envelope(
        ["ALL"],
        Message(
          CodMsg.ERROR,
          data="No es posible responder 'quiero' porque alguien con flor no ha cantado aun")
      )] if p.verbose else []
      return pkts, False
    # se acepta una respuesta 'quiero' solo cuando:
    # - CASO I: se toco un envite+ (con autor del equipo contario)
    # - CASO II: se grito el truco+ (con autor del equipo contario)
    # en caso contrario, es incorrecto -> error

    elEnvidoEsRespondible = (p.ronda.envite.estado >= EstadoEnvite.ENVIDO and p.ronda.envite.estado <= EstadoEnvite.FALTAENVIDO)
    # ojo: solo a la contraflor+ se le puede decir quiero; a la flor sola no
    laContraFlorEsRespondible = p.ronda.envite.estado >= EstadoEnvite.CONTRAFLOR and p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    elTrucoEsRespondible = p.ronda.truco.estado.es_truco_respondible() and p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo

    ok = elEnvidoEsRespondible or laContraFlorEsRespondible or elTrucoEsRespondible
    if not ok:
      # si no, esta respondiendo al pedo
      pkts += [Envelope(
        ["ALL"],
        Message(
          CodMsg.ERROR,
          data='No hay nada "que querer"; ya que: el estado del envido no es \
            "envido" (o mayor) y el estado del truco no es "truco" (o mayor) o \
              bien fue cantado por uno de su equipo')
      )] if p.verbose else []
      return pkts, False
    
    if elEnvidoEsRespondible:
      esDelEquipoContrario = p.manojo(self.jid).jugador.equipo != p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo
      if not esDelEquipoContrario:
        pkts += [Envelope(
          dest=[p.manojo(self.jid).jugador.id],
          m=Message(
            CodMsg.ERROR,
            data="La jugada no es valida")
        )] if p.verbose else []
        return pkts, False
    elif laContraFlorEsRespondible:
      # tengo que verificar si efectivamente tiene flor
      tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
      esDelEquipoContrario = p.manojo(self.jid).jugador.equipo != p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo
      ok = tieneFlor and esDelEquipoContrario
      if not ok:
        pkts += [Envelope(
          dest=[p.manojo(self.jid).jugador.id],
          m=Message(
            CodMsg.ERROR,
            data="La jugada no es valida")
        )] if p.verbose else []
        return pkts, False
    
    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    # se acepta una respuesta 'quiero' solo cuando:
    # - CASO I: se toco un envite+ (con autor del equipo contario)
    # - CASO II: se grito el truco+ (con autor del equipo contario)
    # en caso contrario, es incorrecto -> error

    elEnvidoEsRespondible = (p.ronda.envite.estado >= EstadoEnvite.ENVIDO and p.ronda.envite.estado <= EstadoEnvite.FALTAENVIDO)
    # ojo: solo a la contraflor+ se le puede decir quiero; a la flor sola no
    laContraFlorEsRespondible = p.ronda.envite.estado >= EstadoEnvite.CONTRAFLOR and p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    elTrucoEsRespondible = p.ronda.truco.estado.es_truco_respondible() and p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo

    if elEnvidoEsRespondible:
      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.QUIERO_ENVITE,
          data=p.manojo(self.jid).jugador.id)
      )] if p.verbose else []

      if p.ronda.envite.estado == EstadoEnvite.FALTAENVIDO:
        res = TocarFaltaEnvido(self.jid).eval(p)
        return pkts + res
      
      # si no, era envido/real-envido o cualquier
      # combinacion valida de ellos

      res = TocarEnvido(self.jid).eval(p)
      return pkts + res

    elif laContraFlorEsRespondible:
      
      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.QUIERO_ENVITE,
          data=p.manojo(self.jid).jugador.id)
      )] if p.verbose else []
        
      # empieza cantando el autor del envite no el que "quizo"
      autorIdx = p.ronda.JIX(p.ronda.manojo(p.ronda.envite.cantado_por).jugador.id)
      manojoConLaFlorMasAlta, _, res = p.ronda.exec_las_flores(autorIdx, verbose=p.verbose)

      pkts += res if p.verbose else []

      # manojoConLaFlorMasAlta, _ = p.Ronda.GetLaFlorMasAlta()
      equipoGanador = manojoConLaFlorMasAlta.jugador.equipo

      if p.ronda.envite.estado == EstadoEnvite.CONTRAFLOR:
        puntosASumar = p.ronda.envite.puntaje
        p.suma_puntos(equipoGanador, puntosASumar)
        pkts += [Envelope(
          dest=["ALL"],
          m=Message(
            CodMsg.SUMA_PTS,
            data={
              "autor": manojoConLaFlorMasAlta.jugador.id,
              "razon": Razon.CONTRAFLOR_GANADA,
              "puntos": puntosASumar,
            })
        )] if p.verbose else []

      else:
        # el equipo del ganador de la contraflor al resto
        # gano la partida
        # duda se cuentan las flores?
        # puntosASumar = p.Ronda.Envite.Puntaje + p.CalcPtsContraFlorAlResto(equipoGanador)
        puntosASumar = p.calc_pts_contraflor_al_resto(equipoGanador)
        p.suma_puntos(equipoGanador, puntosASumar)
        pkts += [Envelope(
          dest=["ALL"],
          m=Message(
            CodMsg.SUMA_PTS,
            data={
              "autor": manojoConLaFlorMasAlta.jugador.id,
              "razon": Razon.CONTRAFLOR_AL_RESTO_GANADA,
              "puntos": puntosASumar,
            })
        )] if p.verbose else []

      p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
      p.ronda.envite.sin_cantar = []

    elif elTrucoEsRespondible:
      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.QUIERO_TRUCO,
          data=p.manojo(self.jid).jugador.id)
      )] if p.verbose else []
      p.querer_truco(p.manojo(self.jid))

    return pkts   

class ResponderNoQuiero(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_NO_QUIERO
  
  def __str__(self) -> str:
    return f"{self.jid} no-quiero"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []

    seFueAlMazo = p.manojo(self.jid).se_fue_al_mazo
    if seFueAlMazo:
      pkts += [Envelope(
          dest=[p.manojo(self.jid).jugador.id],
          m=Message(
            CodMsg.ERROR,
            data="Te fuiste al mazo; no podes Hacer esta jugada")
        )] if p.verbose else []
      return pkts, False
    
    # checkeo flor en juego
    # caso particular del checkeo: no se le puede decir quiero a la flor
    # pero si a la contra flor o contra flor al resto
    # FALSO porque el no quiero lo estoy contando como un "con flor me achico"
    # todo: agregar la jugada: "con flor me achico" y editar la variale:
    # AHORA:
    # laFlorEsRespondible := p.Ronda.Flor >= FLOR && p.Ronda.Manojo[p.Ronda.Envite.CantadoPor].Jugador.equipo != p.Manojo(jugada.JID).Jugador.Equipo
    # LUEGO DE AGREGAR LA JUGADA "con flor me achico"
    # laFlorEsRespondible := p.Ronda.Flor > FLOR
    # FALSO ---> directamente se va la posibilidad de reponderle
    # "no quiero a la flor"
    # se acepta una respuesta 'no quiero' solo cuando:
    # - CASO I: se toco el envido (o similar)
    # - CASO II: se grito el truco (o similar)
    # en caso contrario, es incorrecto -> error

    elEnvidoEsRespondible = (p.ronda.envite.estado >= EstadoEnvite.ENVIDO and p.ronda.envite.estado <= EstadoEnvite.FALTAENVIDO) and p.ronda.envite.cantado_por != p.manojo(self.jid).jugador.id
    laFlorEsRespondible = p.ronda.envite.estado >= EstadoEnvite.FLOR and p.ronda.envite.cantado_por != p.manojo(self.jid).jugador.id
    elTrucoEsRespondible = p.ronda.truco.estado.es_truco_respondible() and p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo

    ok = elEnvidoEsRespondible or laFlorEsRespondible or elTrucoEsRespondible

    if not ok:
      # si no, esta respondiendo al pedo
      pkts += [Envelope(
          dest=[p.manojo(self.jid).jugador.id],
          m=Message(
            CodMsg.ERROR,
            data=f"{p.manojo(self.jid).jugador.id} esta respondiendo al pedo; no hay nada respondible")
        )] if p.verbose else []
      return pkts, False
    
    if elEnvidoEsRespondible:
      esDelEquipoContrario = p.manojo(self.jid).jugador.equipo != p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo
      if not esDelEquipoContrario:
        pkts += [Envelope(
            dest=[p.manojo(self.jid).jugador.id],
            m=Message(
              CodMsg.ERROR,
              data=f"La jugada no es valida")
          )] if p.verbose else []
        return pkts, False
    elif laFlorEsRespondible:
      # tengo que verificar si efectivamente tiene flor
      tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
      esDelEquipoContrario = p.manojo(self.jid).jugador.equipo != p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo
      ok = tieneFlor and esDelEquipoContrario
      if not ok:
        pkts += [Envelope(
            dest=[p.manojo(self.jid).jugador.id],
            m=Message(
              CodMsg.ERROR,
              data=f"La jugada no es valida")
          )] if p.verbose else []
        return pkts, False

    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    elEnvidoEsRespondible = (p.ronda.envite.estado >= EstadoEnvite.ENVIDO and p.ronda.envite.estado <= EstadoEnvite.FALTAENVIDO) and p.ronda.envite.cantado_por != p.manojo(self.jid).jugador.id
    laFlorEsRespondible = p.ronda.envite.estado >= EstadoEnvite.FLOR and p.ronda.envite.cantado_por != p.manojo(self.jid).jugador.id
    elTrucoEsRespondible = p.ronda.truco.estado.es_truco_respondible() and p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    
    if elEnvidoEsRespondible:

      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.NO_QUIERO,
          data=p.manojo(self.jid).jugador.id)
      )] if p.verbose else []

      # no se toma en cuenta el puntaje total del ultimo toque
      totalPts :int = 0

      if p.ronda.envite.estado == EstadoEnvite.ENVIDO:
        totalPts = p.ronda.envite.puntaje - 1
      elif p.ronda.envite.estado == EstadoEnvite.REALENVIDO:
        totalPts = p.ronda.envite.puntaje - 2
      elif p.ronda.envite.estado == EstadoEnvite.FALTAENVIDO:
        totalPts = p.ronda.envite.puntaje + 1

      p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
      p.ronda.envite.sin_cantar = []
      p.ronda.envite.puntaje = totalPts

      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.SUMA_PTS,
          data={
          "autor": p.ronda.envite.cantado_por,
          "razon": Razon.ENVITE_NO_QUERIDO,
          "puntos": totalPts,
        })
      )] if p.verbose else []

      p.suma_puntos(p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo, totalPts)

    elif laFlorEsRespondible:

      # todo ok: tiene flor; se pasa a jugar:
      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.CON_FLOR_ME_ACHICO,
          data=p.manojo(self.jid).jugador.id)
      )] if p.verbose else []

      # cuenta como un "no quiero" (codigo copiado)
      # segun el estado de la apuesta actual:
      # los "me achico" no cuentan para la flor
      # Flor		xcg(+3) / xcg(+3)
      # Flor + Contra-Flor		xc(+3) / xCadaFlorDelQueHizoElDesafio(+3) + 1
      # Flor + [Contra-Flor] + ContraFlorAlResto		~Falta Envido + *TODAS* las flores no achicadas / xcg(+3) + 1

      # sumo todas las flores del equipo contrario
      totalPts :int = 0

      for m in p.ronda.manojos:
        esDelEquipoContrario = p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
        tieneFlor, _ = m.tiene_flor(p.ronda.muestra)
        if tieneFlor and esDelEquipoContrario:
          totalPts += 3

      if p.ronda.envite.estado == EstadoEnvite.CONTRAFLOR or p.ronda.envite.estado == EstadoEnvite.CONTRAFLORALRESTO:
        # si es contraflor o al resto
        # se suma 1 por el `no quiero`
        totalPts += 1

      p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
      p.ronda.envite.sin_cantar = []

      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.SUMA_PTS,
          data={
          "autor": p.ronda.envite.cantado_por,
          "razon": Razon.FLOR_ACHICADA,
          "puntos": totalPts,
        })
      )] if p.verbose else []

      p.suma_puntos(p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo, totalPts)

    elif elTrucoEsRespondible:
      
      pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.NO_QUIERO,
          data=p.manojo(self.jid).jugador.id)
      )] if p.verbose else []

      # pongo al equipo que propuso el truco como ganador de la mano actual
      manoActual = p.ronda.mano_en_juego.to_ix()
      p.ronda.manos[manoActual].ganador = p.ronda.truco.cantado_por
      equipoGanador = Resultado.GANO_AZUL
      if p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo == Equipo.ROJO:
        equipoGanador = Resultado.GANO_ROJO
      
      p.ronda.manos[manoActual].resultado = equipoGanador

      NuevaRonda, res = p.evaluar_ronda()

      pkts += res

      if NuevaRonda:
        if not p.terminada():
          # ahora se deberia de incrementar el mano
          # y ser el turno de este
          sigMano = p.ronda.get_sig_el_mano()
          p.nueva_ronda(sigMano) # todo: el tema es que cuando llama aca
          # no manda mensaje de que arranco nueva ronda
          # falso: el padre que llama a .EvaluarRonda tiene que fijarse si
          # retorno true
          # entonces debe crearla el
          # no es responsabilidad de EvaluarRonda arrancar una ronda nueva!!
          # de hecho, si una ronda es terminable y se llama 2 veces consecutivas
          # al mismo metodo booleano, en ambas oportunidades retorna diferente
          # ridiculo
          pkts += [
            Envelope(
              dest=[m.jugador.id],
              m=Message(
                CodMsg.NUEVA_RONDA,
                data=p.perspectiva(m.jugador.id).to_dict())
            ) for m in p.ronda.manojos ] if p.verbose else []    
    
    return pkts   

class IrseAlMazo(IJugada):
  def __init__(self, jid:str):
    self.jid   :str   = jid
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_MAZO
  
  def __str__(self) -> str:
    return f"{self.jid} mazo"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
    pkts :list[Envelope] = []

    # checkeos:
    yaSeFueAlMazo = p.manojo(self.jid).se_fue_al_mazo
    yaTiroTodasSusCartas = p.manojo(self.jid).get_cant_cartas_tiradas() == 3
    if yaSeFueAlMazo or yaTiroTodasSusCartas:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible irse al mazo ahora")
      )] if p.verbose else []
      return pkts, False
    
    seEstabaJugandoElEnvido = (p.ronda.envite.estado >= EstadoEnvite.ENVIDO and p.ronda.envite.estado <= EstadoEnvite.FALTAENVIDO)
    seEstabaJugandoLaFlor = p.ronda.envite.estado >= EstadoEnvite.FLOR
    seEstabaJugandoElTruco = p.ronda.truco.estado.es_truco_respondible()

    # no se puede ir al mazo sii:
    # 1. el fue el que canto el envido (y el envido esta en juego)
    # 2. tampoco se puede ir al mazo si el canto la flor o similar
    # 3. tampoco se puede ir al mazo si el grito el truco
    
    noSePuedeIrPorElEnvite = (seEstabaJugandoElEnvido or seEstabaJugandoLaFlor) and p.ronda.envite.cantado_por == p.manojo(self.jid).jugador.id
    # la de la flor es igual al del envido; porque es un envite
    noSePuedeIrPorElTruco = seEstabaJugandoElTruco and p.ronda.truco.cantado_por == p.manojo(self.jid).jugador.id
    if noSePuedeIrPorElEnvite or noSePuedeIrPorElTruco:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible irse al mazo ahora")
      )] if p.verbose else []
      return pkts, False
    
    # por como esta hecho el algoritmo EvaluarMano:

    esPrimeraMano = p.ronda.mano_en_juego == NumMano.PRIMERA
    tiradas = p.ronda.get_mano_actual().cartas_tiradas
    n = len(tiradas)

    soloMiEquipoTiro = n == 1 and p.ronda.manojo(tiradas[n-1].jugador).jugador.equipo == p.manojo(self.jid).jugador.equipo

    equipoDelJugador = p.manojo(self.jid).jugador.equipo
    soyElUnicoDeMiEquipo = p.ronda.cant_jugadores_en_juego[equipoDelJugador] == 1
    noSePuedeIr = esPrimeraMano and soloMiEquipoTiro and soyElUnicoDeMiEquipo

    # que pasa si alguien dice truco y se va al mazo?

    if noSePuedeIr:
      pkts += [Envelope(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible irse al mazo ahora")
      )] if p.verbose else []
      return pkts, False
      
    return pkts, True

  def hacer(self, p:Partida) -> list[Envelope]:
    pkts :list[Envelope] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    pkts += [Envelope(
        dest=["ALL"],
        m=Message(
          CodMsg.MAZO,
          data=p.manojo(self.jid).jugador.id
        )
      )] if p.verbose else []
    
    p.ir_al_mazo(p.manojo(self.jid))

    equipoDelJugador = p.manojo(self.jid).jugador.equipo

    seFueronTodos = p.ronda.cant_jugadores_en_juego[equipoDelJugador] == 0

    # si tenia flor -> ya no lo tomo en cuenta
    tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
    if tieneFlor:
      p.ronda.envite.jugadores_con_flor = [
        m for m in p.ronda.envite.jugadores_con_flor \
          if m.jugador.id != p.manojo(self.jid).jugador.id
      ]
      
      p.ronda.envite.canto_flor(p.manojo(self.jid).jugador.id)
      # que pasa si era el ultimo que se esperaba que cantara flor?
      # tengo que Hacer el Eval de la flor
      todosLosJugadoresConFlorCantaron = len(p.ronda.envite.sin_cantar) == 0
      if todosLosJugadoresConFlorCantaron:
        pkts += CantarFlor.eval(p)

    # era el ultimo en tirar de esta mano?
    eraElUltimoEnTirar = p.ronda.get_sig_habilitado(p.manojo(self.jid)) == None

    if seFueronTodos:

      seEstabaJugandoElEnvido = (p.ronda.envite.estado >= EstadoEnvite.ENVIDO and p.ronda.envite.estado <= EstadoEnvite.FALTAENVIDO)
      seEstabaJugandoLaFlor = p.ronda.envite.estado >= EstadoEnvite.FLOR

      # el equipo contrario gana la ronda
      # y todo lo que estaba en juego hasta ahora
      # envido; flor; truco;
      # si no habia nada en juego -> suma 1 punto

      if seEstabaJugandoElEnvido:
        # cuenta como un "no quiero"

        # codigo copiado de "no quiero"
        #	no se toma en cuenta el puntaje total del ultimo toque
        totalPts :int = 0
        e = p.ronda.envite

        if e.estado == EstadoEnvite.ENVIDO:
          totalPts = e.puntaje - 1
        elif e.estado == EstadoEnvite.REALENVIDO:
          totalPts = e.puntaje - 2
        elif e.estado == EstadoEnvite.FALTAENVIDO:
          totalPts = e.puntaje + 1

        e.estado = EstadoEnvite.DESHABILITADO
        p.ronda.envite.sin_cantar = []
        e.puntaje = totalPts

        pkts += [Envelope(
          dest=["ALL"],
          m=Message(
            CodMsg.SUMA_PTS,
            data={
            "autor": e.cantado_por,
            "razon": Razon.ENVITE_NO_QUERIDO,
            "puntos": totalPts,
          })
        )] if p.verbose else []

        p.suma_puntos(p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo, totalPts)

      

      if seEstabaJugandoLaFlor:
        # cuenta como un "no quiero"
        # segun el estado de la apuesta actual:
        # los "me achico" no cuentan para la flor
        # Flor		xcg(+3) / xcg(+3)
        # Flor + Contra-Flor		xc(+3) / xCadaFlorDelQueHizoElDesafio(+3) + 1
        # Flor + [Contra-Flor] + ContraFlorAlResto		~Falta Envido + *TODAS* las flores no achicadas / xcg(+3) + 1

        # sumo todas las flores del equipo contrario
        totalPts :int = 0

        for m in p.ronda.manojos:
          esDelEquipoContrario = p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
          tieneFlor, _ = m.tiene_flor(p.ronda.muestra)
          if tieneFlor and esDelEquipoContrario:
            totalPts += 3

        if p.ronda.envite.estado == EstadoEnvite.CONTRAFLOR or p.ronda.envite.estado == EstadoEnvite.CONTRAFLORALRESTO:
          # si es contraflor o al resto
          # se suma 1 por el `no quiero`
          totalPts += 1

        p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
        p.ronda.envite.sin_cantar = []

        pkts += [Envelope(
          dest=["ALL"],
          m=Message(
            CodMsg.SUMA_PTS,
            data={
            "autor": p.ronda.envite.cantado_por,
            "razon": Razon.FLOR_ACHICADA,
            "puntos": totalPts,
          })
        )] if p.verbose else []

        p.suma_puntos(p.ronda.manojo(p.ronda.envite.cantado_por).jugador.equipo, totalPts)

    # evaluar ronda sii:
    # o bien se fueron todos
    # o bien este se fue al mazo, pero alguno de sus companeros no
    # (es decir que queda al menos 1 jugador en juego)
    hayQueEvaluarRonda = seFueronTodos or eraElUltimoEnTirar
    if hayQueEvaluarRonda:
      # de ser asi tengo que checkear el resultado de la mano
      # el turno del siguiente queda dado por el ganador de esta
      empiezaNuevaRonda, res = p.evaluar_mano()

      pkts += res

      if not empiezaNuevaRonda:

        # esta parte no tiene sentido: si se fue al mazo se sabe que va a
        # empezar una nueva ronda. Este `if` es codigo muerto

        # actualizo el mano
        p.ronda.manoEnJuego += 1
        p.ronda.set_next_turno_pos_mano()
        # lo envio
        pkts += [Envelope(
          dest=["ALL"],
          m=Message(
            CodMsg.SIG_TURNO_POSMANO,
            data=p.ronda.turno)
        )] if p.verbose else []

      else:

        if not p.terminada():
          # ahora se deberia de incrementar el mano
          # y ser el turno de este
          sigMano = p.ronda.get_sig_el_mano()
          p.nueva_ronda(sigMano) # todo: el tema es que cuando llama aca
          # no manda mensaje de que arranco nueva ronda
          # falso: el padre que llama a .EvaluarRonda tiene que fijarse si
          # retorno true
          # entonces debe crearla el
          # no es responsabilidad de EvaluarRonda arrancar una ronda nueva!!
          # de hecho, si una ronda es terminable y se llama 2 veces consecutivas
          # al mismo metodo booleano, en ambas oportunidades retorna diferente
          # ridiculo

          pkts += [
            Envelope(
              dest=[m.jugador.id],
              m=Message(
                CodMsg.NUEVA_RONDA,
                data=p.perspectiva(m.jugador.id).to_dict())
            ) for m in p.ronda.manojos ] if p.verbose else []    
      
    else:
      # cambio de turno solo si era su turno
      eraSuTurno = p.ronda.get_el_turno().jugador.id == p.manojo(self.jid).jugador.id
      if eraSuTurno:
        p.ronda.set_next_turno()
        pkts += [Envelope(
          dest=["ALL"],
          m=Message(
            CodMsg.SIG_TURNO,
            data=p.ronda.turno)
        )] if p.verbose else []    
     
    return pkts   

# class TemplateJugadaGenerica(IJugada):
#   def __init__(self, jid:str):
#     self.jid   :str   = jid
  
#   def id() -> IJUGADA_ID:
#     return IJUGADA_ID.JUGADA_GENERICA
  
#   def __str__(self) -> str:
#     return f"{self.jid} foo"

#   # Retorna true si la jugada es valida
#   def ok(self,p:Partida) -> tuple[list[Envelope], bool]:
#     pkts :list[Envelope] = []
#     return pkts, True

#   def hacer(self, p:Partida) -> list[Envelope]:
#     pkts :list[Envelope] = []
#     pre, ok = self.ok(p)
#     pkts += pre

#     if not ok:
#       return pkts
    
#     return pkts   