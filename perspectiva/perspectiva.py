import json

from pdt.partida import Partida
from enco.razon import Razon
from enco.message import Message
from enco.codmsg import CodMsg
from pdt.partida import Partida, CartaTirada
from pdt.envite import EstadoEnvite
from pdt.truco import EstadoTruco
from pdt.mano import NumMano, Resultado
from pdt.carta import Carta
from pdt.chi import chi

class Perspectiva():
  def __init__(self, nick:str, perspectiva: str):
    self.nick = nick
    self.p = Partida.parse(perspectiva)
    pass

  def chi(self, allow_mazo=False):
    return chi(self.p, self.p.manojo(self.nick), allow_mazo)

  def aplicar(self, msg :Message):
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
      if msg.cont in self.p.ronda.envite.sin_cantar:
        self.p.ronda.envite.sin_cantar.remove(msg.cont)
    if str(msg.cod) == str(CodMsg.CANTAR_CONTRAFLOR):
      self.p.ronda.envite.estado = EstadoEnvite.CONTRAFLOR
      self.p.ronda.envite.cantado_por = msg.cont
      if msg.cont in self.p.ronda.envite.sin_cantar:
        self.p.ronda.envite.sin_cantar.remove(msg.cont)
    if str(msg.cod) == str(CodMsg.CANTAR_CONTRAFLOR_AL_RESTO):
      self.p.ronda.envite.estado = EstadoEnvite.CONTRAFLORALRESTO
      self.p.ronda.envite.cantado_por = msg.cont
      if msg.cont in self.p.ronda.envite.sin_cantar:
        self.p.ronda.envite.sin_cantar.remove(msg.cont)
    if str(msg.cod) == str(CodMsg.TOCAR_ENVIDO):
      self.p.ronda.envite.estado = EstadoEnvite.ENVIDO
      self.p.ronda.envite.cantado_por = msg.cont
      self.p.ronda.envite.puntaje += 2
      if msg.cont in self.p.ronda.envite.sin_cantar:
        self.p.ronda.envite.sin_cantar.remove(msg.cont)
    if str(msg.cod) == str(CodMsg.TOCAR_REALENVIDO):
      self.p.ronda.envite.estado = EstadoEnvite.REALENVIDO
      self.p.ronda.envite.cantado_por = msg.cont
      self.p.ronda.envite.puntaje += 3
      if msg.cont in self.p.ronda.envite.sin_cantar:
        self.p.ronda.envite.sin_cantar.remove(msg.cont)
    if str(msg.cod) == str(CodMsg.TOCAR_FALTAENVIDO):
      self.p.ronda.envite.estado = EstadoEnvite.FALTAENVIDO
      self.p.ronda.envite.cantado_por = msg.cont
      if msg.cont in self.p.ronda.envite.sin_cantar:
        self.p.ronda.envite.sin_cantar.remove(msg.cont)
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
      self.p.ronda.envite.cantado_por = msg.cont
      self.p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
      self.p.ronda.envite.sin_cantar = []
    if str(msg.cod) == str(CodMsg.SIG_TURNO):
      self.p.ronda.turno = msg.cont
    if str(msg.cod) == str(CodMsg.SIG_TURNO_POSMANO):
      self.p.ronda.mano_en_juego = NumMano.inc(self.p.ronda.mano_en_juego)
      self.p.ronda.turno = msg.cont
    # if str(msg.cod) == str(CodMsg.DICE_TENGO):
    #   pass
    if str(msg.cod) == str(CodMsg.DICE_SON_MEJORES):
      # doy por ganado el envite
      self.p.ronda.envite.estado = EstadoEnvite.DESHABILITADO
      self.p.ronda.envite.cantado_por = msg.cont["autor"]
      self.p.ronda.envite.sin_cantar = []
    if str(msg.cod) == str(CodMsg.NUEVA_PARTIDA):
      data = json.dumps(msg.cont) # me viene un dict
      self.p = Partida.parse(data)
    if str(msg.cod) == str(CodMsg.NUEVA_RONDA):
      data = json.dumps(msg.cont) # me viene un dict
      self.p = Partida.parse(data)
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
      if msg.cont["razon"] == [Razon.TRUCO_NO_QUERIDO, Razon.TRUCO_QUERIDO, 
                              Razon.SE_FUERON_AL_MAZO]:
        # no hago nada
        pass
    if str(msg.cod) == str(CodMsg.MAZO):
      self.p.ronda.manojo(msg.cont).se_fue_al_mazo = True
    if str(msg.cod) == str(CodMsg.EL_ENVIDO_ESTA_PRIMERO):
      self.p.ronda.envite.estado = EstadoEnvite.ENVIDO
      self.p.ronda.envite.cantado_por = msg.cont
      self.p.ronda.truco.estado = EstadoTruco.NOGRITADOAUN
    if str(msg.cod) == str(CodMsg.LA_MANO_RESULTA_PARDA):
      self.p.ronda.get_mano_actual().resultado = Resultado.EMPARDADA
    if str(msg.cod) == str(CodMsg.MANO_GANADA):
      self.p.ronda.get_mano_actual().ganador = msg.cont["autor"]
    if str(msg.cod) == str(CodMsg.RONDA_GANADA):
      # ???? que voy a hacer
      pass