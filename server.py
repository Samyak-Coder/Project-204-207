import socket
from threading import Thread

SERVER = None

IP_ADDRESS = '127.0.0.1'
PORT = 6000

CLIENTS = {}
nicknames = []

def acceptConnections():
    global CLIENTS
    global SERVER
    
    while True:
        playerSocket , addr = SERVER.accept()
        playerName = playerSocket.recv(1024).decode().strip()
        print(playerName)
        if(len(CLIENTS.key()) == 0):
            CLIENTS[playerName] = {'playerName': 'player1'}
        else:
            CLIENTS[playerName] = {'playerName': 'player2'}

        CLIENTS[playerName]["playerSocket"] = playerSocket
        CLIENTS[playerName]["address"] = addr
        CLIENTS[playerName]["playerName"] = playerName
        CLIENTS[playerName]["turn"] = False

        print(f"Connection established with {playerName} : {addr}")

def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    SERVER.socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.bind(IP_ADDRESS, PORT)

    SERVER.listen(10)

    print("\t\t\t\t SERVER IS WAITING FOR INCOMMING CONNECTIONS...\n")

    acceptConnections()