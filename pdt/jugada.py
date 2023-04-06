from __future__ import annotations
from .partida import Partida
from .jugadas import IJUGADA_ID
from .carta import Carta
from .envite import EstadoEnvite
from .mano import NumMano

from enco.packet import Packet
from enco.message import Message
from enco.codmsg import CodMsg

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
  
class TirarCarta(IJugada):
  def __init__(self, jid:str, carta:Carta):
    self.jid   :str   = jid
    self.carta :Carta = carta
  
  def id() -> IJUGADA_ID:
    return IJUGADA_ID.JID_TIRAR_CARTA
  
  def __str__(self) -> str:
    return f"{self.jid} {self.carta}"

  # Retorna true si la jugada es valida
  def ok(self,p:Partida) -> tuple[list[Packet], bool]:
    pkts :list[Packet] = []
    # checkeo si se fue al mazo
    noSeFueAlMazo = not p.manojo(self.jid).se_fue_al_mazo
    ok = noSeFueAlMazo
    if not ok:
      pkts += [Packet(
        ["ALL"],
        Message(
          CodMsg.ERROR,
          data="No es posible tirar una carta porque ya te fuiste al mazo")
      )]
      return pkts, False
    
    # esto es un tanto redundante porque es imposible que no sea su turno
    # (checkeado mas adelante) y que al mismo tiempo tenga algo para tirar
    # luego de haber jugado sus 3 cartas; aun asi lo dejo
    yaTiroTodasSusCartas = p.manojo(self.jid).get_cant_cartas_tiradas() == 3
    if yaTiroTodasSusCartas:
      pkts += [Packet(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tirar una carta porque ya las tiraste todas")
      )]
      return pkts, False
    
    # checkeo flor en juego
    enviteEnJuego = p.ronda.envite.estado >= EstadoEnvite.ENVIDO
    if enviteEnJuego:
      pkts += [Packet(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tirar una carta ahora porque el envite esta en juego")
      )]
      return pkts, False
    
    # primero que nada: tiene esa carta?
    idx = p.manojo(self.jid).get_carta_idx(self.carta)
    if idx is None:
      pkts += [Packet(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No tienes esa carta en tu manojo")
      )]
      return pkts, False
    
    # ya jugo esa carta?
    todaviaNoLaTiro = not p.manojo(self.jid).tiradas[idx]
    if not todaviaNoLaTiro:
      pkts += [Packet(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="Ya tiraste esa carta")
      )]
      return pkts, False
    
    # luego, era su turno?
    eraSuTurno = p.ronda.get_el_turno().jugador.id == p.manojo(self.jid).jugador.id
    if not eraSuTurno:
      pkts += [Packet(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No era su turno, no puede tirar la carta")
      )]
      return pkts, False
    
    # checkeo si tiene flor
    florHabilitada = (p.ronda.envite.estado >= EstadoEnvite.NOCANTADOAUN and \
                      p.ronda.envite.estado <= EstadoEnvite.FLOR) and \
                      p.ronda.mano_en_juego == NumMano.PRIMERA
    tieneFlor, _ = p.manojo(self.jid).tiene_flor(p.ronda.muestra)
    noCantoFlorAun = p.ronda.envite.no_canto_flor_aun(p.manojo(self.jid).jugador.id)
    noPuedeTirar = florHabilitada and tieneFlor and noCantoFlorAun
    if noPuedeTirar:
      pkts += [Packet(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tirar una carta sin antes cantar la flor")
      )]
      return pkts, False
    
    # cambio: ahora no puede tirar carta si el grito truco
    trucoGritado = p.ronda.truco.estado.es_truco_respondible()
    unoDelEquipoContrarioGritoTruco = trucoGritado and p.ronda.manojo(p.ronda.truco.cantado_por).jugador.equipo != p.manojo(self.jid).jugador.equipo
    yoGiteElTruco = trucoGritado and p.manojo(self.jid).jugador.id == p.ronda.truco.cantado_por
    elTrucoEsRespondible = trucoGritado and unoDelEquipoContrarioGritoTruco and not yoGiteElTruco
    if elTrucoEsRespondible:
      pkts += [Packet(
        dest=[p.manojo(self.jid).jugador.id],
        m=Message(
          CodMsg.ERROR,
          data="No es posible tirar una carta porque tu equipo debe responder \
            la propuesta del truco")
      )]
      return pkts, False

    return pkts, True   

  def hacer(self, p:Partida) -> list[Packet]:
    pkts :list[Packet] = []
    pre, ok = self.ok(p)
    pkts += pre

    if not ok:
      return pkts
    
    # ok la tiene y era su turno -> la juega
    pkts += [Packet(
        dest=["ALL"],
        m=Message(
          CodMsg.TIRAR_CARTA,
          data={
            "autor": p.manojo(self.jid).jugador.id,
            "palo": str(self.carta.palo),
            "valor": self.carta.valor })
      )]

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
        nadieCantoEnvite = p.ronda.envite.estado == EstadoEnvite.NOCANTADOAUN
        if seTerminoLaPrimeraMano and nadieCantoEnvite:
          p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
          p.ronda.envite.sin_cantar = []
        
        # actualizo el mano
        p.ronda.mano_en_juego = NumMano.inc(p.ronda.mano_en_juego)
        p.ronda.set_next_turno_pos_mano()
        # lo envio
        pkts += [Packet(
          dest=["ALL"],
          m=Message(
            CodMsg.SIG_TURNO_POSMANO,
            data={
              "valor": p.ronda.turno })
        )]

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
            Packet(
              dest=[m.jugador.id],
              m=Message(
                CodMsg.NUEVA_RONDA,
                data=p.perspectiva(m))
            ) for m in p.ronda.manojos ]

      # el turno del siguiente queda dado por el ganador de esta
    else:
      p.ronda.set_next_turno()
      pkts += [Packet(
          dest=["ALL"],
          m=Message(
            CodMsg.SIG_TURNO,
            data=p.ronda.turno)
        )]    

    return pkts


      


