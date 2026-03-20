from enum import Enum

class IJUGADA_ID(int, Enum):
  JID_TIRAR_CARTA = 0
  JID_ENVIDO = 1
  JID_REAL_ENVIDO = 2
  JID_FALTA_ENVIDO = 3
  JID_FLOR = 4
  JID_CONTRA_FLOR = 5
  JID_CONTRA_FLOR_AL_RESTO = 6
  JID_TRUCO = 7
  JID_RE_TRUCO = 8
  JID_VALE_4 = 9
  JID_QUIERO = 10
  JID_NO_QUIERO = 11
  JID_MAZO = 12

  def __str__(self) -> str:
    return str(self.value)
  
  def __repr__(self) -> str:
    return str(self)