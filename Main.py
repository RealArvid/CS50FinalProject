from tkinter import *
from random import random
from PIL import ImageTk, Image
from helpers import adjacentCells, Cell, colorFunc, valueBoardCreator, calculateAdjacentMines, importImage, importCombineImages
import time

# Ctrl + K, then Ctrl + C to comment or Ctrl + U to uncomment

max = 20
percentSize = 0.5
pMines = 0.2
iMax = max
jMax = max
gameOver = False


def startGame():
    global firstClick, gameOver
    gameOver = False
    firstClick = True # Variable used in leftClick function to ensure that the first cell clicked in a game does not contain a mine
    frame = createGameFrame(root)
    frame.grid(row=0, column = 0, columnspan=3, sticky="nsew")


# Creates a tkinter frame instace representing the gameboard, excluding cell values which are subsequently set in XXX
# to make sure that the cell the is clicked first is empty (contains no mine or adjacent mine)
def createGameFrame(container):
    frame = Frame(container, height=500, width=500, padx=5, pady=13) #LabelFrame

    for i in range(iMax): # Configuration of rows to dynamically resize according to weights
        frame.rowconfigure(index = i, weight = 1)

    for j in range(jMax): # Configuration of columns to dynamically resize according to weights
        frame.columnconfigure(index = j, weight = 1)
    
    global board
    board = []

    for i in range(iMax):
        boardRow = []
        
        for j in range(jMax):
            cell = Button(frame, bg="gray", font=f"Helvetica {fontSize} bold")#, height = 20, width = 20)
            cell.bind("<Button-1>", leftClick)
            cell.bind("<Button-3>", rightClick)
            cell.stateSymbol = "hidden"
            cell.value = 0 # Dummy value. Acutal values are set by valueBoardAssigner via leftClick for the first click of each game (i.e. when firstClick == True)
            cell.row = i
            cell.col = j
            cell.grid(row=i, column = j, sticky="nsew")

            boardRow.append(cell)
        board.append(boardRow)
    return frame


def leftClick(event):
    global firstClick
    row = event.widget.row
    col = event.widget.col

    if firstClick == True:
        valueBoardAssigner(row, col)
        firstClick = False
    
    if not gameOver:
        reveal(row, col)


# Ensures that the very first cell that is clicked when a new game is started, valueBoard[i][j], does not contain a mine
def valueBoardAssigner(i, j): 
    global board
    while True:
        valueBoard = valueBoardCreator(iMax, jMax, pMines)
        #print(valueBoard[i][j])
        if valueBoard[i][j] == 0:
            break
    for row in range(iMax):
        for col in range(jMax):
            board[row][col].value = valueBoard[row][col]


def reveal(i,j):
    value = board[i][j].value
    if board[i][j].stateSymbol == "hidden":
        if value == 9: # Clicked cell contains mine
            # Once a mine is clicked, all cells containing mines are revealed
            global gameOver
            gameOver = True
            board[i][j].configure(bg="red", image = mineIcon) # Clicked cell is colored red
            board[i][j].stateSymbol = "mine"
            for row in range(iMax):
                for col in range(jMax):
                    if board[row][col].value == 9 and board[row][col].stateSymbol != "flag": # Undiscovered mine
                        board[row][col].stateSymbol = "mine"
                        board[row][col].configure(image = mineIcon)
                    if board[row][col].stateSymbol == "flag" and board[row][col].value != 9: # Wrongly flagged cells
                        board[row][col].stateSymbol = "crossedFlag"
                        board[row][col].configure(image = crossedFlagIcon)
        elif value == 0: # Neither clicked cell or any of its adjacents cell contains any mines
            board[i][j].stateSymbol = "empty"
            board[i][j].configure(bg="white")
            adjacentCellList = adjacentCells(i, j, iMax, jMax)
            for pos in adjacentCellList:
                if board[pos.row][pos.col].stateSymbol == "hidden":
                    reveal(pos.row, pos.col)
        else: # Clicked cell contains no mine, but adjacents cells do
            board[i][j].stateSymbol = str(value)
            board[i][j].configure(bg="white", fg=colorFunc(value), text=value)


def rightClick(event):
    if not gameOver:
        if event.widget.stateSymbol == "hidden":
            event.widget.stateSymbol = "flag"
            event.widget.configure(image = flagIcon)
        elif event.widget.stateSymbol == "flag":
            event.widget.stateSymbol = "questionMark"
            event.widget.configure(image = questionMarkIcon)
        elif event.widget.stateSymbol == "questionMark":
            event.widget.stateSymbol = "hidden"
            event.widget.configure(image = "")

def cheat():
    global firstClick
    if firstClick == False:
        for i in range(iMax):
            for j in range(jMax):
                if board[i][j].stateSymbol == "questionMark":
                    if board[i][j].value == 9:
                        board[i][j].stateSymbol = "flag"
                        board[i][j].configure(image = flagIcon)
                    else:
                        board[i][j].stateSymbol = "hidden"
                        board[i][j].configure(image = "")
                        reveal(i, j)

root = Tk()
root.title("Minesweeper")
root.iconbitmap("images/mine.ico")

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
defaultWindowSize = 1200#int(screenHeight*percentSize)
xPos = int((screenWidth-defaultWindowSize)*0.5)
yPos = int((screenHeight-defaultWindowSize)*0.3)
root.geometry(f"{defaultWindowSize}x{defaultWindowSize}+{xPos}+{yPos}")
#root.resizable(False, False)

iconSize = int(0.3*defaultWindowSize/((iMax+jMax)/2)) #0.6
fontSize=int(0.2*defaultWindowSize/((iMax+jMax)/2)) #0.4

flagIcon = importImage('images/flag.png', iconSize)
mineIcon = importImage('images/mine.png', iconSize)
questionMarkIcon = importImage('images/questionmark.png', iconSize)
crossMarkIcon = importImage('images/crossmark.png', iconSize)
crossedFlagIcon = importCombineImages('images/flag.png', 'images/crossmark.png', iconSize) 


root.rowconfigure(0, weight = 90, uniform="var")
root.rowconfigure(1, weight = 5, uniform="var")
root.rowconfigure(2, weight = 5, uniform="var")

root.columnconfigure(0, weight = 1)
root.columnconfigure(1, weight = 1)
root.columnconfigure(2, weight = 1)


startButton = Button(root, bg="green", font=f"Helvetica {fontSize} bold", text="Start new game!", command=startGame)
cheatButton = Button(root, bg="yellow", font=f"Helvetica {fontSize} bold", text="Cheat – reveal question marks", command=cheat)
exitButton = Button(root, bg="red", font=f"Helvetica {fontSize} bold", text="Exit", command=root.quit)

startGame()
startButton.grid(row=1, column = 2, sticky="nsew")
cheatButton.grid(row=1, column = 0, sticky="nsew")
exitButton.grid(row=1, column = 3, sticky="nsew")
exitButton.grid(row=2, column = 0, sticky="nsew")
root

root.mainloop()