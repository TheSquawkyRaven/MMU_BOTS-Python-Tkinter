
# Glossary
# points -> the points that a player can get during one round
# score -> the total points accumulated by a player
# scoreBoard -> the table showing all scores
# round -> BOTH players play a round
# match -> The entire game, quits when the match is done
# playerRound -> Individual player round (1 round has 2 playerRounds)
# pointsBoard -> Displays points based on current dice roll

import random
from tkinter import *
from tkinter.scrolledtext import *
from PIL import ImageTk, Image

#TKINTER

#Find ' &&& ' for specific edit value



### Constants ###
gameName = " Battle of the Sexes (B.O.T.S) "    #Spaces at both ends to match desired output
titleLineFiller = "="
titleWidth = 80
players = ["Player 1", "Player 2"]
playerUnderline = "========"
rounds = 9
## Categories
categoryBoard = "Category Scores"
categoryList = ["1S", "2S", "3S", "4S", "Trio", "Quartet", "Band", "Doremi", "Orchestra"]
categoryCount = 9
## Scoreboard
scoreBoardTitle = "Score Board"
scoreBoardColumn = categoryList
scoreBoardRow = [players[0], players[1]]
## Points
doremiPoints = 20
bandPoints = 30
orchestraPoints = 40
## Dice
totalDice = 5
diceList = [1,2,3,4,5]
dieValue = [1,2,3,4]
#################

########## Game ##########

## Round
currentRoundIndex = 0
##
## Dice Per Player Round
diceRollResults = [None] * totalDice
diceRolledCount = 0
dicePointsBasedOnCategory = []
##
## Score
playerCategoryScore = [[],[]]
playerScore = []
##
## Player
currentPlayer = 0
receiveCommand = False
##

##########################################################################################
# CUSTOM USER INTERFACE


class Application(Frame):
    def __init__(self, master=None):

        super().__init__(master)
        self.master = master
        self.master.title(gameName)
        self.master.geometry("750x500")
        self.master.resizable(False, False)
        self.configure(background = "pink")
        self.pack(fill="both", expand=1)

        self.coreFrame()
        self.scoreBoard()
        self.playerScore()
        self.firstRollButton()
        self.calculationBoard()
        self.consoleInitializer()
        self.playBoard()
        self.diceResults()
        #self.handleSpace()

    def space(self, event = None):
        if not receiveCommand:
            self.firstRoll()
        else:
            for i in range(len(self.calculationTableElements[0])):
                if self.calculationTableElements[currentPlayer][i]["state"] == NORMAL:
                    self.saveCategory(categoryList[i])
                    break
            
        pass
    def handleSpace(self):
        self.master.bind("<space>", self.space)

    def coreFrame(self):
        
        #Core Frame
        self.coreFrame = Frame(self, width="750", height="500")
        self.coreFrame.pack(side = "left")
        self.coreFrame.pack_propagate(0)
        self.coreFrame.configure(background = "white")

        #Title Label
        self.titleLabel = Label(self.coreFrame)
        self.titleLabel.pack(side="top")
        self.titleLabel.configure(text = gameName, background = "white", fg = "black")

        #Quit Button
        self.quit = Button(self.coreFrame)
        self.quit.configure(text = "QUIT", fg = "red", background = "white", relief = "groove", command = self.master.destroy)
        self.quit.place(relx = 0, rely = 1, anchor = "sw")

        #ShowConsole Butotn
        self.showConsoleButton = Button(self.coreFrame)
        self.showConsoleButton.configure(text = "Console >>", borderwidth = 2, relief = "ridge", fg = "black", background = "white", command = self.activateConsole)
        self.showConsoleButton.place(relx = 1, rely = 1, anchor = "se")
        

    def scoreBoard(self):
        
        #Score Table Frame (Whole Container)
        self.scoreTableFrame = Frame(self.coreFrame, width = "600", height = "150")
        self.scoreTableFrame.pack_propagate(0)
        self.scoreTableFrame.place(relx = 0.5, rely = 0.25, anchor = "center")
        self.scoreTableFrame.configure(background = "#E0E0E0", highlightthickness = 2, highlightbackground = "black")

        #Score Title
        self.scoreNameLabel = Label(self.scoreTableFrame)
        self.scoreNameLabel.configure(text = scoreBoardTitle, background = "#E0E0E0")
        self.scoreNameLabel.pack()

        #Score Table (also a frame)
        self.scoreTable = Frame(self.scoreTableFrame)
        self.scoreTable.place(relx = 0.5, rely = 0.5, anchor = "center")
        self.scoreTable.configure(background = "#E0E0E0", highlightthickness = 2, highlightbackground = "#878787")

        #Table
        self.scoreBoardTableElements = [[None] * (categoryCount + 1), [None] * (categoryCount + 1), [None] * (categoryCount + 1)]
        #Equlaize width of elements
        for i in range(categoryCount + 1):
            self.scoreTable.grid_columnconfigure(i, weight=1, uniform="fred")

        #Row 1
        for i in range(1, categoryCount + 1):
            self.scoreBoardTableElements[0][i] = Label(self.scoreTable)
            self.scoreBoardTableElements[0][i].grid(row = 0, column = i)
            self.scoreBoardTableElements[0][i].configure(background = "#E0E0E0", text = categoryList[i - 1])

        # &&& - EDIT THIS ELEMENT
        #Remaining Rows
        for i in range(1, len(players) + 1):
            for j in range(1, categoryCount + 1):
                self.scoreBoardTableElements[i][j] = Label(self.scoreTable)
                self.scoreBoardTableElements[i][j].grid(row = i, column = j)
                self.scoreBoardTableElements[i][j].configure(background = "#E0E0E0", text = " ")

            #Player Column
            self.scoreBoardTableElements[i][0] = Label(self.scoreTable)
            self.scoreBoardTableElements[i][0].grid(row = i, column = 0)
            self.scoreBoardTableElements[i][0].configure(background = "#E0E0E0", text = players[i - 1])
            

    def playerScore(self):

        self.playerScoreContainer = Frame(self.coreFrame, height = "50")
        self.playerScoreContainer.place(relx = 0.5, rely = 0.5, anchor = "center")
        self.playerScoreContainer.configure(background = "white")

        self.playerScoreLiteralDisplay = Label(self.playerScoreContainer)
        self.playerScoreLiteralDisplay.grid(row = 0, column = 0, sticky = "ns")
        self.playerScoreLiteralDisplay.configure(background = "black", fg = "white", text = "Player Scores:  ")


        #Player Score Display
        self.playerScores = [[None] * 3, [None] * 3]
        for i in range(len(players) -1, -1, -1):
            #Player Frame
            self.playerScores[i][0] = Frame(self.playerScoreContainer, width = "50", height = "50")
            self.playerScores[i][0].grid(row = 0, column = i + 1)
            self.playerScores[i][0].pack_propagate(0)
            self.playerScores[i][0].configure(background = "black", highlightthickness = 1, highlightbackground = "#474747")

            #Player Name Display
            self.playerScores[i][1] = Label(self.playerScores[i][0])
            self.playerScores[i][1].pack(side = "top")
            self.playerScores[i][1].configure(background = "black", fg = "white", text = players[i])

            # &&& - EDIT THIS ELEMENT
            #Player Score Display
            self.playerScores[i][2] = Label(self.playerScores[i][0])
            self.playerScores[i][2].pack(side = "bottom")
            self.playerScores[i][2].configure(background = "black", fg = "white", text = "0")


    def firstRollButton(self):

        #First Roll Frame
        self.firstRollFrame = Frame(self.playerScoreContainer)
        self.firstRollFrame.pack_propagate(0)
        self.firstRollFrame.configure(background = "black", width = "50", height = "22")
        #self.firstRollFrame.grid(row = 1, column = 1)

        #Player First Roll Button
        self.playerFirstRollButton = Button(self.firstRollFrame)
        self.playerFirstRollButton.pack_propagate(0)
        self.playerFirstRollButton.place(relx = 0.5, rely = 0, anchor = "n")
        self.playerFirstRollButton.configure(text = "Roll", background = "black", borderwidth = 0, fg = "yellow", width = "50", command = self.firstRoll)

    def calculationBoard(self):

        #Calculation Board Frame (Whole Container)
        self.calculationBoardFrame = Frame(self.coreFrame, width = "550", height = "75")
        self.calculationBoardFrame.pack_propagate(0)
        self.calculationBoardFrame.place(relx = 0.5, rely = 0.85, anchor = "center")
        self.calculationBoardFrame.configure(background = "#E0E0E0", highlightthickness = 2, highlightbackground = "black")

        #Score Table (also a frame)
        self.calculationTable = Frame(self.calculationBoardFrame)
        self.calculationTable.place(relx = 0.5, rely = 0.5, anchor = "center")
        self.calculationTable.configure(background = "#E0E0E0", highlightthickness = 2, highlightbackground = "#878787")

        #Table
        self.calculationTableElements = [[None] * (categoryCount), [None] * (categoryCount)]

        #Equlaize width of elements
        for i in range(categoryCount):
            self.calculationTable.grid_columnconfigure(i, weight=1, uniform="fred")

        #Row 1
        for i in range(categoryCount):
            self.calculationTableElements[0][i] = Button(self.calculationTable, width = "7")
            self.calculationTableElements[0][i].grid(row = 0, column = i)
            name = categoryList[i]
            self.calculationTableElements[0][i].configure(background = "#E0E0E0", borderwidth = 1, relief = "ridge", text = name, command = lambda name=name: self.saveCategory(name))
            
            # &&& - EDIT THIS ELEMENT
            self.calculationTableElements[1][i] = Button(self.calculationTable, width = "7")
            self.calculationTableElements[1][i].grid(row = 1, column = i)
            name = categoryList[i]
            self.calculationTableElements[1][i].configure(background = "#E0E0E0", borderwidth = 1, relief = "ridge", text = " ", command = lambda name=name: self.saveCategory(name))
        
    def consoleInitializer(self):

        #Console Frame
        self.consoleFrame = Frame(self, width = "300", height = "500")
        
        self.consoleFrame.pack_propagate(0)
        self.consoleFrame.configure(background = "#ebebeb")

        #Console Log Frame
        self.consoleLogFrame = Frame(self.consoleFrame, width = "290", height = "386")
        self.consoleLogFrame.configure(background = "black")
        self.consoleLogFrame.pack_propagate(0)
        self.consoleLogFrame.place(relx = 0.5, rely = 0.01, anchor = "n")

        self.consoleLog = ScrolledText(self.consoleLogFrame)
        self.consoleLog.pack()
        self.consoleLog.configure(fg = "black", borderwidth = 0, highlightthickness = 2, highlightcolor = "black", state = "disabled")
            
        #Console Command Entry
        self.consoleCommandEntry = Entry(self.consoleFrame, width = "30")
        self.consoleCommandEntry.pack_propagate(0)
        self.consoleCommandEntry.configure(borderwidth = 1, relief = "groove", background = "white", fg = "black")
        self.consoleCommandEntry.place(relx = 0.5, y = 440, anchor = "n")
        self.consoleCommandEntry.bind('<Return>', self.submitCommand)

        #Clear Console Command Entry Button
        self.clearConsoleCommandButton = Button(self.consoleFrame)
        self.clearConsoleCommandButton.configure(text = "Clear", borderwidth = 1, relief = "groove", fg = "black", background = "white", command = lambda: self.consoleCommandEntry.delete(0, END))
        self.clearConsoleCommandButton.place(relx = 0.99, y = 437, anchor = "ne")

        #Submit Console Command Button
        self.submitCommandButton = Button(self.consoleFrame)
        self.submitCommandButton.configure(text = ">", borderwidth = 1, relief = "groove", fg = "black", background = "white", command = self.submitCommand)
        self.submitCommandButton.place(relx = 0.87, y = 437, anchor = "ne")

    def submitCommand(self, event = None):
        val = ">" + self.consoleCommandEntry.get()
        self.writeConsole(val)
        InputOptions(self.consoleCommandEntry.get())
        self.consoleCommandEntry.delete(0, END)
        pass

    def activateConsole(self):
        self.master.geometry("1050x500")
        self.consoleFrame.pack(side = "right")
        self.showConsoleButton.destroy()

    def playBoard(self):

        #Play Board Frame
        self.playBoardFrame = Frame(self.coreFrame)
        self.pack_propagate(0)
        self.playBoardFrame.configure(background = "white", width = "450", height = "100")

    def diceResults(self):

        #Dice Results Container
        self.diceResultsContainer = Frame(self.playBoardFrame)
        self.diceResultsContainer.configure(width = "250", height = 72, background = "white")
        self.diceResultsContainer.pack_propagate(0)
        self.diceResultsContainer.place(relx = 0.05, rely = 0.5, anchor = "w")

        diceImagesLocations = ["Assets/No Die.png", "Assets/Die 1.png", "Assets/Die 2.png", "Assets/Die 3.png", "Assets/Die 4.png"]
        self.diceImages = [ImageTk.PhotoImage(Image.open(i).resize((50, 50), Image.ANTIALIAS)) for i in diceImagesLocations]

        # &&& - EDIT THIS
        #Dice Results with images
        self.diceCanvas = [Canvas(self.diceResultsContainer) for i in range(totalDice)]

        self.diceCheckMarks = [None] * totalDice
        # &&& - EDIT AND READ THIS
        self.diceCheckVars = [None] * 5
        for i in range(len(self.diceCanvas)):
            name = str(i)
            self.diceCheckVars[i] = IntVar()
            self.diceCheckMarks[i] = Checkbutton(self.diceCanvas[i], variable=self.diceCheckVars[i])
            self.diceCheckMarks[i].place(relx = 0.5, rely = 1, anchor = "s")
            self.diceCheckMarks[i].pack_propagate(0)
            self.diceCheckMarks[i].configure(selectcolor = "yellow", background = "grey", indicatoron = 0, width = 2, bd = 1, relief = "ridge", command = lambda name = name: self.diceCheckMarkFillCheck(name))

        for i in range(len(self.diceCanvas)):

            self.diceCanvas[i].pack(side = "left")
            self.diceCanvas[i].configure(width = 50, height = 72, background = "white", borderwidth = 0, highlightthickness = 0)
            self.diceCanvas[i].pack_propagate(0)

        self.reRollButton = Button(self.playBoardFrame)
        self.reRollButton.configure(text = "Re-Roll", command = self.reRollDice)
        #self.reRollButton.place(relx = 1, rely = 0.5, anchor = "e")

        self.resetDisplayDice()
    
    def diceCheckMarkFillCheck(self, index):
        index = int(index)
        if self.diceCheckMarks[index]["text"] == "":
            self.diceCheckMarks[index].configure(text = "✓")
        else:
            self.diceCheckMarks[index].configure(text = "")

    #list - one dimensional array for each die roll result
    def displayDice(self, list):
        if len(list) != totalDice:
            raise(SystemError)
        else:
            for i in range(totalDice):
                self.diceCanvas[i].create_image(0, 0, image = self.diceImages[list[i]], anchor = "nw")
            self.playBoardFrame.place(relx = 0.5, rely = 0.673, anchor = "center")
            self.calculationBoardFrame.place(relx = 0.5, rely = 0.85, anchor = "center")
            for j in range(1, categoryCount + 1):
                if self.scoreBoardTableElements[currentPlayer + 1][j]["text"] != " ":
                    self.calculationTableElements[0][j - 1].configure(state = DISABLED)
                    self.calculationTableElements[1][j - 1].configure(state = DISABLED)
                else:
                    self.calculationTableElements[0][j - 1].configure(state = NORMAL)
                    self.calculationTableElements[1][j - 1].configure(state = NORMAL)

            

    def resetDisplayDice(self):
        for i in range(totalDice):
            self.diceCanvas[i].create_image(0, 0, image = self.diceImages[0], anchor = "nw")

    def hidePlayBoard(self):
        self.playBoardFrame.place_forget()
        self.calculationBoardFrame.place_forget()

    def saveCategory(self, category):
        category = categoryList.index(category)

        self.writeConsole("Save: " + categoryList[category] + " - " + str(self.calculationTableElements[1][category]["text"]) + " points")
        
        EnterCategory(category)
        
        self.hidePlayBoard()

        StartPlayerRound()

        pass

    #list - one dimensional array for each score
    def displayCalculationTable(self, list):
        if len(list) != categoryCount:
            raise(SystemError)
        else:
            for i in range(categoryCount):
                self.scoreBoardTableElements[1][i].configure(text = list[i])
            

    #list - multidimensional array for each player, player score 
    def displayScoreBoard(self, list):
        if len(list) != len(players) or len(list[0]) != categoryCount:
            raise(SystemError)
        else:
            for i in range(1, len(players) + 1):
                for j in range(1, categoryCount + 1):
                    value = list[i - 1][i - 1]
                    if value is None:
                        value = " "
                    self.scoreBoardTableElements[i][j].configure(text = list[i - 1][j - 1])
   
    def addToScoreBoard(self, playerIndex, categoryIndex, score):
        if self.scoreBoardTableElements[playerIndex + 1][categoryIndex + 1] is not None:
            self.scoreBoardTableElements[playerIndex + 1][categoryIndex + 1].configure(text = score)
        else:
            raise(SystemError)
        pass

    def displayTemporaryScore(self, list):
        if len(list) == categoryCount:

            for i in range(len(self.calculationTableElements[1])):
                self.calculationTableElements[1][i].configure(text = list[i])

        else:
            raise(SystemError)

    #list - one dimensional array for each player total score
    def displayPlayerScore(self, list):
        if len(list) != len(players):
            raise(SystemError)
        else:
            for i in range(len(players)):
                self.playerScores[i][2].configure(text = list[i])
            self.calculationTable.place(relx = 0.5, rely = 0.5, anchor = "center")

    def writeConsole(self, txt):
        self.consoleLog.configure(state = "normal")
        self.consoleLog.insert(INSERT, txt + "\n")
        self.consoleLog.see("end")
        self.consoleLog.configure(state = "disabled")

    def changePlayer(self, playerIndex):
        self.writeConsole(players[currentPlayer])
        self.hidePlayBoard()

        for i in range(len(self.playerScores)):
            self.playerScores[i][0].configure(borderwidth = 0, background = "black")
            self.playerScores[i][1].configure(fg = "white", background = "black")
            self.playerScores[i][2].configure(fg = "white", background = "black")

        self.playerScores[playerIndex][0].configure(borderwidth = 3, relief = "ridge", background = "yellow")
        self.playerScores[playerIndex][1].configure(fg = "black", background = "yellow")
        self.playerScores[playerIndex][2].configure(fg = "black", background = "yellow")

        self.firstRollFrame.grid(row = 1, column = playerIndex + 1)

    def firstRoll(self):
        global receiveCommand
        receiveCommand = True
        self.diceRolledCount = 0
        self.firstRollFrame.place(relx = 1, rely = 1, anchor = "nw")
        self.reRollButton.place(relx = 0.75, rely = 0.5, anchor = "center")
        for i in range(len(self.diceCheckMarks)):
            self.diceCheckMarks[i].place(relx = 0.5, rely = 1, anchor = "s")
            self.diceCanvas[i].configure(height = 72)

        self.rollDice()
        #Call Roll function
        pass

    #COMMANDS
    def rollDice(self, list = [1, 2, 3, 4, 5], cheat = False):
        self.diceRolledCount += 1
        if cheat:
            self.diceRolledCount = 3
            self.reRollDice(True)
        RollDice(list, cheat)


        pass
    
    def reRollDice(self, checkOnly = False, custom = None):
        if not checkOnly:
            rollAll = True
            for i in self.diceCheckVars:
                if i.get() == 1:
                    rollAll = False
            if custom is not None:
                self.rollDice(custom)
            elif rollAll:
                self.rollDice()
            else:
                diceToReRoll = [i + 1 for i in range(len(self.diceCheckVars)) if self.diceCheckVars[i].get() == 1]
                for i in range(len(self.diceCheckVars)):
                    self.diceCheckVars[i].set(0)
                    self.diceCheckMarks[i].configure(text = "")
                self.rollDice(diceToReRoll)
            
        if self.diceRolledCount == 3:
            self.reRollButton.place_forget()
            for i in range(len(self.diceCheckMarks)):
                self.diceCheckMarks[i].place_forget()
                self.diceCanvas[i].configure(height = 50)
        for i in range(len(self.diceCheckMarks)):
            self.diceCheckMarks[i].configure(text = "")
            self.diceCheckVars[i].set(0)
        pass

# Reset playerCategoryScore to None object on all elements including nested lists, and reset all variables
def ResetGame():
    # 2 rows, 9 columns, all None (null)
    global playerScore, currentRoundIndex, diceRollResults, diceRolledCount, dicePointsBasedOnCategory, playerCategoryScore, currentPlayer     #Python: Modify global variable
    
    playerCategoryScore = [[None] * categoryCount, [None] * categoryCount]

    playerScore = [0,0]

    currentRoundIndex = 0
    
    currentPlayer = 0

    diceRollResults = [0] * totalDice
    diceRolledCount = 0
    dicePointsBasedOnCategory = [0] * rounds


##########################

####### Global Variables #######

##   playerCategoryScore
##
##   playerScore
##
##   currentRoundIndex
##
##   diceRollResults
##   diceRolledCount
##   dicePointsBasedOnCategory
##
##   currentPlayer

################################

# Resets all variables and Starts a specified count of rounds
# Defines a match (game)
def StartMatch():
    ResetGame()     #Reset scores

    currentRoundIndex = 1
    app.changePlayer(currentPlayer)

    #global currentRoundIndex

    #for i in range(rounds):     #Calls 9 consecutive rounds
    #    currentRoundIndex = i
    #    StartRound()

    #StartPlayerRound(True)  #Display scoreboard and scores without anymore rolls

    # Determines who wins
    


# ClearScreen, Output game name, scoreboard, scoreboard table, player scores, CALLS PLAYER ROLL
# Defines a player round
def StartPlayerRound():
    global currentPlayer, currentRoundIndex, receiveCommand
    receiveCommand = False

    playerScore[0] = sum(filter(None, playerCategoryScore[0]))
    playerScore[1] = sum(filter(None, playerCategoryScore[1]))

    app.displayPlayerScore(playerScore)

    if currentRoundIndex == (rounds * len(players) - 1):
        
        winnerTotal = max(playerScore)
        winnerPlayers = []
        for i in range(len(playerScore)):
            if playerScore[i] == winnerTotal:
                winnerPlayers.append(players[i])
        if len(winnerPlayers) == 0:
            raise(SystemError)

        if len(winnerPlayers) == 1:
            winnerText = f"{winnerPlayers[0]} wins!"
        else:
            winnerText = ""
            for i in range(len(winnerPlayers)):
                if len(winnerPlayers) - i == 1:
                    winnerText += f"{winnerPlayers[i]} "
                else:
                    winnerText += f"{winnerPlayers[i]}, "
            winnerText += "are all tied"

        app.writeConsole(winnerText)
        app.writeConsole("--Game Ends--")

        endApp = Tk()
        
        endApp.title("Results")
        endApp.geometry("250x100")
        endApp.resizable(False, False)
        endApp.configure(background = "white")
        text = Label(endApp, text = winnerText, fg = "black", background = "white")
        text.place(relx = 0.5, rely = 0.5, anchor = "center")

        quit = Button(endApp, text = "Quit", fg = "red", background = "white", borderwidth = 1, relief = "ridge", command = lambda: endGame([root, endApp]))
        quit.place(relx = 0.5, rely = 0.99, anchor = "s")

        endApp.protocol("WM_DELETE_WINDOW", lambda: endGame([root, endApp]))

    else:
        currentPlayer = not currentPlayer
        currentRoundIndex += 1
        app.changePlayer(currentPlayer)

def endGame(apps):
    for i in apps:
        i.destroy()

# Defines a roll
# diceNums: [int] which dice to re roll, leave empty if all
def RollDice(diceNums = None, cheat = False):
    global diceRollResults, diceRolledCount

    if cheat:
        diceRollResults = diceNums
        app.diceRolledCount = 3
    else:

        # True condition: Roll all dice
        if diceNums is None:
            for i in range(totalDice):
                diceRollResults[i] = random.choice(dieValue)
        # False condition: Get all values in diceNums and roll the specific dice
        else:
            diceNums = list(dict.fromkeys(diceNums))     #Remove Duplicates

            for i in diceNums:   #All values in diceNums
                diceRollResults[i - 1] = random.choice(dieValue)

    app.displayDice(diceRollResults)

    consoleWrite = ", ".join([str(i) for i in diceRollResults])
    app.writeConsole(consoleWrite)

    CalculateDice()


# Input Options
# SAVE, ROLL, ROLL d1...d5, CHEAT
def InputOptions(command):
    if receiveCommand:

        # Strip whitespaces left & right, case-insensitize for single word commands
        command = command.strip().upper()
        # Split spaces, for ROLL command
        splitCommand = (command.split(" "))

        ##### CHEAT COMMAND ######
        if "CHEAT" == command.split(" ")[0].upper():   #Get the first 'word', Case-Insensitize

            # Split input into a list of strings
            cheatSplitString = command.split(" ")

            correctCheatStructFormat = True #Controller
            if len(cheatSplitString) != 6:   #["CHEAT", 1, 2, 3, 4, 1] -> count = 6
                correctCheatStructFormat = False

            # If Cheat Structure format is wrong, skip
            if correctCheatStructFormat:
                # Initialize cheatDice list with a range
                cheatDice = list(range(totalDice))

                correctCheatNumFormat = True    #Controller
                fail = False    #Also a Controller

                # Loop to check and convert all string elements in list to int
                for i in range(1, len(cheatSplitString)):

                    try:    #If conversion fails
                        cheatDice[i - 1] = int(cheatSplitString[i])
                    except:
                        fail = True
                        break

                    # Check value is within dice acceptable range -> [1,2,3,4]
                    if not (cheatDice[i - 1] in diceList):
                        correctCheatNumFormat = False
                        break

                # Determines whether CHEAT command can proceed
                if (correctCheatNumFormat and correctCheatStructFormat) and not fail:
                    Cheat(cheatDice)
                else:
                    app.writeConsole("<ERROR: Unknown Command>")
            else:
                app.writeConsole("<ERROR: Unknown Command>")
            ##########################

            

            

        elif splitCommand[0] == "SAVE":
            if len(splitCommand) == 2:
                EnterCategory(splitCommand[1], True)
            else:
                app.writeConsole("<ERROR: Invalid Save Command>")

        elif "ROLL" == command:
            app.reRollDice()

        elif splitCommand[0] == "ROLL":
            del(splitCommand[0])   #Remove "ROLL" from int list
            diceNeededToReRoll = list(range(len(splitCommand)))    #Initialize diceNeededToReRoll

            fail = False    #Controller
            # Loop to convert string to int
            for i in range(len(splitCommand)):

                try:
                    # Attempt to convert
                    diceNeededToReRoll[i] = int(splitCommand[i])
                    # Check value within range
                    if not diceNeededToReRoll[i] in diceList:
                        fail = True
                        break
                        
                except:
                    fail = True
                    break
            # If structure is good, execute Roll d1...d5 command
            if not fail:
                app.reRollDice(custom = diceNeededToReRoll)
            # Roll d1...d5 wrong structure
            else:
                app.writeConsole("<ERROR: Invalid Roll Command>")

        # Unkown command
        else:
            app.writeConsole("<ERROR: Unknown Command>")

    else:
        if command == "":
            app.firstRoll()
        else:
            app.writeConsole("<Enter an empty command to start>")

# Enter Category
# Saves the specific score in a category defined by player, calculated in Dice Calculation
def EnterCategory(category, consoleCall = False):
    global playerCategoryScore

    categoryIndexChosen = -1    #Controller

    if consoleCall:

        categoryInput = category
        categoryInput = categoryInput.lower()   #Case-Insensitize

        for i in range(len(categoryList)):
            if categoryInput == categoryList[i].lower():    #Check with category list elements case-insensitized
                categoryIndexChosen = i     #Determine the exact index to save the specific points/score into the defined category
                break

        if (categoryIndexChosen < 0):
            app.writeConsole(f"<ERROR: '{categoryInput}' does not exist>")
        else:
            # If the category doesn't have a value yet, proceed and save
            if playerCategoryScore[currentPlayer][categoryIndexChosen] is None: 
                playerCategoryScore[currentPlayer][categoryIndexChosen] = dicePointsBasedOnCategory[categoryIndexChosen]
                app.addToScoreBoard(currentPlayer, categoryIndexChosen, dicePointsBasedOnCategory[categoryIndexChosen])
                StartPlayerRound()
            # Else request input again
            else:
                app.writeConsole(f"<ERROR: '{categoryInput}' has been used>")
    
    else:
        categoryIndexChosen = category
        # Saves score into the 2D list
        playerCategoryScore[currentPlayer][categoryIndexChosen] = dicePointsBasedOnCategory[categoryIndexChosen]
        app.addToScoreBoard(currentPlayer, category, dicePointsBasedOnCategory[categoryIndexChosen])


# Calculates diceRollResults and the points and calls to the print dice roll results and points function
def CalculateDice():
    global dicePointsBasedOnCategory
    dicePointsBasedOnCategory = [0] * categoryCount     #Initialize list filled with 0s
    ## diceRollResults Analysis
    oneSToFourS = [0,0,0,0]     #Initialize temporary list variable, defines total dice value occurence based on index starting from 0
    
    onlyTrio = False            #Controller for Band Check
    # Calculate the number of dice appearing of each value
    for i in diceRollResults:
        oneSToFourS[i - 1] += 1

    for i in range(len(oneSToFourS)):
        dicePointsBasedOnCategory[i] = oneSToFourS[i] * (i+1)   #1S,2S,3S,4S calculation and assignment

        if oneSToFourS[i] > 2:  #Trio achieved
            dicePointsBasedOnCategory[4] = sum(diceRollResults) #Trio Assignment
            onlyTrio = True
            trioIndex = i

            if oneSToFourS[i] > 3:  #Quartet achieved
                dicePointsBasedOnCategory[5] = sum(diceRollResults) #Quartet Assignment
                onlyTrio = False

                if oneSToFourS[i] > 4:  #Orchestra achieved
                    dicePointsBasedOnCategory[8] = orchestraPoints

    if onlyTrio:    #Possible Band
        for i in range(len(oneSToFourS)):
            if i == trioIndex:  #Skip all values corresponding to the trio values
                continue
            if oneSToFourS[i] > 1:  #Band achieved
                dicePointsBasedOnCategory[6] = bandPoints

    if oneSToFourS[0] > 0 and oneSToFourS[1] > 0 and oneSToFourS[2] > 0 and oneSToFourS[3] > 0: #Doremi achieved
        dicePointsBasedOnCategory[7] = doremiPoints

    app.displayTemporaryScore(dicePointsBasedOnCategory)


# The cheat method, changes dice results based on cheat command
def Cheat(cheatValues):
    global diceRollResults
    # Directly assigns all values in CHEAT command to replace dice roll value results
    diceRollResults = cheatValues
    app.rollDice(diceRollResults, True)
    # Recalculate dice based on new cheated values
    CalculateDice()
    
def startAppGame():
    global root, app
    startApp.destroy()
    root = Tk()
    app = Application(master=root)
    # Start Game
    StartMatch()
    app.master.mainloop()

startApp = Tk()
startApp.title("Start")
startApp.geometry("250x100")
startApp.resizable(False, False)
startApp.configure(background = "white")
startAppTitle = Label(startApp, text = gameName, fg = "black", background = "white")
startAppTitle.place(relx = 0.5, rely = 0.25, anchor = "center")

startAppGame = Button(startApp, text = "START", fg = "blue", background = "white", borderwidth = 1, relief = "ridge", command = startAppGame)
startAppGame.place(relx = 0.5, rely = 0.75, anchor = "center")

quitStart = Button(startApp, text = "Quit", fg = "red", background = "white", borderwidth = 1, relief = "ridge", command = startApp.destroy)
quitStart.place(relx = 0.995, rely = 0.99, anchor = "se")

startApp.mainloop()


# Exit PAUSE (for direct execution)
#input("\nProgram Ended. Press ENTER To Quit")

