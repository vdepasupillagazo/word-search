################################################################
# Code for our version of the game Word Search (a.k.a. Boggle) #
# Written by Group 6 for CMSC 202, 1st Sem AY 2024-2025        #
################################################################
import shutil  #Module for getting terminal dimensions
import random
import re      

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
            gridsize = 3
            print("Selected Grid: 3x3")
            break
        elif grid_choice == "2":
            gridsize = 4
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

def create_grid(size):
    # Initialize an empty list to hold the grid
    grid = []

    # Loop to create each row
    for i in range(size):
        # Create a row for each grid row
        row = ["_"] * size  # Fill each row with spaces
        # Add the row to the grid
        grid.append(row)

    return grid

def print_grid(grid):
    # Print according to selected size
    rows = len(grid)
    cols = len(grid[0])

    #Centering the Grid
    terminal_width, _ = shutil.get_terminal_size() # Get terminal width
    grid_width = cols * 2 + (cols - 1) + 2  #Each cell is 2 chars, borders, and dividers 
    left_padding = max(0, (terminal_width - grid_width) // 2) #Calculate left padding for centering, adds pads to center in terminal

    #Top border
    print(" " * left_padding + "┌" + "───┬" * (cols - 1) + "───┐")
    for i, row in enumerate(grid):
        # Row content
        print(" " * left_padding + "│" + "│".join("{:^3}".format(j) for j in row) + "│")
        # Row divider (except after the last row)
        if i < rows - 1:
            print(" " * left_padding + "├" + "───┼" * (cols - 1) + "───┤")
    # Bottom border
    print(" " * left_padding + "└" + "───┴" * (cols - 1) + "───┘")

def load_word_library(grid, min=3, filename= "word-list.txt"):
    # read words from file and return as dict for use in program
    
    #transform grid as the letter_list (flatten 2d array - 1d array using comprehension)
    letter_list_ref = [letter for row in grid for letter in row]

    valid_word_dict = {}

    #max letters in a word
    max = len(letter_list_ref)

    #filter words in the raw txt file 
    with open(filename, "r") as file:
        for line in file:
            word = line.strip()
            
            #filter based on word length
            if len(word) >= min and len(word) <= max: 
                letter_list = letter_list_ref.copy()

                #handling if word has 'qu'
                word_qu = re.findall(r"qu|.", word) if 'qu' in word else word

                #filter based on word structure
                  #1. letter in letter_list
                  #2. Letter in letter_list is used only once
                for letter in word_qu:
                    if letter in letter_list:
                        letter_list.remove(letter)
                        continue
                    else:
                        break

                #if the word passed inspections:
                else:

                    #create a key from the first 3 letter of the word
                    key = word[:3]

                    #append the word as a value to the existing key
                    if key in valid_word_dict.keys():
                        if word in valid_word_dict[key]:
                            continue
                        else:
                            valid_word_dict[key].append(word)

                    #else create a new key/val 
                    else:
                        valid_word_dict[key] = [word]

    return valid_word_dict

def timer():
    # handles logic for timer
    return

# generates random list of letters to use in game
# allow letter repetition by default
def letter_draw(count, letterSet, repeat=True):
    drawnLetters = ()
    while len(drawnLetters) < count:
        index = random.randint(0, len(letterSet)-1)
        if (not repeat and letterSet[index] in drawnLetters):
            # choose another letter if already exists
            continue
        else:
            # if repeat=True letters are allowed to have multiple instances
            # else only first instance is inserted
            drawnLetters += (letterSet[index],)

    return drawnLetters

def generate_vowel_list(size):
    vowels = ('a', 'e', 'i', 'o', 'u')

    # sets the min and max number of vowels for each grid size
    rangeLimit = [3, 4] if size == 3 else [4, 7]
    vowelCount = random.randint(rangeLimit[0], rangeLimit[1])
    vowelList = letter_draw(vowelCount, vowels)

    return vowelList

def generate_consonant_list(consonantCount):
    # uncommon defined as letter frequency of less than 1%
    uncommonConsonants = ('j', 'k', 'qu', 'v', 'x', 'z')
    # additional entries for letters with frequency higher than 5%
    commonConsonants = ('b', 'c', 'd', 'f', 'g', 'h', 'l', 'l',
                        'm', 'n', 'n', 'p', 'r', 'r', 's', 's', 't', 't', 'w', 'y')

    # mechanism to include a maximum of 2 uncommon consonants in list
    uConsonantCount = random.randint(0, 2)

    if (uConsonantCount > 0):
        uConsonantList = letter_draw(uConsonantCount, uncommonConsonants, False)
        consonantList = letter_draw(
            consonantCount-uConsonantCount, commonConsonants)

        # insert into random index in cosonantList
        for uc in uConsonantList:
            index = random.randint(0, len(consonantList))
            consonantList = consonantList[0:index] + \
                (uc,) + consonantList[index:len(consonantList)]
    else:
        consonantList = letter_draw(consonantCount, commonConsonants)

    return consonantList

def randomizer(grid):
    vowelList = generate_vowel_list(len(grid))
    consonantList = generate_consonant_list((len(grid)**2)-len(vowelList))

    # increment only when a vowel is inserted
    vCounter = 0
    while vCounter < len(vowelList):
        x = random.randint(0, len(grid)-1)
        y = random.randint(0, len(grid)-1)

        if (grid[x][y] == "_"):
            grid[x][y] = vowelList[vCounter]
            vCounter += 1

    # insert consonants into remaining slots in grid
    cCounter = 0
    for x in range(0, len(grid)):
        for y in range(0, len(grid[x])):
            if (grid[x][y] == "_"):
                grid[x][y] = consonantList[cCounter]
                cCounter += 1

    return grid

def generateWordList():
    # compiles the list of words that the user can find in the game
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

def word_search():
    # game start!
    gridsize, timeroption = menu()
    gridTemplate = create_grid(gridsize)
    grid = randomizer(gridTemplate)
    print_grid(grid)
    valid_words = load_word_library(grid)
  

word_search()