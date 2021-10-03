from tkinter import *
from random import random
from PIL import ImageTk, Image
import time

max = 20
percentSize = 0.5
pMines = 0.1
iMax = max
jMax = max


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

def adjacentCells(i,j):
    adjacentCellList = []
    for row in [i-1, i, i+1]: # Checking the previous row, the current row and the next row
        if row >= 0 and row < iMax: # Checking so that the row index is not out of range
            for column in [j-1, j, j+1]: # Checking the previous column, the current column and the next column
                if column >= 0 and column < jMax: # Checking so that the column index is not out of range
                    if not (row == i and column == j): # Not adding the input coordinates to the list
                        adjacentCellList.append(Cell(row,column))
    return adjacentCellList

def boardCreator():
    rowList=[]
    for i in range(0, iMax):
        columnList=[]
        for j in range(0, jMax):
            if random() < pMines:
                columnList.append(9) # Mines are assigned value 9
            else:
                columnList.append(0) # Cells with no mines are assinged value 0
        rowList.append(columnList)
    board = calculateAdjacentMines(rowList)
    return board

# Cells, i.e. list items in board[i][j], are assigned values corresponing to the number of adjacent mines
def calculateAdjacentMines(board):
    for i in range(0, iMax): # For each row, i, in board[i][j]
        for j in range(0, jMax):  # For each column, j, in board[i][j]
            
            if board [i][j] != 9: # Number 9 denotes a mine. If evaluated to true, thus, there's no need to count adjacent mines
                adjacentMines = 0 # The number of adjacent mines is reset to 0 for each iteration
                adjacentCellList = adjacentCells(i,j)
                for pos in adjacentCellList:
                    if board[pos.x][pos.y] == 9: # If adjacent cell is a mine
                        adjacentMines += 1
                board[i][j] = adjacentMines
    return board

def leftClick(event):
    value = event.widget.value
    if event.widget.stateSymbol == "hidden":
        if value == 9:
            event.widget.stateSymbol = "mine"
            event.widget.configure(bg="red")
            event.widget.configure(image = mineIcon)
        elif value == 0:
            event.widget.stateSymbol = "empty"
            event.widget.configure(bg="white")
        else:
            event.widget.stateSymbol = str(value)
            event.widget.configure(bg="white")
            event.widget.configure(text=value)


def rightClick(event):
    if event.widget.stateSymbol == "hidden":
        event.widget.stateSymbol = "flag"
        event.widget.configure(image = flagIcon)
    elif event.widget.stateSymbol == "flag":
        event.widget.stateSymbol = "questionMark"
        event.widget.configure(image = questionMarkIcon)
    elif event.widget.stateSymbol == "questionMark":
        event.widget.stateSymbol = "hidden"
        event.widget.configure(image = "")


root = Tk()
root.title("Minesweeper")

screenWidth = root.winfo_screenwidth()
screenHeight = root.winfo_screenheight()
defaultWindowSize = int(screenHeight*percentSize)
xPos = int((screenWidth-defaultWindowSize)*0.5)
yPos = int((screenHeight-defaultWindowSize)*0.3)
root.geometry(f"{defaultWindowSize}x{defaultWindowSize}+{xPos}+{yPos}")

iconSize = int(0.6*defaultWindowSize/((iMax+jMax)/2))

#pixel = PhotoImage(width=1, height=1)
with Image.open('images/flag.png') as img:
    flagIcon = ImageTk.PhotoImage(img.resize((iconSize, iconSize), Image.ANTIALIAS))

with Image.open('images/mine.png') as img:
    mineIcon = ImageTk.PhotoImage(img.resize((iconSize, iconSize), Image.ANTIALIAS))

with Image.open('images/questionmark.png') as img:
    questionMarkIcon = ImageTk.PhotoImage(img.resize((iconSize, iconSize), Image.ANTIALIAS))   

for i in range(0,iMax): # Configuration of rows to dynamically resize according to weights
    Grid.rowconfigure(root, index = i, weight = 1)

for j in range(0,jMax): # Configuration of columns to dynamically resize according to weights
    Grid.columnconfigure(root, index = j, weight = 1)

board = boardCreator()
gameboard = []
for i in range(0,iMax):
    gameboardRow = []
    
    for j in range(0,jMax):
        cell = Button(root, bg="gray", height = 80, width = 80)#, image = pixel
        cell.bind("<Button-1>", leftClick)
        cell.bind("<Button-3>", rightClick)
        cell.value = board[i][j]
        cell.stateSymbol = "hidden"
        cell.grid(row=i, column = j, sticky="nsew")

        gameboardRow.append(cell)
    gameboard.append(gameboardRow)

def resize(event):
    size = int(event.width / 10)
    #time.sleep(5)
    for widget in root.winfo_children():
        widget.config(font=("Helvetica", size))  
    #for i in range(0, iMax):
    #    for j in range(0, jMax):
    #        gameboard[i][j].config(font=("Helvetica", size))  

#root.bind("<Configure>", resize)

root.mainloop()