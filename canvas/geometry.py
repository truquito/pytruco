import math

class Point:
  def __init__(self, x:int, y:int) -> None:
    self.x = x
    self.y = y
  
class Rectangle:
  def __init__(self, _from:Point, _to:Point) -> None:
    self._from = _from
    self._to = _to
  
  @staticmethod
  def calc_width(obj:str) -> int:
    lines = obj.split("\n")
    return max([len(l) for l in lines])
  
  def center(self, obj:str) -> str:
    # res = ""
    rectanguloWidth = self._to.x - self._from.x + 1
    objWidth = self.calc_width(obj)
    restante = rectanguloWidth - objWidth
    paddingLeft = restante / 2.0
    PLredondeado = math.floor(paddingLeft)
    renderedPadding = " " * PLredondeado
    
    # for j, letter in enumerate(obj):
    #   if j == 0:
    #     res += renderedPadding
    #     res += letter
    #   elif obj[j] == '\n':
    #     res += letter
    #     res += renderedPadding
    #   else:
    #     res += letter
      
    return "".join([
      f"{renderedPadding}{letter}" if j == 0 else \
      f"{letter}{renderedPadding}" if obj[j] == '\n' else \
      f"{letter}"
      for j,letter in enumerate(obj) 
    ])

  def right(self, obj:str) -> str:
    # res = ""
    rectanguloWidth = self._to.x - self._from.x + 1
    objWidth = self.calc_width(obj)
    paddingLeft = rectanguloWidth - objWidth
    renderedPadding = " " * paddingLeft
      
    return "".join([
      f"{renderedPadding}{letter}" if j == 0 else \
      f"{letter}{renderedPadding}" if obj[j] == '\n' else \
      f"{letter}"
      for j,letter in enumerate(obj) 
    ])

  def left(self, obj:str) -> str:
    # res = ""
    rectanguloWidth = self._to.x - self._from.x + 1
    objWidth = self.calc_width(obj)
    paddingRight = rectanguloWidth - objWidth
    renderedPadding = " " * paddingRight
      
    return "".join([
      f"{letter}{renderedPadding}" if len(obj)-1 else \
      f"{renderedPadding}{letter}" if obj[j] == '\n' else \
      f"{letter}" \
      for j,letter in enumerate(obj) 
    ])