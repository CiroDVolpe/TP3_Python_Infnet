import socket, pickle
import os

PATH = os.getcwd()
HOST = socket.gethostname()
PORT = 8881
ORIG = (HOST, PORT)
BUFFER_SIZE = 4096

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.bind(ORIG)
tcp.listen()

def encoded_resp(resp, client):
  byte_resp = pickle.dumps(resp)
  client.send(byte_resp)

print('Servidor pronto!')

(cliente, addr) = tcp.accept()

while True:
  req = cliente.recv(1024).decode('ascii')

  print("Pedido", req)

  if req == "exit" :
    break
  elif not os.path.isfile(req):
    encoded_resp('-1', cliente)
  else:
    file_name = (PATH + '/' + req)
    file_size = os.path.getsize(file_name)
    encoded_resp(str(file_size), cliente)

    with open(file_name, "rb") as f:
      print(f"INICIO: {req}")
      while True:
        bytes_read = f.read(BUFFER_SIZE)
        if not bytes_read:
          break
        cliente.sendall(bytes_read)
      print(f"FINALIZADO: {req}")

tcp.close()
