import argparse
import json
import socket

from pytruco.pdt.partida import Partida
from pytruco.pdt.chi import chis as get_chis

BUFFER_SIZE = 1024_00


def print_pytruco_version():
  print("pytruco version: 0.1.0")


def split_message(msg: str) -> tuple[str, str]:
  parts = msg.split(";", 1)
  if len(parts) != 2:
    return "", ""
  return parts[0], parts[1]


def envs_to_str(pkts) -> str:
  res = ""
  for pkt in pkts:
    d = {
      "destination": pkt.destination,
      "message": pkt.message.to_dict(),
    }
    res += json.dumps(d) + "|"
  return res


def chis_to_str(chis_list) -> str:
  res = ""
  for chi in chis_list:
    for a in chi:
      res += str(a) + ";"
  return res


def resolve_command(msg: str, p_ref: list, conn: socket.socket) -> bool:
  cmd, data = split_message(msg)
  if not cmd:
    return False

  if cmd == "PING":
    conn.sendall(b"PONG")
  elif cmd == "EXIT":
    conn.sendall(b"OK")
    return True
  elif cmd == "LOAD":
    p = Partida.parse(data)
    p.verbose = True
    p_ref[0] = p
    conn.sendall(b"OK")
  elif cmd == "ACTION":
    envs = p_ref[0].cmd(data)
    res = envs_to_str(envs)
    conn.sendall(res.encode())
  elif cmd == "REQ_CHIS":
    chis_list = get_chis(p_ref[0])
    res = chis_to_str(chis_list)
    conn.sendall(res.encode())
  else:
    raise RuntimeError(f"Unknown command: `{cmd}` (len={len(cmd)})")

  return False


def game_loop(conn: socket.socket):
  p_ref = [None]
  while True:
    data = conn.recv(BUFFER_SIZE)
    if not data:
      break
    msg = data.decode()
    if resolve_command(msg, p_ref, conn):
      break


def main():
  print_pytruco_version()

  parser = argparse.ArgumentParser()
  parser.add_argument("--validator_addr", default="localhost:8080")
  args = parser.parse_args()

  host, port = args.validator_addr.rsplit(":", 1)

  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conn:
    conn.connect((host, int(port)))
    game_loop(conn)


if __name__ == "__main__":
  main()
