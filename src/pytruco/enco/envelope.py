from .message import Message

class Envelope():
  def __init__(self, dest:list[str], m:Message) -> None:
    self.destination :list[str] = dest
    self.message     :Message   = m

  def __str__(self) -> str:
    import json
    return f"{self.destination} {json.dumps(self.message.to_dict())}"

