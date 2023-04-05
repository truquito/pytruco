from __future__ import annotations
from .partida import Partida
from .jugadas import IJUGADA_ID

from enco.packet import Packet


# IJugada Interface para las jugadas
class IJugada():
  def ok(self,p:Partida) -> tuple[list[Packet], bool]:
    pass
  def hacer(self, p:Partida) -> list[Packet]:
    pass
  def __str__(self) -> str:
    pass
  def ID() -> IJUGADA_ID:
    pass