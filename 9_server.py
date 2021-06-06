import socket, pickle
import shutil

HOST = socket.gethostname()
PORT = 9991
ORIG = (HOST, PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp.bind(ORIG)

def memory_spec():
  disk_usage = shutil.disk_usage("/")
  total = disk_usage.total// (2**30)
  free = disk_usage.free// (2**30)
  return(f"Memoria total: {total}Gb | Memoria disponivel: {free}Gb")

def encoded_resp(resp, client):
  byte_resp = pickle.dumps(resp)
  udp.sendto(byte_resp, client)

print('Servidor pronto!')

while True:
  (encoded_msg, cliente) = udp.recvfrom(1024)
  msg = encoded_msg.decode('ascii')
  print("Pedido", msg)
  if msg == "exit":
    break
  if msg == "memory_spec":
    encoded_resp(memory_spec(), cliente)
  else:
    encoded_resp("Erro: requisicao invalida", cliente)

udp.close()
