import socket
import threading
from customtkinter import *
from CTkMessagebox import CTkMessagebox
from PIL import Image
import time


HOST = input('Enter server IP: ')
PORT = 8888

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

app = CTk()
app.geometry('540x725')
app.title('Tic-Tac-Toe Game')
app.resizable(False, False)

player_name = ""
player_symbol = 'X'
opponent_name = ""
opponent_symbol = 'O'
is_my_turn = False
board = ['' for _ in range(9)]
buttons = []

img = Image.open('./background.png')

logo = CTkImage(dark_image=img, light_image=img, size=(540, 100))
logo_label = CTkLabel(master=app, text='', image=logo)
logo_label.grid(row=0, column=0, columnspan=3)

info_label = CTkLabel(master=app, text='Waiting for second player to connect...')
info_label.grid(row=1, column=0, columnspan=3)

player_label = CTkLabel(master=app, text=f'Your nickname: {player_name} ({player_symbol})')
player_label.grid(row=2, column=0, columnspan=3)

turn_label = CTkLabel(master=app, text='')
turn_label.grid(row=3, column=0, columnspan=3)

dialog = CTkInputDialog(title='Player name', text='Enter your name:')
player_name = dialog.get_input().strip()
client.sendall(f'name:{player_name}'.encode('utf-8'))

button_size = 180

for i in range(9):
	button = CTkButton(master=app, text='', font=('normal', 120), width=button_size, height=button_size, command=lambda i=i: on_button_click(i))
	button.grid(row=(i // 3) + 4, column=i % 3)
	buttons.append(button)

def on_button_click(index):
	global player_symbol, is_my_turn
	if board[index] == '' and is_my_turn:
		board[index] = player_symbol
		buttons[index].configure(text=player_symbol)
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
		CTkMessagebox(title="Результат", message="Гра завершилась внічию!")
	else:
		winner_name = player_name if winner == player_symbol else opponent_name
		CTkMessagebox(title="Перемога", message=f"Гравець {winner_name} переміг!")
	time.sleep(2)
	app.destroy()

def update_turn_label():
	if is_my_turn:
		turn_label.configure(text=f"Ваш хід ({player_symbol})")
	else:
		turn_label.configure(text=f"Хід {opponent_name} ({opponent_symbol})")

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
				player_symbol = '×' if player_name == name1 else '⚬'
				opponent_symbol = 'O' if player_symbol == '×' else '×'
				is_my_turn = player_symbol == '×'
				info_label.configure(text=f"{name1} (×) vs {name2} (⚬)")
				player_label.configure(text=f"Ваш нік: {player_name} ({player_symbol})")
				update_turn_label()
			elif data == 'game_over':
				app.destroy()
			else:
				index, symbol = data.split(':')
				index = int(index)
				board[index] = symbol
				buttons[index].configure(text=symbol)
				is_my_turn = (symbol != player_symbol)
				update_turn_label()
				check_winner()
		except Exception as e:
			print(f"Error: {e}")
			break

threading.Thread(target=receive_data).start()

app.mainloop()
client.close()
