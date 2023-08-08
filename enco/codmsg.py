from enum import Enum

class CodMsg(Enum):
  # errores async
  ABANDONO                   = "Abandono"
  TIMEOUT                    = "TimeOut"
  # --
  ERROR                      = "Error"
  BYEBYE                     = "ByeBye"
  DICE_SON_BUENAS            = "DiceSonBuenas"
  CANTAR_FLOR                = "CantarFlor"
  CANTAR_CONTRAFLOR          = "CantarContraFlor"
  CANTAR_CONTRAFLOR_AL_RESTO = "CantarContraFlorAlResto"
  TOCAR_ENVIDO               = "TocarEnvido"
  TOCAR_REALENVIDO           = "TocarRealEnvido"
  TOCAR_FALTAENVIDO          = "TocarFaltaEnvido"
  GRITAR_TRUCO               = "GritarTruco"
  GRITAR_RETRUCO             = "GritarReTruco"
  GRITAR_VALE4               = "GritarVale4"
  NO_QUIERO                  = "NoQuiero"
  CON_FLOR_ME_ACHICO         = "ConFlorMeAchico"
  QUIERO_TRUCO               = "QuieroTruco"
  QUIERO_ENVITE              = "QuieroEnvite"
  SIG_TURNO                  = "SigTurno"
  SIG_TURNO_POSMANO          = "SigTurnoPosMano"
  DICE_TENGO                 = "DiceTengo"
  DICE_SON_MEJORES           = "DiceSonMejores"
  NUEVA_PARTIDA              = "NuevaPartida"
  NUEVA_RONDA                = "NuevaRonda"
  TIRAR_CARTA                = "TirarCarta"
  SUMA_PTS                   = "SumaPts"
  MAZO                       = "Mazo"
  EL_ENVIDO_ESTA_PRIMERO     = "ElEnvidoEstaPrimero"
  LA_MANO_RESULTA_PARDA      = "LaManoResultaParda"
  MANO_GANADA                = "ManoGanada"
  RONDA_GANADA               = "RondaGanada"

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)