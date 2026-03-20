import json

from pytruco.pdt.partida import Partida
from pytruco.enco.razon import Razon
from pytruco.enco.message import Message
from pytruco.enco.codmsg import CodMsg
from pytruco.pdt.partida import Partida, CartaTirada
from pytruco.pdt.envite import EstadoEnvite
from pytruco.pdt.truco import EstadoTruco
from pytruco.pdt.mano import NumMano, Resultado
from pytruco.pdt.carta import Carta
from pytruco.pdt.chi import chi

class Perspectiva():
  def __init__(self, nick: str, perspectiva: str):
    self.nick = nick
    self.parse(perspectiva)

  def parse(self, perspectiva: str):
    self.p = Partida.parse(perspectiva)
    self.indexar_manojos()
    self.cachear_flores(True)
    self.p.verbose = False

  def chi(self, allow_mazo=False):
    return chi(self.p, self.p.manojo(self.nick), allow_mazo)

  def get_flores(self):
    manojos_con_flor = []
    mi_equipo = self.p.manojo(self.nick).jugador.equipo

    for m in self.p.ronda.manojos:
      es_de_mi_equipo = mi_equipo == m.jugador.equipo
      if not es_de_mi_equipo:
        continue

      tiene_flor, _ = m.tiene_flor(self.p.ronda.muestra)
      if tiene_flor:
        manojos_con_flor.append(m)

    hay_flor = len(manojos_con_flor) > 0
    return hay_flor, manojos_con_flor

  def cachear_flores(self, reset: bool):
    _, jugadores_con_flor = self.get_flores()
    self.p.ronda.envite.jugadores_con_flor = jugadores_con_flor

    if reset:
      con_flor = []
      for m in jugadores_con_flor:
        con_flor.append(m.jugador.id)
      self.p.ronda.envite.sin_cantar = con_flor

  def indexar_manojos(self):
    if self.p.ronda.MIXS is None:
      self.p.ronda.MIXS = {}

    for i, m in enumerate(self.p.ronda.manojos):
      jid = m.jugador.id
      self.p.ronda.MIXS[jid] = i

  def canto_flor(self, j: str):
    xs = self.p.ronda.envite.sin_cantar

    for i, x in enumerate(self.p.ronda.envite.sin_cantar):
      if x == j:
        xs[i] = xs[len(xs) - 1]
        xs = xs[:len(xs) - 1]
        self.p.ronda.envite.sin_cantar = xs
        return

  def aplicar(self, msg: Message):
    # if str(msg.cod) == str(CodMsg.ABANDONO):
    #   pass
    # if str(msg.cod) == str(CodMsg.TIMEOUT):
    #   pass
    # if str(msg.cod) == str(CodMsg.BYEBYE):
    #   pass
    if str(msg.cod) == str(CodMsg.DICE_SON_BUENAS):
      # sé qué equipo ganó el envite
      self.p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
      self.p.ronda.envite.sin_cantar = []
    if str(msg.cod) == str(CodMsg.CANTAR_FLOR):
      self.p.ronda.envite.estado = EstadoEnvite.FLOR
      self.p.ronda.envite.cantado_por = msg.cont
      self.canto_flor(msg.cont)
    if str(msg.cod) == str(CodMsg.CANTAR_CONTRAFLOR):
      self.p.ronda.envite.estado = EstadoEnvite.CONTRAFLOR
      self.p.ronda.envite.cantado_por = msg.cont
      self.canto_flor(msg.cont)
    if str(msg.cod) == str(CodMsg.CANTAR_CONTRAFLOR_AL_RESTO):
      self.p.ronda.envite.estado = EstadoEnvite.CONTRAFLORALRESTO
      self.p.ronda.envite.cantado_por = msg.cont
      self.canto_flor(msg.cont)
    if str(msg.cod) == str(CodMsg.TOCAR_ENVIDO):
      self.p.ronda.envite.estado = EstadoEnvite.ENVIDO
      self.p.ronda.envite.cantado_por = msg.cont
      self.p.ronda.envite.puntaje += 2
      self.canto_flor(msg.cont)
    if str(msg.cod) == str(CodMsg.TOCAR_REALENVIDO):
      self.p.ronda.envite.estado = EstadoEnvite.REALENVIDO
      self.p.ronda.envite.cantado_por = msg.cont
      self.p.ronda.envite.puntaje += 3
      self.canto_flor(msg.cont)
    if str(msg.cod) == str(CodMsg.TOCAR_FALTAENVIDO):
      self.p.ronda.envite.estado = EstadoEnvite.FALTAENVIDO
      self.p.ronda.envite.cantado_por = msg.cont
      self.canto_flor(msg.cont)
    if str(msg.cod) == str(CodMsg.GRITAR_TRUCO):
      self.p.ronda.truco.estado = EstadoTruco.TRUCO
      self.p.ronda.truco.cantado_por = msg.cont
    if str(msg.cod) == str(CodMsg.GRITAR_RETRUCO):
      self.p.ronda.truco.estado = EstadoTruco.RETRUCO
      self.p.ronda.truco.cantado_por = msg.cont
    if str(msg.cod) == str(CodMsg.GRITAR_VALE4):
      self.p.ronda.truco.estado = EstadoTruco.VALE4
      self.p.ronda.truco.cantado_por = msg.cont
    if str(msg.cod) == str(CodMsg.NO_QUIERO):
      if self.p.ronda.envite.estado != EstadoEnvite.DESHABILITADO:
        self.p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
        self.p.ronda.envite.sin_cantar = []
      else:
        # si es al truco al que le esta diciendo `NO_QUIERO` entonces deberia de
        # empezar una nueva ronda.
        # enotnces antes de tomar una accion deberia esperar un tiempo asi le doy
        # tiempo a que lleguen los otros mensajes 
        pass
    if str(msg.cod) == str(CodMsg.CON_FLOR_ME_ACHICO):
      self.p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
      self.p.ronda.envite.sin_cantar = []
    if str(msg.cod) == str(CodMsg.QUIERO_TRUCO):
      if self.p.ronda.truco.estado == EstadoTruco.TRUCO:
        self.p.ronda.truco.estado = EstadoTruco.TRUCOQUERIDO
      elif self.p.ronda.truco.estado == EstadoTruco.RETRUCO:
        self.p.ronda.truco.estado = EstadoTruco.RETRUCOQUERIDO
      elif self.p.ronda.truco.estado == EstadoTruco.VALE4:
        self.p.ronda.truco.estado = EstadoTruco.VALE4QUERIDO
      self.p.ronda.truco.cantado_por = msg.cont # <--- que tipo de cont
    if str(msg.cod) == str(CodMsg.QUIERO_ENVITE):
      # self.p.ronda.envite.estado = # el estado queda igual ?
      # se pasaria a evaluar
      if self.p.ronda.envite.estado >= EstadoEnvite.FLOR:
        self.canto_flor(msg.cont)
      self.p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
      self.p.ronda.envite.sin_cantar = []
    if str(msg.cod) == str(CodMsg.SIG_TURNO):
      self.p.ronda.turno = msg.cont
    if str(msg.cod) == str(CodMsg.SIG_TURNO_POSMANO):
      self.p.ronda.mano_en_juego = NumMano.inc(self.p.ronda.mano_en_juego)
      self.p.ronda.turno = msg.cont
      if self.p.ronda.envite.estado == EstadoEnvite.NOGRITADOAUNAUN:
        self.p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
    if str(msg.cod) == str(CodMsg.DICE_TENGO):
      pass
    if str(msg.cod) == str(CodMsg.DICE_SON_MEJORES):
      self.p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
      self.p.ronda.envite.cantado_por = msg.cont["autor"]
      self.p.ronda.envite.sin_cantar = []
    if str(msg.cod) == str(CodMsg.NUEVA_PARTIDA):
      data = json.dumps(msg.cont) # me viene un dict
      self.parse(data)
    if str(msg.cod) == str(CodMsg.NUEVA_RONDA):
      data = json.dumps(msg.cont) # me viene un dict
      self.parse(data)
    if str(msg.cod) == str(CodMsg.TIRAR_CARTA):
      jid, palo, valor = msg.cont["autor"], msg.cont["palo"], msg.cont["valor"]
      m = self.p.ronda.manojo(jid)
      c = Carta(valor, palo)
      # si no es de mi equipo, entonces supongo que la carta es desconocida
      # le asigno cualquier slot
      es_de_equipo_contrario = m.jugador.equipo != self.p.manojo(self.nick).jugador.equipo
      if es_de_equipo_contrario:
        # entonces uso el primer slot
        for i,x in enumerate(m.cartas):
          if x == None:
            m.ultima_tirada = i
            m.tiradas[i] = True
            m.cartas[i] = c
            break
      else:
        for i,x in enumerate(m.cartas):
          if x == c:
            m.ultima_tirada = i
            m.tiradas[i] = True
            break
      # tambien la agrego a la mano/tiradas
      self.p.ronda.get_mano_actual().agregar_tirada(CartaTirada(jid, c))
    if str(msg.cod) == str(CodMsg.SUMA_PTS):
      jid, pts = msg.cont["autor"], msg.cont["puntos"]
      self.p.puntajes[self.p.ronda.manojo(jid).jugador.equipo] += pts
      # ahora la razon pude contener info importante:
      
      if msg.cont["razon"] in [Razon.ENVIDO_GANADO, Razon.REALENVIDO_GANADO, 
                              Razon.FALTA_ENVIDO_GANADO, Razon.ENVITE_NO_QUERIDO, 
                              Razon.FLOR_ACHICADA, Razon.LA_UNICA_FLOR, 
                              Razon.LAS_FLORES, Razon.LA_FLOR_MASALTA, 
                              Razon.CONTRAFLOR_GANADA, 
                              Razon.CONTRAFLOR_AL_RESTO_GANADA]:
        self.p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
        self.p.ronda.envite.sin_cantar = []
      elif msg.cont["razon"] == [Razon.TRUCO_NO_QUERIDO, Razon.TRUCO_QUERIDO, 
                              Razon.SE_FUERON_AL_MAZO]:
        # no hago nada
        pass
    if str(msg.cod) == str(CodMsg.MAZO):
      self.p.ronda.manojo(msg.cont).se_fue_al_mazo = True
    if str(msg.cod) == str(CodMsg.EL_ENVIDO_ESTA_PRIMERO):
      self.p.ronda.envite.estado = EstadoEnvite.ENVIDO
      self.p.ronda.envite.cantado_por = msg.cont
    if str(msg.cod) == str(CodMsg.LA_MANO_RESULTA_PARDA):
      self.p.ronda.get_mano_actual().resultado = Resultado.EMPARDADA
    if str(msg.cod) == str(CodMsg.MANO_GANADA):
      self.p.ronda.get_mano_actual().ganador = msg.cont["autor"]
    if str(msg.cod) == str(CodMsg.RONDA_GANADA):
      pass
