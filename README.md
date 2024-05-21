# Tic-Tac-Toe Game

This repository contains a simple implementation of the classic Tic-Tac-Toe game using Python. The game is designed to be played between two players over a network connection, where one player acts as the server and the other as the client.

## Features

- **Client-Server Architecture**: The game utilizes a client-server model for network communication.
- **Graphical User Interface**: Implemented using Tkinter, the game provides a simple GUI for players to interact with.
- **Turn-based Gameplay**: Players take turns placing their symbols (X or O) on the board.
- **Win Detection**: The game automatically detects when a player has won or if the game ends in a draw.

## How to Play

1. Clone the repository to your local machine.
2. Run the server script (`server.py`) on one computer.
3. Run the client script (`client.py`) on two computers connected to the same network
4. Enter server IP address in the console.
5. Enter your name when prompted in the client application.
6. Wait for the server to establish a connection with another player.
7. Play the game by clicking on the squares in the GUI to place your symbol.

## Requirements

- Python 3.x
- Tkinter (usually comes pre-installed with Python)

To install all required packages simply run `pip install -r requirements.txt`.

## Credits

This project was developed by Sn1peRzGG as a simple exercise in network programming and GUI development with Python.

P.S. If you don't know the IP address of the server, just run `python3 getmyip.py` on the PC where the server is running
