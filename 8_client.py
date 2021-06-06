import socket, pickle

HOST = socket.gethostname()
PORT = 9991
DEST = (HOST, PORT)

udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

print("Bem vindo ao cliente UDP!")
print("Envie 'memory_spec' para ver detalhes do disco.")
print("Ou envie 'exit' para sair e desligar o servidor.")

while True:
  msg = input("Entre com a mensagem:\n")
  udp.sendto(msg.encode('ascii'), DEST)

  if msg == "exit":
    break

  received = udp.recv(1024)
  response = pickle.loads(received)
  print(response)

udp.close()
