from random import random
from PIL import ImageTk, Image


class Cell:
    def __init__(self, i, j):
        self.row = i
        self.col = j


def valueBoardCreator(iMax, jMax, pMines): # Returns a board of values in which 0-8 indicate the number of adjacent mines and 9 indicates mines
    rowList=[]
    for i in range(0, iMax):
        columnList=[]
        for j in range(0, jMax):
            if random() < pMines:
                columnList.append(9) # Mines are assigned value 9
            else:
                columnList.append(0) # Cells with no mines are assinged value 0
        rowList.append(columnList)
    valueBoard = calculateAdjacentMines(rowList, iMax, jMax)
    return valueBoard


# Cells, i.e. list items in board[i][j], are assigned values corresponing to the number of adjacent mines
def calculateAdjacentMines(board, iMax, jMax):
    for i in range(iMax): # For each row, i, in board[i][j]
        for j in range(jMax):  # For each column, j, in board[i][j]
            
            if board [i][j] != 9: # Number 9 denotes a mine. If evaluated to true, thus, there's no need to count adjacent mines
                adjacentMines = 0 # The number of adjacent mines is reset to 0 for each iteration
                adjacentCellList = adjacentCells(i, j, iMax, jMax)
                for pos in adjacentCellList:
                    if board[pos.row][pos.col] == 9: # If adjacent cell is a mine
                        adjacentMines += 1
                board[i][j] = adjacentMines
    return board


def adjacentCells(i, j, iMax, jMax): # Returns a list of adjacent cells within the limits of 0 to iMax and 0 to jMax, whithin which each element is an instance of the Cell class.
    adjacentCellList = []
    for row in [i-1, i, i+1]: # Checking the previous row, the current row and the next row
        if row >= 0 and row < iMax: # Checking so that the row index is not out of range
            for col in [j-1, j, j+1]: # Checking the previous column, the current column and the next column
                if col >= 0 and col < jMax: # Checking so that the column index is not out of range
                    if not (row == i and col == j): # Not adding the input coordinates to the list
                        adjacentCellList.append(Cell(row,col))
    return adjacentCellList


def colorFunc(value):
    if value == 1:
        return "blue"
    if value == 2:
        return "green"
    if value == 3:
        return "red"
    if value == 4:
        return "#0A0A82"
    if value == 5:
        return "#7B0000"
    if value == 6:
        return "#006E6E"
    if value == 7:
        return "black"
    if value == 8:
        return "gray"


def importImage(inputLocation, iconSize): # Creates and ImageTK class instance of an image at the specified file location
    with Image.open(inputLocation) as img:
        outputObject = ImageTk.PhotoImage(img.resize((iconSize, iconSize), Image.ANTIALIAS))
    return outputObject


# Creates and ImageTK class instance of an image by superimposing the image at the second file location on the image at the first file location
def importCombineImages(inputLocation1, inputLocation2, iconSize): 
    img1 = Image.open(inputLocation1).resize((iconSize, iconSize))
    img2 = Image.open(inputLocation2).resize((iconSize, iconSize))
    img = img1.paste(img2, (0, 0), img2)
    outputObject = ImageTk.PhotoImage(img1.resize((iconSize, iconSize), Image.ANTIALIAS))
    return outputObject