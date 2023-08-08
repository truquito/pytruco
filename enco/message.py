from .codmsg import CodMsg
from typing import Dict, Any

class Message():
  def __init__(
    self,
    t:CodMsg,
    data:any=None) -> None:

    self.cod :CodMsg = t
    self.cont   :str    = data
  
  def to_dict(self) -> Dict[str,Any]:
    return {
      "cod": str(self.cod),
      "cont": self.cont
    }
