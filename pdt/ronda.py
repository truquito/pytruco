from __future__ import annotations
from typing import Dict

from .mano import NumMano
from .carta import Carta, get_cartas_random
from .equipo import Equipo
from .envite import Envite
from .truco import Truco
from .manojo import Manojo
from .mano import Mano, Resultado
from .jugador import Jugador

from enco.packet import Packet
from enco.message import Message
from enco.codmsg import CodMsg

class Ronda():
  def __init__(self, azules:list[str], rojos:list[str], dummy=False):

    """
    - crea los Jugador'es
    - setea el numero de mano
    - setea el numero de jugadores en juego
    - setea mano, turno
    - crea Envite, Truco
    - crea manojos linkeados a los jugadores
    - crea el mapping MIXS: str -> int
    - crea 3 manos vacias

    si no es dummy:
      - reparte cartas+muestras
      - cachea flores
    """

    # check
    ok = len(azules) + len(rojos) == len(set(azules+rojos))
    if not ok:
      raise Exception("hay ID's de jugadores repetidos")

    cant_jugadores_por_equipo = len(azules)

    jugadores = [x for y in zip(azules, rojos) for x in y]
    jugadores = [
      Jugador(
        id=j,
        equipo=Equipo.AZUL if i % 2 == 0 else Equipo.ROJO
      ) for i,j in enumerate(jugadores)
    ]

    self.mano_en_juego  :NumMano  = NumMano.PRIMERA
    self.cant_jugadores_en_juego :Dict[Equipo, int] = {
      Equipo.ROJO: cant_jugadores_por_equipo,
      Equipo.AZUL: cant_jugadores_por_equipo,
    }
    self.el_mano  :int    = 0
    self.turno    :int    = 0
    self.envite   :Envite = Envite()
    self.truco    :Truco  = Truco()
    
    self.manojos :list[Manojo] = [
      Manojo(j) for j in jugadores
    ]

    self.MIXS :Dict[str, int] = None
    self.indexar_manojos()

    self.manos :list[Mano] = [Mano() for _ in range(3)]
    
    # reparto 3 cartas al azar a cada jugador
	  # y ademas una muestra, tambien al azar.
    self.muestra :Carta = None
    
    if dummy: return;
  
    self.repartir_cartas()
    self.cachear_flores(reset=True)
  
  def to_dict(self) -> Dict[str, any]:
    return {
      "manoEnJuego": self.mano_en_juego.to_ix(),
      "cantJugadoresEnJuego": {
        str(e).capitalize(): v \
        for e,v in self.cant_jugadores_en_juego.items()},
      "elMano": self.el_mano,
      "turno": self.turno,
      "envite": self.envite.to_dict(),
      "truco": self.truco.to_dict(),
      "manojos": [m.to_dict() for m in self.manojos],
      "mixs": self.MIXS,
      "muestra": self.muestra.to_dict(),
      "manos": [m.to_dict() for m in self.manos],
    }
  
  # GETTERS

  """dado un id de un jugador, retorna un puntero a su manojo"""
  def manojo(self, jid:str) -> Manojo:
    return self.manojos[self.MIXS[jid]] if jid in self.MIXS else None

  """retorna el indice del jugador identificado por `jid`"""
  def JIX(self, jid:str) -> int:
    return self.MIXS[jid]
  
  def get_el_mano(self) -> Manojo:
    return self.manojos[self.el_mano]
  
  """retorna el id del que deberia ser el siguiente mano"""
  def get_sig_el_mano(self) -> int:
    return self.JIX(self.get_siguiente(self.get_el_mano()).jugador.id)
  
  def get_el_turno(self) -> Manojo:
    return self.manojos[self.turno]
  
  def get_mano_anterior(self) -> Mano:
    return self.manos[self.mano_en_juego.to_ix() - 1]
  
  def get_mano_actual(self) -> Mano:
    return self.manos[self.mano_en_juego.to_ix()]
  
  def get_idx(self, m:Manojo) -> int:
    return self.MIXS[m.jugador.id]
  
  """retorna el indice del jugador siguiente a `j`"""
  def get_sig(self, j:int) -> int:
    cant_jugadores = len(self.manojos)
    es_el_ultimo = j == cant_jugadores - 1
    return 0 if es_el_ultimo else j + 1
  
  """para uso interno only; retorna un puntero al manojo que le sigue a `m`"""
  def get_siguiente(self, m:Manojo) -> Manojo:
    # ix = self.JIX(m.jugador.id)
    # cant_jugadores = len(self.manojos)
    # es_el_ultimo = ix == cant_jugadores - 1
    # return self.manojos[0] if es_el_ultimo else self.manojos[ix+1]
    ix = self.JIX(m.jugador.id)
    n = len(self.manojos)
    return self.manojos[(ix + 1) % n]
  
  """no era el ultimo si todavia queda al menos uno
  que viene despues de el que todavia no se fue al mazo
  y todavia no tiro carta en esta mano
  o bien: era el ultimo sii el siguiente de el era el mano
  """
  def get_sig_habilitado(self, m:Manojo) -> Manojo:
    sig = m
    n = len(self.manojos)
    for i in range(n):
      sig = self.get_siguiente(sig)
      no_se_fue_al_mazo = not sig.se_fue_al_mazo
      ya_tiro_carta_en_esta_mano = sig.ya_tiro_carta(self.mano_en_juego)
      no_es_el = sig.jugador.id != m.jugador.id
      ok = no_se_fue_al_mazo and (not ya_tiro_carta_en_esta_mano) and no_es_el
      if ok:
        break
    
    return sig if sig.jugador.id != m.jugador.id else None
  
  """retorna todos los manojos que tienen flor"""
  def get_flores(self) -> tuple[bool, list[Manojo]]:
    flores = [m for m in self.manojos if m.tiene_flor(self.muestra)[0]]
    hay_flores = len(flores) > 0
    return (hay_flores, flores)

  """retorna el manojo con la flor mas alta en la ronda y su valor
  PRE: hay flor"""
  def get_la_flor_mas_alta(self) -> tuple[Manojo, int]:
    flores   = [m.calc_flor(self.muestra) for m in self.manojos]
    max_flor = max(flores)
    max_ix   = flores.index(max_flor)
    return self.manojos[max_ix], max_flor
  
  def get_manojo(self, jix:int) -> Manojo:
    return self.manojos[jix]
  
  """
  
  PREDICADOS
  
  """

  def le_gana_de_mano(self, i:int, j:int) -> bool:
    """cambio de variable"""
    def cv(x:int, mano:int, cant_jugs:int) -> int:
      return x - mano if x >= mano else x + cant_jugs - mano
    
    n = len(self.manojos)
    # cambio de variables
    p = cv(i, self.el_mano, n)
    q = cv(j, self.el_mano, n)
    return p < q
  
  def hay_equipos_sin_cantar(self, equipo:Equipo) -> bool:
    for jid in self.envite.sin_cantar:
      mismo_equipo = self.manojo(jid).jugador.equipo == equipo
      if mismo_equipo:
        return True
    
    return False
  
  """este metodo es inseguro ya que manojoSigTurno puede ser nil"""
  def set_next_turno(self):
    manojo_turno_actual = self.manojos[self.turno]
    manojo_sig_turno = self.get_sig_habilitado(manojo_turno_actual)
    self.turno = self.JIX(manojo_sig_turno.jugador.id)

  def set_next_turno_pos_mano(self):
    # checkeo: si justo el nuevo turno, resulta que se fue al mazo
	  # entonces elijo el primero que encuentre que sea de su mismo equipo
	  # que no se haya ido al mazo:
    def safety_check():
      candidato = self.manojos[self.turno]
      if candidato.se_fue_al_mazo:
        n = len(self.manojos)
        start_from = self.el_mano
        for i in range(n):
          ix = (start_from + i) % n
          m = self.manojos[ix]
          mismo_equipo = m.jugador.equipo == candidato.jugador.equipo
          if mismo_equipo:
            self.turno = self.JIX(m.jugador.id)
            break
    
    # si es la Primera mano que se juega
	  # entonces es el turno del mano
    if self.mano_en_juego == NumMano.PRIMERA:
      self.turno = self.el_mano
      # si no, es turno del ganador de
		  # la mano anterior
      safety_check()
    else:
      # solo si la mano anterior no fue parda
		  # si fue parda busco la que empardo mas cercano al mano
      if self.get_mano_anterior().resultado != Resultado.EMPARDADA:
        ganador_anterior = self.get_mano_anterior().ganador
        manojo_ganador_anterior = self.manojo(ganador_anterior)
        self.turno = self.JIX(manojo_ganador_anterior.jugador.id)
        safety_check()
      else:
        # 1. obtengo la carta de maximo valor de la mano anterior
        # 2. busco a partir de la mano quien es el primero en tener
        #    esa carta y que no se haya ido al mazo aun
        # 3. si todos los que empardaron ya se fueron, entonces hago la
        #    vieja confiable (302)
        # 1.
        muestra = self.muestra
        _max = max([t.carta.calc_poder(muestra) \
                      for t in self.get_mano_anterior().cartas_tiradas])
        # 2.
        for tirada in self.get_mano_anterior().cartas_tiradas:
          poder = tirada.carta.calc_poder(muestra)
          if poder == _max:
            if not self.manojo(tirada.jugador).se_fue_al_mazo:
              m = self.manojo(tirada.jugador)
              self.turno = self.JIX(m.jugador.id)
              safety_check()
              return
        # 3.
        # si llegue aca es porque los vejigas que empardaron se fueron
        # entonces agarro al primero a partir del mano que aun
        # no se haya ido
        el_mano = self.get_el_mano()
        sig = self.get_sig_habilitado(el_mano)
        self.turno = self.JIX(sig.jugador.id)
        safety_check()
  

  """
  
  SETTERS
  
  """

  def cachear_flores(self, reset:bool):
    _, jugadores_con_flor = self.get_flores()
    self.envite.juegadores_con_flor = jugadores_con_flor

    if reset:
      self.envite.sin_cantar = [m.jugador.id for m in jugadores_con_flor]


  """dada una lista de manojos: simplemente hace una copia de las cartas
  de las cartas del parametro `manojo` a `self`"""
  # DEPRECATED
  # def set_manojos(self, manojos:list[Manojo]):
  #   for i,m in enumerate(manojos):
  #     self.manojos[i] = m.cartas
  #   self.cachear_flores(True)

  def set_cartas(self, manojos:list[list[Carta]]):
    for i,m in enumerate(manojos):
      self.manojos[i].cartas = m
    self.cachear_flores(True)

  def set_muestra(self, muestra:Carta):
    self.muestra = muestra
    self.cachear_flores(True)
  
  """
  
  EDITORES
  
  """

  """exec_el_envido computa el envido de la ronda
  @return `jIdx JugadorIdx` Es el indice del jugador con
  el envido mas alto (i.e., ganador)
  @return `max int` Es el valor numerico del maximo envido
  @return `pkts []*Packet` Es conjunto ordenado de todos
  los mensajes que normalmente se escucharian en una ronda
  de envido en la vida real.
  e.g.:
  	`pkts[0] = Jacinto dice: "tengo 9"`
    `pkts[1] = Patricio dice: "son buenas" (tenia 3)`
    `pkts[2] = Pedro dice: "30 son mejores!"`
  	`pkts[3] = Juan dice: "33 son mejores!"`
  """
  def exec_el_envido(self) -> tuple[int, int, list[Packet]]:
    pkts :list[Packet] = []
    
    cant_jugadores = len(self.manojos)

    # decir envidos en orden segun las reglas:
	  # empieza la mano
	  # canta el siguiente en sentido anti-horario sii
	  # tiene MAS pts que el maximo actual y es de equipo
	  # contrario. de no ser asi: o bien "pasa" o bien dice
	  # "son buenas" dependiendo del caso
	  # asi hasta terminar una ronda completa sin decir nada

	  # calculo y cacheo todos los envidos
    envidos = [m.calcular_envido(self.muestra) for m in self.manojos]

    # `yaDijeron` indica que jugador ya "dijo"
    # si tenia mejor, o peor envido. Por lo tanto,
    # ya no es tenido en cuenta.
    ya_dijeron = [False] * cant_jugadores

    # empieza el mas cercano a la mano (inclusive), el que no se haya ido aun
    jIdx = self.el_mano
    while self.manojos[jIdx].se_fue_al_mazo:
      jIdx = (jIdx + 1) % cant_jugadores
    
    ya_dijeron[jIdx] = True

    pkts += [Packet(
      ["ALL"],
      Message(
        CodMsg.DICE_TENGO,
        data={
          "autor": self.manojos[jIdx].jugador.id,
          "valor": envidos[jIdx]
        })
    )]
    
    # `todaviaNoDijeronSonMejores` se usa para
    # no andar repitiendo "son bueanas" "son buenas"
    # por cada jugador que haya jugado "de callado"
    # y ahora resulte tener peor envido.
    # agiliza el juego, de forma tal que solo se
    # escucha decir "xx son mejores", "yy son mejores"
    # "zz son mejores"
    todaviaNoDijeronSonMejores = True

    # iterador
    i = self.el_mano + 1 if self.el_mano != cant_jugadores - 1 else 0

    # termina el bucle cuando se haya dado
    # "una vuelta completa" de:mano+1 hasta:mano
    # ergo, cuando se "resetea" el iterador,
    # se setea a `p.Ronda.elMano + 1`
    while i != self.el_mano:
      se_fue_al_mazo = self.manojos[i].se_fue_al_mazo
      todaviaEsTenidoEnCuenta = (not ya_dijeron[i]) and (not se_fue_al_mazo)
      if todaviaEsTenidoEnCuenta:
        esDeEquipoContrario = self.manojos[i].jugador.equipo != self.manojos[jIdx].jugador.equipo
        tieneEnvidoMasAlto  = envidos[i] > envidos[jIdx]
        tieneEnvidoIgual    = envidos[i] == envidos[jIdx]
        leGanaDeMano        = self.le_gana_de_mano(i, jIdx)
        sonMejores          = tieneEnvidoMasAlto or (tieneEnvidoIgual and leGanaDeMano)

        if sonMejores:
          if esDeEquipoContrario:
            pkts += [Packet(
              ["ALL"],
              Message(
                CodMsg.DICE_SON_MEJORES,
                data={
                  "autor": self.manojos[i].jugador.id,
                  "valor": envidos[i]
                })
            )]

            jIdx = i
            ya_dijeron[i] = True
            todaviaNoDijeronSonMejores = False
            # se "resetea" el bucle
            i = self.get_sig(self.el_mano)

          else: # es del mismo equipo
            # no dice nada si es del mismo equipo
            # juega de callado & sigue siendo tenido
            # en cuenta
            i = self.get_sig(i)

        else: # tiene el envido mas chico
          if esDeEquipoContrario:
            if todaviaNoDijeronSonMejores:

              pkts += [Packet(
                ["ALL"],
                Message(
                  CodMsg.DICE_SON_BUENAS,
                  data={
                    "autor": self.manojos[i].jugador.id,
                    # valor de su envido es `envidos[i]` pero no corresponde decirlo
                  })
              )]

              ya_dijeron[i] = True
              # pasa al siguiente
            
            i = self.get_sig(i)
          else:
            # es del mismo equipo pero tiene un envido
            # mas bajo del que ya canto su equipo.
            # ya no lo tengo en cuenta, pero no dice nada.
            ya_dijeron[i] = True
            i = self.get_sig(i)

      else:
        # si no es tenido en cuenta,
        # simplemente pasar al siguiente
        i = self.get_sig(i)
      
    # fin bucle while

    max_envido = envidos[jIdx]
    return jIdx, max_envido, pkts

  
  """computa los cantos de la flor
  @return `j *Manojo` Es el ptr al manojo con
  la flor mas alta (i.e., ganador)
  @return `max int` Es el valor numerico de la flor mas alta
  @return `pkts []*Packet` Es conjunto ordenado de todos
  los mensajes que normalmente se escucharian en una ronda
  de flor en la vida real empezando desde jIdx
  e.g.:
  	`pkts[0] = Jacinto dice: "tengo 9"`
    `pkts[1] = Patricio dice: "son buenas" (tenia 3)`
    `pkts[2] = Pedro dice: "30 son mejores!"`
    `pkts[3] = Juan dice: "33 son mejores!"`
  """
  def exec_las_flores(self, aPartirDe:int) -> tuple[Manojo, int, list[Packet]]:
    pkts:list[Packet] = []

    # si solo un equipo tiene flor, entonces se saltea esta parte
    soloUnEquipoTieneFlores = True
    equipo = self.envite.juegadores_con_flor[0].jugador.equipo
    for m in self.envite.juegadores_con_flor[1:]:
      if m.jugador.equipo != equipo:
        soloUnEquipoTieneFlores = False
        break
    
    if soloUnEquipoTieneFlores:
      return self.envite.juegadores_con_flor[0], 0, []

    # decir flores en orden segun las reglas:
    # empieza el autor del envite
    # canta el siguiente en sentido anti-horario sii
    # tiene MAS pts que el maximo actual y es de equipo
    # contrario. de no ser asi: o bien "pasa" o bien dice
    # "son buenas" dependiendo del caso
    # asi hasta terminar una ronda completa sin decir nada

    # calculo y cacheo todas las flores
    flores = [m.calc_flor(self.muestra) for m in self.manojos] 

    # `yaDijeron` indica que jugador ya "dijo"
    # si tenia mejor, o peor envido. Por lo tanto,
    # ya no es tenido en cuenta.
    yaDijeron = [not(flores[i] and not m.se_fue_al_mazo)
                 for i,m in enumerate(self.manojos)]

    # `jIdx` indica el jugador con la flor mas alta

    # empieza el del parametro
    if flores[aPartirDe] > 0:
      yaDijeron[aPartirDe] = True
      pkts += [Packet(
        ["ALL"],
        Message(
          CodMsg.DICE_TENGO,
          data={
            "autor": self.manojos[aPartirDe].jugador.id,
            "valor": flores[aPartirDe],
          })
      )]

    # `todaviaNoDijeronSonMejores` se usa para
    # no andar repitiendo "son bueanas" "son buenas"
    # por cada jugador que haya jugado "de callado"
    # y ahora resulte tener peor envido.
    # agiliza el juego, de forma tal que solo se
    # escucha decir "xx son mejores", "yy son mejores"
    # "zz son mejores"
    todaviaNoDijeronSonMejores = True
    jIdx = aPartirDe
    i = self.get_sig(aPartirDe)

    # termina el bucle cuando se haya dado
    # "una vuelta completa" de:aPartirDe hasta:aPartirDe
    # ergo, cuando se "resetea" el iterador,
    while i != aPartirDe:
      todaviaEsTenidoEnCuenta = not yaDijeron[i]
      if todaviaEsTenidoEnCuenta:

        esDeEquipoContrario = self.manojos[i].jugador.equipo != self.manojos[jIdx].jugador.equipo
        tieneEnvidoMasAlto = flores[i] > flores[jIdx]
        tieneEnvidoIgual = flores[i] == flores[jIdx]
        leGanaDeMano = self.le_gana_de_mano(i, jIdx)
        sonMejores = tieneEnvidoMasAlto or (tieneEnvidoIgual and leGanaDeMano)

        if sonMejores:
          if esDeEquipoContrario:
            pkts += [Packet(
              ["ALL"],
              Message(
                CodMsg.DICE_SON_MEJORES,
                data={
                  "autor": self.manojos[i].jugador.id,
                  "valor": flores[i],
                })
            )]

            jIdx = i
            yaDijeron[i] = True
            todaviaNoDijeronSonMejores = False
            # se "resetea" el bucle
            i = self.get_sig(aPartirDe)

          else: # es del mismo equipo
            # no dice nada si es del mismo equipo
            # juega de callado & sigue siendo tenido
            # en cuenta
            i = self.get_sig(i)

        else: # tiene el envido mas chico
          if esDeEquipoContrario:
            if todaviaNoDijeronSonMejores:
              pkts += [Packet(
                ["ALL"],
                Message(
                  CodMsg.DICE_SON_BUENAS,
                  data={
                    "autor": self.manojos[i].jugador.id,
                    # valor de su envido es `flores[i]` pero no corresponde decirlo
                  })
              )]

              yaDijeron[i] = True
              # pasa al siguiente
            
            i = self.get_sig(i)
          else:
            # es del mismo equipo pero tiene un envido
            # mas bajo del que ya canto su equipo.
            # ya no lo tengo en cuenta, pero no dice nada.
            yaDijeron[i] = True
            i = self.get_sig(i)

      else:
        # si no es tenido en cuenta,
        # simplemente pasar al siguiente
        i = self.get_sig(i)

    max_flor = flores[jIdx]
    return self.get_manojo(jIdx), max_flor, pkts
    

  """
  
  INICIALIZADORES
  
  """

  def cachear_flores(self, reset:bool) -> None:
    _, jugadores_con_flor = self.get_flores()
    self.envite.juegadores_con_flor = jugadores_con_flor

    if reset:
      self.envite.sin_cantar = [m.jugador.id for m in jugadores_con_flor]

  def repartir_cartas(self) -> None:
    cant_jugadores = len(self.manojos)
    random_cards = get_cartas_random(3 * cant_jugadores + 1)
    for i,m in enumerate(self.manojos):
      seg = i*3
      m.cartas = random_cards[seg:seg+3]
      m.tiradas = [False] * 3
    
    # la ultima es la muestra
    self.muestra = random_cards[-1]

  def indexar_manojos(self) -> None:
    self.MIXS = {m.jugador.id:i for i,m in enumerate(self.manojos)}

  """resetea una ronda"""
  def reset(self, elMano:int) -> None:
    cant_jugadores = len(self.manojos)
    cant_jugadores_por_equipo = int(cant_jugadores / 2)

    self.mano_en_juego = NumMano.PRIMERA
    self.cant_jugadores_en_juego[Equipo.ROJO] = cant_jugadores_por_equipo
    self.cant_jugadores_en_juego[Equipo.AZUL] = cant_jugadores_por_equipo
    self.el_mano = elMano
    self.turno = elMano
    self.envite = Envite()
    self.turno = Truco()
    self.manos = [Mano() for _ in range(3)]

    for m in self.manojos:
      m.se_fue_al_mazo = False
      m.tiradas = [False] * 3

  def nueva_ronda(self, elMano:int) -> None:
    self.reset(elMano)
    # reparto 3 cartas al azar a cada jugador
	  # y ademas una muestra, tambien al azar.
    self.repartir_cartas()
    # flores
    self.cachear_flores(True)
  

