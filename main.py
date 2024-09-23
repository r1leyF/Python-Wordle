import random
import pygame
import sys
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((640,500))
pygame.display.set_caption("Wordle")
font = pygame.font.SysFont('Comic Sans MS', 28)

green = pygame.Color(93,151,88)
yellow = pygame.Color(191, 169, 69)
gray = pygame.Color(78,78,80)
darkGray = pygame.Color(28,28,29)
white = pygame.Color(248,248,248)
black = pygame.Color(18,18,19)

boxXPos = [200,250,300,350,400]
boxYPos = [10,65,120,175,230,285]
pointerXPos = 160

currBox = [0,0]
inputLetters = ['','','','','']

alphabet = ('Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M')

# get a list of words from an input file
fileName = 'input.txt'

with open(fileName, 'r') as file:
    wordleWords = []
    line = file.readline()

    while line:
        # get the word minus \n character
        wordleWords.append(line[:len(line)-1].upper())
        line = file.readline()

# get a random word from the list
todaysWord = ['word']

# set of letters already used
lettersUsed = set()
lettersCorrect = set()
lettersMaybe = set()

def create_box(text, color, width, x, y, fontType = font):
    pygame.draw.rect(screen, color, (x,y, width, width))
    text = str(text)
    text = fontType.render(text, True, black)
    screen.blit(text, (x+(width/5),y))

def display_word_error(hide):
    xPos = 185
    yPos = 330
    width = 370
    height = 35
    if not hide:
        pygame.draw.rect(screen, darkGray, (xPos,yPos,width,height))
        text = font.render('word not in database', True, white)
        screen.blit(text, (xPos, yPos))
    else:
        pygame.draw.rect(screen, darkGray, (xPos,yPos,width,height))

def update_alphabet():
    xpos = 130
    ypos = 380
    #tinyFont = pygame.font.Font(pygame.font.get_default_font(), 28)
    tinyFont = pygame.font.SysFont('Comic Sans MS', 22)
    color = white
    # print first row
    for i in range(10):
        if alphabet[i] in lettersCorrect:
            color = green
        elif alphabet[i] in lettersMaybe:
            color = yellow
        elif alphabet[i] in lettersUsed:
            color = gray
        else:
            color = white
        create_box(alphabet[i], color, 30, xpos, ypos, tinyFont)
        xpos += 40
    xpos = 150
    ypos += 40
    # print second row
    for i in range(10, 19):
        if alphabet[i] in lettersCorrect:
            color = green
        elif alphabet[i] in lettersMaybe:
            color = yellow
        elif alphabet[i] in lettersUsed:
            color = gray
        else:
            color = white
        create_box(alphabet[i], color, 30, xpos, ypos, tinyFont)
        xpos += 40
    xpos = 180
    ypos += 40
    # print third row
    for i in range(19, 26):
        if alphabet[i] in lettersCorrect:
            color = green
        elif alphabet[i] in lettersMaybe:
            color = yellow
        elif alphabet[i] in lettersUsed:
            color = gray
        else:
            color = white
        create_box(alphabet[i], color, 30, xpos, ypos, tinyFont)
        xpos += 40

def restart_game():
    screen.fill(darkGray)

    # redraw empty boxs
    for i in range(5):
        for j in range(6):
            create_box('', white, 40, boxXPos[i], boxYPos[j])

    # reset inputLetters and currBox
    currBox[0] = 0
    currBox[1] = 0
    todaysWord[0] = random.choice(wordleWords)
    print(todaysWord[0])
    lettersCorrect.clear()
    lettersMaybe.clear()
    lettersUsed.clear()
    update_alphabet()
    pygame.display.update()

restart_game()

gameisDone = False

while True:
    for event in pygame.event.get():
        
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

        elif gameisDone:
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                elif event.key == K_RETURN:
                    restart_game()
                    gameisDone = False
                    continue

        elif event.type == KEYDOWN:
            display_word_error(True)

            if event.key == K_ESCAPE:
                pygame.quit()
                sys.exit()

            elif event.key == K_BACKSPACE:
                if currBox[0] != 0:
                    currBox[0] -= 1;
                    create_box('', white, 40, boxXPos[currBox[0]], boxYPos[currBox[1]])

            elif event.key == K_RETURN:
                # if boxs are full try out the word
                if currBox[0] == 5:
                    # get the user word as a string
                    userWord = str(inputLetters[0]+inputLetters[1]+inputLetters[2]+inputLetters[3]+inputLetters[4])

                    # if the word is in database accept word and compare
                    if userWord in wordleWords:
                        # the current box we are checking
                        currBox[0] = 0

                        # The indexs we still need to check checked
                        greenLetters = []
                        lettersRemain = list(todaysWord[0])
                        
                        # check for perfect matches
                        for i in range(5):
                            if(userWord[i] == todaysWord[0][i]):
                                # make box green
                                create_box(userWord[i], green, 40, boxXPos[currBox[0]], boxYPos[currBox[1]])
                                greenLetters.append(i)
                                lettersRemain.remove(userWord[i])
                                lettersCorrect.add(userWord[i])
                            currBox[0] += 1
                        currBox[0] = 0
                        # check for letters in the word but not right place
                        for i in range(5):
                            if(userWord[i] in todaysWord[0]) and (i not in greenLetters) and (userWord[i] in lettersRemain):
                                #make box yellow
                                create_box(userWord[i], yellow, 40, boxXPos[currBox[0]], boxYPos[currBox[1]])
                                lettersRemain.remove(userWord[i])
                                lettersMaybe.add(userWord[i])
                            elif userWord[i] != todaysWord[0][i]:
                                create_box(userWord[i], gray, 40, boxXPos[currBox[0]], boxYPos[currBox[1]])
                                lettersUsed.add(userWord[i])
                            currBox[0] += 1

                        # move to the next guess row
                        currBox[1] += 1
                        currBox[0] = 0

                        #check if player won
                        if userWord == todaysWord[0]:
                            # clear alphabet
                            pygame.draw.rect(screen, darkGray, (130,380,400,150))
                            # print win stuff
                            text = font.render('Winner! Press enter to replay', True, white)
                            screen.blit(text, (125,380))
                            # press enter to replay
                            gameisDone = True
                            continue

                        # check if player is out of guesses
                        if currBox[1] > 5:
                            # clear alphabet
                            pygame.draw.rect(screen, darkGray, (130,380,400,150))
                            # print loser message
                            text = font.render(f'Loser! Word was \'{todaysWord[0]}\'', True, white)
                            screen.blit(text, (160,365))
                            text = font.render('Press enter to replay', True, white)
                            screen.blit(text, (180, 405))
                            gameisDone = True
                            continue

                        update_alphabet()
                    else:
                        # print that word does not exist
                        display_word_error(False)

            elif event.unicode.upper() in alphabet:
                #create a new box at current box pos
                if currBox[0] < 5:
                    create_box(event.unicode.upper(), white, 40, boxXPos[currBox[0]], boxYPos[currBox[1]])
                    # increment the box position
                    inputLetters[currBox[0]] = event.unicode.upper()
                    currBox[0] += 1
                    

    pygame.display.update()