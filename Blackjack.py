#import modules for math and random handling
import math
from random import randint
import random

#declaration of global variables, such as player names, values and names for each suit and card
AI_Names = ['Botmas Midchael Wack', 'Wacktrick Squeal', 'Paia Prips', 'Puke Pilliams', 'Moody Maroline', 'Flappy Ben', 'ChatGPT']
cardNames = ['Ace', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'Jack', 'Queen', 'King']
cardValues = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10]
suitNames = ['Spades', 'Clubs', 'Hearts', 'Diamonds']

#creates an ordered deck of 52 cards
def createDeck():
    deck = []
    suits = ['0','1','2','3']
    for s in suits:
        for i in range(13):
            deck.append(s + str(i+1))
    return deck

#takes user input for player name, number of decks and number of AI playersaa
def generatePlayers():
    #player name and deck number
    playerName = str(input('Enter your name: '))
    deckNumber = int(input('How many decks would you like to play with? (2 to 5): '))
    if deckNumber >= 2 and deckNumber <= 5:
        pass
    else:
        print('\nInvalid option\n')
        generatePlayers()

    #handles the number of players and assigns a name to each
    numberOfPlayers = int(input('Enter the number of players you wish to play against (0 to 4): '))
    if numberOfPlayers <= 4:
        players = [playerName]
        currentHands = [[]]
        namesLeft = AI_Names
        for i in range(numberOfPlayers):
            digit = randint(0,len(namesLeft))
            players.append(namesLeft[digit-1])
            namesLeft.pop(digit-1)
            currentHands.append([])
        players.append('The Dealer')
        currentHands.append([])
    else:
        print('\nInvalid option\n')
        generatePlayers()

    #displays the players in the game, including the user and the dealer
    print('\nThe current players are:')
    for p in players:
        print(p)
    print('')
    return playerName, players, currentHands, deckNumber

#generates a shuffled pile of 'n' amount of decks for the start of a game
def generatePile(currentPile, deckNumber, deck):
    for i in range(deckNumber):
        shuffledDeck = deck
        random.shuffle(shuffledDeck)
        for i in range(52):
            currentPile.append(shuffledDeck[i])
    random.shuffle(currentPile)
    return currentPile

#is called at the start of the game and calls generatePile function to create a new pile
#is called at the start of each hand. when the pile drops 52 cards below the target pile size, a new shuffled deck is added to the top
def handlePile(currentPile, deckNumber, deck):
    if len(currentPile) == 0:
        currentPile = generatePile(currentPile, deckNumber, deck)
    elif len(currentPile) <= (deckNumber - 1) * 52:
        shuffledDeck = deck
        random.shuffle(shuffledDeck)
        for i in range(52):
            currentPile.append(shuffledDeck[i])

#used to check whether the current hand has blackjack (21 with 2 cards)
def checkBlackjack(hand):
    if (int(hand[1]) == 1 and cardValues[int(hand[3])-1] == 10) or (int(hand[3]) == 1 and cardValues[int(hand[1])-1] == 10):
        return True
    else:
        return False

#handles the 
def gameplay(playerName, players, currentHands, currentPile, deckNumber, deck):
    #handles the pile for the game
    handlePile(currentPile, deckNumber, deck)
    for h in range(len(players)):
        currentHands[h] = []
    for i in range(2):
        for h in currentHands:
            h.append(currentPile[0])
            currentPile.pop(0)

    #checks the dealer's hand for blackjack
    dealerHand = []
    for i in range(len(currentHands[len(players)-1])):
        dealerHand.append(currentHands[len(players)-1][i][0])
        dealerHand.append(currentHands[len(players)-1][i][1:])
    checkDealerWin = checkBlackjack(dealerHand)
    if checkDealerWin == True:
        print("The dealer's hand is:")
        for i in range(len(currentHands[len(players)-1])):
            print(cardNames[int(dealerHand[(2*i)+1])-1],'of',suitNames[int(dealerHand[2*i])])
        print('The dealer wins by default because they got blackjack!')

    #game continues if dealer does not have blackjack
    else:
        playerHand = []
        for i in range(len(currentHands[0])):
            playerHand.append(currentHands[0][i][0])
            playerHand.append(currentHands[0][i][1:])
        checkWin = checkBlackjack(playerHand)
        if checkWin == True:
            print('Your hand is:')
            for i in range(len(currentHands[0])):
                print(cardNames[int(playerHand[(2*i)+1])-1],'of',suitNames[int(playerHand[2*i])])
            print('Your total is 21! You got blackjack!')
        else:
            bust = False
            while bust == False:
                score = 0
                playerHand = []
                aces = 0
                for i in range(len(currentHands[0])):
                    playerHand.append(currentHands[0][i][0])
                    playerHand.append(currentHands[0][i][1:])

                print('Your hand is:')
                for i in range(len(currentHands[0])):
                    print(cardNames[int(playerHand[(2*i)+1])-1],'of',suitNames[int(playerHand[2*i])])

                for i in range(len(playerHand)):
                    if i % 2 == 1:
                        if playerHand[i] == '1':
                            aces += 1
                        score += cardValues[int(playerHand[i])-1]
                if score > 21:
                    print('\nYou went bust with a total of:', score)
                    bust = True
                    break
                elif aces > 0 & score <= 21:
                    if score > 11:
                        print('\nYour total is', score)
                    elif score <= 11:
                        print('\nYour total is', score,'or',score + 10)
                elif aces == 0 & score <= 21:
                    print('\nYour total is',score)

                userInput = str(input('\nHit or stand? (h/s): '))
                if userInput.upper() == 'H':
                    currentHands[0].append(currentPile[0])
                    currentPile.pop(0)
                else:
                    break

        AIgameplay(players, currentHands, currentPile)

def AIgameplay(players, currentHands, currentPile):
    for i in range(len(players)-2):
        bust = False
        while bust == False:
            print(currentHands[i+1])
            AIhand = []
            AIscore = 0
            for j in range(len(currentHands[i+1])):
                AIhand.append(currentHands[i+1][j][0])
                AIhand.append(currentHands[i+1][j][1:])
            for s in range(len(currentHands[i+1])):
                AIscore += AIhand[(2*s)+1]
            if AIscore < 16:
                pass
            



        




def dealerGameplay(players, currentHands, currentPile):
    pass

def menu():
    print('Welcome to Blackjack!\n')
    deck = createDeck()
    playerName, players, currentHands, deckNumber = generatePlayers()
    currentPile = []
    playing = True
    while playing == True:
        userInput = str(input('\nNew hand?(y/n): '))
        print('')
        if userInput.upper() == 'Y':
            gameplay(playerName, players, currentHands, currentPile, deckNumber, deck)
        else:
            playing = False

menu()