from pdt.partida import Partida

n = 2 # <-- num. of players
azules = ["Alice", "Ariana", "Annie"]
rojos = ["Bob", "Ben", "Bill"]
p = Partida(20, azules[:n>>1], rojos[:n>>1], verbose=False)
# p = Partida.parse('{"puntuacion": 20, "puntajes": {"Azul": 19, "Rojo": 19}, "ronda": {"manoEnJuego": 0, "cantJugadoresEnJuego": {"Rojo": 1, "Azul": 1}, "elMano": 0, "turno": 0, "envite": {"estado": "noCantadoAun", "puntaje": 0, "cantadoPor": "", "sinCantar": []}, "truco": {"cantadoPor": "", "estado": "noCantado"}, "manojos": [{"seFueAlMazo": false, "cartas": [{"palo": "Oro", "valor": 1}, {"palo": "Oro", "valor": 6}, {"palo": "Espada", "valor": 12}], "tiradas": [false, false, false], "ultimaTirada": -1, "jugador": {"id": "Alice", "equipo": "Azul"}}, {"seFueAlMazo": false, "cartas": [{"palo": "Copa", "valor": 4}, {"palo": "Basto", "valor": 10}, {"palo": "Basto", "valor": 2}], "tiradas": [false, false, false], "ultimaTirada": -1, "jugador": {"id": "Bob", "equipo": "Rojo"}}], "mixs": {"Alice": 0, "Bob": 1}, "muestra": {"palo": "Oro", "valor": 5}, "manos": [{"resultado": "ganoRojo", "ganador": "", "cartasTiradas": null}, {"resultado": "ganoRojo", "ganador": "", "cartasTiradas": null}, {"resultado": "ganoRojo", "ganador": "", "cartasTiradas": null}]}}')
print(p)
print(p.to_json())

while True:
  cmd = input("<< ")
  if not len(cmd.strip()): continue;
  try:
    pkts = p.cmd(cmd)
    print(p)
    for i, pkt in enumerate(pkts): print(f"pkt#{i}", pkt)
    print("")
  except Exception as e: print(e)
  if p.terminada(): break;
