import socket, pickle, time

HOST = socket.gethostname()
PORT = 8881
DEST = (HOST, PORT)
BUFFER_SIZE = 4096

def imprime_status(bytes, tam):
  kbytes = bytes/1024
  tam_bytes = tam/1024
  texto = 'Baixando... '
  texto = texto + '{:<.2f}'.format(kbytes) + ' KB '
  texto = texto + 'de ' + '{:<.2f}'.format(tam_bytes) + ' KB'
  print(texto)

tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp.settimeout(3)

try:
  tcp.connect(DEST)
  print("Cliente conectado no servidor!")

  while True:
    file_name = input("Escreva o nome com extensão do arquivo que quer verificar se existe ou 'exit' para sair: ")

    tcp.send(file_name.encode('ascii')) 

    if file_name == "exit":
      break

    received = tcp.recv(1024)
    file_size = int(pickle.loads(received))
    print(str(file_size) + ' bytes')

    if file_size > 0:
      soma = 0
      bytes = tcp.recv(BUFFER_SIZE)

      arq = open(f'received-{file_name}', "wb")
      print(f"Arquivo baixando como 'received-{file_name}'")

      try:
        while bytes:
          arq.write(bytes)
          soma = soma + len(bytes)
          imprime_status(soma, file_size)
          bytes = tcp.recv(BUFFER_SIZE)
      except:
        pass
      arq.close()
      print(f"Download finalizado")

except Exception as erro:
  print(str(erro))

tcp.close()
