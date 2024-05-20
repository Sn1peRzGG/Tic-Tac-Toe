#!python3

import socket
import tkinter as tk
from tkinter import simpledialog, messagebox
import threading

# Параметри з'єднання
HOST = input('Enter server IP: ')
PORT = 8888

# Ініціалізація клієнтського сокету
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

# Створення графічного інтерфейсу
root = tk.Tk()
root.title("Tic-Tac-Toe Game")
root.resizable(False, False)

player_name = simpledialog.askstring("Ім'я гравця", "Введіть своє ім'я:")
client.sendall(f'name:{player_name}'.encode('utf-8'))

player_symbol = 'X'
opponent_name = ""
opponent_symbol = 'O'
is_my_turn = False
board = ['' for _ in range(9)]
buttons = []

info_label = tk.Label(root, text="Очікування підключення другого гравця...")
info_label.grid(row=0, column=0, columnspan=3)

player_label = tk.Label(root, text=f"Ваш нік: {player_name} ({player_symbol})")
player_label.grid(row=1, column=0, columnspan=3)

turn_label = tk.Label(root, text="")
turn_label.grid(row=2, column=0, columnspan=3)

def on_button_click(index):
	global player_symbol, is_my_turn
	if board[index] == '' and is_my_turn:
		board[index] = player_symbol
		buttons[index].config(text=player_symbol)
		client.sendall(f"{index}:{player_symbol}".encode('utf-8'))
		is_my_turn = False
		update_turn_label()
		check_winner()

def check_winner():
	for i in range(0, 9, 3):
		if board[i] == board[i+1] == board[i+2] != '':
			show_winner(board[i])
			return
	for i in range(3):
		if board[i] == board[i+3] == board[i+6] != '':
			show_winner(board[i])
			return
	if board[0] == board[4] == board[8] != '' or board[2] == board[4] == board[6] != '':
		show_winner(board[4])
		return
	if '' not in board:
		show_winner('Нічия')

def show_winner(winner):
	if winner == 'Нічия':
		messagebox.showinfo("Результат", "Гра завершилась внічию!")
	else:
		winner_name = player_name if winner == player_symbol else opponent_name
		messagebox.showinfo("Перемога", f"Гравець {winner_name} переміг!")
	client.sendall('game_over'.encode('utf-8'))

def update_turn_label():
	if is_my_turn:
		turn_label.config(text=f"Ваш хід ({player_symbol})")
	else:
		turn_label.config(text=f"Хід {opponent_name} ({opponent_symbol})")

def receive_data():
	global opponent_name, is_my_turn, player_symbol, opponent_symbol
	while True:
		try:
			data = client.recv(1024).decode('utf-8')
			if not data:
				break
			if data.startswith('names:'):
				_, name1, name2 = data.split(':')
				opponent_name = name2 if player_name == name1 else name1
				player_symbol = 'X' if player_name == name1 else 'O'
				opponent_symbol = 'O' if player_symbol == 'X' else 'X'
				is_my_turn = player_symbol == 'X'
				info_label.config(text=f"{name1} (X) vs {name2} (O)")
				player_label.config(text=f"Ваш нік: {player_name} ({player_symbol})")
				update_turn_label()
			elif data == 'game_over':
				root.quit()
			else:
				index, symbol = data.split(':')
				index = int(index)
				board[index] = symbol
				buttons[index].config(text=symbol)
				is_my_turn = (symbol != player_symbol)
				update_turn_label()
				check_winner()
		except:
			break

# Створення кнопок для гри
for i in range(9):
	button = tk.Button(root, text='', font=('normal', 40), width=5, height=2, command=lambda i=i: on_button_click(i))
	button.grid(row=(i//3)+3, column=i%3)
	buttons.append(button)

# Запуск потоку для отримання даних від сервера
threading.Thread(target=receive_data).start()

root.mainloop()
client.close()
