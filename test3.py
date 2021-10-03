max = 20
iMax = max
jMax = max

class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    def print(self):
        print(f"x: {self.x}, y: {self.y}")

def adjacentCells(i,j):
    adjacentCellList = []
    for row in [i-1, i, i+1]: # Checking the previous row, the current row and the next row
        if row >= 0 and row < iMax: # Checking so that the row index is not out of range
            for column in [j-1, j, j+1]: # Checking the previous column, the current column and the next column
                if column >= 0 and column < jMax: # Checking so that the column index is not out of range
                    if not (row == i and column == j): # Not adding the input coordinates to the list
                        testCell = Cell(row,column)
                        testCell.print()
                        adjacentCellList.append(Cell(row,column))
    return adjacentCellList

adjacentCellList = adjacentCells(2,2)

for pos in adjacentCellList:
    pass
    #pos.print()
