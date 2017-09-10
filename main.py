#!/usr/bin/python3

from classes import player
from classes import die
import random
import datetime


# create attributes
# playerList : A dictionary to hold classes objects
# endScoreReached : Boolean to check if the game is over

playerList = {}
endScoreReached = False
endTurnReason = 0
scoreList = []
gameOn = True
newPlayers = True
#methods

def createPlayers():
    "Create classes object depending on number of players"
    playing = int(raw_input("No of Players?"))
    for number in range(1,playing+1):
        nameInput = raw_input("Name of player " + str(number) + "? ")
        playerList[number] = player(nameInput)   

def takeTurn(playerNumber):
    #empty current players dice list
    currentPlayer = playerList[playerNumber]
    currentPlayer.dice = []
    #generate a dice object
    dice = die()
    #as new turn this is the first roll
    roll = True
    rollAgain = 0
    #as new turn set turn score to 0
    thisTurnScore = 0
    #populate first dice roll
    for x in range(9):
        currentPlayer.dice.append(random.choice(dice.dieSide))
    #show player their initial roll and stop after third roll.
    while roll == True:
        if rollAgain == 1:
            break
        currentPlayer.dice.sort()
        print "You have rolled %s" % ", ".join(map(str,currentPlayer.dice))
        # expect return in list - [threeScore, fiveScore, sevenScore, scoreType]
        availableScore = showScoreOptions(currentPlayer.dice)
        if availableScore[3] == 0: # if no numbers rolled
            roll = False
            break
        if availableScore[3] == 1: # if only one option available find which one score and set turn score
            if availableScore[0] > 0:
                thisTurnScore += availableScore[0]
            if availableScore[1] > 0:
                thisTurnScore += availableScore[1]
            if availableScore[2] > 0:
                thisTurnScore += availableScore[2]
            roll = False
            break        
        if availableScore[3] == 2: # if you have many many rats
            roll = False
            break
        # 1 excess rat or loadsa numbers allow for a reroll
        if (availableScore[3] == 3) or (availableScore[3] == 4): 
            endTurnCheck = reroll(currentPlayer, availableScore[3])
            if endTurnCheck > 0:
                menuItemSelected = 0
                while menuItemSelected == 0:
                    scoreWhat = raw_input("3's 5's or 7's?")
                    if scoreWhat == '3':
                        thisTurnScore = availableScore[0]
                        menuItemSelected = 1
                    if scoreWhat == '5':
                        thisTurnScore = availableScore[1]
                        menuItemSelected = 1
                    if scoreWhat == '7':
                        thisTurnScore = availableScore[2]
                        menuItemSelected = 1                                            
                rollAgain = 1            
    return thisTurnScore

def reroll(player, reason):
    rerollingPlayer = player
    whichMenu = reason
    turnOver = 0
    dice = die()
    menuItemSelected = False       
    while menuItemSelected == False:
        if whichMenu == 4:
            print "Choose which number to keep - 3,5,7,E(nd turn)?"
        elif whichMenu == 3:
            print "Choose which number to keep - 3,5,7?"
        else:
            print "error 1"
        rerollOption = raw_input()
        if rerollOption == "3":
            rerollingPlayer.dice[:] = [ random.choice(dice.dieSide) if (x == "5" or x == "7") else x for x in rerollingPlayer.dice ]
            menuItemSelected = True
        if rerollOption == "5":
            rerollingPlayer.dice[:] = [ random.choice(dice.dieSide) if (x == "3" or x == "7") else x for x in rerollingPlayer.dice ]
            menuItemSelected = True
        if rerollOption == "7":
            rerollingPlayer.dice[:] = [ random.choice(dice.dieSide) if (x == "3" or x == "5") else x for x in rerollingPlayer.dice ]
            menuItemSelected = True
        if (rerollOption == "e" or rerollOption == "E") and (whichMenu == 4):
            turnOver = 1
            menuItemSelected = True
    return turnOver            
             
def showScoreOptions(dice):
    currentDieFaces = dice
    catzCount = currentDieFaces.count("Cat")
    ratzCount = currentDieFaces.count("Rat")
    batzCount = currentDieFaces.count("Bat")
    threeCount = currentDieFaces.count("3")
    fiveCount = currentDieFaces.count("5")
    sevenCount = currentDieFaces.count("7")
    totalNumbersCount = threeCount + fiveCount + sevenCount
    threeScore =  (threeCount * 3) + ((catzCount-ratzCount+batzCount) * 3 * threeCount)
    fiveScore =  (fiveCount * 5) + ((catzCount-ratzCount) * 5 * fiveCount)
    sevenScore = (sevenCount * 7) + ((catzCount-ratzCount-batzCount) * 7 * sevenCount)
    scoreType = 8 #setting scoreType to uncalculated
    #does Catz-Ratz equal -2 or below???
    if (totalNumbersCount == 0):
        print "No Numbers rolled"
        scoreType = 0 # setting score type to 0 as no numbers available
    if (ratzCount-catzCount) >= 2:
        print "%d excess Ratz.Turn Over" % ((ratzCount-catzCount))
        scoreType = 2 #setting score type to excess Ratz
    if (totalNumbersCount == threeCount) and (totalNumbersCount >= 1) and (scoreType != 2):
        if threeScore > 0:    
            print "Only one number available. Must score."
            scoreType = 1 #setting score type to 1 number only available
        else:
            print "Not enough Catz for those pesky Ratz"
            scoreType = 0 
    if (totalNumbersCount == fiveCount) and (totalNumbersCount >= 1) and (scoreType != 2):
        if fiveScore > 0:    
            print "Only one number available. Must score."
            scoreType = 1 #setting score type to 1 number only available
        else:
            print "Not enough Catz for those pesky Ratz"
            scoreType = 0 
    if (totalNumbersCount == sevenCount) and (totalNumbersCount >= 1) and (scoreType != 2):
        if sevenScore > 0:    
            print "Only one number available. Must score."
            scoreType = 1 #setting score type to 1 number only available
        else:
            print "Not enough Catz for those pesky Batz and Ratz"
            scoreType = 0 
    if ((ratzCount-catzCount) == 1) and (scoreType != 0):
        print "You have a Rat screwing your day."    
        if scoreType != 1:
            scoreType = 3 #setting score type to allow reroll but no score while excess Ratz 
    if scoreType == 8:
        if threeScore <= 0:
            print "3's not currently scoring"
        else:
            print "3's Score. %d x 3's with %d excess Catz and  %d Batz = %d" % (threeCount,(catzCount-ratzCount),batzCount,threeScore)
        if fiveScore <= 0:
            print "5's not currently scoring"
        else:
            print "5's Score. %d x 5's with %d excess Catz = %d" % (fiveCount,(catzCount-ratzCount),fiveScore)
        if sevenScore <= 0:
            print "7's not currently scoring"
        else:
            print "7's Score. %d 7's with %d excess Catz = %d" % (sevenCount,(catzCount-ratzCount-batzCount),sevenScore)
        scoreType = 4 #score type for normal score available
    return [threeScore,fiveScore,sevenScore,scoreType]

def writeLog():
    now = datetime.datetime.now()
    gameLogFile = "/Users/Fiachra/Documents/cbr_game_log/gameLog.txt"
    gameLog = open(gameLogFile,"a")
    gameLog.write("\n\nDATE: " + now.strftime("%d-%m-%Y %H:%M"))
    for p in playerList:
        player = playerList[p]
        gameLog.write("\nPlayer:" + str(player.name) +", Score:" + str(player.score))
    gameLog.close()

    print "Game Log written."

def playAgain():
    choiceMade = 0
    while choiceMade == 0:
        choice = raw_input("\nDo you wish to play again?")
        if (choice == "Y") or (choice == "y"):
            who = 0
            while who == 0:
                samePlayers = raw_input("\nSame Players?")
                if (samePlayers == "Y") or (samePlayers == "y"):
                    for i in playerList:
                        resetScore = playerList[i]
                        resetScore.score = 0
                    newPlayers = False
                else:
                    newPlayers = True
            choiceMade = 1
        else:
            print "\n\n\nThanks for playing!"
            gameOn = False
            choiceMade = 1
            
def takeTurnEach():
    for i in xrange(1,len(playerList)+1):
        turnPlayer = playerList[i]
        print ""
        print ""
        print "%s's turn" % (turnPlayer.name)
        #Roll the dice up 3 times dice roll for the player turn
        score = takeTurn(i)
        print "You had an existing score of {}".format(turnPlayer.score)
        print "You have taken a score of {}".format(score)        
        turnPlayer.score += score
        print "You now have a score of {}".format(turnPlayer.score)
        print ""
        print "------------------------------------"
        raw_input("Press Enter for next turn")

def checkEndScore():
    gameOver = False
    for i in playerList:
        playerToCheck = playerList[i]
        if playerToCheck.score > 250:
            gameOver = True
            print "\n\n\n\n---------- GAME OVER!!! ----------"
    return gameOver

def finalScores():
    for i in playerList:
        playersScore = playerList[i]
        scoreList.append(playersScore.score)
    maxScore = max(scoreList)
    for i in playerList:
        isMaxScorer = playerList[i]
        print "%s scores %d" % (isMaxScorer.name, isMaxScorer.score)
        if maxScore == isMaxScorer.score:
            print "{} is a winner !".format(isMaxScorer.name)
#start game
"doc ext"
while gameOn == True:
    if newPlayers == True:
            createPlayers()
            newPlayers = False
    while endScoreReached == False:
    # keep alternating player turns
        takeTurnEach()
        endScoreReached = checkEndScore()#check high score reached
    finalScores()
    #Write Game Log        
    writeLog()
    playAgain()