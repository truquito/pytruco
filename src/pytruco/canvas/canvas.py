from .geometry import Point

class Canvas:
  """
  canvas[x][y]
  """
  def __init__(self, width:int, height:int) -> None:
    self.width: int = width
    self.height: int = height
    self.content: list[list[str]] = [
      [' ' for _ in range(height)]
      for _ in range(width)
    ]

  @staticmethod
  def raw(obj:str) -> str:
    return obj.strip()
  
  @staticmethod
  def replace(this:str, that:str, here:str) -> str:
    return here.replace(this, that, 1)

  def debug(self, p:Point) -> tuple[str, str]:
    res = self.content[p.x][p.y]
    return res, res
  
  def render(self) -> str:
    """
    el string va a tener el mismo tamano que
    el canvas + los \n que no estan
    """
    res = [self.content[x][y] for y in range(self.height)[::-1] for x in range(self.width)]
    res = ["".join(res[i:i+self.width]) for i in range(0, len(res), self.width)]
    res  = "\n".join(res[::-1])
    return res

  def draw(self, fromX:int, fromY:int, obj:str) -> None:
    x, y = fromX, fromY

    for char in obj:
      if char == '\n':
        y += 1
        x = fromX
      else:
        self.content[x][y] = char
        x += 1

  def draw_at(self, p:Point, obj:str) -> None:
    self.draw(p.x, p.y, obj)