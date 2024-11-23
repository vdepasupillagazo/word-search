################################################################
# Code for our version of the game Word Search (a.k.a. Boggle) #
# Written by Group 6 for CMSC 202, 1st Sem AY 2024-2025        #
################################################################
#creating menu for the word search game
def menu():
    print("CMSC 202 | Group 6 (Word Search)")
    #adding options for selecting grid size
    while True:
        print("\nSelect Grid Size:")
        print("1. 3x3")
        print("2. 4x4")
        grid_choice = input("Enter Your Choice (1 or 2): ").strip()

        if grid_choice == "1":
            gridsize = 1
            print("Selected Grid: 3x3")
            break
        elif grid_choice == "2":
            gridsize = 2
            print("Selected Grid: 4x4")
            break
        else:
            print("Invalid Choice. Please Select 1 or 2.")
    #adding the time options (4 selections)
    while True:
        print("\nSelect Timer Option (1-4):")
        print("1. 1 Minute")
        print("2. 3 Minutes")
        print("3. 5 Minutes")
        print("4. Untimed")
        timer_choice = input("Enter Your Choice (1 - 4): ").strip()

        if timer_choice in {"1", "2", "3", "4"}:
            timeroption = int(timer_choice)
            
            timer_d = {1: "1 Minute", 2: "3 Minutes", 3: "5 Minutes", 4: "Untimed"}
            
            print(f"Selected Timer: {timer_d[timeroption]}")
            break
        else:
            print("Invalid Choice. Please Select Between 1 - 4.")

    return gridsize, timeroption

gridsize, timeroption = menu()




def loadWordLibrary():
    # read words from file and return as list for use in program
    return

def generateGrid():
    # generate empty tile grid prepopulated with placeholder characters
    return

def timer():
    # handles logic for timer
    return

def randomizer():
    # generate random list of letters to use as game tiles
    return

def generateWordList():
    # compiles the list of words that the user can find in the game
    return

def printTiles():
    # prints the game tiles
    return

def scoreWord():
    # assigns a score to each word found, depending on the length
    return

def checkWord():
    # checks if user found a correct word
    return

def printWordList():
    # prints all possible words to be found at game end
    return

def wordSearch():
    # game start!
    return