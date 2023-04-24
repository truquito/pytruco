from enum import Enum

class Razon(str, Enum):
  ENVIDO_GANADO              = "EnvidoGanado"
  REALENVIDO_GANADO          = "RealEnvidoGanado"
  FALTA_ENVIDO_GANADO        = "FaltaEnvidoGanado"
  ENVITE_NO_QUERIDO          = "EnviteNoQuerido"
  FLOR_ACHICADA              = "FlorAchicada"
  LA_UNICA_FLOR              = "LaUnicaFlor"
  LAS_FLORES                 = "LasFlores"
  LA_FLOR_MASALTA            = "LaFlorMasAlta"
  CONTRAFLOR_GANADA          = "ContraFlorGanada"
  CONTRAFLOR_AL_RESTO_GANADA = "ContraFlorAlRestoGanada"
  TRUCO_NO_QUERIDO           = "TrucoNoQuerido"
  TRUCO_QUERIDO              = "TrucoQuerido"
  SE_FUERON_AL_MAZO          = "SeFueronAlMazo"

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)