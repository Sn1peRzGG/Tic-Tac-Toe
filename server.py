#!python3

import socket
import threading

# Параметри з'єднання
HOST = socket.gethostbyname(socket.gethostname())
PORT = 8888

# Ініціалізація сокету
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen(2)

clients = []
names = []
current_turn = 0

def handle_client(client_socket, player_id):
	global current_turn
	while True:
		try:
			data = client_socket.recv(1024).decode('utf-8')
			if not data:
				break
			if data.startswith('name:'):
				name = data.split(':')[1]
				names.append(name)
				print(f"Гравець {player_id + 1} підключився під іменем: {name}")
				if len(names) == 2:
					for client in clients:
						client.sendall(f'names:{names[0]}:{names[1]}'.encode('utf-8'))
			else:
				if player_id == current_turn:
					for client in clients:
						client.sendall(data.encode('utf-8'))
					current_turn = 1 - current_turn
		except:
			clients.remove(client_socket)
			client_socket.close()
			break

print("Сервер очікує підключення...")
while len(clients) < 2:
	client_socket, addr = server.accept()
	clients.append(client_socket)
	# server.setblocking(False)
	threading.Thread(target=handle_client, args=(client_socket, len(clients) - 1)).start()
	print(f"Гравець {len(clients)} підключився з адресою {addr[0]}:{addr[1]}")

server.close()
