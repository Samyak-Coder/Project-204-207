import socket
from tkinter import  *
import tkinter as tk
from threading import Thread
import random
from PIL import ImageTk, Image
import platform

screenWidth = None
screenHeight = None

SERVER = None
PORT = None
IP_ADDRESS = None
playerName = None

nameEntry = None
nameWindow = None
gameWindow = None

canvas1 = None
canvas2 = None

ticketGrid  = []
currentNumberList = []
flashNumberList = []
flashNumberLabel = None

def createTicket():
    global gameWindow
    global ticketGrid

    mainLable = Label(gameWindow, 
                      width=65,
                      height=16, 
                      relief= 'ridge',
                      borderwidth=5,
                      bg="white" )
    mainLable.place(x=95, y=119)

    xPos = 105
    yPos = 130

    for row in range(0,3):
        rowList = []
        for col in range(0,9):
            if(platform.system() == "Darwin"):
                boxButton = Button(gameWindow,
                                   font=("Calboard SE", 18),
                                   borderwidth=3,
                                   pady=23,
                                   padx=22,
                                   bg="#fff176",
                                   highlightbackground="#fff176",
                                   activebackground="#c5ela5")
                boxButton.place(x=xPos, y=yPos)

            else:
                boxButton = tk.Button(gameWindow, 
                                      font=("Chalboard SE", 30),
                                      width=3,
                                      height=2,
                                      borderwidth=5,
                                      bg="#fff176")
            
            rowList.append(boxButton)
            xPos+=69

        ticketGrid.append(rowList)
        xPos = 105
        yPos += 82

def placeNumbers():
    global ticketGrid
    global currentNumberList

    for row in range(0,3):
        randomColList = []
        counter = 0

        while counter <= 4:
            randomCol = random.randit(0,8)
            if(randomCol not in randomColList):
                randomColList.append(randomCol)
                counter += 1

    numberContainer = {
        "0": [1, 2, 3, 4, 5, 6, 7, 8, 9],
        "1": [10, 11, 12, 13, 14, 15, 16, 17, 18, 19],
        "2": [20, 21, 22, 23, 24, 25, 26, 27, 28, 29], 
        "3": [30, 31, 32, 33, 34, 35, 36, 37, 38, 39],
        "4": [40, 41, 42, 43, 44, 45, 46, 47, 48, 49],
        "5": [50, 51, 52, 53, 54, 55, 56, 57, 58, 59],
        "6": [60, 61, 62, 63, 64, 65, 66, 67, 68, 69],
        "7": [70, 71, 72, 73, 74, 75, 76, 77, 78, 79],
        "8": [80, 81, 82, 83, 84, 85, 86 , 87, 88, 89, 90]
    }

    counter = 0
    while(counter < len(randomColList)):
        colNum = randomColList[counter]
        numberListByIndex = numberContainer[str(colNum)]
        randomNumber = random.choice(numberListByIndex)

        if(randomNumber not in currentNumberList):
            numberBox = ticketGrid[row][colNum]
            numberBox.configure(text=randomNumber, fg = "black")

            currentNumberList.append(randomNumber)
            counter += 1           

    for row in ticketGrid:
           for numberBox in row:
               if(not numberBox['text']):
                   numberBox.configure(state='disabled',
                                       disabledbackground='#ff8a65', 
                                       highlightbackground='#ff8a65')

def askPlayerName():
    global playerName
    global nameEntry
    global nameWindow
    global canvas1

    nameWindow = Tk()
    nameWindow.title("Tambola Family Fun")
    nameWindow.geometry("800x600")

    screenWidth = nameWindow.winfo_screenwidth()
    screenHeight = nameWindow.winfo_screenheight()

    bg = ImageTk(file = "./assets/background.png")

    canvas1 = Canvas(nameWindow, 
                     width=500,
                     height=500)
    canvas1.pack(fill="both", expand=True)

    canvas1.create_image(0,0, image=bg, anchor="nw")
    canvas1.create_text(screenWidth/4.5, 
                        screenHeight/8,
                        text="Enter Name",
                        font=("Chalkboard SE", 60),
                        fill="black")

    nameEntry = Entry(nameWindow, 
                      width=15, 
                      justify="center",
                      font=("Calkboard SE", 60),
                      bd=5,
                      bg="whtie")
    nameEntry.place(x=screenWidth/7, y= screenHeight/5.5)

    button = Button(nameWindow  , 
                    text = "Save",
                    font = ("Chalkboard SE", 30),
                    width=11, 
                    command=saveName,
                    height=2,
                    bd=3,
                    bg="#80deea")
    button.place(x=screenWidth/6, y=screenHeight/4)

    nameWindow.resizable(True, True)
    nameWindow.mainloop()

def saveName():
    global SERVER
    global playerName
    global nameWindow
    global nameEntry

    playerName = nameEntry.get()    
    nameEntry.delete(0, END)
    nameWindow.destroy()

    SERVER.send(playerName.encode())

def gameWindow():
    global gameWindow
    global canvas2
    global screenWidth
    global screenHeight
    global dice
    global winningMessage
    global resetButton
    global flashNumberLabel

    gameWindow = Tk()
    gameWindow.title("Tambola Family Fun")
    gameWindow.geometry("800x600")

    screenHeight = gameWindow.winfo_screenheight()
    screenWidth = gameWindow.winfo_screenwidth()

    bg = ImageTk.PhotoImage(file = "./assets/background.png")

    canvas2 = Canvas(gameWindow, width=500, height=500)
    canvas2.pack(fill = "both", expand= True)
    canvas2.create_image(0, 0, image=bg, anchor="nw")
    canvas2.create_text( screenWidth/4.5,50, text = "Tambola Family Fun", font=("Chalkboard SE",50), fill="#3e2723")

    createTicket()
    placeNumbers()

    flashNumberLabel = canvas2.create_text(400, 
                                           screenHeight/2.3,
                                           text="Waiting for others to join...",
                                           font=("Calkboard SE", 30),
                                           fill="#3e2723")
    
    gameWindow.resizable(True, True)
    gameWindow.mainloop()

def recivedMsg():
    global SERVER
    global displayNumberList
    global flashNumberLabel
    global canvas2
    global gameOver

    number = [str(i) for i in range(1,91)]

    while True:
        chunk = SERVER.recv(2048).decode()
        if(chunk in number and flashNumberLabel and not gameOver):
            flashNumberLabel.append(int(chunk))
            canvas2.itemconfigure(flashNumberLabel, text=chunk, font=("Chalkboard SE", 60))
        elif('wins the game.' in chunk):
            gameOver = True
            canvas2.itemconfigure(flashNumberLabel, text=chunk, font=("Calkboard SE", 40))
            

                
def setup():
    global SERVER
    global PORT
    global IP_ADDRESS

    PORT = 6000
    IP_ADDRESS = '127.0.0.1'

    SERVER = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    SERVER.connect(IP_ADDRESS, PORT)

    thread = Thread(target=recivedMsg)
    thread.start()
