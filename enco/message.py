from .codmsg import CodMsg
from typing import Dict

class Message():
  def __init__(
    self,
    t:CodMsg,
    data:any=None) -> None:

    self.codmsg :CodMsg = t
    self.cont   :str    = data