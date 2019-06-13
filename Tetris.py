
# constructor for the game
def __init__(data):

    """
    __init__ function is used to allocate the board by setting color, time, along with other attributes
    tetrisPieces are a collection of standard tetris pieces, code can be found in above link
    """

    # initializing board
    data.emptyColor = "cadetblue"
    data.backGround = "antiquewhite"
    data.rows = 15
    data.cols = 10
    data.margin = 25
    data.cellSize = 20
    # filling the with color specified in emptyColor
    data.board = [([data.emptyColor]*10) for row in range(15)]
    data.timerDelay = 300
    data.isGameOver = False
    data.isPaused = False
    data.score = 0

    # pieces specs 

    #color
    data.tetrisPieceColors = [ "red", "yellow", "magenta", "cyan", "mediumaquamarine", "green", "orange" ]

    #shape
    """
    Shape is taken directly from below:
    https://www.cs.cmu.edu/~112/notes/notes-tetris/2_3_CreatingTheFallingPiece.html
    """

    iPiece = [
        [  True,  True,  True,  True ]
    ]

    jPiece = [
        [  True, False, False ],
        [  True,  True,  True ]
    ]

    lPiece = [
        [ False, False,  True ],
        [  True,  True,  True ]
    ]

    oPiece = [
        [  True,  True ],
        [  True,  True ]
    ]

    sPiece = [
        [ False,  True,  True ],
        [  True,  True, False ]
    ]

    tPiece = [
        [ False,  True, False ],
        [  True,  True,  True ]
    ]

    zPiece = [
        [  True,  True, False ],
        [ False,  True,  True ]
    ]

    # putting all the pieces into the list tetrisPieces
    data.tetrisPieces = [ iPiece, jPiece, lPiece, oPiece,

    sPiece, tPiece, zPiece ]



    newFallingPiece(data)



def playTetris(rows=15,cols=10):
    """
    playTetris() is used to set up the dimensions of the game
    The dimensions are defaulted to be 15 rows * 10 columns
    """

    cellSize = 20
    margin = 25
    width = margin * 2 + cellSize * cols
    height = margin * 2 + cellSize * rows
    return (width, height)



def drawBoard(canvas, data):
    """drawing the board by calling drawCell iteratively on every cell"""
    for i in range(len(data.board)):
        for j in range(len(data.board[0])):
            color=data.board[i][j]
            drawCell(canvas, data, i, j, color)


def drawCell(canvas, data, rows, cols, color):
    """draw every cell individually for the board and for every falling piece"""
    left = data.margin + data.cellSize * cols
    top = data.margin + data.cellSize * rows
    right = left + data.cellSize
    bottom = top + data.cellSize
    canvas.create_rectangle(left, top, right, bottom, fill = color,
    outline = "bisque", width = 1 )

def newFallingPiece(data):
    """creating a falling piece"""
    # randomly choose an index from the tetrisPieces list
    # to randomize piece type and color
    randomIndex = random.randint(0, len(data.tetrisPieces) - 1)
    data.fallingPiece = data.tetrisPieces[randomIndex]
    data.fallingPieceColor = data.tetrisPieceColors[randomIndex]
    #number of rows in falling piece
    fallingPieceRows = len(data.fallingPiece)
    #number of cols in falling piece
    fallingPieceCols = len(data.fallingPiece[0])
    #the index of the upmost row of the new falling piece
    data.fallingPieceRow = 0
    #the index of the left most column of the new falling piece
    data.fallingPieceCol = data.cols//2 - fallingPieceCols//2


def drawFallingPiece(canvas,data):
    """drawing the falling piece on the board"""
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j] == True:
            #draw the cells for a piece that is True in that position
                drawCell(canvas,data,data.fallingPieceRow+i,
                data.fallingPieceCol + j,data.fallingPieceColor)

def moveFallingPiece(data, row, col):
    """move the falling piece on the board"""
    data.fallingPieceRow += row
    data.fallingPieceCol += col
    if not fallingPieceIsLegal(data):
    #if the move is not avaliable - don't make the move
        data.fallingPieceRow -= row
        data.fallingPieceCol -= col
        return False



def fallingPieceIsLegal(data):
    """ Check if the piece is legal by checking if:
    1. the piece is going out of the board
    2. the piece is going to crash into the pile of pieces placed
    """
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j] == True:
                actualRow = data.fallingPieceRow + i
                actualCol = data.fallingPieceCol + j
                if not (actualRow in range(len(data.board))
                and actualCol  in range(len(data.board[0]))
                and data.board[actualRow][actualCol] == data.emptyColor):
            #if the piece go out of the board/crash into other pieces
                    return False
    return True

def rotateFallingPiece(data):
    """Rotate the falling piece by modifying its row/col attributes"""
    #getting information for old piece
    oldPiece = data.fallingPiece
    oldRowPosition, oldColPosition = data.fallingPieceRow, data.fallingPieceCol
    oldNumRows, oldNumCols = len(data.fallingPiece), len(data.fallingPiece[0])

    # calculating grid for new piece
    newNumRows, newNumCols = oldNumCols, oldNumRows
    newRow = oldRowPosition + oldNumRows//2 - newNumRows//2
    newCol = oldColPosition + oldNumCols//2 - newNumCols//2

    #rotate the grid of the piece by "rotating" the list of that piece

    rotatePiece = [["None"]*len(data.fallingPiece) \
    for col in range(len(data.fallingPiece[0]))]
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            rotatePiece[oldNumCols-1-j][i] = data.fallingPiece[i][j]
    data.fallingPieceRow = newRow
    data.fallingPieceCol = newCol
    data.fallingPiece = rotatePiece


    # if the piece is not valid, change the piece back to its original form
    if not fallingPieceIsLegal(data):
        data.fallingPiece = oldPiece
        data.fallingPieceRow=oldRowPosition
        data.fallingPieceCol=oldColPosition

def placeFallingPiece(data):
    """when a piece falls to the bottom, it become part of the board"""
    for i in range(len(data.fallingPiece)):
        for j in range(len(data.fallingPiece[0])):
            if data.fallingPiece[i][j] == True:
                data.board[data.fallingPieceRow + i][data.fallingPieceCol + j] = data.fallingPieceColor
# calling removeFullRows to remove a row that is already full
    removeFullRows(data)

def removeFullRows(data):
    """removing a full row; if success, increment total score"""
    board = data.board
    score = 0
    filledRowIndex = []
    newBoard = []
    emptyRow = [data.emptyColor] * data.cols

    # find index for full rows
    for i in range(data.rows):
        if not data.emptyColor in board[i]:
            filledRowIndex.append(i)
            score += 1

    # remove full rows, store the rest of the rows in a new board
    for i in range(data.rows):
        if not i in filledRowIndex:
            newBoard.append(board[i])

    # add empty row to the new board
    for k in range (len(filledRowIndex)):
        newBoard.insert(0,emptyRow)
    # replace the old board with the new board we just get
    data.board = newBoard

    # keep scoring
    data.score += score**2

def drawGameOver(canvas,data):
    """display a message when the game is over"""
    #background
    canvas.create_rectangle(0, 50, playTetris()[0], 300, fill = "black", width = 0)
    canvas.create_text( width/2, height/2 - height/7, text="Game",
    fill = "white", font="Impact 45 ")
    canvas.create_text(width/2 ,height/2 + height/25, text="Over",
    fill = "white", font="Impact 45 ")
    canvas.create_text(width/2, height/2+height/4, text="Press R to Restart",
    fill = "white", font="Arial 12 bold")
    #playsound('/Users/zijianliu/Downloads/Roblox-death-sound/Roblox-death-sound.mp3')

def drawPause(canvas,data):
    """display a message when the game is paused"""
    canvas.create_rectangle(0, 50, playTetris()[0], 300, fill = "black", width = 0)
    canvas.create_text(width/2, height/2 - height/5, text="The game has been",
    fill = "white", font="Impact 20 ")
    canvas.create_text(width/2, height/2, text="PAUSED",
    fill = "white", font="Impact 40 ")
    canvas.create_text(width/2, height/2 + height/5, text="Press P to continue",
    fill = "white", font="Arial 10 bold")

def mousePressed(event,data):
    """Not using mouse, so just pass"""
    pass

def keyPressed(event, data):
    """For each key pressed, manipulate the game in various ways"""
    # reset the whole game
    if (event.keysym == "r"):
        __init__(data)
    # switch between pause & unpause
    if (event.keysym == "p"):
        data.isPaused = not data.isPaused
    # when game is not paused
    if not data.isPaused:
        # when game is not over
        if data.isGameOver != True:
            # press key to control the direction/rotation of the falling piece
            if (event.keysym == "Down"):
                moveFallingPiece(data,+1,0)
            elif (event.keysym == "Left"):
                moveFallingPiece(data,0,-1)
            elif (event.keysym == "Right"):
                moveFallingPiece(data,0,+1)
            elif (event.keysym == "Up"):
                rotateFallingPiece(data)

def timerFired(data):
    """the functions natually take place when certain limitation is reached"""
    # when game is not paused
    if not data.isPaused :
        if  moveFallingPiece(data,1,0) == False:
        # when the falling piece stopped
            placeFallingPiece(data)
            # if game is not over
            if data.isGameOver != True:
                newFallingPiece(data)
            if fallingPieceIsLegal(data) == False:
            # if the new piece is immediately illegal when it "enters" the board
            # then the game is over
                data.isGameOver = True

def redrawAll(canvas, data):
    """drawing everything(board, pieces, text)"""
    canvas.create_rectangle( 0, 0, width, height, fill = data.backGround )
    drawBoard(canvas,data)
    drawFallingPiece(canvas, data)
    canvas.create_text( width/2, height/23, text="score: %d" %data.score,
                       fill = "lightsalmon", font = "Arial 12 bold")
    canvas.create_text( width/2, height - height/27,
    text="P to Pause    R to Restart", fill = "lightsalmon", font = "Arial 12 bold")
    if data.isPaused == True:
        drawPause(canvas,data)
    if data.isGameOver == True:
        drawGameOver(canvas,data)

def run(width=900, height=900):
    """run function adapted from the starter code(link listed at the start)"""

    def redrawAllWrapper(canvas, data):
        """wrapper function for redrawAll"""
        canvas.delete(ALL)
        canvas.create_rectangle(0, 0, data.width, data.height,
                                fill='white', width=0)
        redrawAll(canvas, data)
        canvas.update()

    def mousePressedWrapper(event, canvas, data):
        """
        wrapper function for mousePressed
        I didn't implement any function that involves using mouse
        """
        mousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        """wrapper function for keyPressed"""
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        """wrapper function for timerFired"""
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # delay for a short time as specified in timerDelay, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call the constructor
    class Struct(object): pass
    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 100 # milliseconds
    root = Tk()
    __init__(data)
    # create the root and the canvas
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.configure(bd=0, highlightthickness=0)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            mousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # launch the game
    root.mainloop()
    print("bye!")