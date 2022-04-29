from helpers import *
from time import perf_counter
from tkinter import *
from tkinter import messagebox

# According to the scaling factor, the application window will never occupy more than the corresponding percentage of either the screen width or screen height
# Fonts and icon sizes are also scaled accordingly
scalingFactor = 0.7 
maxDefault = 25 # Default number of rows and columns
pMinesDefault = 0.15


# Creates the main window in which the game is played. This involves starting the game through the startGame function and adding the menu
def main():
    global root
    root = Tk()
    root.title("Minesweeper")
    root.iconbitmap("images/mine.ico")
    startGame(root, maxDefault, maxDefault, pMinesDefault) # Default values are passed in for first game after application is started
    menuBar(root)
    root.mainloop()


# Function for starting a new game. Called automatically when program is started and manually through the menu
def startGame(container, iMaxInput, jMaxInput, pMinesInput):
    global clickedCells, firstClick, gameOver, fontSize, flagIcon, mineIcon, questionMarkIcon, crossMarkIcon, crossedFlagIcon, pixel
    
    if "startGameDialog" in globals(): # Closes startGameDialog window created by startGameDialogCreator(), which is the case if a new game is started through the menu
        startGameDialog.destroy()

    inputHandler(iMaxInput, jMaxInput, pMinesInput) # Sets global variables iMax, jMax and pMines based on input
    
    clickedCells = 0 # Counter for the number of clicked cells used to determine a win
    firstClick = True # Variable used in leftClick function to ensure that the first cell clicked in a game does not contain a mine
    gameOver = False

    screenWidth = container.winfo_screenwidth() #3840
    screenHeight = container.winfo_screenheight() #2560
    unitLength = min(int(scalingFactor*screenWidth/jMax),int(scalingFactor*screenHeight/iMax))

    windowHeight = iMax*unitLength
    windowWidth = jMax*unitLength
    container.geometry(f"{windowWidth}x{windowHeight}")

    iconSize = int(0.6*unitLength)
    fontSize = int(0.4*unitLength)
    
    # Creating the icons used in the game. Process has to be repated for each game as the icon size depends on the user input for number of rows and columns. 
    flagIcon = importImage('images/flag.png', iconSize) #Icons downloaded freely from https://icons8.com/
    mineIcon = importImage('images/mine.png', iconSize)
    questionMarkIcon = importImage('images/questionmark.png', iconSize)
    crossMarkIcon = importImage('images/crossmark.png', iconSize)
    crossedFlagIcon = importCombineImages('images/flag.png', 'images/crossmark.png', iconSize) 

    # This code serves to make the frame produced by createGameFrame via startGame span the entire application window
    for row in range(1): 
        container.rowconfigure(row, weight = 1, uniform="varRow")
    for col in range(1):
        container.columnconfigure(col, weight = 1, uniform = "varCol")
    
    frame = createGameFrame(container)
    frame.grid(row=0, column=0, rowspan=1, columnspan=1, sticky="nsew")


# Creates a tkinter frame instace representing the gameboard, excluding cell values which are subsequently set in XXX
# to make sure that the cell the is clicked first is empty (contains no mine or adjacent mine)
def createGameFrame(container):
    global board    
    

    frame = Frame(container, padx=5, pady=5)

    for i in range(iMax): # Configuration of rows to dynamically resize according to weights
        frame.rowconfigure(index = i, weight = 1, uniform = "uniR")

    for j in range(jMax): # Configuration of columns to dynamically resize according to weights
        frame.columnconfigure(index = j, weight = 1, uniform = "uniC")
    
    board = []
    for i in range(iMax):
        boardRow = [] 
        for j in range(jMax):
            cell = Button(frame, bg="gray", font=f"Helvetica {fontSize} bold")
            cell.bind("<Button-1>", leftClick)
            cell.bind("<Button-3>", rightClick)
            cell.stateSymbol = "hidden"
            cell.value = 0 # Dummy value. Actual values are set by valueBoardAssigner via leftClick for the first click of each game (i.e. when firstClick == True)
            cell.row = i
            cell.col = j
            cell.grid(row=i, column = j, sticky="nsew")
            boardRow.append(cell)
        board.append(boardRow)
    return frame


# Sets global variables to default, or assigns them the passed-in values if values have been passed-in and if these values meet the specifed conditions.
def inputHandler(iMaxInput, jMaxInput, pMinesInput):
    global iMax, jMax, pMines
    
    iMax = maxDefault
    jMax = maxDefault
    pMines = pMinesDefault

    # Note: Maxiumum values are checked for when typing in the entry box, using the function trueForEmptyOrDigitMax(input, inputMax)
    if iMaxInput:
        if int(iMaxInput) >= 10:
            iMax = int(iMaxInput)

    if jMaxInput:
        if int(jMaxInput) >= 10:
            jMax = int(jMaxInput)

    if pMinesInput:
        if int(pMinesInput) >= 10:
            pMines = int(pMinesInput)/100    


# Function is called when user left clicks the gameboard
def leftClick(event):
    global firstClick, startTime
    row = event.widget.row
    col = event.widget.col

    if firstClick == True:
        valueBoardAssigner(row, col)
        firstClick = False
        startTime = perf_counter()
    
    if not gameOver: # If user has not won or lost
        reveal(row, col)


# Simulates a left click, whether function is called on by the leftClick function and recursively called on by itself
def reveal(i,j):
    global gameOver, clickedCells
    value = board[i][j].value
    if board[i][j].stateSymbol == "hidden":
        if value == 9: # Clicked cell contains mine
            gameOver = True
            wonOrLostDialogCreator("loser")            
            # Once a mine is clicked, all cells containing mines are revealed
            board[i][j].configure(bg="red", image = mineIcon) # Clicked cell is colored red
            board[i][j].stateSymbol = "mine"
            for row in range(iMax):
                for col in range(jMax):
                    if board[row][col].value == 9 and board[row][col].stateSymbol != "flag": # Undiscovered mine
                        #sleep(0.1)
                        board[row][col].stateSymbol = "mine"
                        board[row][col].configure(image = mineIcon)
                    if board[row][col].stateSymbol == "flag" and board[row][col].value != 9: # Wrongly flagged cells
                        board[row][col].stateSymbol = "crossedFlag"
                        board[row][col].configure(image = crossedFlagIcon)
        elif value == 0: # Neither clicked cell nor any of its adjacents cell contains any mines
            clickedCells += 1
            board[i][j].stateSymbol = "empty"
            board[i][j].configure(bg="white", image="")
            adjacentCellList = adjacentCells(i, j, iMax, jMax)
            for pos in adjacentCellList:
                if board[pos.row][pos.col].stateSymbol == "hidden":
                    reveal(pos.row, pos.col)
                if clickedCells == numberOfEmptyCell:
                    gameOver == True
                    wonOrLostDialogCreator("winner")
        else: # Clicked cell contains no mine, but adjacents cells do
            clickedCells += 1
            board[i][j].stateSymbol = str(value)
            board[i][j].configure(bg="white", fg=colorFunc(value), image="", text=value)
            if clickedCells == numberOfEmptyCell:
                gameOver == True
                wonOrLostDialogCreator("winner")


# Ensures that the very first cell that is clicked when a new game is started, valueBoard[i][j], does not contain a mine
def valueBoardAssigner(i, j): 
    global board, numberOfEmptyCell
    while True:
        valueBoard, numberOfMines = valueBoardCreator(iMax, jMax, pMines)
        numberOfEmptyCell = iMax*jMax-numberOfMines
        if valueBoard[i][j] == 0: # Clicked cell does not contain a mine
            break
    for row in range(iMax):
        for col in range(jMax):
            board[row][col].value = valueBoard[row][col]


# Function is called when user right clicks the gameboard
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


# Creates a dialog box shown when user wins or loses. The dialog box always has the same two buttons,
# but different text and color depending on the whether the input variable result == "winner"
def wonOrLostDialogCreator(result):
    global wonOrLostDialog
    wonOrLostDialog = Toplevel(root)
    wonOrLostDialog.iconbitmap("images/mine.ico")    
    
    if result.lower() == "winner":
        wonOrLostDialog.title("Congratulations!")
        elapsedTime = round(perf_counter()-startTime, 1)
        headingText = "Congratulations, you won!"
        infoText = f"Your time was {elapsedTime} seconds. Do you want to start a new game?"
        color = "#BCFF03"
    else:
        wonOrLostDialog.title("You lost")
        headingText = "You lost :("
        infoText = "Better luck next time. Do you want to start a new game?"
        color = "#b03030"

    wonOrLostDialog.configure(bg=color)    
    windowWidth = 300
    windowHeight = 150
    wonOrLostDialog.geometry(f"{windowWidth}x{windowHeight}")
    wonOrLostDialog.resizable(False, False)
    padding = 5

    for row in range(4):
        wonOrLostDialog.rowconfigure(row, weight = 3, uniform="varRow")
    wonOrLostDialog.rowconfigure(2, weight = 1, uniform="varRow")
    for col in range(12):
        wonOrLostDialog.columnconfigure(col, weight = 1, uniform = "varCol")

    headingsLabel = Label(wonOrLostDialog, bg=color, justify=CENTER, font="Helvetica 14 bold", padx=padding, pady=padding, wraplength=int(windowWidth - 2*padding), text = headingText)
    informationLabel = Label(wonOrLostDialog, bg=color, justify=LEFT, font="Arial 12", padx=padding, pady=padding, wraplength=int(windowWidth - 2*padding), text = infoText)
    yesButton = Button(wonOrLostDialog, justify=LEFT, font="Arial 11", padx=padding, text="Yes", command=startGameDialogCreator)
    noButton = Button(wonOrLostDialog, justify=LEFT, font="Arial 11", padx=padding, text="No", command=root.destroy)
    
    headingsLabel.grid(row=0, column=0, columnspan=12, sticky="w")
    informationLabel.grid(row = 1, column = 0, columnspan=12, sticky="w")
    yesButton.grid(row=3, column=3, columnspan=2, sticky="ew")
    noButton.grid(row=3, column=7, columnspan=2, sticky="ew")


# Used to create the menubar for the game main window
def menuBar(container):
    menuBar = Menu(container)
    
    fileMenu = Menu(menuBar)
    menuBar.add_cascade(label = "File", menu = fileMenu)
    fileMenu.add_command(label = "Start new game", command = startGameDialogCreator)
    fileMenu.add_separator()
    fileMenu.add_command(label = "Exit", command = container.quit)

    optionsMenu = Menu(menuBar)
    menuBar.add_cascade(label = "Options", menu = optionsMenu)
    optionsMenu.add_command(label = "About", command = aboutDialog)
    optionsMenu.add_command(label = "Cheat", command = cheatDialog)
    
    container.config(menu=menuBar)


# Dialog box for starting a new game via the menu
def startGameDialogCreator(): 
    # When a game is won or lost and the function wonOrLostDialogCreator is run, these two rows make sure to close the previous dialog window wonOrLostDialog
    if "wonOrLostDialog" in globals(): 
        wonOrLostDialog.destroy()
    
    global startGameDialog
    startGameDialog = Toplevel(root)
    startGameDialog.iconbitmap("images/mine.ico")
    startGameDialog.title("Start new game")
    windowWidth = 330
    windowHeight = 220
    startGameDialog.geometry(f"{windowWidth}x{windowHeight}")
    startGameDialog.resizable(False, False)
    padding = 5

    for row in range(5):
        startGameDialog.rowconfigure(row, weight = 1, uniform="varRow")
    for col in range(12):
        startGameDialog.columnconfigure(col, weight = 1, uniform = "varCol")

    verifyDigitInput30 = startGameDialog.register(trueForEmptyOrDigitMax30) # Used to verrify that that pMinesEntry input is of type integer and <= 30
    verifyDigitInput50 = startGameDialog.register(trueForEmptyOrDigitMax50) # Used to verrify that that iMaxEntry and jMaxEntry input is of type integer and <= 50

    headingsLabel = Label(startGameDialog, justify=LEFT, font="Arial 12 bold", padx = padding, pady = padding, wraplength = int(windowWidth - 2*padding),
        text = "Configurations for starting a new game (default values are prefilled):")
    iMaxLabel = Label(startGameDialog, justify=LEFT, font="Arial 11", padx = padding, pady = padding,
        text="Number of rows.\nEnter a number between 10 and 50:")
    jMaxLabel = Label(startGameDialog, justify=LEFT, font="Arial 11", padx = padding, pady = padding,
        text="Number of columns.\nEnter a number between 10 and 50:")
    pMinesLabel = Label(startGameDialog, justify=LEFT, font="Arial 11", padx = padding, pady = padding, 
        text="Probability of each cell containing a mine.\nEnter a number between 10 and 30:")

    iMaxEntry = Entry(startGameDialog, borderwidth = 5, font="Arial 11", justify=CENTER, validate = "key", width = 4, validatecommand = (verifyDigitInput50, '%P'))
    jMaxEntry = Entry(startGameDialog, borderwidth = 5, font="Arial 11", justify=CENTER, validate = "key", width = 4, validatecommand = (verifyDigitInput50, '%P'))
    pMinesEntry = Entry(startGameDialog, borderwidth = 5, font="Arial 11", justify=CENTER, validate = "key", width = 4, validatecommand = (verifyDigitInput30, '%P'))
    
    startButton = Button(startGameDialog, borderwidth = 5, bg="#BCFF03", font="Helvetica 14 bold", text="Start new game!",
        padx = 5, pady = 5, command=lambda: startGame(root, iMaxEntry.get(), jMaxEntry.get(), pMinesEntry.get()))

    headingsLabel.grid(row = 0, column = 0, columnspan = 12, sticky="w")
    iMaxLabel.grid(row = 1, column = 0, columnspan = 10, sticky="w")
    jMaxLabel.grid(row = 2, column = 0, columnspan = 10, sticky="w")
    pMinesLabel.grid(row = 3, column = 0, columnspan = 10, sticky="w")

    iMaxEntry.grid(row = 1, column = 10, columnspan = 2, sticky="e")
    jMaxEntry.grid(row = 2, column = 10, columnspan = 2, sticky="e")
    pMinesEntry.grid(row = 3, column = 10, columnspan = 2, sticky="e")
 
    iMaxEntry.insert(0, maxDefault)
    jMaxEntry.insert(0, maxDefault)
    pMinesEntry.insert(0, int(pMinesDefault*100))

    startButton.grid(row = 4, column = 0, columnspan = 12, rowspan = 1, sticky="nsew")

# Accessed via the menu. Creates a popup window with the provided text
def aboutDialog():
    messagebox.showinfo("About this game – Minesweeper", "A rendition of a classic, this game was created as part of the final project of the course \"CS50x\" offered by Harvard University through edX. \n\n© Arvid Hedbäck, October 2021")

# Accessed via the menu. Creates a dialog window from which the cheat function can be called
def cheatDialog():
    response = messagebox.askquestion("Cheat – Reveal question marks", "Depending on the difficulty chosen by the user (i.e. the prevalence of mines), \
there exists the possibility that a gameboard cannot be solved without guessing. The reason for this is that this program does not involve any presolving algorithm, \
meaning that mines are simply randomly located according to the specified (or default) probability of each cell containing a mine. \
As a workaround of this problem, this function enables user to \"cheat\" by revealing all cells marked with a question mark \
(To mark a cell with a question mark, right click it twice). In the case that any question marked cell contains a mine, the question mark is replaced by a flag.\
\n\nDo you wish to proceed?")
    if response == "yes":
        cheat()


# Reveals cells marked with questionmark
def cheat(): 
    global firstClick
    # Not possible to cheat on the first click of a new game, as the values of the gameboard have not yet been assigned via the function valueBoardCreator
    if firstClick == False: 
        for i in range(iMax):
            for j in range(jMax):
                if board[i][j].stateSymbol == "questionMark": # For each cell marked with a question mark
                    if board[i][j].value == 9: # If a mine is located under question mark, the question mark is replaced by a flag
                        board[i][j].stateSymbol = "flag"
                        board[i][j].configure(image = flagIcon)
                    else: # If no mine is located under question mark, the state of the cell is reveal through the reveal function
                        board[i][j].stateSymbol = "hidden" # For the reveal function to work properly, the stateSymbol needs to be reverted back to "hidden"
                        board[i][j].configure(image = "") # For the same reason, the question mark image also needs to be removed
                        reveal(i, j)


if __name__ == "__main__":
    main()
