from .message import Message

class Packet():
  def __init__(self, dest:list[str], m:Message) -> None:
    destination :list[str] = dest
    message     :Message   = m

  # def __str__(self) -> str:
  #   return f"???"

