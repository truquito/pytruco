from .codmsg import CodMsg
from typing import Dict, Any

class Message():
  def __init__(
    self,
    t:CodMsg,
    data:any=None) -> None:

    self.codmsg :CodMsg = t
    self.cont   :str    = data
  
  def to_dict(self) -> Dict[str,Any]:
    return {
      "codmsg": str(self.codmsg),
      "cont": self.cont
    }