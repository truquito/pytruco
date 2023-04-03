class Jugador():
  def __init__(self, id, equipo):
    self.id = id
    self.equipo = equipo
  
  def __str__(self):
    return f"{self.id}"

  def __repr__(self) -> str:
    return str(self)