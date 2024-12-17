################################################################
# Code for our version of the game Word Search (a.k.a. Boggle) #
# Written by Group 6 for CMSC 202, 1st Sem AY 2024-2025        #
################################################################
import shutil  #Module for getting terminal dimensions
import random
import re      
import sys
import time
from datetime import datetime
from collections import defaultdict

# Welcome message
def welcomeMessage(message):
    width = 80
    print("\n" + message.center(width) + "\n")

# Short game description
def gameDesc():
    message = '''
    Find the hidden words in the grid. 
    Words can appear in any direction. 
    Choose your desired grid size, and enjoy the relaxing untimed mode 
    or challenge yourself with the clock. 
    Ready? Let’s begin!'''
    width = 80
    centered_gameDesc = "\n".join(line.strip().center(width) for line in message.strip().splitlines())
    return centered_gameDesc

def get_player_name():
    # Ask the player for their name
    player_name = input("Enter your name: ").strip()
    return player_name

def record_score(player_name, score):
    # Get the current date and time
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Open the scores file in append mode to add a new entry
    with open("scores.txt", "a") as file:
        # Write the player's name, score, and timestamp to the file
        file.write(f"{player_name} | {timestamp} | {score}\n")
    print(f"Score for {player_name} recorded!")

def get_top_scorers():
    top_scorers = []
    with open("scores.txt", "r") as f:
        for line in f:
            parts = line.strip().split(" | ")
            if len(parts) == 3:
                name, timestamp, score = parts
                try:
                    score = int(score)  # Ensure score is an integer for sorting
                except ValueError:
                    continue  # Skip if the score isn't a valid integer
                top_scorers.append((name, timestamp, score))
    
    # Sort the list by score in descending order
    top_scorers.sort(key=lambda x: x[2], reverse=True)

    # Return only the top 10 players (or fewer if there aren't 10)
    return top_scorers[:10]

def display_top_scorers():
    top_scorers = get_top_scorers()
    
    # Print the top 10 scorers
    print("\nTop 10 High Scorers:")
    for i, (player, timestamp, score) in enumerate(top_scorers, 1):
        print(f"{i}. {player} - {score} points (Achieved on: {timestamp})")
    print("\nThank you for playing!")

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
    print("\n") 

# splits word or key into characters, treating 'qu' as one character
def word_splitter(word):
    return re.findall(r"qu|.", word) if 'qu' in word else word

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
                word_qu = word_splitter(word)

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

# creates a dictionary of all distinct letters in the grid as keys
# and the list of all their coordinate locations as the value
def find_starting_coordinates(grid):
    startingCoordinates = {}
    for x in range(0, len(grid)):
        for y in range(0, len(grid[x])):
            if grid[x][y] in startingCoordinates.keys():
                startingCoordinates[grid[x][y]].append([x, y])
            else:
                startingCoordinates[grid[x][y]] = [[x, y]]
    return startingCoordinates

def find_next_tile(nextLetter, xyCoordinates, grid, usedTiles):
    x = xyCoordinates[0]
    y = xyCoordinates[1]
    # requested to make the code easier to read
    up = x-1
    down = x+1
    left = y-1
    right = y+1
    maxIndex = len(grid)-1
    matches = []

    # checks each of the surround tiles if it exists,
    # if it has not yet been used to form the word,
    # and if is equal to the next letter in the key/word
    if (up >= 0 and left >= 0 and (not [up, left] in usedTiles) and nextLetter == grid[up][left]):
        matches.append([up, left])
    if (up >= 0 and (not [up, y] in usedTiles) and nextLetter == grid[up][y]):
        matches.append([up, y])
    if (up >= 0 and y+1 <= maxIndex and (not [up, right] in usedTiles) and nextLetter == grid[up][right]):
        matches.append([up, right])
    if (left >= 0 and (not [x, left] in usedTiles) and nextLetter == grid[x][left]):
        matches.append([x, left])
    if (right <= maxIndex and (not [x, right] in usedTiles) and nextLetter == grid[x][right]):
        matches.append([x, right])
    if (down <= maxIndex and left >= 0 and (not [down, left] in usedTiles) and nextLetter == grid[down][left]):
        matches.append([down, left])
    if (down <= maxIndex and (not [down, y] in usedTiles) and nextLetter == grid[down][y]):
        matches.append([down, y])
    if (down <= maxIndex and right <= maxIndex and (not [down, right] in usedTiles) and nextLetter == grid[down][right]):
        matches.append([down, right])

    # all matching coordinates are noted
    return matches

def word_mapper(charList, coordinates, grid, usedTiles=[]):
    if (len(charList) > 0):
        for c in coordinates:
            # copy to keep a separate list for each branch of the coordinate paths
            copy = usedTiles.copy()
            # append current coordinate used for the letter
            copy.append(c)
            # find all tile matched for the next letter
            tileMatches = find_next_tile(charList[0], c, grid, copy)

            if (len(tileMatches) > 0):
                # repeat mapping for the next character if there are more letters in the key/word
                res = word_mapper(charList[1:], tileMatches, grid, copy)
                if (res):
                    # the word is found in this branch
                    return res
                else:
                    # continue to the next iteration in the coordinates loop
                    continue
            else:
                # continue to the next iteration in the coordinates loop
                continue
    else:
        # base case for keys or words mapped successfully
        # return all coordinate matches
        usedTiles.append(coordinates)
        return usedTiles
    
# compiles the list of words that the user can find in the game
def generate_word_list(valid_words, grid):
    keys = valid_words.keys()
    # finds all starting coordinates for each letter in the grid
    startingCoordinates = find_starting_coordinates(grid)

    # where we will append all words found in grid
    allPossibleWords = []
    # map through keys first to test if we are able to spell
    # the first 3 letters successfully using surrounding tiles
    for key in keys:
        # split to individual characters, treating 'qu' as a single character
        keyChars = word_splitter(key)
        # get strating coordinates of first letter in key
        keyCoordinates = startingCoordinates[keyChars[0]]
        # loop through all paths of starting coordinates here to capture all branches that spell out the key
        # this will cause repeating words in allPossibleWords, but we will clean this before returning the list
        for firstCoor in keyCoordinates:
            # attempt to find all characters in key
            keyRes = word_mapper(keyChars[1:], [firstCoor], grid)
            if (keyRes):
                # if key is successfully spelled using surrounding tiles, proceed here
                wordGroup = valid_words[key]
                # loop through all words under each key/word group
                for word in wordGroup:
                    if (word == key):
                        # word has already been spelled successfully
                        allPossibleWords.append(word)
                    else:
                        # split to individual characters, treating 'qu' as a single character
                        wordChars = word_splitter(word)
                        # take last returned coordinate as starting point
                        wordCoordinates = keyRes[-1]
                        # start mapping from character after last letter in key
                        # make sure to pass keyRes as usedTiles param for continuity in tracking
                        wordRes = word_mapper(wordChars[len(keyRes):], wordCoordinates, grid, keyRes)
                        if (wordRes):
                            allPossibleWords.append(word)

    # way to get all distinct values from the list
    # the set() func converts data into a set data type, taking only unique value from the data
    # set is like a dict, but only made up of "keys" (no values)
    # convert set to list to return to original data type 
    uniqueWords = list(set(allPossibleWords))
    # sort for faster tracking
    uniqueWords.sort()
    return uniqueWords

def scoreWord(word):
    # assigns a score to each word found
    length = len(word)
    if length >= 8:
        score = 6
    else:
        score = len(word) - 2
    return score

def print_word_list(gridWordList, foundWords):
    # Prints all possible words to be found at game end
    # Reveals player's answers and possible answers
    # Group words by their lengths from gridWordList
    word_groups = defaultdict(list)

    # Sort the words within each group
    for word in gridWordList:
        word_groups[len(word)].append(word)

    # Group words by length
    for length in word_groups:
        word_groups[length].sort()

    # Print possible words
    print("\nHere are all the words:")
    for length in sorted(word_groups.keys()):
        word_count = len(word_groups[length])
        print(f"\n{length}-LETTER WORDS = {word_count} WORD{'S' if word_count > 1 else ''}")

        # Separate found and not found words, and sort them
        found = sorted([word for word in word_groups[length] if word in foundWords])
        not_found = sorted([word for word in word_groups[length] if word not in foundWords])

         # Display found words first, then not found words
        for word in found + not_found:
            status = "FOUND" if word in foundWords else "NOT FOUND"
            print(f"{word} ({status})")

    return

#this reshuffles the letters in the grid
def reshuffle_grid(grid):
    # take all the letters from the grid 
    letters = [letter for row in grid for letter in row]

    # shuffle the letters
    random.shuffle(letters)

    #return the shuffled letters into the grid
    size = len(grid)
    reshuffled_grid = [letters[i * size:(i + 1) * size] for i in range(size)]

    return reshuffled_grid

def timer(timeroption):
    # Map timer options to durations (seconds)
    timer_durations = {1: 60, 2: 180, 3: 300, 4: None}
    return timer_durations[timeroption]

def print_grid_sequence(grid, game_duration):
    print_grid(grid)
    print("\nGame Start! Find words in the grid.")
    if game_duration: # Timer active options 1, 2, 3
        print (f"Game Timer: {game_duration} seconds")
    else:
        print("\nGame is untimed!")

def print_word_list_sequence(msg, currentScore, gridWordList, foundWords):
    print(f"Your final score is: {currentScore}.")
    print_word_list(gridWordList, foundWords)
    print(f"\n{msg}\n")

def new_game():  # merged and renamed word_search() into new_game()
    welcomeMessage("Welcome to Word Search!")
    print(gameDesc())
    player_name = get_player_name()

    while True:  # main loop for game, handles restarting
        clear_screen() # start with clean console
        gridsize, timeroption = menu()
        gridTemplate = create_grid(gridsize)
        grid = randomizer(gridTemplate)
        valid_words = load_word_library(grid)
        gridWordList = generate_word_list(valid_words, grid)
        
        foundWords = []
        currentScore = 0

        # Timer integaration
        game_duration  = timer(timeroption)
        start_time = time.time() if game_duration else None
        remaining_time = game_duration if game_duration else None

        print_grid_sequence(grid, game_duration)

        # Game loop
        while True:
            # Timer logic
            if game_duration:
                elapsed_time = time.time() - start_time
                remaining_time = game_duration - int(elapsed_time)
                if remaining_time <= 0: # Time's up
                    print("\nTime's up. Game Over!")
                    time.sleep(1) # allows user to read game over message before restarting
                    break

                print(f"\rTime remaining: {remaining_time} seconds", end="", flush=True)

            # Game Interaction     
            wordInput = input('\nEnter word (or type "0" to quit, "1" to restart, "2" to reshuffle): ').strip().lower()

            clear_lines(3)

            if wordInput == "0":
                msg = "Thank you for playing!"
                print_word_list_sequence(msg, currentScore, gridWordList, foundWords)
                # Record the score at the end of the game
                record_score(player_name, currentScore)
                # Show top 10 scorers
                display_top_scorers()
                return 
            elif wordInput == "1":
                msg = "Restarting the game..."
                print_word_list_sequence(msg, currentScore, gridWordList, foundWords)
                time.sleep(10) # allow the user to read word list before clearing terminal
                break  # Break from current game loop to restart
            elif wordInput == "2":  # Trigger reshuffle
                grid = reshuffle_grid(grid)
                lineCount = 0
                if (game_duration):
                    lineCount = 13 if gridsize == 4 else 11
                else:
                    lineCount = 14 if gridsize == 4 else 12

                clear_lines(lineCount)
                print("\nReshuffling the grid...")
                time.sleep(1) # allows user to read reshuffle message before reprint
                clear_lines(2)
                print_grid_sequence(grid, game_duration) # Print the reshuffled grid
                gridWordList = generate_word_list(valid_words, grid)  # Re-generate word list for reshuffled grid
                continue  # Continue  to prompt the user for the next word input (score remains unchanged)
            else:
                if wordInput in foundWords:
                    print("You've already found this word. Try another one!")
                elif wordInput in gridWordList:
                    foundWords.append(wordInput)
                    score = scoreWord(wordInput)
                    currentScore += score
                    print(f"Valid word! Your current score is {currentScore}.")
                else:
                    print("Invalid word. Try again.")

def clear_screen(): #clear console
    print("\033[3J\033[H\033[J", end="")
    sys.stdout.flush()

def clear_lines(lineCount):
    #formatting to clear and print in the same lines
    for _ in range(0, lineCount):
        sys.stdout.write("\033[F")  # Move cursor up one line           
        sys.stdout.write("\033[K")  # Clear input line
    sys.stdout.flush() #immediate refresh
new_game()