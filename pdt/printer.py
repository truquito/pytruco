# from __future__ import annotations
from enum import Enum
from typing import Dict

# canvas
from canvas.canvas import Canvas
from canvas.geometry import Rectangle, Point

# pdt
from .partida import Partida
from .carta import Carta
from .manojo import Manojo
from .ronda import Ronda
from .equipo import Equipo

max_len_msg = 13

class Templates:
  @staticmethod
  def render_valor_carta(valor:int) -> str:
    return f"{valor}─" if valor <= 9 else str(valor)

  @staticmethod
  def marco() -> str:
    marco = Canvas.raw("""
╔══════════════════════════════╗
║                              ║
║                              ║
║                              ║
║                              ║
║                              ║
║                              ║
║                              ║
╚══════════════════════════════╝
""")
    return marco
  
  @staticmethod
  def dialogo(up:bool) -> str:
    template = Canvas.raw("""
╭──────U──────╮
│             │
╰──────D──────╯
""")
    if up:
      template = Canvas.replace("U", "╩", template)
      template = Canvas.replace("D", "─", template)
    else:
      template = Canvas.replace("U", "─", template)
      template = Canvas.replace("D", "╦", template)
    return template

  @staticmethod
  def estadisticas() -> str:
    marco = Canvas.raw("""
╔════════════════╗
│ #Mano:         │
╠────────────────╣
│ Mano:          │
╠────────────────╣
│ Turno:         │
╠────────────────╣
│ Puntuacion:    │
╚════════════════╝
╔════════════════╗
│ Envite:        │
│ Por:           │
╠────────────────╣
│ Truco:         │
│ Por:           │
╚════════════════╝
╔═══════╦╦═══════╗
│       ││       │
╠───────┼┼───────╣
│       ││       │
╚═══════╩╩═══════╝
""")
    return marco
  
  @staticmethod
  def vacio() -> str:
    return ""

  @staticmethod
  def mk_carta(valor:str, palo:str) -> str:
    template = "┌xx┐" + "\n"
    template += "│PP│" + "\n"
    template += "└──┘"
    template = Canvas.replace("xx", valor, template)
    template = Canvas.replace("PP", palo.capitalize(), template)
    return template

  @staticmethod
  def carta(carta:Carta) -> str:
    valor, palo = carta.valor, str(carta.palo)
    numStr = Templates.render_valor_carta(valor)
    return Templates.mk_carta(numStr, palo[:2])
  
  @staticmethod
  def carta_oculta() -> str:
    return Templates.mk_carta("──", "#")
  
  @staticmethod
  def carta_doble_solapada(carta:Carta) -> str:
    valor, palo = carta.valor, str(carta.palo)
    cartaDobleSolapada = Canvas.raw("""
┌xx┐┐
│PP││
└──┘┘
""")
    numStr = Templates.render_valor_carta(valor)
    cartaDobleSolapada = Canvas.replace("xx", numStr, cartaDobleSolapada)
    cartaDobleSolapada = Canvas.replace("PP", palo[:2].capitalize(), cartaDobleSolapada)
    return cartaDobleSolapada
  
  @staticmethod
  def carta_triple_solapada(carta:Carta) -> str:
    valor, palo = carta.valor, str(carta.palo)
    cartaTripleSolapada = Canvas.raw("""
┌xx┐┐┐
│PP│││
└──┘┘┘
""")
    numStr = Templates.render_valor_carta(valor)
    cartaTripleSolapada = Canvas.replace("xx", numStr, cartaTripleSolapada)
    cartaTripleSolapada = Canvas.replace("PP", palo[:2].capitalize(), cartaTripleSolapada)
    return cartaTripleSolapada
  
  @staticmethod
  def mk_carta_doble_visible(valores:list[str], palos:list[str]) -> str:
    cartaDobleSolapada = Canvas.raw("""
┌xx┐yy┐
│PP│QQ│
└──┘──┘
""")
    cartaDobleSolapada = Canvas.replace("xx", valores[0], cartaDobleSolapada)
    cartaDobleSolapada = Canvas.replace("PP", palos[0].capitalize(), cartaDobleSolapada)
    cartaDobleSolapada = Canvas.replace("yy", valores[1], cartaDobleSolapada)
    cartaDobleSolapada = Canvas.replace("QQ", palos[1].capitalize(), cartaDobleSolapada)
    return cartaDobleSolapada
  
  @staticmethod
  def carta_doble_visible(cartas:list[Carta]) -> str:
    valor1, palo1 = cartas[0].valor, str(cartas[0].palo)
    numStr1 = Templates.render_valor_carta(valor1)
    valor2, palo2 = cartas[1].valor, str(cartas[1].palo)
    numStr2 = Templates.render_valor_carta(valor2)
    valores = [numStr1, numStr2]
    palos = [palo1[:2], palo2[:2]]
    return Templates.mk_carta_doble_visible(valores, palos)
  
  @staticmethod
  def carta_doble_oculta() -> str:
    valores = ["──", "──"]
    palos = ["#", "#"]
    return Templates.mk_carta_doble_visible(valores, palos)
  
  @staticmethod
  def mk_carta_triple_visible(valores:list[str], palos:list[str]) -> str:
    cartaDobleSolapada = Canvas.raw("""
┌xx┐yy┐zz┐
│PP│QQ│RR│
└──┘──┘──┘
""")
    cartaDobleSolapada = Canvas.replace("xx", valores[0], cartaDobleSolapada)
    cartaDobleSolapada = Canvas.replace("PP", palos[0].capitalize(), cartaDobleSolapada)
    cartaDobleSolapada = Canvas.replace("yy", valores[1], cartaDobleSolapada)
    cartaDobleSolapada = Canvas.replace("QQ", palos[1].capitalize(), cartaDobleSolapada)
    cartaDobleSolapada = Canvas.replace("zz", valores[2], cartaDobleSolapada)
    cartaDobleSolapada = Canvas.replace("RR", palos[2].capitalize(), cartaDobleSolapada)
    return cartaDobleSolapada
  
  @staticmethod
  def carta_triple_visible(cartas:list[Carta]) -> str:
    valor1, palo1 = cartas[0].valor, str(cartas[0].palo)
    numStr1 = Templates.render_valor_carta(valor1)
    valor2, palo2 = cartas[1].valor, str(cartas[1].palo)
    numStr2 = Templates.render_valor_carta(valor2)
    valor3, palo3 = cartas[2].valor, str(cartas[2].palo)
    numStr3 = Templates.render_valor_carta(valor3)
    valores = [numStr1, numStr2, numStr3]
    palos = [palo1[:2], palo2[:2], palo3[:2]]
    return Templates.mk_carta_triple_visible(valores, palos)
  
  @staticmethod
  def carta_triple_oculta() -> str:
    valores = ["──", "──", "──"]
    palos = ["#", "#", "#"]
    return Templates.mk_carta_triple_visible(valores, palos)
  


""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""

class Posicion(int, Enum):
  a = 0
  b = 1
  c = 2
  d = 3
  e = 4
  f = 5

class Dialogo:
  def __init__(self, id:str, msg:str) -> None:
    self.id :str = id
    self.msg :str = msg
  
class IPrinter:
  def dibujar_marco(self) -> None:
    pass
  def dibujar_estadisticas(self, p :Partida) -> None:
    pass
  def dibujar_muestra(self, muestra :Carta) -> None:
    pass
  def dibujar_nombres(self, manojos :list[Manojo], muestra :Carta) -> None:
    pass
  def dibujar_tiradas(self, manojos :list[Manojo]) -> None:
    pass
  def dibujar_posesiones(self, manojos :list[Manojo]) -> None:
    pass
  def dibujar_tooltips(self, r :Ronda) -> None:
    pass
  def dibujar_dialogos(self, r :Ronda, dialogos :list[Dialogo]) -> None:
    pass
  def render(self) -> str:
    pass

class Impresora:
  def __init__(self) -> None:      
    self.canvas          :Canvas                              = Canvas(80, 25)
    self.areas_jugadores :Dict[str, Dict[Posicion,Rectangle]] = None
    self.otras_areas     :Dict[str, Rectangle]                = None
  
  def render(self) -> str:
    return "\n" + self.canvas.render()
  
  def dibujar_marco(self) -> None:
    marco = Templates.marco()
    self.canvas.draw_at(self.otras_areas["exteriorMesa"]._from, marco)

  def dibujar_estadisticas(self, p:Partida) -> None:
    template = Templates.estadisticas()
    self.canvas.draw_at(self.otras_areas["estadisticas"]._from, template)

    # NUMERO DE Mano en juego
    numMano = str(p.ronda.mano_en_juego)
    self.canvas.draw_at(self.otras_areas["#Mano"]._from, numMano)

    # Mano
    mano = p.ronda.get_el_mano().jugador.id
    mano = mano[:8]
    self.canvas.draw_at(self.otras_areas["Mano"]._from, mano)

    # Turno
    turno = p.ronda.get_el_turno().jugador.id
    turno = turno[:8]
    self.canvas.draw_at(self.otras_areas["Turno"]._from, turno)

    # puntuacion
    puntuacion = str(p.puntuacion)
    self.canvas.draw_at(self.otras_areas["Puntuacion"]._from, puntuacion)

    # ------------------

    # Envite
    envite = str(p.ronda.envite.estado)
    envite = envite[:6]
    self.canvas.draw_at(self.otras_areas["Envite"]._from, envite)

    # Envite Autor
    envite_por = p.ronda.envite.cantado_por
    envite_por = envite_por[:6]
    self.canvas.draw_at(self.otras_areas["EnvitePor"]._from, envite_por)

    # Truco
    truco = str(p.ronda.truco.estado)
    truco = truco[:8]
    self.canvas.draw_at(self.otras_areas["Truco"]._from, truco)

    # Truco Autor
    truco_por = p.ronda.truco.cantado_por
    truco_por = truco_por[:9]
    self.canvas.draw_at(self.otras_areas["TrucoPor"]._from, truco_por)

    # ------------------

    # nombres
    nombreR, nombreA = "", ""

    if p.ronda.manojos[0].jugador.equipo == Equipo.ROJO:
      nombreR = p.ronda.manojos[0].jugador.id
      nombreA = p.ronda.manojos[1].jugador.id
    else:
      nombreR = p.ronda.manojos[1].jugador.id
      nombreA = p.ronda.manojos[0].jugador.id
    
    nombreR, nombreA = nombreR[:5], nombreA[:5]
    self.canvas.draw_at(self.otras_areas["nombreRojo"]._from, nombreR)
    self.canvas.draw_at(self.otras_areas["nombreAzul"]._from, nombreA)

    # ROJO
    ptjRojo = str(p.puntajes[Equipo.ROJO])
    self.canvas.draw_at(self.otras_areas["puntajeRojo"]._from, ptjRojo)

    # AZUL
    ptjAzul = str(p.puntajes[Equipo.AZUL])
    self.canvas.draw_at(self.otras_areas["puntajeAzul"]._from, ptjAzul)

  def dibujar_muestra(self, muestra:Carta) -> None:
    carta = Templates.carta(muestra)
    self.canvas.draw_at(self.otras_areas["muestra"]._from, carta)

  def dibujar_nombres(self, manojos:list[Manojo], muestra:Carta) -> None:
    for i, manojo in enumerate(manojos):
      nombre = manojo.jugador.id
      nombre = nombre[:10]
      area = self.areas_jugadores["nombres"][Posicion(i)]
      nombreCentrado :str = ""
      if Posicion(i) == Posicion.f:
        nombreCentrado = area.center(nombre)
      elif Posicion(i) == Posicion.c:
        nombreCentrado = area.center(nombre)
      else:
        nombreCentrado = area.center(nombre)
      
      self.canvas.draw_at(area._from, nombreCentrado)
    
  def dibujar_tiradas(self, manojos:list[Manojo]) -> None:
    area :Rectangle = None

    for i, _ in enumerate(manojos):
      area = self.areas_jugadores["tiradas"][Posicion(i)]
      # necesito saber cuantas tiro
      manojo = manojos[i]
      cantTiradas = manojo.get_cant_cartas_tiradas()
      carta = manojo.cartas[manojo.ultima_tirada]
      tiradas:str = Templates.carta(carta) if cantTiradas == 1 \
               else Templates.carta_doble_solapada(carta) if cantTiradas == 2 \
               else Templates.carta_triple_solapada(carta) if cantTiradas == 3 \
               else Templates.vacio()

      self.canvas.draw_at(area._from, area.center(tiradas))

  @staticmethod
  def las_conoce(cartas:list[Carta]) -> bool:
    return not any([c is None for c in cartas])
  
  def dibujar_posesiones(self, manojos:list[Manojo]) -> None:
    area :Rectangle = None

    for i, _ in enumerate(manojos):
      if manojos[i].se_fue_al_mazo:
        continue
      
      area = self.areas_jugadores["posesiones"][Posicion(i)]
      manojo = manojos[i]

      cartasEnPosesion = [
        c \
        for j,c in enumerate(manojo.cartas) if not manojo.tiradas[j]
      ]

      cantTiradas = manojo.get_cant_cartas_tiradas()
      cantPosesion = 3 - cantTiradas

      template :str = ""

      if Impresora.las_conoce(cartasEnPosesion):
        template = Templates.carta(cartasEnPosesion[0]) if cantPosesion == 1 \
              else Templates.carta_doble_visible(cartasEnPosesion) if cantPosesion == 2 \
              else Templates.carta_triple_visible(cartasEnPosesion) if cantPosesion == 3 \
              else Templates.vacio()
      else:
        template = Templates.carta_oculta() if cantPosesion == 1 \
              else Templates.carta_doble_oculta() if cantPosesion == 2 \
              else Templates.carta_triple_oculta() if cantPosesion == 3 \
              else Templates.vacio()
      
      self.canvas.draw_at(area._from, area.center(template))

  def dibujar_tooltips(self, r:Ronda) -> None:
    turno = r.turno

    for i, manojo in enumerate(r.manojos):
      tooltip = ""

      if manojo.se_fue_al_mazo:
        tooltip += "✗ "

      # flor
      if Impresora.las_conoce(manojo.cartas[:]):
        tieneFlor, _ = manojo.tiene_flor(r.muestra)
        if tieneFlor:
          tooltip += "❀"      

      # el turno
      esSuTurno = turno == i
      if esSuTurno:
        pos = Posicion(turno)
        tooltip += " ↑" if pos in [Posicion.a, Posicion.b] else " ↓"
      
      tooltip = tooltip.strip(" ")
      area = self.areas_jugadores["tooltips"][Posicion(i)]
      self.canvas.draw_at(area._from, area.center(tooltip))

  def dibujar_dialogos(self, r:Ronda, dialogos:list[Dialogo]) -> None:
    for d in dialogos:
      pos = next(i for i,m in enumerate(r.manojos) if m.jugador.id.lower() == d.id.lower())
     
      # d.Msg
      up = pos in [0,1]
      m = Templates.dialogo(up)

      area = self.areas_jugadores["dialogos"][Posicion(pos)]
      self.canvas.draw_at(area._from, m)

      m = d.msg[:max_len_msg]
      area = self.areas_jugadores["msgs"][Posicion(pos)]
      self.canvas.draw_at(area._from, area.center(m))

class Impresora6p(Impresora):
  def __init__(self) -> None:
    super().__init__()

    self.areas_jugadores = {
      "nombres": {
        Posicion.a: Rectangle(
          Point(19, 17),
          Point(28, 17),
        ),
        Posicion.b: Rectangle(
          Point(33, 17),
          Point(42, 17),
        ),
        Posicion.c: Rectangle(
          Point(50, 12),
          Point(59, 12),
        ),
        Posicion.d: Rectangle(
          Point(33, 7),
          Point(42, 7),
        ),
        Posicion.e: Rectangle(
          Point(19, 7),
          Point(28, 7),
        ),
        Posicion.f: Rectangle(
          Point(2, 12),
          Point(11, 12),
        ),
      },
      "tiradas": {
        Posicion.a: Rectangle(
          Point(23, 13),
          Point(28, 15),
        ),
        Posicion.b: Rectangle(
          Point(33, 13),
          Point(38, 15),
        ),
        Posicion.c: Rectangle(
          Point(39, 11),
          Point(44, 16),
        ),
        Posicion.d: Rectangle(
          Point(33, 9),
          Point(38, 11),
        ),
        Posicion.e: Rectangle(
          Point(23, 9),
          Point(28, 11),
        ),
        Posicion.f: Rectangle(
          Point(17, 11),
          Point(22, 13),
        ),
      },
      "posesiones": {
        Posicion.a: Rectangle(
          Point(19, 19),
          Point(28, 21),
        ),
        Posicion.b: Rectangle(
          Point(33, 19),
          Point(42, 21),
        ),
        Posicion.c: Rectangle(
          Point(50, 13),
          Point(59, 15),
        ),
        Posicion.d: Rectangle(
          Point(33, 3),
          Point(42, 5),
        ),
        Posicion.e: Rectangle(
          Point(19, 3),
          Point(28, 5),
        ),
        Posicion.f: Rectangle(
          Point(2, 13),
          Point(11, 15),
        ),
      },
      "tooltips": {
        Posicion.a: Rectangle(
          Point(19, 18),
          Point(28, 18),
        ),
        Posicion.b: Rectangle(
          Point(33, 18),
          Point(42, 18),
        ),
        Posicion.c: Rectangle(
          Point(48, 11),
          Point(57, 11),
        ),
        Posicion.d: Rectangle(
          Point(33, 6),
          Point(42, 6),
        ),
        Posicion.e: Rectangle(
          Point(19, 6),
          Point(28, 6),
        ),
        Posicion.f: Rectangle(
          Point(4, 11),
          Point(9, 15),
        ),
      },
      "dialogos": {
        Posicion.a: Rectangle(
          Point(16, 22),
          Point(30, 25),
        ),
        Posicion.b: Rectangle(
          Point(31, 22),
          Point(45, 25),
        ),
        Posicion.c: Rectangle(
          Point(47, 8),
          Point(56, 10),
        ),
        Posicion.d: Rectangle(
          Point(31, 0),
          Point(45, 3),
        ),
        Posicion.e: Rectangle(
          Point(16, 0),
          Point(30, 3),
        ),
        Posicion.f: Rectangle(
          Point(0, 8),
          Point(14, 10),
        ),
      },
      "msgs": {
        Posicion.a: Rectangle(
          Point(17, 23),
          Point(29, 23),
        ),
        Posicion.b: Rectangle(
          Point(32, 23),
          Point(44, 23),
        ),
        Posicion.c: Rectangle(
          Point(48, 9),
          Point(60, 9),
        ),
        Posicion.d: Rectangle(
          Point(32, 1),
          Point(44, 1),
        ),
        Posicion.e: Rectangle(
          Point(17, 1),
          Point(29, 1),
        ),
        Posicion.f: Rectangle(
          Point(1, 9),
          Point(13, 9),
        ),
      }
    }

    self.otras_areas = {
      "muestra": Rectangle(
        Point(29, 11),
        Point(32, 13),
      ),
      "exteriorMesa": Rectangle(
        Point(15, 8),
        Point(46, 16),
      ),
      "interiorMesa": Rectangle(
        Point(16, 9),
        Point(45, 15),
      ),
      "estadisticas": Rectangle(
        Point(62, 2),
        Point(79, 20),
      ),
      # -----------------------
      "#Mano": Rectangle(
        Point(71, 3),
        Point(77, 3),
      ),
      "Mano": Rectangle(
        Point(70, 5),
        Point(77, 5),
      ),
      "Turno": Rectangle(
        Point(71, 7),
        Point(77, 7),
      ),
      "Puntuacion": Rectangle(
        Point(76, 9),
        Point(77, 9),
      ),
      # -----------------------
      "Envite": Rectangle(
        Point(72, 12),
        Point(77, 12),
      ),
      "EnvitePor": Rectangle(
        Point(69, 13),
        Point(77, 13),
      ),
      "Truco": Rectangle(
        Point(71, 15),
        Point(77, 15),
      ),
      "TrucoPor": Rectangle(
        Point(69, 16),
        Point(77, 16),
      ),
      # -----------------------
      "nombreAzul": Rectangle(
        Point(64, 19),
        Point(77, 19), # tam 5
      ),
      "nombreRojo": Rectangle(
        Point(73, 19),
        Point(77, 19),
      ),
      "puntajeAzul": Rectangle(
        Point(66, 21),
        Point(67, 21),
      ),
      "puntajeRojo": Rectangle(
        Point(75, 21),
        Point(76, 21),
      ),
    }

class Impresora4p(Impresora):
  def __init__(self) -> None:
    super().__init__()
    im6 = Impresora6p()

    def mask6(attr:str) -> Dict[Posicion,Rectangle]:
      return {
        Posicion.a: im6.areas_jugadores[attr][Posicion.a],
        Posicion.b: im6.areas_jugadores[attr][Posicion.b],
        Posicion.c: im6.areas_jugadores[attr][Posicion.d],
        Posicion.d: im6.areas_jugadores[attr][Posicion.e],
      }

    self.areas_jugadores = {
      "nombres":    mask6("nombres"),
      "tiradas":    mask6("tiradas"),
      "posesiones": mask6("posesiones"),
      "tooltips":   mask6("tooltips"),
      "dialogos":   mask6("dialogos"),
      "msgs":       mask6("msgs"),
    }

    self.otras_areas = im6.otras_areas
      
class Impresora2p(Impresora):
  def __init__(self) -> None:
    super().__init__()
    im6 = Impresora6p()

    def mask6(attr:str) -> Dict[Posicion,Rectangle]:
      return {
        Posicion.a: im6.areas_jugadores[attr][Posicion.c],
        Posicion.b: im6.areas_jugadores[attr][Posicion.f],
      }

    self.areas_jugadores = {
      "nombres":    mask6("nombres"),
      "tiradas":    mask6("tiradas"),
      "posesiones": mask6("posesiones"),
      "tooltips":   mask6("tooltips"),
      "dialogos":   mask6("dialogos"),
      "msgs":       mask6("msgs"),
    }
    
    self.otras_areas = im6.otras_areas
  
  def dibujar_tooltips(self, r :Ronda) -> None:
    turno = r.turno

    for i, manojo in enumerate(r.manojos):
      tooltip = ""

      if Impresora.las_conoce(manojo.cartas[:]):
        tieneFlor, _ = manojo.tiene_flor(r.muestra)
        if tieneFlor:
          tooltip += "❀"

      esSuTurno = turno == i
      if esSuTurno:
        tooltip += " ↓"

      tooltip = tooltip.strip(" ")
      area = self.areas_jugadores["tooltips"][Posicion(i)]
      self.canvas.draw_at(area._from, area.center(tooltip))
    
  def dibujar_dialogos(self, r:Ronda, dialogos:list[Dialogo]) -> None:
    dialogo = Templates.dialogo(False)
    for d in dialogos:
      # que usuario es? ~ que pos le corresponde?
      pos :int = None
      pos = next(i for i,m in enumerate(r.manojos) if m.jugador.id.lower() == d.id.lower())
      area = self.areas_jugadores["dialogos"][Posicion(pos)]
      self.canvas.draw_at(area._from, dialogo)

      area = self.areas_jugadores["msgs"][Posicion(pos)]
      m = d.msg[:max_len_msg]
      self.canvas.draw_at(area._from, area.center(m))
    
def renderizar(p:Partida, dialogos:list[Dialogo]=[]) -> str:
  # como tiene el parametro en Print
  # basta con tener una sola instancia de impresora
  # para imprimir varias instancias de partidas diferentes
  n = len(p.ronda.manojos)
  pr :IPrinter = Impresora2p() if n == 2 \
            else Impresora4p() if n == 4 \
            else Impresora6p()

  pr.dibujar_marco()
  pr.dibujar_estadisticas(p)
  pr.dibujar_muestra(p.ronda.muestra)
  pr.dibujar_nombres(p.ronda.manojos, p.ronda.muestra)
  pr.dibujar_tiradas(p.ronda.manojos)
  pr.dibujar_posesiones(p.ronda.manojos)
  pr.dibujar_tooltips(p.ronda)
  pr.dibujar_dialogos(p.ronda, dialogos)

  return pr.render()